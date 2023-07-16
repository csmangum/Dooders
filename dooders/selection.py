import random
from typing import Tuple

import numpy as np
from sklearn.decomposition import PCA

from dooders.experiment import Experiment
from dooders.sdk.modules.recombination import recombine

gene_embedding = PCA(n_components=3)


def embeddings(weights: dict) -> list:
    """ 
    Returns a list of the embeddings of the weights of each dooder in a gene pool

    Parameters
    ----------
    weights : (dict)
        A dictionary containing the dooder ids as keys and their weights as values

    Returns
    -------
    all_weights : (list)
        A list of the embeddings of the weights of each dooder in a gene pool
    """
    all_weights = []
    for dooder in weights.values():
        weight = dooder['Consume'][0]
        embedding = gene_embedding.fit(weight)
        all_weights.append(embedding.singular_values_)

    return all_weights


def random_parents(gene_pool: dict) -> Tuple[tuple, tuple]:
    """ 
    Returns two random dooders' weights from a directory of weight files

    Parameters
    ----------
    gene_pool : (dict)
        A dictionary containing the dooder ids as keys and their weights as values

    Returns
    -------
    parent_a : (tuple)
        The id and weights of the first dooder
    parent_b : (tuple)
        The id and weights of the second dooder
    """

    parent_a, parent_b = random.sample(list(gene_pool.keys()), 2)

    parent_a_weights = gene_pool[parent_a]['Consume']
    parent_b_weights = gene_pool[parent_b]['Consume']

    return (parent_a, parent_a_weights), (parent_b, parent_b_weights)


def produce_genes(gene_pool: dict, recombination_type: str = 'crossover') -> np.ndarray:
    """ 
    Produces a new set of genes from two random dooders' weights 
    from a provided gene pool

    Parameters
    ----------
    gene_pool : (dict)
        A dictionary containing the dooder ids as keys and their weights as values
    recombination_type : (str)
        The type of recombination to use. 
        Options are 'crossover', 'random','range', and 'average'

    Returns 
    -------
    new_genes : (np.ndarray)
        The new set of genes produced from the two random dooders' weights
    """

    parent_a, parent_b = random_parents(gene_pool)

    parent_a_genes = parent_a[1][0]
    parent_b_genes = parent_b[1][0]

    new_genes = recombine(parent_a_genes, parent_b_genes,
                          recombination_type=recombination_type)

    return np.array(new_genes)


def recursive_artificial_selection(settings: dict = {}, iterations: int = 100) -> list:
    """ 
    Runs a recursive artificial selection experiment

    Parameters
    ----------
    settings : (dict)
        The settings to use for the experiment
    iterations : (int)
        The number of iterations to run the experiment

    Returns
    -------
    results : (list)
        A list of the number of unique dooders in the gene pool after each iteration
    """

    gene_pool = {}
    results = []

    def inherit_weights(experiment):

        if gene_pool == {}:
            pass
        else:
            new_genes = produce_genes(gene_pool)
            dooder = experiment.simulation.arena.get_dooder()
            dooder.internal_models['Consume'].inherit_weights(new_genes)

    for i in range(iterations):

        experiment = Experiment(settings)
        experiment.batch_simulate(1000,
                                  i,
                                  'recursive_artificial_selection',
                                  custom_logic=inherit_weights)
        gene_pool = experiment.gene_pool.copy()
        results.append(len(experiment.gene_pool.keys()))
        del experiment

    return results
