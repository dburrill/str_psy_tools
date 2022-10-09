#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  8 13:25:18 2022.

@author: dan
"""
class Zequation:
    """Creates table object for ACT calculations.
    
    Each of the tables below are used in impression formation equations to 
    weight the effect of EPA terms involved in impression formation equations.
    There are several hard coded tables, representing male and female equations
    as derived by Heise and Dawn-Robinson. Users may pass their own table of
    equations as well.
    
    init args:
        table -- a dictionary of coefficients used to weight ABO EPA values.
    """
    def __init__(self, table='default'):
        if table == 'default':
            self.table = {"Ae": [-.31, .47, .00, .00, .24, .00, .00,
                                  .08, -.06, .00, -.07],
                          "Ap": [-.57, .00, .37, .00, .16, .00, .21,
                                  .00, .00, .00, .00],
                          "Aa": [-.19, .00, -.07, .57, .10, -.18, .37,
                                  .00, .00, .02, .00],
                          "Be": [-.45, .31, .00, .00, .29, .00, .00,
                                  .07, -.08, .00, .00],
                          "Bp": [-.53, .07, .22, .00, .07, .16, .13,
                                 .00, .00, .00, .00],
                          "Ba": [-.26, .00, -.06, .43, .07, -.14, .45,
                                 .02, .00, .00, .00]}
            
def i_deflection(fundamentals, transients, matrix=False):
    """Immediate form of deflection.

    Given a list of fundamentals and transients, returns the sum of squared
    differences between the two. Assumes both lists conform to the
    following pattern: AE AP AO BE BP BO OE OP OA *SE *SP *SO.
    *Settings are optional

    Arguments:
        fundamentals -- values for the fundamental sentiments
        transients -- values for the transient impressions
        matrix (default False) -- if True, function returns a tuple, with
            deflection as the first element, and a nested whose elements
            consist of 0: passed fundamental sentiments
                       1: passed transients impressions
                       3: the squared differences between the two
            Returning the matrix is useful for examining how individual
            elements contribute to deflection


    Returns:
        deflection -- The sum of squared difference between fundamentals and
        transients.
        
        (deflection, matrix) -- tuple of deflection and its componets
    """
    if len(fundamentals) != len(transients):
        raise ValueError("Lengths of fundamentals and transients are not equal"
                         )

    differences = [(f-t)**2 for f, t in zip(fundamentals, transients)]

    if not matrix:
        return sum(differences)

    else:
        mat = [fundamentals, transients, differences]
        return sum(differences), mat


def deflection(fundamentals, zequation):
    """
    Estimates deflection for an event given a set of fundamental sentiments.

    CITATION HERE

    Arguments:
        fundamentals -- an iterable of fundamental sentiments with the
        following order: AE AP AO BE BP BO OE OP OA *SE *SP *SO.
        *Settings are optional.

        zequation --  an object of class zequation. Sets the weights used for
        calculating deflection.

    """

def ztab_import (file):
    """
    Utility for importing impression formation equation coefficients.
    
    Historically, these equations were organized into a matrix with the leading 
    column providing informaiton about where in the equation the coefficent
    should appear. The other columns corrospond to the specific ABO-EPA
    equation being calculated. This approach is (reasonably) fast in java,
    but slow in  python, so this utility transforms these tables into a
    dictionary format that is faster in python.
    
    Arguments:
        file -- a csv file contaning the ztable to import. The first column of
        which should contain the zero-one values, all other columns should
        contain ABO-EPA values, the order of which should be as follows:
            Ae, Ap, Aa, Be, Bp, Ba, Oe, Op, Oa, Se, Sp, Sa.
        Settings and objects may be omitted as is the case for situations
        involving self-directed action
    """
    import csv
    with open(file, mode='r') as ztab:
        csv_reader = csv.DictReader(ztab) 
        
