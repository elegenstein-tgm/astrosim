# coding=UTF-8

from abc import ABC


class Body(ABC):
    """


  :version: 0.1
  :author: erik
  """

    def __init__(self, mass, pos, name, orbit=None):
        self.mass = mass
        self.orbit = orbit
        self.pos = pos
        self.name = name
        pass

    def set_orbit(self, orbit):
        self.orbit = orbit

    def has_orbit(self):
        if self.orbit is None:
            return False
        return True


