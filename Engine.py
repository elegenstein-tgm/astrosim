# coding=UTF-8
import numpy as np
from sympy import Symbol, solve
import Star
import Planet


class Engine:
    """


    :version:
    :author:
    """

    def __init__(self):
        self.bodies = []

    def tick(self):
        pass

    def add_body(self, body):
        self.bodies.append(body)

    def calc_schwerpunkt(self, Body1, Body2):
        distv = np.array(Body2.pos) - np.array(Body1.pos)
        # print(distv)
        dist = 0
        # print(distv * distv)
        for e in distv * distv:
            dist += np.abs(e)
            # dist = dist**(1 / 2)
        # print(dist)
        dist = np.sqrt(np.abs(dist))
        # print(dist)
        a1 = Symbol("a1")
        m1 = Body1.mass
        m2 = Body2.mass
        t1 = (dist - a1) * m2 - a1 * m1
        # print(t1)
        a1x = solve(t1, a1)[0]
        # a2x = dist - a1x
        b1posv = np.array(Body1.pos)
        richtv = distv / dist
        # print(distv)
        for i in range(0, 3):
            if np.isnan(richtv[i]):
                richtv[i] = 0
        sp = b1posv + richtv * a1x
        return sp.tolist()

    def print_status(self):
        counter = 1
        for body in self.bodies:
            if body.has_orbit():
                print(body.name + " with mass of " + str(body.mass) + " at " + str(body.pos) + "with orbit")
            else:
                print(body.name + " with mass of " + str(body.mass) + " at " + str(body.pos))
            counter += 1


if __name__ == '__main__':
    e = Engine()
    sun = Star.Star(2 * 10 ** 30, [0, 0, 0], name='sun')
    earth = Planet.Planet(6 * 10 ** 24, [150 * 10 ** 9, 0, 0], name='earth')
    e.add_body(sun)
    e.add_body(earth)
    erg = e.calc_schwerpunkt(sun, earth)
    print(erg)
    e.print_status()
