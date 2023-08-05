#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 31 17:16:22 2018
@author: Nathan de Lara <ndelara@enst.fr>
@author: Thomas Bonald <bonald@enst.fr>
"""

import warnings
from typing import Union

import numpy as np
from scipy import sparse

from sknetwork.linalg import SparseLR, SVDSolver, HalkoSVD, LanczosSVD, auto_solver, safe_sparse_dot
from sknetwork.utils.algorithm_base_class import Algorithm
from sknetwork.utils.checks import check_format, check_weights


class SVD(Algorithm):
    """
    Graph embedding by Generalized Singular Value Decomposition.

    Setting **weights** and **secondary_weights** to ``'uniform'`` leads to the standard SVD.

    Parameters
    -----------
    embedding_dimension: int
        Dimension of the embedding.
    weights: ``'degree'`` or ``'uniform'`` (default = ``'degree'``)
        Weights of the nodes.
    secondary_weights: ``None`` or ``'degree'`` or ``'uniform'`` (default= ``None``)
        Weights of the secondary nodes (taken equal to **weights** if ``None``).
    regularization: ``None`` or float (default= ``0.01``)
        Implicitly add edges of given weight between all pairs of nodes.
    relative_regularization : bool (default = ``True``)
        If ``True``, consider the regularization as relative to the total weight of the graph.
    scaling:  ``None`` or ``'multiply'`` or ``'divide'`` (default = ``'multiply'``)
        If ``'multiply'``, multiply by the singular values .

    Attributes
    ----------
    embedding_ : np.ndarray, shape = (n1, embedding_dimension)
        Embedding of the nodes (rows of the adjacency matrix).
    coembedding_ : np.ndarray, shape = (n2, embedding_dimension)
        Embedding of the feature nodes (columns of the adjacency matrix).
    singular_values_ : np.ndarray, shape = (embedding_dimension)
        Generalized singular values of the adjacency matrix (first singular value ignored).

    Example
    -------
    >>> from sknetwork.toy_graphs import house
    >>> adjacency = house()
    >>> svd = SVD()
    >>> embedding = svd.fit(adjacency).embedding_
    >>> embedding.shape
    (5, 2)

    References
    ----------
    Abdi, H. (2007). Singular value decomposition (SVD) and generalized singular value decomposition.
    Encyclopedia of measurement and statistics, 907-912.
    https://www.cs.cornell.edu/cv/ResearchPDF/Generalizing%20The%20Singular%20Value%20Decomposition.pdf
    """

    def __init__(self, embedding_dimension=2, weights='degree', secondary_weights=None,
                 regularization: Union[None, float] = 0.01, relative_regularization: bool = True,
                 scaling: Union[None, str] = 'multiply', solver: Union[str, SVDSolver] = 'auto'):
        self.embedding_dimension = embedding_dimension
        self.weights = weights
        if secondary_weights is None:
            secondary_weights = weights
        self.secondary_weights = secondary_weights
        self.regularization = regularization
        self.relative_regularization = relative_regularization
        self.scaling = scaling

        if scaling == 'divide':
            if weights != 'degree' or secondary_weights != 'degree':
                warnings.warn(Warning("The scaling 'divide' is valid only with ``weights = 'degree'`` and "
                                      "``secondary_weights = 'degree'``. It will be ignored."))

        if solver == 'halko':
            self.solver: SVDSolver = HalkoSVD()
        elif solver == 'lanczos':
            self.solver: SVDSolver = LanczosSVD()
        else:
            self.solver = solver

        self.embedding_ = None
        self.coembedding_ = None
        self.singular_values_ = None

    def fit(self, adjacency: Union[sparse.csr_matrix, np.ndarray]) -> 'SVD':
        """
        Computes the generalized SVD of the adjacency matrix.

        Parameters
        ----------
        adjacency: array-like, shape = (n1, n2)
            Adjacency matrix, where n1 = n2 is the number of nodes for a standard graph,
            n1, n2 are the number of nodes in each part for a bipartite graph.

        Returns
        -------
        self: :class:`SVD`
        """
        adjacency = check_format(adjacency).asfptype()
        n1, n2 = adjacency.shape

        if self.solver == 'auto':
            solver = auto_solver(adjacency.nnz)
            if solver == 'lanczos':
                self.solver: SVDSolver = LanczosSVD()
            else:
                self.solver: SVDSolver = HalkoSVD()

        total_weight = adjacency.dot(np.ones(n2)).sum()
        regularization = self.regularization
        if regularization:
            if self.relative_regularization:
                regularization = regularization * total_weight / n1 / n2
            adjacency = SparseLR(adjacency, [(regularization * np.ones(n1), np.ones(n2))])

        w_samp = check_weights(self.weights, adjacency)
        w_feat = check_weights(self.secondary_weights, adjacency.T)

        # pseudo inverse square-root out-degree matrix
        diag_samp = sparse.diags(np.sqrt(w_samp), shape=(n1, n1), format='csr')
        diag_samp.data = 1 / diag_samp.data
        # pseudo inverse square-root in-degree matrix
        diag_feat = sparse.diags(np.sqrt(w_feat), shape=(n2, n2), format='csr')
        diag_feat.data = 1 / diag_feat.data

        normalized_adj = safe_sparse_dot(diag_samp, safe_sparse_dot(adjacency, diag_feat))

        # svd
        if self.embedding_dimension > min(n1, n2) - 1:
            warnings.warn(Warning("The dimension of the embedding must be less than the minimum of the number of rows "
                                  "and columns."))
            n_components = min(n1, n2) - 1
        else:
            n_components = self.embedding_dimension + 1
        self.solver.fit(normalized_adj, n_components)

        index = np.argsort(-self.solver.singular_values_)
        self.singular_values_ = self.solver.singular_values_[index[1:]]
        self.embedding_ = np.sqrt(total_weight) * diag_samp.dot(self.solver.left_singular_vectors_[:, index[1:]])
        self.coembedding_ = np.sqrt(total_weight) * diag_feat.dot(self.solver.right_singular_vectors_[:, index[1:]])

        # rescale to get barycenter property
        self.embedding_ *= self.singular_values_

        if self.scaling:
            if self.scaling == 'multiply':
                self.embedding_ *= self.singular_values_
            elif self.scaling == 'divide':
                energy_levels: np.ndarray = np.sqrt(1 - np.clip(self.singular_values_, 0, 1) ** 2)
                energy_levels[energy_levels > 0] = 1 / energy_levels[energy_levels > 0]
                self.embedding_ *= energy_levels
                self.coembedding_ *= energy_levels

        return self
