# coding=UTF-8
from builtins import print

import numpy as np
from sympy import *
from scipy import constants

import Star
import Planet
import Orbit

# ploting
import matplotlib.pyplot as plt


class Engine:
    """


    :version:
    :author:
    """

    def __str__(self):
        return self.print_status()

    def __init__(self):
        self.bodies = []
        self.star = None

    def applysystem(self, system):
        self.bodies = system.bodies
        self.star = self.bodies[0]

    def tick(self):
        # body.has_orbit()

        pass

    def add_body(self, body):
        self.bodies.append(body)

    def print_status(self):
        counter = 1
        text = ""
        for body in self.bodies:
            if body.has_orbit():
                text += body.name + " with mass of " + str(body.mass) + " at " + str(
                    body.pos) + " with orbit around " + body.orbit.mother.name + " at " + str(
                    body.orbit.speed) + " m/s\n"
            else:
                text += body.name + " with mass of " + str(body.mass) + " at " + str(body.pos) + "\n"
            counter += 1
        return text

    def two_norm(self, x1, x2):
        a = np.array(x2) - np.array(x1)
        return np.abs(np.dot(a, a)) ** (1 / 2)

    def draw_orbits(self, body):
        ax = plt.subplot(111, projection='polar')
        p = np.arange(0.0, 2 * np.pi, 0.01)
        if body is not None:
            r1 = self.two_norm(body.pos, body.orbit.sp)
            r2 = self.two_norm(body.orbit.mother.pos, body.orbit.sp)
            ax.plot(p, np.array([r1] * p.size))
            ax.plot(p, np.array([r2] * p.size))
        else:
            ax.plot(p, np.array([1] * p.size))
            ax.plot(p, np.array([2] * p.size))
        plt.show()

    def draw_spec_orbit(self, body):
        if body.orbit.type is body.orbit.TYPE_SIMP_ORB:
            self.draw_orbits(body)
        elif body.orbit.type is body.orbit.TYPE_EXCENTRICAL_ORB:
            t = Symbol('t')
            tr = body.orbit.track
            ts = np.arange(0, 2 * np.pi + 0.2, 0.1)
            xs = tr[0]
            ys = tr[1]
            xv = []
            yv = []
            for te in ts:
                xv.append(xs.subs(t, te))
                yv.append(ys.subs(t, te))
            ax = plt.subplot()
            ax.plot(np.array(xv), np.array(yv))
            plt.grid()
            plt.show()

    def plot_spec_orbit(self, ax, body):
        if body.orbit.type is body.orbit.TYPE_SIMP_ORB:
            raise Exception("Not implemented")
        elif body.orbit.type is body.orbit.TYPE_EXCENTRICAL_ORB:
            t = Symbol('t')
            tr = body.orbit.track
            ts = np.arange(0, 2 * np.pi + 0.1, 0.1)
            xs = tr[0]
            ys = tr[1]
            xv = []
            yv = []
            for te in ts:
                xv.append(xs.subs(t, te))
                yv.append(ys.subs(t, te))
            ax.plot(np.array(xv), np.array(yv), label=body.name)
            return ax

    """
    for e in erg:
    ...:     f=lambdify(t,e,"math")
    ...:     erg2.append(f(np.pi/2))
    """

    def draw_exzentri_system(self, bodies):
        ax = plt.subplot()
        for body in bodies:
            if body.has_orbit() and body.orbit.type is 2:
                body.orbit.calc_exzentri_orbit()
                self.plot_spec_orbit(ax, body)
        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
                   ncol=len(bodies), mode="expand", borderaxespad=0.)

        plt.grid()
        plt.show()

    def calc_given_things(self):
        for b in self.bodies:
            b.orbit.calc_speed()
            b.orbit.calc_period()
            if b.hasOrbit():
                b.orbit.calc_orbit()
            else:
                b.orbit = Orbit.Orbit(self.star, b)
                b.orbit.type = b.orbit.TYPE_SUGGESTED


if __name__ == '__main__':
    e = Engine()
    sun = Star.Star(2.0 * 10 ** 30, [0, 0], name='sun')
    earth = Planet.Planet(5.972 * 10 ** 24, [constants.astronomical_unit, 0], name='earth')
    earth.set_orbit(orbit=Orbit.Orbit(orbital_body=sun, self_body=earth, ga=constants.astronomical_unit))
    e.add_body(sun)
    e.add_body(earth)
    erg = earth.orbit.calc_schwerpunkt()
    print(erg)
    earth.orbit.sp = erg
    erg = earth.orbit.calc_speed()
    earth.orbit.speed = erg
    erg = earth.orbit.calc_period()
    print(str(erg) + " sec -> " + str(erg / 31536000) + "years")
    e.print_status()
    print(earth.orbit.calc_simp_orbit())
    # earth.orbit.sp
    # e.drawOrbits(earth)
    earth.orbit.exzentritaet = 0.0167
    earth.orbit.inklination = np.pi / 4  # random value

    earth.orbit.calc_kb()
    orbite = earth.orbit.calc_exzentri_orbit()
    print("Orbit of is " + str(orbite))


# for i in range(0, 9 * 10 ** 4):
#    print(i)
