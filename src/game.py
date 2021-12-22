# rows = 6 columns = 7
import os
import csv
from board import Board
from player import Player


class Game(Board):
    def __init__(self, player1_name="player1", player2_name="player2", rows=6, columns=7):
        self.player1 = Player(player1_name, 1)
        self.player2 = Player(player2_name, 2)
        self.next = self.player1.color
        self.moves = []
        self.winner = None
        self.looser = None
        self.game_end = False
        self.path_to_file = "data/results.csv"
        Board.__init__(self, rows, columns)

    def change_player(self):
        if self.next == self.player1.color:
            self.next = self.player2.color
        else:
            self.next = self.player1.color

    def save_result(self):
        fieldnames = ['player', 'points', "games_played", "win", "lose", "draw"]
        file_exists = os.path.exists(self.path_to_file)
        if self.winner is None:
            records = {
                self.player1.color: {"player": self.player1.name, "points": 1, "games_played": 1, "win": 0, "lose": 0, "draw": 1},
                self.player2.color: {"player": self.player2.name, "points": 1, "games_played": 1, "win": 0, "lose": 0, "draw": 1}}
        else:
            records = {
                self.winner: {"player": self.winner, "points": 3, "games_played": 1, "win": 1, "lose": 0,"draw": 0},
                self.looser: {"player": self.looser, "points": 0, "games_played": 1, "win": 0, "lose": 1,"draw": 0}}

        if not file_exists:
            with open(self.path_to_file, "w", newline="") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
                writer.writeheader()

        with open(self.path_to_file, newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=";")
            try:
                next(reader)
            except:
                raise Exception("Error")

            for row in reader:
                record = {"player": row[0],
                          "points": int(row[1]),
                          "games_played": int(row[2]),
                          "win": int(row[3]),
                          "lose": int(row[4]),
                          "draw": int(row[5])}

                # wyszukiwanie czy gracz nie powtarza się w tabeli wyników
                for key, val in records.items():
                    if row[0] == key:
                        record["points"] += int(val["points"])
                        record["games_played"] += val["games_played"]
                        record["win"] += val["win"]
                        record["lose"] += val["lose"]
                        record["draw"] += val["draw"]
                records[row[0]] = record

        with open(self.path_to_file, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            for key, value in records.items():
                writer.writerow(value)
        return True

    def check_winning_conditions(self):
        result = self.check_board(self.player1.color, self.player2.color)
        if result[0]:
            if result[1] == self.player1.color:
                self.winner = self.player1.name
                self.looser = self.player2.name
            else:
                self.winner = self.player2.name
                self.looser = self.player1.name
            self.game_end = True
            self.save_result()
            return True
        return False

    def move(self, col):
        if self.game_end:
            raise Exception("Koniec gry, wygrał: {}".format(self.winner))
        if type(col) is not int:
            raise ValueError("!!! BŁĘDNE DANE WEJŚCIOWE {} !!!".format(type(col)))
        if col not in range(1, 8):
            raise Exception("!!! ZŁY ZAKRES !!!")

        col -= 1
        if self.board[0][col] == self.separator:
            for i in range(5, -1, -1):
                if self.board[i][col] == self.separator:
                    self.board[i][col] = self.next
                    self.moves.append(col)
                    self.check_winning_conditions()
                    self.change_player()
                    break
        else:
            raise Exception("Nie mogę wykonać ruchu, kolumna {} pełna, spróbuj ponownie.".format(col + 1))

        return self.board

    def move_back(self):
        if self.game_end:
            raise Exception("Koniec gry, wygrał: {}".format(self.winner))
        if not self.moves:
            raise Exception("Nie można cofnąć ruchu")

        else:
            col = self.moves.pop()
            for i in range(5, -1, -1):
                if self.board[i][col] != self.separator:
                    self.board[i][col] = self.separator
                    self.change_player()
                    return self.board
            raise Exception("Error")
