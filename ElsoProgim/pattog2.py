import turtle
import random
from base import vector

ball = vector(0, 0)
ir = vector(3, 3)

def draw():
    "Move ball and draw game."
    ball.move(ir)

    x = ball.x
    y = ball.y

    turtle.clear()
    turtle.goto(x, y)
    turtle.dot(10)

    turtle.ontimer(draw, 20)


turtle.setup(420, 420, 370, 0)
turtle.hideturtle()
turtle.tracer(False)
turtle.up()

draw()

turtle.done()