import os
import random
import time


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')
    # print("\n" * 15)


class TicTacToe:

    def __init__(self):
        self.player1 = None
        self.player2 = None
        self.turn = None
        self.choice_allowed = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.winning_list = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"],
                             ["1", "4", "7"], ["2", "5", "8"], ["3", "6", "9"],
                             ["1", "5", "9"], ["3", "5", "7"]]
        self.place_to_play = ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ']
        self.used_numbers = []

    def select_mode(self):
        print("\nChoose what mode are you interested in?")
        mode = input("1 - One Player | 2 - Two Players: ")
        if mode == "1" or mode == "2":
            cls()
            return mode

        else:
            print("Wrong choice. Try again")
            cls()
            self.select_mode()

    def select_side(self):
        side_x = ["1", "X", "x"]
        side_o = ["2", "O", "o"]
        print("\nChoose what side do you want to be?")
        side = input("1 - X | 2 - O : ")
        if side in side_x:
            return side_x
        elif side in side_o:
            return side_o
        else:
            print("Wrong choice. Try again")
            self.select_side()

    def set_game(self):
        mode = self.select_mode()

        # Mode 1 Player vs CPU
        if mode == "1":
            side = self.select_side()
            # Side 1 == sign "x'
            if "x" in side:
                self.player1 = Player(" x ")
                self.player2 = Cpu(" o ", self.player1.moves)
            else:
                self.player2 = Player(" o ")
                self.player1 = Cpu(" x ", self.player2.moves)

        else:
            self.player1 = Player(" x ")
            self.player2 = Player(" o ")

        self.turn = self.player1

    def check_win(self):
        check = False
        for winning_sequence in self.winning_list:
            # for every item in winning_sequence check if the item is in self.turn.moves(actual player moves list)
            check = all(item in self.turn.moves for item in winning_sequence)
            if check:
                print(f"Player{self.turn.sign}is the winner.")
                time.sleep(3)
                break

        if len(self.used_numbers) >= 9 and check is False:
            print("Nobody win. It's a draw.")
            time.sleep(3)
            check = True
        return check

    def display_game(self):
        print(f"\n{self.place_to_play[0]}|{self.place_to_play[1]}|{self.place_to_play[2]}")
        print("-----------")
        print(f"{self.place_to_play[3]}|{self.place_to_play[4]}|{self.place_to_play[5]}")
        print("-----------")
        print(f"{self.place_to_play[6]}|{self.place_to_play[7]}|{self.place_to_play[8]}")

    @staticmethod
    def display_pattern():
        print("\n 1 | 2 | 3 ")
        print("-----------")
        print(" 4 | 5 | 6 ")
        print("-----------")
        print(" 7 | 8 | 9 ")
        time.sleep(2)

    # place user input on display screen
    def set_player_choice(self, choice):
        self.place_to_play[int(choice) - 1] = self.turn.sign
        self.turn.add_move(choice)
        self.used_numbers.append(choice)

    # check if the actual user input is valid or is or is not used already
    def is_valid(self):
        valid = False
        while not valid:
            # used_numbers = self.player1.moves + self.player2.moves
            choice = self.turn.next_move()
            if choice not in self.choice_allowed:
                print("Invalid Input. Use numbers from 1 to 9.")
            elif choice in self.used_numbers:
                print("Invalid Input. This number is used already.")
            else:
                self.set_player_choice(choice)
                valid = True

    def play_again(self):
        cls()
        choice = input("\nDo you want to play again? Yes or No: ")
        yes = ["Yes", "yes", "1", "Y", "y"]
        if choice in yes:
            self.player1 = None
            self.player2 = None
            self.turn = None
            self.place_to_play = ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ']
            self.used_numbers = []
            self.set_game()
            self.display_pattern()
            return False
        else:
            return True


class Player:

    def __init__(self, sign):
        self.moves = []
        self.sign = sign

    def add_move(self, move):
        self.moves.append(move)

    def next_move(self):
        return input("Please choice your position: ")


class Cpu(Player):

    def __init__(self, sign, opponent_moves):
        super().__init__(sign)
        self.winning_pairs = [["1", "2"], ["1", "3"], ["1", "4"], ["1", "5"], ["1", "7"], ["1", "9"],
                              ["2", "3"], ["2", "5"], ["2", "8"], ["3", "5"], ["3", "6"], ["3", "7"],
                              ["3", "9"], ["4", "5"], ["4", "6"], ["4", "7"], ["5", "6"], ["5", "7"],
                              ["5", "8"], ["5", "9"], ["6", "9"], ["7", "8"], ["7", "9"], ["8", "9"],
                              ]
        self.winning_list = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"],
                             ["1", "4", "7"], ["2", "5", "8"], ["3", "6", "9"],
                             ["1", "5", "9"], ["3", "5", "7"]
                             ]
        self.opponent_moves = opponent_moves
        self.choice_allowed = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.corners = ["1", "3", "7", "9"]

    def find_win_pairs(self, moves):
        list_of_possibly_wins = []
        for pair in self.winning_pairs:
            check = all(item in moves for item in pair)
            if check:
                list_of_possibly_wins.append(pair)

        return list_of_possibly_wins

    def possible_moves(self, moves_to_win):
        used_numbers = self.moves + self.opponent_moves
        possibly_moves_list = []

        for win in self.winning_list:

            for move in moves_to_win:
                check = all(item in win for item in move)

                if check:

                    for item in win:

                        if item not in move and item not in used_numbers:
                            possibly_moves_list.append(item)

        return possibly_moves_list

    def next_move(self):
        used_numbers = self.opponent_moves + self.moves
        opponent_wins_moves = self.possible_moves(self.find_win_pairs(self.opponent_moves))
        my_wins_moves = self.possible_moves(self.find_win_pairs(self.moves))

        # if there is any move to win then return this move
        if len(my_wins_moves) > 0:
            return random.choice(my_wins_moves)

        # if there isn't any moves and opponent don't have any then...
        if len(opponent_wins_moves) < 1:

            if "5" not in used_numbers:
                move = "5"

            elif len(used_numbers) <= 4:
                move = random.choice([item for item in self.corners if item not in used_numbers])

            else:
                move = random.choice([item for item in self.choice_allowed if item not in used_numbers])

        else:
            move = random.choice(opponent_wins_moves)
            if move in used_numbers:
                rest_choices = [item for item in self.choice_allowed if item not in used_numbers]
                move = random.choice(rest_choices)

        print(f"Please choice your position: {move}")
        return move


game = TicTacToe()

stop = False
print("Welcome to TicTacToe Game")
game.set_game()
game.display_pattern()

while not stop:

    print(f"Turn player:{game.turn.sign}")
    game.is_valid()
    cls()
    game.display_game()
    stop = game.check_win()

    if game.turn.sign == " x ":
        game.turn = game.player2
    else:
        game.turn = game.player1

    if stop:
        stop = game.play_again()
