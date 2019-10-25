class Player():
    def __init__(self, nev, kor):
        self.name = nev
        self.kora = kor


    def allapot(self):
        print("A Játékos neve {} és életkora {}".format(self.name, self.kora))


class Wizzard(Player):
    def __init__(self,nev, kor, varazs):
        super().__init__(nev,kor)
        self.__varazsero = varazs

    def allapot(self):
        super().allapot()
        print("Varázserő szintje {}".format(self.__varazsero))




erno = Player("Ernő",28)
#erno.allapot()

zoli = Player("Zoli",32)

geza = Wizzard("Géza", 45,34)
geza.allapot()
