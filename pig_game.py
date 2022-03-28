import random
import argparse
import time

random.seed(time.time())


class Player(object):

    def __init__(self, id_value):
        self.score = 0
        self.id = id_value
        self.is_computer = False

    def add_score(self, new_score):
        self.score = self.score + new_score

    def get_score(self):
        return self.score

    def get_id(self):
        return self.id

    def roll(self):
        return random.randint(1, 6)


class ComputerPlayer(Player):
    def __init__(self, id_value):
        super().__init__(id_value)
        self.is_computer = True

    def follow_strategy(self, current_turn_total):
        if current_turn_total < 25 and 100 - self.get_score() > 25:
            return 'r'
        elif 100 - self.get_score() < 25 and current_turn_total < 100 - self.get_score():
            return 'r'
        else:
            return 'k'


class PlayerFactory(object):
    def getPlayer(self, kind, p_id):
        if kind == 'human':
            return Player(p_id)
        elif kind == 'computer':
            return ComputerPlayer(p_id)


class Game(object):

    def __init__(self, player1_type, player2_type, player_factory):
        self.players = [player_factory.getPlayer(player1_type, "Player 1"),
                        player_factory.getPlayer(player2_type, "Player 2")]
        self.current_active_player = self.players[0]
        self.current_active_index = 0

    def get_players_and_scores(self):
        results = {}

        for p in self.players:
            results[p.get_id()] = p.get_score()

        return results

    def get_current_active_player(self):
        return self.current_active_player

    def get_current_active_player_id(self):
        return self.current_active_player.get_id()

    def change_current_active_player(self):
        self.current_active_index += 1

        if self.current_active_index > len(self.players) - 1:
            self.current_active_index = 0

        self.current_active_player = self.players[self.current_active_index]

    def game_loop(self):
        winner = False
        turn_player_total = 0

        while not winner:

            if self.get_current_active_player().is_computer:

                computer_input = self.get_current_active_player().follow_strategy(turn_player_total)

                print(f"Computer {self.get_current_active_player_id()} chose '{computer_input}'")

                decision = computer_input

            else:

                decision = input(
                    f"{self.get_current_active_player_id()} type 'r' to roll or type 'k' to keep your score.\n")

            while decision != 'r' and decision != 'k':

                if self.get_current_active_player().is_computer:

                    computer_input = self.get_current_active_player().follow_strategy(turn_player_total)

                    print(f"Computer {self.get_current_active_player_id()} chose '{computer_input}'")

                    decision = computer_input

                else:

                    decision = input(
                        f"{self.get_current_active_player_id()} type 'r' to roll or type 'k' to keep your score.\n")

            while decision == 'r':

                current_roll = self.get_current_active_player().roll()

                if current_roll != 1:

                    print(f"{self.get_current_active_player_id()} rolled a {current_roll}")

                    turn_player_total += current_roll

                    print(f"{self.get_current_active_player_id()} has a total roll of {turn_player_total}.")

                    print(
                        f"{self.get_current_active_player_id()} would have a total score of {self.get_current_active_player().get_score() + turn_player_total}.")

                    if self.get_current_active_player().is_computer:

                        computer_input = self.get_current_active_player().follow_strategy(turn_player_total)

                        print(f"Computer {self.get_current_active_player_id()} chose '{computer_input}'")

                        decision = computer_input

                    else:

                        decision = input(
                            f"{self.get_current_active_player_id()} type 'r' to roll or type 'k' to keep your score.\n")

                else:

                    print(f"{self.get_current_active_player_id()} rolled a 1 and forfeited their turn.")

                    turn_player_total = 0

                    decision = 'k'

            if decision == 'k':

                print(f"{self.get_current_active_player_id()} added a total of {turn_player_total} to their score.")

                self.get_current_active_player().add_score(turn_player_total)

                print(
                    f"{self.get_current_active_player_id()} currently has a total score of {self.get_current_active_player().get_score()}")

                turn_player_total = 0

                if self.get_current_active_player().get_score() >= 100:

                    winner = True

                    print(f"Congratulations {self.get_current_active_player_id()}!")

                else:

                    self.change_current_active_player()

                    print(f"{self.get_current_active_player_id()} it's your turn.")


