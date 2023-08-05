#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Nov 6 2018

Authors:
Nathan De Lara <ndelara@enst.fr>

Quality metrics for adjacency embeddings
"""

from typing import Union

import numpy as np
from scipy import sparse
from scipy.stats import hmean

from sknetwork.utils.checks import check_format


def linear_fit(adjacency: Union[sparse.csr_matrix, np.ndarray], embedding: np.ndarray, order: int = 1,
               damping: float = 0.85) -> tuple:
    """Linear multi order proximity fit and diversity.

    Parameters
    ----------
    adjacency:
        Adjacency matrix of the adjacency.
    embedding:
        Embedding of each node.
    order:
        Number of proximity order to consider.
    damping:
        Decay factor for multi-order metrics, only useful if ``order > 1``.

    Returns
    -------
        A tuple of non-negative floats.

    """
    adjacency = check_format(adjacency)
    n_nodes, m_nodes = adjacency.shape
    if embedding.shape[0] != adjacency.shape[0]:
        raise ValueError('The embedding and the adjacency must have the same number of rows.')
    scale = 1.
    total_scale = 0.
    fit, div = 0., 0.
    degree = np.ones(adjacency.shape[1])
    current = embedding
    for k in range(order):
        scale *= damping
        total_scale += scale
        degree = adjacency.dot(degree)
        total_weight = degree.sum()
        current = adjacency.dot(current)
        fit += scale * np.multiply(embedding, current).sum() / total_weight
        div += scale * np.linalg.norm(embedding.T.dot(degree) / total_weight)

    normalization = np.linalg.norm(embedding) ** 2 / np.sqrt(n_nodes * m_nodes)
    fit /= (total_scale * normalization)
    div /= (total_scale * normalization)
    return fit, div


def dot_modularity(adjacency, embedding: np.ndarray, coembedding=None, resolution=1., weights='degree',
                   return_all: bool = False):
    """
    Quality metric of an embedding :math:`x` defined by:

    :math:`Q = \\sum_{ij}(\\dfrac{A_{ij}}{w} - \\gamma \\dfrac{d_id_j}{w^2})x_i^Tx_j`

    This metric is normalized to lie between -1 and 1 (for :math:`\\gamma = 1`).

    If the embeddings are normalized, this reduces to cosine modularity.

    Parameters
    ----------
    adjacency: sparse.csr_matrix or np.ndarray
        Adjacency matrix of the graph.
    embedding: np.ndarray
        Embedding of the nodes.
    coembedding: None or np.ndarray
        For bipartite graphs, coembedding of features.
    resolution: float
        Resolution parameter.
    weights: ``'degree'`` or ``'uniform'``
        Weights of the nodes.
    return_all: bool, default = ``False``
        whether to return (fit, diversity) or fit - diversity

    Returns
    -------
    dot_modularity: a float or a tuple of floats.
    """
    adjacency = check_format(adjacency)
    n_nodes, m_nodes = adjacency.shape
    total_weight: float = adjacency.data.sum()

    if coembedding is None:
        if n_nodes != m_nodes:
            raise ValueError('coembedding cannot be None for non-square adjacency matrices.')
        else:
            normalization = np.linalg.norm(embedding) ** 2 / np.sqrt(n_nodes * m_nodes)
            coembedding = embedding
    else:
        normalization = np.linalg.norm(embedding.dot(coembedding.T)) / np.sqrt(n_nodes * m_nodes)

    if weights == 'degree':
        wou = adjacency.dot(np.ones(m_nodes)) / total_weight
        win = adjacency.T.dot(np.ones(n_nodes)) / total_weight
    elif weights == 'uniform':
        wou = np.ones(n_nodes) / n_nodes
        win = np.ones(m_nodes) / m_nodes
    else:
        raise ValueError('weights must be degree or uniform.')

    fit = (np.multiply(embedding, adjacency.dot(coembedding))).sum() / (total_weight * normalization)
    diversity = (embedding.T.dot(wou)).dot(coembedding.T.dot(win)) / normalization

    if return_all:
        return fit, diversity, fit - resolution * diversity
    else:
        return fit - resolution * diversity


def hscore(adjacency, embedding: np.ndarray, order='second', return_all: bool = False):
    """
    Harmonic mean of fit and diversity with respect to first or second order node similarity.

    Parameters
    ----------
    adjacency: sparse.csr_matrix or np.ndarray
        the adjacency matrix of the adjacency
    embedding: np.ndarray
        the embedding to evaluate, embedding[i] must represent the embedding of node i
    order: \'first\' or \'second\'.
        The order of the node similarity metric to use. First-order corresponds to edges weights while second-order
        corresponds to the weights of the edges in the normalized cocitation adjacency.
    return_all: bool, default = ``False``
        whether to return (fit, diversity) or hmean(fit, diversity)

    Returns
    -------
    hscore: a float or a tuple of floats.

    """
    adjacency = check_format(adjacency)
    n_nodes, m_nodes = adjacency.shape
    if order == 'first' and (n_nodes != m_nodes):
        raise ValueError('For fist order similarity, the adjacency matrix must be square.')
    total_weight = adjacency.data.sum()
    # out-degree vector
    dou = adjacency.dot(np.ones(m_nodes))
    # in-degree vector
    din = adjacency.T.dot(np.ones(n_nodes))

    prob_out, prob_in = np.zeros(n_nodes), np.zeros(m_nodes)
    prob_out[dou.nonzero()] = 1 / np.sqrt(dou[dou.nonzero()])
    prob_in[din.nonzero()] = 1 / np.sqrt(din[din.nonzero()])

    normalization = np.linalg.norm(embedding.T * np.sqrt(dou)) ** 2
    if order == 'first':
        fit = (np.multiply(embedding, adjacency.dot(embedding))).sum()
        fit /= total_weight * (np.linalg.norm(embedding) ** 2 / n_nodes)
    elif order == 'second':
        fit = np.linalg.norm(adjacency.T.dot(embedding).T * prob_in) ** 2 / normalization
    else:
        raise ValueError('The similarity order should be \'first\' or \'second\'.')
    diversity = (np.linalg.norm(embedding.T.dot(dou))) ** 2 / total_weight
    diversity = 1 - diversity / normalization

    if return_all:
        return fit, diversity
    else:
        if np.isclose(fit, 0.) or np.isclose(diversity, 0.):
            return 0.
        else:
            return hmean([fit, diversity])
