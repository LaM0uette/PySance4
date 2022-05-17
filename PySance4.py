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

    def init_display(self):
        os.system(f"mode con: cols={32 + (3 * self.sizeGame)} lines={7 + self.sizeGame}")

    def get_header_numbers(self):
        return ''.join("%02d " % (i + 1) for i in range(self.sizeGame)) if self.sizeGame >= 10 else '  '.join(f"{i + 1}" for i in range(self.sizeGame))

    def draw_player_turn(self):
        header = self.get_header_numbers()

        txt = self.player_turn.name if self.run else ""
        self.draw_rgb(txt)

        print(f"\t\t {header}")

    def draw_matrix_game(self):
        for i in range(self.sizeGame):

            row_txt = ""
            for token in self.matrix_game[i]:
                match token:
                    case 1:
                        token_rgb = colored('O', 'yellow')
                    case 2:
                        token_rgb = colored('O', 'red')
                    case 3:
                        token_rgb = colored('O', 'green', attrs=['bold'])
                    case 6:
                        token_rgb = colored('O', 'green', attrs=['bold'])
                    case _:
                        token_rgb = " "

                row_txt += f"[{token_rgb}]"

            print(f"\t\t{row_txt}")
        print()

    def draw_game(self):
        os.system("cls")

        self.draw_player_turn()
        self.draw_matrix_game()

    def draw_rgb(self, msg):
        rgb_txt = colored(msg, 'yellow') if self.player_turn.value == 1 else colored(msg, 'red')
        print(f"{rgb_txt}\n")

    def gen_matrice(self):
        lst = []

        for row in range(self.sizeGame):
            lst.append([])

            for _ in range(self.sizeGame):
                lst[row].append(0)

        return lst

    def add_token(self, token_played):
        if not token_played.isdigit() or not 0 < int(token_played) < self.sizeGame+1:
            print("Valeur incorect !")
            time.sleep(1)
            return

        token = int(token_played) - 1

        for i in range(self.sizeGame):
            inv = self.sizeGame - (i + 1)

            if self.matrix_game[inv][token] == 0:
                self.matrix_game[inv][token] = self.player_turn.value
                break
        else:
            return

        self.check_all_win()
        self.check_end()
        self.switch_player()
        
    def win_rgb(self, index_win):
        for i in range(self.tokenWin):
            row, col = index_win[i][0], index_win[i][1]
            self.matrix_game[row][col] = self.player_turn.value * 3
        
    def check_win(self, result, index_win):
        if f"{self.player_turn.value}" * self.tokenWin in result:
            self.win_rgb(index_win)
            self.run = False
            self.draw_game()
            self.draw_rgb(f"{self.player_turn.name} à gagné la partie !")

    def check_all_win(self):
        # check row
        for row in range(self.sizeGame):
            result = "".join(str(x) for x in self.matrix_game[row])

            idxCol = result.find(f"{self.player_turn.value}" * self.tokenWin)
            index_win = [[row, idxCol + i] for i in range(self.tokenWin)]
            self.check_win(result, index_win)

            if not self.run: break

        # check column
        for col in range(self.sizeGame):
            lstGD = []
            for row in range(self.sizeGame):
                lstGD.append(self.matrix_game[row][col])

            result = ''.join(str(x) for x in lstGD)

            idxCol = result.find(f"{self.player_turn.value}" * self.tokenWin)
            index_win = [[idxCol + i, col] for i in range(self.tokenWin)]
            self.check_win(result, index_win)

            if not self.run: break

        # check diagoCol
        sizeGameUseful = self.sizeGame-3

        for row in range(sizeGameUseful):
            lst = [[], []]
            index_win = [[], []]
            rowInc = row

            for col in range(self.sizeGame-row):
                lst[0].append(self.matrix_game[rowInc][col])
                lst[1].append(self.matrix_game[col][rowInc])
                rowInc += 1

            result = ''.join(str(x) for x in lst[1])
            idxCol = result.find(f"{self.player_turn.value}" * self.tokenWin)
            index_win = [[idxCol + i, row + idxCol + i] for i in range(self.tokenWin)]
            self.check_win(result, index_win)

            if not self.run: break

            result = ''.join(str(x) for x in lst[0])
            idxCol = result.find(f"{self.player_turn.value}" * self.tokenWin)
            index_win = [[row + idxCol + i, idxCol + i] for i in range(self.tokenWin)]
            self.check_win(result, index_win)

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
            index_win = [[idxCol + i, (Inv-(row + idxCol)) - i] for i in range(self.tokenWin)]
            self.check_win(result, index_win)
            if not self.run: break

            result = ''.join(str(x) for x in lst[0])
            idxCol = result.find(f"{self.player_turn.value}" * self.tokenWin)
            index_win = [[row + idxCol + i, (Inv-idxCol) - i] for i in range(self.tokenWin)]
            self.check_win(result, index_win)
            if not self.run: break

    def check_end(self):
        for token in self.matrix_game[0]:
            if token == 0:
                return

        self.run = False
        self.draw_game()
        self.draw_rgb("Grille pleine !")

    def switch_player(self):
        self.player_turn = Player.Player2 if self.player_turn == Player.Player1 else Player.Player1

    def start(self):
        self.init_display()

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
