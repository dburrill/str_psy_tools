#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 09:26:12 2024.

@author: dan
"""
import uuid
import pandas as pd
import numpy as np
import re
import Utils


class Event:
    """ACT Event Handler."""

    def __init__(self, funds, Z, M=None, estimate_transients=True, W='identity',
                 t='Heise', k=0, vf=1, vt=1):
        # fundamentals for culture
        self.funds = funds
        f = np.array(funds[['e', 'p', 'a']]).reshape(-1)  # vector of ABO epa

        # Identify relavent fundamentals and their interactions
        if estimate_transients:
            # Get fundamentals involved in t
            t = self.__build_t(t)
            # Get coefficient and selection matrices for fundamentals
            self.M = M
            self.Z = Z

            # Get weights for fundamentals and transients
            self.W = self.__build_W(W)

        else:  # will always fail at present (need to fix weighting)
            try:
                t[0] - 2

            except TypeError:
                raise ValueError(f'estimate_transients is False, expected sequence of transient'
                                 f'impressions in t but got {t}.')

        # Construct row and column vectors for f and t

        self.ft_row = np.concatenate([f, t])
        self.ft_col = self.ft_row.reshape(len(self.ft_row), 1)

        # Get first order weights for fundamentals and transients
        vf = self.__build_v(vf)
        vt = self.__build_v(vt, add_M=True)
        print(vf)
        print(vt)
        self.vft = np.concatenate([vf, vt])  # fundamental transient weight row vec

    def __build_t(self, pattern):
        """Build t vector for U equations"""
        # check if t is a default equation
        match pattern:
            case 'Heise':  # default for abo
                pattern = [1, 'Ae', 'Ap', 'Aa', 'Be', 'Bp', 'Ba', 'Oe', 'Op', 'Oa',
                           'AeBe', 'AeBp', 'AeOe', 'ApBe', 'ApBp', 'ApBa', 'ApOe',
                           'ApOp', 'ApOa', 'AaBp', 'AaBa', 'BeOe', 'BeOp', 'BpOe',
                           'BpOp', 'BpOa', 'BaOp',
                           'AeBeOe', 'AeBpOp', 'ApBpOp', 'ApBpOa']
            case 'Heise_Settings':  # abo and settings
                pattern = [1, 'Ae', 'Ap', 'Aa', 'Be', 'Bp', 'Ba', 'Oe', 'Op', 'Oa',
                           'Se', 'Sp', 'Sa',
                           'AeBe', 'AeBp', 'AeOe', 'ApBe', 'ApBp', 'ApBa', 'ApOe',
                           'ApOp', 'ApOa', 'AaBp', 'AaBa', 'BeOe', 'BeOp', 'BpOe',
                           'BpOp', 'BpOa', 'BaOp',
                           'AeBeOe', 'AeBpOp', 'ApBpOp', 'ApBpOa']
            case 'Smith-Lovin':  # Smith-Lovin's MLE version for abo
                pattern = [1, 'Ae', 'Ap', 'Aa', 'Be', 'Bp', 'Ba', 'Oe', 'Op', 'Oa',
                           'AeBe', 'AeBp', 'AeBa', 'ApBe', 'ApOa', 'AaBa',
                           'BeOe', 'BeOp', 'BpOe', 'BpOp', 'BpOa', 'BaOe', 'BaOp',
                           'AeBeOe', 'AeBpOp', 'ApBpOp', 'ApBpOa', 'AaBaOa']

        # construct fundamental sentiment vector t
        funds = self.funds[['E', 'P', 'A']].to_numpy()
        t = []

        # get intercept
        if isinstance(pattern[0], (int, float)):
            t.append(pattern[0])

        # convert human readable to cords
        pattern = pattern[1:]  # ignore intercept
        pattern = [re.sub('A', '0', i) for i in pattern]
        pattern = [re.sub('B', '1', i) for i in pattern]
        pattern = [re.sub('O', '2', i) for i in pattern]

        pattern = [re.sub('e', '0', i) for i in pattern]
        pattern = [re.sub('p', '1', i) for i in pattern]
        pattern = [re.sub('a', '2', i) for i in pattern]

        # get fundamentals
        for i in pattern:
            if len(i) == 2:
                t.append(funds[int(i[0]), int(i[1])])
            elif len(i) > 2:
                cords = [j for j in zip(*(iter(i),) * 2)]  # break elements into cords
                cords = [funds[int(i[0]), int(i[1])] for i in cords]
                t.append(np.prod(cords))  # interaction of all elements
        return(t)

    def __build_v(self, v, add_M=False):
        if v == 1:
            vw = ([1] * self.funds.shape[0] * 3)
        else:
            vw = v
        if add_M:
            return(np.array(vw).reshape(len(vw), 1).dot(self.M))
        else:
            return(np.array(vw))

    def __build_W(self, W, add_M=False):
        if W == 'identity' and add_M:
            W = np.identity(self.funds.shape[0] * 3)
            negWU = np.matmul(-W, self.M.transpose())  # upper right
            negWL = np.matmul(-self.M, W)  # lower left
            mwm = self.M.dot(W).dot(self.M.transpose())  # lower right
            Wu = np.concatenate([W, negWU], axis=1)
            Wl = np.concatenate([negWL, mwm], axis=1)
            W = np.concatenate([Wu, Wl])
        else:
            pass  # generalizations can be added here
        return(W)

    def deflection(self):
        U = self.ft_row.dot(self.W).dot(self.ft_col)+self.vft.dot(self.ft_col)
        return(U)

    def optimize(self, element, culture):
        pass






