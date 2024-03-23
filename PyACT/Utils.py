#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 15:51:03 2024

@author: dan
"""

import pandas as pd
import numpy as np


def construct_mats(ztab: str, delim: str = ','):
    r"""
    Construct weight and Z matricies for impression formation equations.

    Given a table of coefficients and 'z-terms' as appears in the java program interact,
    construct_mats builds a z matrix and a matrix of coefficents for impression formation equations.

    Parameters
    ----------
    ztab : str
        Directory address of table used for constructing equations. Accepts .txt or .csv files.
    delim : str, optional
        Delimiter used to seperate fields in ztab. If you are copying over a table from interact,
        use '\\s+' as the tables are formated with two whitespace characters. The default is ','.

    Returns
    -------
    Tuple containing the z matrix in the first position and the m matrix in the second.

    References
    ----------
    Heise, David. 2007. "Mathmematics of Affect Control Theory" pp 81-124 in Expressive Order:
        Confirming Sentiments in Social Actions. NY:Springer
    """
    m = pd.read_csv(ztab, header=None, sep=delim)
    # extract z matrix from z table and seperate z from M
    z = m.iloc[:, 0].str.replace('Z|z', '', regex=True).str.split('', expand=True)
    z = z.iloc[:, 1:-1].astype(int).to_numpy()
    m = m.iloc[:, 1:].astype(float).to_numpy()

    # add funds id mat to z
    zi = np.identity(n=z.shape[1], dtype=int)
    z = np.concatenate([zi, z])

    return (z, m)


def event_from_labels(culture: pd.DataFrame, a: str, b: str, o: str):
    """
    Get an event from a culture based on event labels.

    Parameters
    ----------
    culture : pd.DataFrame
        dataframe containing EPA ratings from a given culture in long form.
        Must contain the following columns: e, p and a and term. term is the labeld element of the
        event.
    a : str
        label for the actor.
    b : str
        label for the behavior.
    o : str
        label for the object.

    Returns
    -------
    Pandas data frame containing EPA elements asociated with the event.

    """
    return (culture.loc[culture.term.isin([a, b, o]), ['term', 'e', 'p', 'a']])
