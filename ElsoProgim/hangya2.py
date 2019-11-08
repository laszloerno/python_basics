from random import *
from turtle import *
from base import vector

def draw():
    "Move ant and draw screen."
    ant.move(aim)
 #   ant.x = wrap(ant.x)
 #   ant.y = wrap(ant.y)

    aim.move(random() - 0.5)
    aim.rotate(random() * 10 - 5)

#    clear()
    goto(ant.x, ant.y)
    dot(10)

    if running:
        ontimer(draw, 100)

ant = vector(0, 0)
aim = vector(random()-1, 0)

setup(500, 500, 250, 250)
hideturtle()
tracer(False)
up()
running = True
draw()
done()