"""
Problem 21 of the Advent-of-Code 2021
"""

from collections import defaultdict
from typing import Counter, Dict, List, Optional, Tuple
import dataclasses
import itertools


@dataclasses.dataclass
class Space:
    value: int
    next: Optional["Space"] = None
    previous: Optional["Space"] = None


@dataclasses.dataclass
class Track:
    spaces: List[Space]

    def get_space_with_value(self, value: int) -> Optional[Space]:
        for space in self.spaces:
            if space.value == value:
                return space
        return None


@dataclasses.dataclass
class Pawn:
    current_space: Space

    def move(self, number_of_spaces: int) -> None:
        for _ in range(number_of_spaces):
            if self.current_space.next is None:
                raise Exception
            self.current_space = self.current_space.next

    def land(self) -> int:
        return self.current_space.value


@dataclasses.dataclass
class DeterministicDice:
    total_rolls: int = 0
    det_counter: int = 1

    def get_roll(self) -> int:
        ret_val = self.det_counter
        self.det_counter += 1
        if self.det_counter > 100:
            self.det_counter = 1
        self.total_rolls += 1
        return ret_val


@dataclasses.dataclass
class Player:
    pawn: Pawn
    score: int = 0

    def has_won(self):
        return self.score >= 1000

    def move(self, number_of_spaces: int) -> None:
        self.pawn.move(number_of_spaces)
        self.score += self.pawn.land()


@dataclasses.dataclass
class Players:
    players: List[Player]
    players_turn: int = 0

    def get_losing_player(self) -> Optional[Player]:
        for player in self.players:
            if not player.has_won():
                return player
        return None

    def is_game_over(self) -> bool:
        return any(player.has_won() for player in self.players)

    def next_turn(self) -> None:
        self.players_turn = (self.players_turn + 1) % len(self.players)

    def get_current_player(self) -> Player:
        return self.players[self.players_turn]


def read_inputs(filename: str) -> List[int]:
    initial_positions = []
    with open(filename, "r") as fp:
        for line in fp:
            initial_positions.append(int(line.strip().split(":")[1].strip()))

    return initial_positions


def part_a(player_1_start: int, player_2_start: int) -> int:
    """
    I created a bunch of objects in a very object oriented and almost
    'game-esque' way to do all my logic in an effort to anticipate any changes
    for part B. Turns out that it didn't help at all anyway...
    """
    # Generate 10 spaces in a ring as our track.
    spaces = [Space(i + 1) for i in range(10)]
    for i in range(10):
        spaces[i].next = spaces[(i + 1) % 10]
        spaces[i].previous = spaces[(i - 1) % 10]

    track = Track(spaces=spaces)

    # Generate pawns
    player_1_pawn = Pawn(current_space=track.get_space_with_value(player_1_start))
    player_2_pawn = Pawn(current_space=track.get_space_with_value(player_2_start))

    # Generate players
    player_1 = Player(pawn=player_1_pawn)
    player_2 = Player(pawn=player_2_pawn)
    players = Players(players=[player_1, player_2])

    # Generate dice
    dice = DeterministicDice()

    # Play the game
    while not players.is_game_over():
        player = players.get_current_player()
        total_rolls = dice.get_roll() + dice.get_roll() + dice.get_roll()
        player.move(total_rolls)
        players.next_turn()

    # Calculate the score
    return players.get_losing_player().score * dice.total_rolls


def part_b(player_1_start: int, player_2_start: int) -> int:
    """
    In order to be efficient because the numbers get so huge, lets keep track
    of the number of universes in different 'states', where a 'state' is a
    combination of (current_location, current_score). After all, there can only
    be 10 * 20 different states that are currently playing.

    We can fairly easily create mappings from states to other states when a
    turn is executed. Eg (1, 4) -> (2, 6) + (3, 7) + (4, 8).

    We can continue taking turns and keep track of how many turns it take for
    each universe to complete. These are aggregated nicely as in, 'there were
    12345 universes that took 6 turn to finish'. We don't need to calculate it
    12345 times individually. These are stored in dicts of {n_turns_to_finish:
    number_of_universes}

    Lastly, we get these dicts for the two starting positions. Since each dice
    roll is the same, then for each single universe for player 1, they could
    have versed every single universe for player 2. Therefore we do a little
    fancy multiplication to figure out all the outcomes of games at the end.
    """
    state_mappings = get_state_mappings()

    num_universes_in_each_state = {}
    games_won_by_player = {initial_position: 0 for initial_position in (0, 1)}

    num_universes_in_each_state[((player_1_start, 0), (player_2_start, 0))] = 1
    player_turn = 0
    while num_universes_in_each_state:
        num_universes_in_each_state = take_turn(num_universes_in_each_state, state_mappings, player_turn)
        finished_games = (state for state in num_universes_in_each_state if state[player_turn] is None)
        universes_to_remove = set()
        for finished_game in finished_games:
            games_won_by_player[player_turn] += num_universes_in_each_state[finished_game]
            universes_to_remove.add(finished_game)
        for universe_to_remove in universes_to_remove:
            num_universes_in_each_state.pop(universe_to_remove)
        player_turn = (player_turn + 1) % 2

    return max(games_won_by_player.values())


State = Tuple[Tuple[int, int], Tuple[int, int]]


def get_state_mappings() -> Dict[State, Dict[Optional[State], int]]:
    spaces_moved_after_3_rolls = Counter(sum(i) for i in itertools.product([1, 2, 3], [1, 2, 3], [1, 2, 3]))

    state_mappings = defaultdict(dict)
    for location in range(10):
        for points in range(21):
            # Current state
            state = (location + 1, points)

            # Calculate all next states
            for spaces_moved, num_states in spaces_moved_after_3_rolls.items():
                new_location = (location + spaces_moved) % 10 + 1
                next_state = (new_location, points + new_location)
                if next_state[1] >= 21:  # If state is complete, it is None
                    next_state = None
                state_mappings[state][next_state] = state_mappings[state].get(next_state, 0) + num_states
    return state_mappings


def take_turn(
    num_universes_in_each_state: Dict[State, int], state_mappings: Dict[State, Dict[State, int]], player_turn: int
) -> Dict[Optional[State], int]:
    """
    Returns the number of universes in each state after taking a turn. Requires
    the number of universes in each state before taking that turn.
    """
    new_universes = {}

    for initial_state, num_universes_in_initial_state in num_universes_in_each_state.items():
        player_state = initial_state[player_turn]
        non_player_state = initial_state[(player_turn + 1) % 2]
        for new_player_state in state_mappings[player_state]:
            if player_turn == 0:
                new_state = (new_player_state, non_player_state)
            else:
                new_state = (non_player_state, new_player_state)

            new_universes[new_state] = new_universes.get(new_state, 0) + (
                num_universes_in_initial_state * state_mappings[initial_state[player_turn]][new_player_state]
            )

    return new_universes


if __name__ == "__main__":
    player_1_start, player_2_start = read_inputs("input.txt")

    print(f"Part A: {part_a(player_1_start, player_2_start)}")
    print(f"Part B: {part_b(player_1_start, player_2_start)}")
