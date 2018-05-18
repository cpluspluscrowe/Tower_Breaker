import fileinput
import sys
from collections import defaultdict
from copy import deepcopy
from functools import reduce

sys.setrecursionlimit(15000000)


def get_input():
    for file_line in fileinput.input("./input.txt"):
        yield file_line


class Static:
    input_generator = get_input()
    dynamic_store = {}
    factors_store = {}

    @staticmethod
    def get_next_line():
        return next(Static.input_generator)

    @staticmethod
    def hash_game(game_to_hash):  # Only for flat dictionaries
        return hash(frozenset(game_to_hash.towers.items()))


def get_factors_gt_one(n):
    if n in Static.factors_store:
        return Static.factors_store[n]
    factors = set([x for x in reduce(list.__add__,
                                     ([i, n // i] for i in range(1, int(pow(n, 0.5) + 1)) if n % i == 0)) if x > 1])
    Static.factors_store[n] = factors
    return factors


class Game:
    def __init__(self, towers):
        self.towers = defaultdict(lambda: 0)
        for tower in towers:
            if tower > 1:
                self.towers[tower] += 1

    def is_game_over(self):
        """
        >>> game = Game([1,1])
        >>> game.is_game_over()
        True
        >>> game = Game([2])
        >>> game.is_game_over()
        False
        """
        for value in self.towers.values():
            if value > 0:
                return False
        return True

    def to_list(self):
        """
        >>> game = Game([1,2])
        >>> game.to_list()
        [2]
        >>> game = Game([2,4,8])
        >>> game.to_list()
        [2, 4, 8]
        """
        towers = []
        for key in self.towers:
            for iteration in range(self.towers[key]):
                towers.append(key)
        return towers

    def undo_breakdown(self, old_tower_size, breakdown_factor):
        """
        >>> game = Game([1,1,1,1])
        >>> game.undo_breakdown(4, 4)
        >>> game.towers[4]
        1
        """
        number_of_new_towers = breakdown_factor
        size_of_new_towers = int(old_tower_size / breakdown_factor)
        self.towers[old_tower_size] += 1
        if size_of_new_towers > 1:
            for new_tower_count in range(number_of_new_towers):
                self.towers[size_of_new_towers] -= 1
        if self.towers[size_of_new_towers] == 0:
            del self.towers[size_of_new_towers]

    def breakdown(self, old_tower_size, breakdown_factor):
        """
        >>> game = Game([1,2])
        >>> game.towers[2]
        1
        >>> game.breakdown(2,2)
        >>> game.towers[2]
        0
        >>> game = Game([1,4,2])
        >>> game.breakdown(4,2)
        >>> game.towers[2]
        3
        >>> game = Game([1,4,2])
        >>> game.towers[4]
        1
        >>> game.breakdown(4,4)
        >>> game.towers[1]
        0
        >>> game.towers[2]
        1
        >>> game.towers[4]
        0
        """
        if breakdown_factor == 1:
            raise Exception("Invalid number for breakdown")
        number_of_new_towers = breakdown_factor
        assert old_tower_size % breakdown_factor == 0
        size_of_new_towers = int(old_tower_size / breakdown_factor)
        self.towers[old_tower_size] -= 1
        if self.towers[old_tower_size] == 0:
            del self.towers[old_tower_size]
        if size_of_new_towers > 1:
            for new_tower_count in range(number_of_new_towers):
                self.towers[size_of_new_towers] += 1


def can_force_win(current_game):
    """
    >>> game = Game([1,1])
    >>> can_force_win(game)
    False
    >>> game = Game([1,2])
    >>> can_force_win(game)
    True
    >>> game = Game([1,2,3])
    >>> can_force_win(game)
    False
    """
    if current_game.is_game_over():
        return False
    game_hash = Static.hash_game(current_game)
    if game_hash in Static.dynamic_store:
        return Static.dynamic_store
    for tower in list(current_game.towers):  # tower is tower_size
        if current_game.towers[tower] > 0:
            for factor in get_factors_gt_one(tower):
                current_game.breakdown(tower, factor)
                if not can_force_win(current_game):
                    return True
                else:
                    current_game.undo_breakdown(tower, factor)

    return False


number_of_games = int(Static.get_next_line())
for number in range(number_of_games):
    Static.get_next_line()  # number_of_towers
    tower_heights = [int(tower) for tower in Static.get_next_line().split()]
    game = Game(tower_heights)
    can_player_one_force_win = can_force_win(deepcopy(game))
    if can_player_one_force_win:
        print(1)
    else:
        print(2)

if __name__ == "__main__":
    print("Done!")