class TimedGameProxy(Game):
    def __init__(self, player1, player2, player_factory):
        self.time_start = 0
        self.turn_player_total = 0
        super().__init__(player1, player2, player_factory)

    def game_loop(self):
        winner = False

        self.time_start = time.time()
        time_since_start = time.time() - self.time_start

        while not winner and time_since_start < 60.0:

            if self.get_current_active_player().is_computer:

                computer_input = self.get_current_active_player().follow_strategy(self.turn_player_total)

                print(f"Computer {self.get_current_active_player_id()} chose '{computer_input}'")

                decision = computer_input

            else:

                decision = input(
                    f"{self.get_current_active_player_id()} type 'r' to roll or type 'k' to keep your score.\n")

            while decision != 'r' and decision != 'k':

                if self.get_current_active_player().is_computer:

                    computer_input = self.get_current_active_player().follow_strategy(self.turn_player_total)

                    print(f"Computer {self.get_current_active_player_id()} chose '{computer_input}'")

                    decision = computer_input

                else:

                    decision = input(
                        f"{self.get_current_active_player_id()} type 'r' to roll or type 'k' to keep your score.\n")

                time_since_start = time.time() - self.time_start

            while decision == 'r':

                current_roll = self.get_current_active_player().roll()

                if current_roll != 1:

                    print(f"{self.get_current_active_player_id()} rolled a {current_roll}")

                    self.turn_player_total += current_roll

                    print(f"{self.get_current_active_player_id()} has a total roll of {self.turn_player_total}.")

                    print(
                        f"{self.get_current_active_player_id()} would have a total score of {self.get_current_active_player().get_score() + self.turn_player_total}.")

                    if self.get_current_active_player().is_computer:

                        computer_input = self.get_current_active_player().follow_strategy(self.turn_player_total)

                        print(f"Computer {self.get_current_active_player_id()} chose '{computer_input}'")

                        decision = computer_input

                    else:

                        decision = input(
                            f"{self.get_current_active_player_id()} type 'r' to roll or type 'k' to keep your score.\n")

                    time_since_start = time.time() - self.time_start

                else:

                    print(f"{self.get_current_active_player_id()} rolled a 1 and forfeited their turn.")

                    self.turn_player_total = 0

                    decision = 'k'

                    time_since_start = time.time() - self.time_start

            if decision == 'k':

                print(
                    f"{self.get_current_active_player_id()} added a total of {self.turn_player_total} to their score.")

                self.get_current_active_player().add_score(self.turn_player_total)

                print(
                    f"{self.get_current_active_player_id()} currently has a total score of {self.get_current_active_player().get_score()}")

                self.turn_player_total = 0

                if self.get_current_active_player().get_score() >= 100:

                    winner = True

                    print(f"Congratulations {self.get_current_active_player_id()}!")

                else:

                    self.change_current_active_player()

                    print(f"{self.get_current_active_player_id()} it's your turn.")

                time_since_start = time.time() - self.time_start

        if time_since_start >= 60.0:
            print(f"Time is up!")

            default_winner = self.players[0].get_id() if self.players[0].get_score() > self.players[1].get_score() else \
            self.players[1].get_id()

            print(f"Congratulations {default_winner}!")


def main():
    parser = argparse.ArgumentParser(description='Pig self.', usage="%{prog}s --player1 human --player2 computer")
    parser.add_argument('--player1', metavar='\b', required=True, type=str, help='Player 1, computer or human.')
    parser.add_argument('--player2', metavar='\b', required=True, type=str, help='Player 2, computer or human.')

    parser.add_argument('--timed', action='store_true', required=False, help='Run a timed game.')

    args = parser.parse_args()

    player_factory = PlayerFactory()

    if args.timed:

        proxy = TimedGameProxy(args.player1, args.player2, player_factory)
        proxy.game_loop()

    else:

        game = Game(args.player1, args.player2, player_factory)
        game.game_loop()


if __name__ == '__main__':
    main()
