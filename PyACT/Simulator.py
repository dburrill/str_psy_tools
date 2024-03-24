#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 20:47:32 2024.

Currently this is a memory aid for describing how to use the pyACT classes

@author: dan
"""
# Load libraries
import pandas as pd
import Events
import Utils

# Load culture
amcult = pd.read_csv('./Data/Culture/ACT2015Combined.csv')

# Load ztable. These tables have the reference weights and their corrosponding map for estimating
# transient impressions
zm = Utils.construct_mats('./Data/Ztabs/Zmabo.csv')

# get event fundamentals by label
ef = Utils.event_from_labels(amcult, 'scientist', 'lie_to', 'American')

# create event. The event class will estimate the transient impressions from the fundamentals passed
# to the class constructor (and do other things)
E = Events.Event(f=ef, Z=zm[0], M=zm[1])
