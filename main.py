"""
Pong Game with Kivy
"""

# The "App" class is the base class for all Kivy apps.
from kivy.app import App

# Widgets are the building blocks of your app
from kivy.uix.widget import Widget

# Properties are needed to define variable types for cross-platform compatibility
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty

# the Pong Ball's current position = last known position + velocity
# Vector uses this to calculate the next position, e.g. animation
from kivy.vector import Vector

# Clock is used to schedule events, usually in FPS
from kivy.clock import Clock

from random import randint


class PongPaddle(Widget):
    # The Paddle is a Rectangle (defined in the .kv file)
    # it checks whether the ball has collided with it, and
    # keeps track of the player's score.
    score = NumericProperty(0)  # defining an "int" property

    def bounce_ball(self, ball):
        if self.collide_widget(ball):  # collide_widget is built-in to Kivy
            ball.velocity_x *= -1.1


class PongBall(Widget):
    # PongBall's appearance is defined in the .kv file
    # here we define its position and velocity, along with
    # its movement.
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    # defining a "list" or "tuple" property
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        # Updates the position of the ball based on the velocity.
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
    # ObjectProperties are basically a bridge between the .kv file and this code

    # In pong.kv, we create the PongBall widget and add it to PongGame
    # giving it a unique id ("pong_ball"). Then it's connected to this "ball" variable
    # with "ball: pong_ball"
    ball = ObjectProperty(None)

    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def serve_ball(self):
        self.ball.pos = self.center
        # using a randint to randomize the angle of the ball
        self.ball.velocity = Vector(4, 0).rotate((randint(0, 360)))

    # update() is called every frame
    #   - checks for collisions
    #   - moves the ball
    #   - re-serves the ball if it goes out of bounds
    #   - moves the paddles

    def update(self, fps):
        self.ball.move()

        # bounce top / bottom
        if self.ball.y < 0 or self.ball.y > self.height - self.ball.height:
            self.ball.velocity_y *= -1

        # bounce off left
        if self.ball.x < 0:
            self.ball.velocity_x *= -1
            self.player1.score += 1
            self.serve_ball()

        # bounce off right
        if self.ball.x > self.width - self.ball.width:
            self.ball.velocity_x *= -1
            self.player2.score += 1
            self.serve_ball()

        # bounce off paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

    # Kivy automatically calls this method if the user touches / clicks the screen
    def on_touch_move(self, touch):
        if touch.x < self.width * 0.25:
            self.player1.center_y = touch.y
        if touch.x > self.width * 0.75:
            self.player2.center_y = touch.y


class PongApp(App):
    def build(self):
        # start the game
        game = PongGame()
        game.serve_ball()
        # call update() every frame
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == "__main__":
    PongApp().run()
