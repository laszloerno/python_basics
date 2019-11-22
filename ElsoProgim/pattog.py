"""Bounce, a simple animation demo.

Exercises

1. Make the ball speed up and down.
2. Change how the ball bounces when it hits a wall.
3. Make the ball leave a trail.
4. Change the ball color based on position.
   Hint: colormode(255); color(0, 100, 200)

"""

import turtle
import random
"from turtle import *"
from base import vector

def value():
    "Randomly generate value between (-5, -3) or (3, 5)."
    return (3 + random.random() * 1) * random.choice([1, -1])



ball = vector(0, 0)
ir = vector(value(), value())

def draw():
    "Move ball and draw game."
    ball.move(ir)

    x = ball.x
    y = ball.y

    if x < -200 or x > 200:
        ir.x = -ir.x
        turtle.colormode(255)
        r = random.randrange(0, 257, 10)
        g = random.randrange(0, 257, 10)
        b = random.randrange(0, 257, 10)
        turtle.color(r, g, b)

    if y < -200 or y > 200:
        ir.y = -ir.y
        turtle.colormode(255)
        r = random.randrange(0, 257, 10)
        g = random.randrange(0, 257, 10)
        b = random.randrange(0, 257, 10)
        turtle.color(r, g, b)

    # 4
    """
    turtle.colormode(255)
    if x < 0 and y < 0:
        turtle.color(255, 0, 0)

    if x > 0 and y < 0:
        turtle.color(0, 255, 0)

    if x > 0 and y > 0:
        turtle.color(0, 0, 255)


    if x < 0 and y > 0:
        turtle.color(0, 100, 100)
    """

    print("X=" + str(ball.x))
    print("Y=" + str(ball.y))

    #turtle.clear()
    turtle.goto(x, y)
    turtle.dot(10)

    turtle.ontimer(draw, 5)

turtle.setup(420, 420, 370, 0)
turtle.hideturtle()
turtle.tracer(False)
turtle.up()
draw()
turtle.done()
