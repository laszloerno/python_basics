class Parent():
    def MyMethod(self):
        print("parent")

class Child(Parent):
    def myMethd(self):
        print("child")

c = Child()
c.myMethd()