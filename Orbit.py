# coding=UTF-8
from Body import *


class Orbit:
    def __init__(self, orbital_body, self_body=None, schwerpunkt=None, speed=None, period=None):
        self.bd = self_body
        self.mother = orbital_body
        self.sp = schwerpunkt
        self.speed = speed
        self.period = period


""" ATTRIBUTES

 Der zu obitierende Körper

mother  (public)

 distanz zum schwerpunkt


schwerpunkt  (protected)

"""
