
from random import choice
from turtle import *
from base import floor, vector

speed=5
aim = vector(speed, 0)
pacman = vector(-100, 160)
state = {'score': 0}
meret = 20

ghosts = [
    [vector(-180, 160), vector(5, 0)],
    [vector(-180, -160), vector(0, 5)],
    [vector(100, 160), vector(0, -5)],
    [vector(100, -160), vector(-5, 0)],
]


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
    print("Vilag kocka X=" + str(x) + "Y=" + str(y))
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
        x = (i % meret) * 20 - 200
        y = 180 - (i // meret) * 20
        negyzet(x, y)
        if lap == 1:
            palya.up()
            palya.goto(x + 10, y + 10)
            palya.dot(4, 'gold')

def offset(obj):
    x = (floor(obj.x, 20) + 200) / 20
    y = (180 - floor(obj.y, 20)) / 20
    index = int(x+y*meret)
    return index

def inside(head):
    "Return True if head inside screen."
    index = offset(head)

    if lapok[index] == 0:
        return False

    index = offset(head + 19)

    if lapok[index] == 0:
        return False

    return head.x % 20 == 0 or head.y % 20 == 0

def move():
    "Move pacman and all ghosts."

    clear()

    if inside(pacman+aim):
        pacman.move(aim)

    index = offset(pacman)

    if lapok[index] == 1:
        lapok[index] = 2
        state['score'] += 1
        x = (index % 20) * 20 - 200
        y = 180 - (index // 20) * 20
        negyzet(x, y)


    up()
    goto(pacman.x+10, pacman.y+10)
    dot(20, 'yellow')




    for point, course in ghosts:
        if inside(point + course):
            point.move(course)
        else:
            options = [
                vector(5, 0),
                vector(-5, 0),
                vector(0, 5),
                vector(0, -5),
            ]
            plan = choice(options)
            course.x = plan.x
            course.y = plan.y

        up()
        goto(point.x + 10, point.y + 10)
        dot(20, 'red')

    update()

    for point, course in ghosts:
        if abs(pacman - point) < 20:
            return



    ontimer(move, 100)

def change(x, y):
    "Change pacman aim if valid."
    if inside(pacman + vector(x, y)):
        aim.x = x
        aim.y = y





setup(420, 420, 370, 0)
hideturtle()
tracer(False)
writer.goto(160,160)
writer.color('white')
writer.write(state['score'])

listen()
onkey(lambda: change(speed, 0), 'Right')
onkey(lambda: change(-speed, 0), 'Left')
onkey(lambda: change(0, speed), 'Up')
onkey(lambda: change(0, -speed), 'Down')



vilag()
move()
done()