from math import *

def p(str1):
    print(str1)

def felhasznalo(nev = "Senki", kor = 0):
    p("A felhasználó neve: {} és életkora {}".format(nev,kor))

def tanulok(*osztaly):
    for diak in osztaly:
        felhasznalo(str(diak["Nev"]),int(diak["kor"]))

def add(*num):
    eredm = 0
    for n in num:
        eredm = eredm + n
    return eredm

p(add(1,2,3))

p(eval("add(9,9,9)"))


# osztalynevsor = [{"Nev":"Ernő", "Kor":"37"},
#                 {"Nev":"Peti", "Kor":"13"}
#                 ]
#tanulok(osztalynevsor)

#Kiir("hello")
#felhasznalo(kor = 4)
