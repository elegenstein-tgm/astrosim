# coding=UTF-8
import numpy as np
from sympy import Symbol, solve
from scipy import constants
import Star
import Planet
import Orbit


class Engine:
    """


    :version:
    :author:
    """

    def __init__(self):
        self.bodies = []

    def tick(self):
        body.has_orbit()

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
                print(body.name + " with mass of " + str(body.mass) + " at " + str(
                    body.pos) + " with orbit around " + body.orbit.mother.name + " at " + str(
                    body.orbit.speed) + " m/s")
            else:
                print(body.name + " with mass of " + str(body.mass) + " at " + str(body.pos))
            counter += 1

    def calc_speed(self, body):
        if body.has_orbit():
            ms = body.orbit.mother.mass
            vk = Symbol("vk")
            distv = np.array(body.orbit.sp) - np.array(body.pos)
            r = np.dot(distv, distv)
            r = np.abs(r)
            r = r ** (1 / 2)
            te = (constants.gravitational_constant * ms / r) ** (1 / 2) - vk
            vkx = solve(te, vk)
            v = 0
            for f in vkx:
                v = abs(f)
            return v
        else:
            return 0

    def calc_period(self, body):
        if body.has_orbit():
            v = np.array(body.orbit.sp) - np.array(body.pos)
            np.abs(np.dot(v, v)) ** (1 / 2)


if __name__ == '__main__':
    e = Engine()
    sun = Star.Star(2 * 10 ** 30, [0, 0, 0], name='sun')
    earth = Planet.Planet(6 * 10 ** 24, [constants.astronomical_unit, 0, 0], name='earth')
    earth.set_orbit(orbit=Orbit.Orbit(orbital_body=sun, self_body=earth))
    e.add_body(sun)
    e.add_body(earth)
    erg = e.calc_schwerpunkt(sun, earth)
    earth.orbit.sp = erg
    erg = e.calc_speed(earth)
    earth.orbit.speed = erg

    e.print_status()
