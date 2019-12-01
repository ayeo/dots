import random

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.vector import Vector
from kivy.clock import Clock


class Car(Widget):
    angle = NumericProperty(0)
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self, rotation):
        self.pos = Vector(self.velocity) + self.pos
        self.angle = self.angle + rotation

class Game(Widget):
    car = None
    action2rotation = [0, 20, -20]
    init = True

    def set_car(self, car, pos):
        self.car = car
        self.car.pos = pos
        self.add_widget(car)

    def update(self, dt):
        if (self.init):
            self.set_car(Car(), self.center)
            self.init = False

        action = random.randint(0, 2)
        rotation = self.action2rotation[action]
        self.car.move(rotation)
        self.car.velocity = Vector(5, 0).rotate(self.car.angle)


class CarApp(App):

    def build(self):
        parent = Game()

        Clock.schedule_interval(parent.update, 1.0 / 60.0)
        return parent


# Running the whole thing
if __name__ == '__main__':
    CarApp().run()
