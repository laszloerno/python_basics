
from random import choice
from turtle import *
from base import floor, vector

speed=5
aim = vector(speed, 0)
pacman = vector(0, 0)

#   1  2  3  4  5  6  7  8  9  0  1  2  3  4  5  6  7  8  9  0
lapok = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0,
    0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    ]
palya = Turtle(visible=False)

def negyzet(x,y):
    palya.up()
    palya.goto(x, y)
    palya.down()
    palya.begin_fill()

    for count in range(4):
        palya.forward(20)
        palya.left(90)

    palya.end_fill()


def vilag():
    bgcolor('grey')
    palya.color('blue')

    for i in range(len(lapok)):
        lap = lapok[i]
        if lap == 0:
            palya.color('black')
        if lap > 0:
            palya.color('blue')
        x = (i % 20) * 20 - 200
        y = 180 - (i // 20) * 20
        negyzet(x, y)
        if lap == 1:
            palya.up()
            palya.goto(x + 10, y + 10)
            palya.dot(4, 'gold')

def inside(head):
    "Return True if head inside screen."
    return -200 < head.x < 200 and -200 < head.y < 200

def move():
    "Move pacman and all ghosts."

    clear()

    if inside(pacman+aim):
        pacman.move(aim)

    up()

    goto(pacman.x, pacman.y)
    dot(20, 'red')

    update()
    print("Pacman = " + str(pacman) + " Irány = " + str(aim) )

    ontimer(move, 100)

def change(x, y):
    "Change pacman aim if valid."
    aim.x = x
    aim.y = y





setup(420, 420, 370, 0)
hideturtle()
tracer(False)
listen()
onkey(lambda: change(speed, 0), 'Right')
onkey(lambda: change(-speed, 0), 'Left')
onkey(lambda: change(0, speed), 'Up')
onkey(lambda: change(0, -speed), 'Down')



vilag()
move()
done()