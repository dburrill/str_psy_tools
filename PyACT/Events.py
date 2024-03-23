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

    def __init__(self, Z, f, t='estimate', M=None, W='identity', k=0, vf=1, vt=1):
        # fundamentals for culture
        self.funds = f
        f = np.array(f[['e', 'p', 'a']]).reshape(-1)  # vector of ABO epa

        # Identify relavent fundamentals and their interactions
        if t == 'estimate':
            t = f
        else:
            t = np.array(t)
        # Get coefficient and selection matrices for fundamentals
        self.M = M
        self.Z = Z

        # Get weights for fundamentals and transients
        self.W = self.__build_W(W)

        # Construct row and column vectors for f and t
        self.ft_row = np.concatenate([f, t])
        self.ft_col = self.ft_row.reshape(len(self.ft_row), 1)

        # Get first order weights for fundamentals and transients
        vf = self.__build_v(vf)
        vt = self.__build_v(vt, add_M=True)

        self.vft = np.concatenate([vf, vt])  # fundamental transient weight row vec

        # calculate weight matrix
        self.W = self.__build_W(W)

        # get deflection for event
        self.deflection = self.get_deflection()

    def __build_v(self, v, add_M=False):
        """
        Construct first-order weighting matrix for deflection based equations.

        Parameters
        ----------
        v : np.array
             one dimnensional Array of weights .
        add_M : Boolean, optional
            If True an array of coefficents is added to the weights. The default is False.

        Returns
        -------
        vw : TYPE
            DESCRIPTION.

        """
        if v == 1:  # no weights, means these are all equal to one
            vw = ([1] * self.funds.shape[0] * 3)
        else:  # Otherwise, take what was given as gosple
            vw = v
        if add_M:
            # vw must have same length as M has rows
            vw = vw + ([1] * (self.M.shape[0] - len(vw)))
            vw = np.array(vw).T.dot(self.M)
        else:  # M was not passed, so we ignore it
            vw = np.array(vw)
        return (vw)

    def __build_W(self, W: str | np.ndarray, add_M: bool = False):
        """
        Construct weighting matrix for deflection based equations.

        Parameters
        ----------
        W : str | np.array
            Weighting matrix. If a custom matrix is passed, it should be a diagonal with the diag
            elements equal to the number of EPA elements in the equation. EG: an ABO equation would
            require 3 terms (A,B,O) times 3 componets (E,P,A) for 9 elements in the diagonal.
        add_M : bool, optional
            If True an array of coefficents is added to the weights. The default is False.

        Returns
        -------
        W : TYPE
            DESCRIPTION.

        """
        if W == 'identity':
            W = np.identity(self.funds.shape[0] * 3)
        else:
            pass
        if add_M:
            WUr = np.matmul(-W, self.M.T)  # upper right
            WLr = np.matmul(np.matmul(self.M, W), self.M.T)  # lower right
            WLl = np.matmul(-self.M, W)  # lower left
        else:
            WUr = -W
            WLl = -W
            WLr = W
        WUl = W
        WU = np.concatenate([WUl, WUr], axis=1)
        WL = np.concatenate([WLl, WLr], axis=1)
        W = np.concatenate([WU, WL])

        return (W)

    def get_deflection(self):
        """
        Calculate deflection for the event.

        Returns
        -------
        U : float
            The "uncanniness" of an event. Equal to deflection when k is 0 (check this is so.)

        """
        term1 = np.matmul(np.matmul(self.ft_row, self.W), self.ft_col)
        term2 = np.matmul(self.vft, self.ft_col)
        U = term1 + term2
        return (U)

    def optimize(self, element, culture):
        pass






