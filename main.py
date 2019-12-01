import random

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.vector import Vector
from kivy.clock import Clock


class Test(Widget):
    pass

class Buttons(Widget):
    pass

class Car(Widget):
    angle = NumericProperty(0)
    velocity = (0, 0)

    def move(self, rotation):
        self.pos = Vector(self.velocity) + self.pos
        self.angle = self.angle + rotation

class Game(Widget):
    car = None
    test = None
    buttons = None
    action2rotation = [0, 20, -20]

    def update(self, dt):
        action = random.randint(0, 2)
        rotation = self.action2rotation[action]
        self.car.move(rotation)
        self.car.velocity = Vector(5, 0).rotate(self.car.angle)

class MyPaintWidget(Widget):
    pass

class CarApp(App):

    def build(self):
        parent = Game()

        Clock.schedule_interval(parent.update, 1.0 / 60.0)
        return parent


# Running the whole thing
if __name__ == '__main__':
    CarApp().run()
