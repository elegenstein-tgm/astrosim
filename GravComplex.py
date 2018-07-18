class Solarsystem:
    def __init__(self):
        self.bodies = []

    def add_body(self, body):
        self.bodies.append(body)

    def set_star(self,body):
        self.bodies.insert(-1,body)

