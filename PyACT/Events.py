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

    def __init__(self, Z, f, t='Heise', M=None, W='identity', k=0, vf=1, vt=1):
        # fundamentals for culture
        self.funds = f

        self.f = np.array(f[['e', 'p', 'a']]).reshape(-1)  # vector of ABO epa

        # Identify relavent fundamentals and their interactions
        if isinstance(t, str):
            self.t = self.__build_t(t)  # use one of two default estimators
        else:
            self.t = np.array(t)  # use a vector supplied by the user

        # Get coefficient and selection matrices for fundamentals
        self.M = M
        self.Z = Z

        # Get weights for fundamentals and transients
        self.W = self.__build_W(W)

        # Construct row and column vectors for f and t
        self.ft_row = np.concatenate([self.f, self.t])
        self.ft_col = self.ft_row.reshape(len(self.ft_row), 1)

        # Get first order weights for fundamentals and transients
        vf = self.__build_v(vf)
        vt = self.__build_v(vt, add_M=True)

        self.vft = np.concatenate([vf, vt])  # fundamental transient weight row vec

        # calculate weight matrix
        self.W = self.__build_W(W, add_M=True)

    def __build_t(self, t):
        # intercept and main effects
        t_est = self.f
        # interactions
        match t:
            case 'Heise':
                intacts = [t_est[0] * t_est[3],             # AeBe
                           t_est[0] * t_est[4],             # AeBp
                           t_est[0] * t_est[6],             # AeOe
                           t_est[1] * t_est[3],             # ApBe
                           t_est[1] * t_est[4],             # ApBp
                           t_est[1] * t_est[5],             # ApBa
                           t_est[1] * t_est[6],             # ApOe
                           t_est[1] * t_est[7],             # ApOp
                           t_est[1] * t_est[8],             # ApOa
                           t_est[2] * t_est[4],             # AaBp
                           t_est[2] * t_est[5],             # AaBa
                           t_est[3] * t_est[6],             # BeOe
                           t_est[3] * t_est[7],             # BeOp
                           t_est[4] * t_est[6],             # BpOe
                           t_est[4] * t_est[7],             # BpOp
                           t_est[4] * t_est[8],             # BpOa
                           t_est[5] * t_est[7],             # BaOp
                           t_est[0] * t_est[3] * t_est[6],  # AeBeOe
                           t_est[0] * t_est[4] * t_est[7],  # AeBpOp
                           t_est[2] * t_est[4] * t_est[7],  # ApBpOp
                           t_est[2] * t_est[4] * t_est[8],  # ApBpOa
                           ]
            case 'Smith-Lovin':
                # interactions
                intacts = [t_est[0] * t_est[3],             # AeBe
                           t_est[0] * t_est[4],             # AeBp
                           t_est[0] * t_est[5],             # AeBa
                           t_est[1] * t_est[3],             # ApBe
                           t_est[1] * t_est[4],             # ApBp
                           t_est[1] * t_est[8],             # ApOa
                           t_est[2] * t_est[5],             # AaBa
                           t_est[3] * t_est[6],             # BeOe
                           t_est[3] * t_est[7],             # BeOp
                           t_est[4] * t_est[6],             # BpOe
                           t_est[4] * t_est[7],             # BpOp
                           t_est[4] * t_est[8],             # BpOa
                           t_est[5] * t_est[6],             # BaOe
                           t_est[5] * t_est[7],             # BaOp
                           t_est[0] * t_est[3] * t_est[6],  # AeBeOe
                           t_est[0] * t_est[4] * t_est[7],  # AeBpOp
                           t_est[2] * t_est[4] * t_est[7],  # ApBpOp
                           t_est[2] * t_est[4] * t_est[8],  # ApBpOa
                           t_est[3] * t_est[5] * t_est[8],  # AaBaOa
                           ]
            case _:
                raise TypeError(f'{t} is not a valid transient estimator. Pass one of "Heise" or'
                                '"Smith-Lovin".')
        t_est = np.append(t_est, np.array(intacts))
        t_est = np.append(np.array([1]), t_est)
        return (t_est)

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
            vw = ([1] * self.f.shape[0])
        else:  # Otherwise, take what was given
            vw = v
        if add_M:
            # vw must have same length as M has rows
            vw = np.array([1] * self.M.shape[0]).dot(self.M)
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
            W = np.identity(self.f.shape[0])
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

    def optimize(self, element):
        """
        Find optimal componet of event, give element to optimize.

        The optimizer works by following Heise's 2007 solutions to his U equation.

        Parameters
        ----------
        element : str
            Element to optimize, can be one of:
                    Actor
                    Behvior
                    Object.


        Returns
        -------
        None.

        References
        ----------
        Heise, David. 2007. "Optimal Behavior" pp 81-90 in Expressive Order:
            Confirming Sentiments in Social Actions. NY:Springer

        Heise, David. 2007. "Optimal Identity" pp 91-95 in Expressive Order:
            Confirming Sentiments in Social Actions. NY:Springer

        """
        pass






