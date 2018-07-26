# coding=UTF-8
from Body import Body
import numpy as np
from sympy import *
from scipy import constants


# from Engine import Engine


class Orbit:
    TYPE_NOT_DEF = 0
    TYPE_SIMP_ORB = 1
    TYPE_EXCENTRICAL_ORB = 2
    TYPE_SUGGESTED = -1

    def __init__(self, orbital_body, self_body=None, schwerpunkt=None, speed=None, period=None, track=None,
                 exzentritaet=None, ga=None, b=None, inkl=0, typ=TYPE_NOT_DEF):
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
        self.typ = typ

    def calc_kb(self):
        self.kb = (self.ga ** 2 - (self.ga * self.exzentritaet) ** 2) ** (1 / 2)
        self.typ = 2

    def set_type(self, type):
        self.typ = type

    def calc_speed(self):
        body = self.bd
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

    def calc_period(self):
        body = self.bd
        if body.has_orbit():
            v = np.array(body.orbit.sp) - np.array(body.pos)
            r = np.abs(np.dot(v, v)) ** (1 / 2)
            if body.orbit.speed is not None:
                return 2 * r * constants.pi / body.orbit.speed
            else:
                p = 2 * r * constants.pi / self.calc_speed()
                return p
        else:
            raise Exception("Assign Orbit first")

    def calc_schwerpunkt(self, bbody1=None, bbody2=None):
        if bbody1 is None:
            bbody1 = self.mother
        if bbody2 is None:
            bbody2 = self.bd
        if len(bbody1.pos) > len(bbody2.pos):
            bbody2.pos.append(0)
        elif len(bbody1.pos) < len(bbody2.pos):
            bbody1.pos.append(0)
        distv = np.array(bbody2.pos) - np.array(bbody1.pos)
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
        m1 = bbody1.mass
        m2 = bbody2.mass
        t1 = (dist - a1) * m2 - a1 * m1
        # print(t1)
        a1x = solve(t1, a1)[0]
        # a2x = dist - a1x
        b1posv = np.array(bbody1.pos)
        richtv = distv / dist
        # print(distv)
        for i in range(0, richtv.size):
            if np.isnan(richtv[i]):
                richtv[i] = 0
        sp = b1posv + richtv * a1x
        return sp.tolist()

    def calc_simp_orbit(self):
        body = self.bd
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

    def calc_exzentri_orbit(self, override_pos=True):
        body = self.bd
        s = body.orbit
        s.calc_kb()
        dist = (1 + s.exzentritaet) * s.ga
        # for inkl = 0
        # positioning on x-axis with inklination (2D -> 3D)
        if body.orbit.inklination is not 0:
            xp = dist * np.sin(np.pi / 2 + body.orbit.inklination)
            yp = 0
            zp = dist * np.cos(body.orbit.inklination)
            npos = np.array([xp, yp, zp])
        else:
            npos = np.array(s.mother.pos) + np.array([1, 0]) * dist
        sw = np.array(self.calc_schwerpunkt(s.mother, bbody2=Body(s.bd.mass, npos.tolist(), '')))
        a = s.ga
        b = s.kb
        t = Symbol('t')
        term = ""
        if len(npos.tolist()) is 2:
            term = sw + np.array([a * cos(t), b * sin(t)])
        elif len(npos.tolist()) is 3:
            c = np.dot((npos - sw), np.array([0, 0, 1]))  # z-offset
            term = sw + np.array([a * cos(t), b * sin(t), c * cos(t)])
            # dy = np.array([[np.cos(body.orbit.inklination), 0, np.sin(body.orbit.inklination)], [0, 1, 0],
            # [-np.sin(body.orbit.inklination), 0, np.cos(body.orbit.inklination)]])

        s.track = term
        if override_pos:
            body.pos = npos.tolist()
            body.orbit.sp = sw.tolist()
        return term

    def calc_orbit(self):
        body = self.bd
        if body.has_orbit():
            if body.orbit.type is 1:
                self.calc_simp_orbit()
            elif body.orbit.type is 2:
                self.calc_exzentri_orbit(body)


""" ATTRIBUTES

 Der zu obitierende Körper

mother  (public)

 distanz zum schwerpunkt


schwerpunkt  (protected)

"""
