from random import *
from turtle import *
from base import vector

colors  = ["red","green","blue","orange","purple","pink","yellow"]

colormode(255)

def draw():
    "Move ant and draw screen."
    ha.move(ir)
    #   ant.x = wrap(ant.x)
    #   ant.y = wrap(ant.y)

    ir.move(random() - 0.5)
    ir.rotate(random() * 90 - 45)

    #    clear()
    goto(ha.x, ha.y)

    #color(choice(colors))
   #   color("blue")
    r = randrange(0, 257, 10)
    g = randrange(0, 257, 10)
    b = randrange(0, 257, 10)
    color(r, g, b)

    dot(random()*15)

    if running:
        ontimer(draw, 100)


ha = vector(0, 0)
ir = vector(2, 0)


setup(500, 500, 250, 250)

hideturtle()
tracer(False)
up()
running = True
draw()

done()