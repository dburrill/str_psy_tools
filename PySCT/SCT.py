#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 10:07:13 2022.

@author: dan
"""


def expectations(elements, method='fisek'):
    """Calculate an expectation state for an actor.

    Expectation states describe the effect that status characteristics have
    on an actor's expectations for future performance at a task. This function
    models the assumptions of status characteristics theory needed to produce
    expectation states. Note that this function does not produce expectation
    advantage, the relative difference between the expectations of two or
    more actors in the same task group.

    This function implements the equation model described by Whitmeyer (2003)

    Whitmeyer, Joseph. 2003. "The Mathemeatics of Expectation States Theory"
        Social Psychology Quarterly. 66(3):238-253

    Arguments:
        elements -- a dictionary of elements, each key representing the
        following convention:
            h1 -- The number of high state specific task abilites (C*)
            h2 -- The number of high state explicitly relavent status elements
              (C or D)
            h3 -- The number of high state non explicitly relavent status
              elements (C, D, or b)
            l1 -- The number of low state specific task abilites (C*)
            l2 -- The number of low state explicitly relavent status elements
              (C or D)
            l3 -- The number of low state non explicitly relavent status
              elements (C, D, or b)

            If a key is not passed in elements, then it will be defaulted to 0.
            Keys other than h1-l3 are ignored.

        method -- One of three methods for calculating magnitutde of status
                  relavence. berger, balkwell and fisek are valid options
                  (default fisek).

    Returns:
        expectationState -- the expected competence the actor has for
        themsleves based on their status position
    """
    import math
    # set k and scale params
    if method.lower() == 'berger':
        k = 3
        scale = -0.0865
    elif method.lower() == 'balkwell':
        k = 3.192
        scale = -0.0671
    elif method.lower() == 'fisek':
        k = 2.618
        scale = -0.0770
    else:
        raise Warning(f"Method '{method}' is unrecognized. Allowed methods are"
                      " Fisek, Berger and Balkwell.")

    # set relavence levels for count vars
    h = [(1, elements.get("h1", 0)), (2, elements.get("h2", 0)),
         (3, elements.get("h3", 0))]

    l = [(1, elements.get("l1", 0)), (2, elements.get("l2", 0)),
         (3, elements.get("l3", 0))]

    lowStates = math.exp(scale*sum([r[1]*k**(4-r[0]) for r in l]))
    highStates = math.exp(scale*sum([r[1]*k**(4-r[0]) for r in h]))
    expectationState = lowStates-highStates
    return(expectationState)


def exp_standing(actors, method='fisek'):
    """
    Calculate expectation standing for a group of actors.

    This function calculates the ratio of one individual's performance
    expectations, to the total value of expectations held by all group members.
    This function is a relative comparison of one's performance, used for
    groups with more than two individuals.

    References:
            Fiesk, Hamit, Joseph Berger, and Robert Norman. 1991.
                "Participation in Heterogeneous and Homogeneous Groups: a
                Theoretical Integration" American Journal of Sociology. 97(1)
                114-142.

            Whitmeyer, Joseph. 2003. "The Mathemeatics of Expectation States
                Theory" Social Psychology Quarterly. 66(3):238-253

    Arguments:
        actors -- A dictionary of actors in the group following this
        convention: {actor1: {h1:1, h2:0, h3:1 . . . l3:0}}
            where h1-l3 are counts of status elements for three levels of
            relavence. The h and l stand for 'high' and 'low' respectivly.
            There are three relavence levels r1,r2, and r3, thus h3, represents
            the count of all high-status elements of relavence level 3, while
            l1 would represent the count of all low-status elements of
            relavence level 1.

            For relavence levels with 0 elements, the level may be
            omitted.

            EG: Suppose you have an actor with one high-status element of
            relavence 1, two high-status elements of relavnce 2, and none of
            relavence 3. Further suppose they had one low-status element of
            relavence 3 and none of 1 or 2. Such a case would be passed as
            {'actor1': {'h1': 1, 'h2': 2, 'l1':1}}

        method -- One of three methods for calculating magnitutde of status
                  relavence. berger, balkwell and fisek are valid options
                  (default fisek).

    Returns:
        expectation standing
    """
    actors = {actor: 1 + expectations(actors[actor], method) for
              actor in actors}
    standing = {actor: actors[actor]/sum(actors.values()) for actor in actors}
    return(actors, standing)
