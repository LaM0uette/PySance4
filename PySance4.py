import os
import time
from enum import Enum
from termcolor import colored


class Player(Enum):
    Player1 = 1
    Player2 = 2


class NewGame:
    def __init__(self, sizeGame=7, tokenWin=4):
        self.run = True
        self.sizeGame = sizeGame
        self.tokenWin = tokenWin
        self.player_turn = Player.Player1
        self.matrix_game = self.gen_matrice()

    def gen_matrice(self):
        lst = []

        for row in range(self.sizeGame):
            lst.append([])

            for col in range(self.sizeGame):
                lst[row].append(0)

        return lst

    def draw_game(self):
        os.system("cls")

        lstIndex = '  '.join(f"{i + 1}" for i in range(self.sizeGame))
        if self.sizeGame >= 10:
            lstIndex = ''.join(f"%02d " % (i + 1) for i in range(self.sizeGame))

        print(f"""{f"Tour: {self.player_turn.name}" if self.run else ""}

                    {lstIndex}""")

        for i in range(self.sizeGame):
            print(f"""                   {''.join(f"[{colored('O', 'yellow') if x == 1 else colored('O', 'red') if x == 2 else colored('O', 'green', attrs=['bold']) if x == 3 else colored('O', 'green', attrs=['bold']) if x == 6 else ' '}]" for x in self.matrix_game[i])}""")

        print("")

    def add_token(self, token_played):
        if not token_played.isdigit():
            print("Valeur incorect !")
            time.sleep(0.5)
            return
        if not 0 < int(token_played) < self.sizeGame+1:
            print("Valeur incorect !")
            time.sleep(0.5)
            return

        token = int(token_played) - 1

        for i in range(self.sizeGame):
            iInv = self.sizeGame-1 - i

            if self.matrix_game[iInv][token] == 0:
                self.matrix_game[iInv][token] = self.player_turn.value
                break
        else: return

        self.check_win()
        self.check_end()

        self.player_turn = Player.Player2 if self.player_turn == Player.Player1 else Player.Player1

    def check_win(self):
        def check(result):
            if f"{self.player_turn.value}"*self.tokenWin in result:

                for i in range(self.tokenWin):
                    self.matrix_game[indexWin[i][0]][indexWin[i][1]] = self.player_turn.value*3

                self.run = False
                self.draw_game()

                self.draw_end(f"{self.player_turn.name} à gagné la partie !")

        # check row
        for row in range(self.sizeGame):
            result = "".join(str(x) for x in self.matrix_game[row])

            idxCol = result.find(f"{self.player_turn.value}" * self.tokenWin)
            indexWin = [[row, idxCol + i] for i in range(self.tokenWin)]
            check(result)

            if not self.run: break

        # check column
        for col in range(self.sizeGame):
            lstGD = []
            for row in range(self.sizeGame):
                lstGD.append(self.matrix_game[row][col])

            result = ''.join(str(x) for x in lstGD)

            idxCol = result.find(f"{self.player_turn.value}" * self.tokenWin)
            indexWin = [[idxCol + i, col] for i in range(self.tokenWin)]
            check(result)

            if not self.run: break

        # check diagoCol
        sizeGameUseful = self.sizeGame-3

        for row in range(sizeGameUseful):
            lst = [[], []]
            indexWin = [[], []]
            rowInc = row

            for col in range(self.sizeGame-row):
                lst[0].append(self.matrix_game[rowInc][col])
                lst[1].append(self.matrix_game[col][rowInc])
                rowInc += 1

            result = ''.join(str(x) for x in lst[1])
            idxCol = result.find(f"{self.player_turn.value}" * self.tokenWin)
            indexWin = [[idxCol + i, row + idxCol + i] for i in range(self.tokenWin)]
            check(result)

            if not self.run: break

            result = ''.join(str(x) for x in lst[0])
            idxCol = result.find(f"{self.player_turn.value}" * self.tokenWin)
            indexWin = [[row + idxCol + i, idxCol + i] for i in range(self.tokenWin)]
            check(result)

            if not self.run: break

        for row in range(sizeGameUseful):
            lst = [[], []]
            rowInc = row

            for col in range(self.sizeGame - row):
                colInv = self.sizeGame - 1 - col
                lst[0].append(self.matrix_game[rowInc][colInv])
                lst[1].append(self.matrix_game[self.sizeGame-1 - colInv][self.sizeGame-1 - rowInc])
                rowInc += 1

            Inv = self.sizeGame - 1

            result = ''.join(str(x) for x in lst[1])
            idxCol = result.find(f"{self.player_turn.value}" * self.tokenWin)
            indexWin = [[idxCol + i, (Inv-(row + idxCol)) - i] for i in range(self.tokenWin)]
            check(result)
            if not self.run: break

            result = ''.join(str(x) for x in lst[0])
            idxCol = result.find(f"{self.player_turn.value}" * self.tokenWin)
            indexWin = [[row + idxCol + i, (Inv-idxCol) - i] for i in range(self.tokenWin)]
            check(result)
            if not self.run: break

    def check_end(self):
        for item in self.matrix_game[0]:
            if item == 0:
                return

        self.run = False
        self.draw_game()
        self.draw_end("Grille pleine !")

    def draw_end(self, msg):
        print(f"""{colored(msg, 'yellow') if self.player_turn.value == 1 else colored(msg, 'red')}
                """)

    def start(self):
        os.system(f"mode con: cols={38 + (3 * self.sizeGame)} lines={7 + self.sizeGame}")

        while self.run:
            self.draw_game()

            input_player = input(f"Entrez le numéro d'une colonne (1 - {self.sizeGame}) : ")
            self.add_token(token_played=input_player)

run = True

while run:
    txt = input("Une partie ? (o|n) (c pour custom) : ")

    if txt.lower() == "o":
        NewGame().start()
    elif txt.lower() == "n":
        run = False
    elif txt.lower() == "c":
        size = int(input("Taille du plateau : "))
        tokenWin = int(input("Nombres de jetons à aligner : "))
        NewGame(sizeGame=size, tokenWin=tokenWin).start()
    else:
        print("Saisie incorect !")
