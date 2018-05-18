import fileinput
from collections import defaultdict
from copy import deepcopy
from functools import reduce


def get_input():
    for file_line in fileinput.input("./input.txt"):
        yield file_line


class Static:
    input_generator = get_input()

    @staticmethod
    def get_next_line():
        return next(Static.input_generator)


def get_factors_gt_one(n):
    return set([x for x in reduce(list.__add__,
                                  ([i, n // i] for i in range(1, int(pow(n, 0.5) + 1)) if n % i == 0)) if x > 1])


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
    for tower in current_game.towers:  # tower is tower_size
        if current_game.towers[tower] > 0:
            for factor in get_factors_gt_one(tower):
                game_after_move = deepcopy(current_game)
                game_after_move.breakdown(tower, factor)
                if not can_force_win(game_after_move):
                    return True
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
    pass
