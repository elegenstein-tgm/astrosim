# coding=UTF-8
from Body import *


class Planet(Body):
    """


    :version:
    :author:
    """

    def __init__(self, mass, pos, name = 'Planet'):
        super(Planet, self).__init__(mass, pos, name, None)

    pass
