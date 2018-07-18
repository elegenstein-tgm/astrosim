# coding=UTF-8
from matplotlib import projections, legend
import numpy as np
from sympy import *
from scipy import constants
import Star
import Planet
import Orbit
import Body
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
        for i in range(0, richtv.size):
            if np.isnan(richtv[i]):
                richtv[i] = 0
        sp = b1posv + richtv * a1x
        return sp.tolist()

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
            r = np.abs(np.dot(v, v)) ** (1 / 2)
            if body.orbit.speed is not None:
                return 2 * r * constants.pi / body.orbit.speed
            else:
                p = 2 * r * constants.pi / self.calc_speed(body)
                return p
        else:
            raise Exception("Assign Orbit first")

    def two_norm(self, x1, x2):
        a = np.array(x2) - np.array(x1)
        return np.abs(np.dot(a, a)) ** (1 / 2)

    def calc_simp_orbit(self, body):
        v = np.array(body.pos) - np.array(body.orbit.sp)
        r = np.abs(np.dot(v, v)) ** (1 / 2)
        theta, phi = symbols("theta phi")
        if v.size == 3:
            the = acos(v[3] / r)
        elif v.size == 2:
            theta = pi / 2
        else:
            raise Exception("Unknown Dimensions")

        pih = atan2(v[1], v[0])
        # term = [r * cos(t), r * sin(t)]
        termx = r * cos(phi + pih) * sin(theta)
        termy = r * sin(phi + pih) * sin(theta)
        termz = r * cos(theta)
        print(r)
        if v.size == 2:
            return [termx, termy]
        raise Exception("Not implemented yet :(")

    def drawOrbits(self, body):
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
            self.drawOrbits(body)
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

    def calc_exzentri_orbit(self, body, override_pos=True):
        s = body.orbit
        s.calc_kb()
        dist = (1 + s.exzentritaet) * s.ga
        # for inkl = 0
        # positioning on x-axis
        npos = np.array(s.mother.pos) + np.array([1, 0]) * dist
        sw = np.array(self.calc_schwerpunkt(s.mother, Body.Body(s.bd.mass, npos.tolist(), '')))
        a = s.ga
        b = s.kb
        t = Symbol('t')
        term = sw + np.array([a * cos(t), b * sin(t)])
        s.track = term
        if override_pos:
            body.pos = npos.tolist()
        return term

    def draw_exzentri_system(self, bodies):
        ax = plt.subplot()
        for body in bodies:
            if body.has_orbit() and body.orbit.type is 2:
                self.calc_exzentri_orbit(body)
                self.plot_spec_orbit(ax, body)
        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
                   ncol=len(bodies), mode="expand", borderaxespad=0.)

        plt.grid()
        plt.show()

    def calc_orbit(self, body):
        if body.has_orbit():
            if body.orbit.type is 1:
                self.calc_simp_orbit(body)
            elif body.orbit.type is 2:
                self.calc_exzentri_orbit(body)

    def calc_given_things(self):
        for b in self.bodies:
            self.calc_speed(b)
            self.calc_period(b)
            if b.hasOrbit():
                self.calc_orbit(b)
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
    erg = e.calc_schwerpunkt(sun, earth)
    print(erg)
    earth.orbit.sp = erg
    erg = e.calc_speed(earth)
    earth.orbit.speed = erg
    erg = e.calc_period(earth)
    print(str(erg) + " sec -> " + str(erg / 31536000) + "years")
    e.print_status()
    print(e.calc_simp_orbit(earth))
    earth.orbit.sp
    # e.drawOrbits(earth)
    earth.orbit.exzentritaet = 0.0167
    earth.orbit.calc_kb()
    print(e.calc_exzentri_orbit(earth))
    e.draw_spec_orbit(earth)


# for i in range(0, 9 * 10 ** 4):
#    print(i)
