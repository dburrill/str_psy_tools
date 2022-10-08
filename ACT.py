#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  8 13:25:18 2022.

@author: dan
"""


def i_deflection(fundamentals, transients, matrix=False):
    """Immediate form of deflection.

    Given a list of fundamentals and transients, returns the sum of squared
    differences betwteen the two. Assumes both lists conform to the
    following pattern: AE AP AO BE BP BO OE OP OA *SE *SP *SO.
                      *Settings are optional

    Arguments:
        fundamentls -- values for the fundamental sentiments
        transients -- values for the transient impressions
        matrix (default False) -- if True, function returns a tuple, with
            deflection as the first element, and a nested whose elements
            consist of 0: passed fundamental sentiments
                       1: passed transients impressions
                       3: the squared differences between the two
            Returning the matrix is usefull for examining how individual
            elements contribute to deflection


    Returns:
        deflection:: The sum of squared difference between fundamentals and
        transients.
    """
    if len(fundamentals) != len(transients):
        raise ValueError("Lengths of fundamentals and transients are not equal"
                         )

    differences = [(a-b)**2 for a, b in zip(fundamentals, transients)]

    if not matrix:
        return sum(differences)

    else:
        mat = [fundamentals, transients, differences]
        return sum(differences), mat


def deflection(fundamentals, estimates="Hesie"):
    """
    Estimates deflection for an event given a set of fundamental sentiments.

    CITITATION HERE

    Arguments:
        fundamentals -- a itterable of fundamental sentiments with the
        following order: AE AP AO BE BP BO OE OP OA *SE *SP *SO.
        *Settings are optional.

        estimates (default Heise) --  Sets the estimates used to weight terms
        in the impression formation equations. Custom estimeates can be passed,
        but should conform to the pattern below

    """
