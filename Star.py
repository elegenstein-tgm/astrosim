# coding=UTF-8
from Body import *


class Star(Body):
    """


    :version:
    :author:
    """

    def __init__(self, mass, pos, name='Star'):
        super(Star, self).__init__(mass=mass, pos=pos, name=name, orbit=None)

    pass
