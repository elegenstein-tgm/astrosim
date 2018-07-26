from Engine import Engine
import Planet
import Star
import Orbit
from GravComplex import Solarsystem

au = 149597870691.0

if __name__ == '__main__':
    e = Engine()
    # init bodies
    sun = Star.Star(2e30, [0, 0], "Sun")
    merk = Planet.Planet(mass=3.301e23, pos=[1, 0], name='Merkur')
    merk.set_orbit(Orbit.Orbit(sun, merk, exzentritaet=0.20563, ga=0.387099273))
    venus = Planet.Planet(mass=4.869e24, pos=[2, 0], name='Venus')
    venus.set_orbit(Orbit.Orbit(sun, venus, exzentritaet=0.0067, ga=0.723))
    earth = Planet.Planet(mass=5.974e24, pos=[3, 0], name='Earth')
    earth.set_orbit(Orbit.Orbit(sun, earth, exzentritaet=0.0167, ga=1))
    mars = Planet.Planet(mass=6.419e23, pos=[4, 0], name='Mars')
    mars.set_orbit(Orbit.Orbit(sun, mars, exzentritaet=0.0935, ga=1.524))
    jupiter = Planet.Planet(mass=1.899e27, pos=[5, 0], name='Jupiter')
    jupiter.set_orbit(Orbit.Orbit(sun, jupiter, exzentritaet=0.0484, ga=5.203))
    jupiter.orbit.inklination = 2.277e-2
    s = Solarsystem()
    s.add_body(merk)
    s.add_body(venus)
    s.add_body(earth)
    s.add_body(mars)
    s.add_body(jupiter)

    for p in s.bodies:
        p.orbit.ga *= au
        p.orbit.type = p.orbit.TYPE_EXCENTRICAL_ORB

    s.set_star(sun)
    e.applysystem(s)
    print(str(e))
    e.draw_exzentri_system(s.bodies)
