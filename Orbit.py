# coding=UTF-8
from Body import *
import numpy as np
from sympy import *



class Orbit:
    TYPE_NOT_DEF = 0
    TYPE_SIMP_ORB = 1
    TYPE_EXCENTRICAL_ORB = 2
    TYPE_SUGGESTED = -1

    def __init__(self, orbital_body, self_body=None, schwerpunkt=None, speed=None, period=None, track=None,
                 exzentritaet=None, ga=None, b=None, inkl=None):
        self.bd = self_body
        self.mother = orbital_body
        self.sp = schwerpunkt
        self.speed = speed
        self.period = period
        self.track = track
        self.exzentritaet = exzentritaet
        self.ga = ga
        self.kb = b
        self.inklination = inkl
        self.type = 0

    def calc_kb(self):
        self.kb = (self.ga ** 2 - (self.ga * self.exzentritaet) ** 2) ** (1 / 2)
        self.type = 2

    def elliptic_param_x(self, t, a, b):
        return -a * sin(t)

    def set_type(self, type):
        self.type = type

""" ATTRIBUTES

 Der zu obitierende Körper

mother  (public)

 distanz zum schwerpunkt


schwerpunkt  (protected)

"""
