"""
Solutions for the Advent of Code - Day 22
"""


def get_decks(file_name: str):
    """ Return two lists representing each deck """
    deck_1 = []
    deck_2 = []

    with open(file_name, 'r') as fb:
        destination = deck_1
        for line in fb:
            if line[-1] == '\n':
                line = line[:-1]
            if line == '':
                destination = deck_2
                continue
            destination.append(line)

    return ([int(x) for x in deck_1[1:]], [int(x) for x in deck_2[1:]])


def is_game_done(deck_1: list, deck_2: list) -> int:
    """
    Return 0 if the game is not done, 1 if player 1 wins, and 2 if player
    2 wins.
    """
    if len(deck_1) == 0:
        return 2
    if len(deck_2) == 0:
        return 1
    return 0


def carry_out_normal_round(deck_1: list, deck_2: list) -> None:
    """ Carry out a round of easy non-recursive combat """
    player_1_plays = deck_1[0]
    player_2_plays = deck_2[0]
    deck_1 = deck_1[1:]
    deck_2 = deck_2[1:]

    if player_1_plays > player_2_plays:
        deck_1 = deck_1 + [player_1_plays, player_2_plays]
    else:
        deck_2 = deck_2 + [player_2_plays, player_1_plays]

    return (deck_1, deck_2)


def carry_out_normal_game(deck_1: list, deck_2: list) -> None:
    """ Carry out a game of non-recursive combat to completion """
    while not is_game_done(deck_1, deck_2):
        deck_1, deck_2 = carry_out_normal_round(deck_1, deck_2)
    return (deck_1, deck_2)


def part_a(deck_1: list, deck_2: list) -> int:
    """
    Play out a normal game of combat and calculate the value of the winning deck
    """
    deck_1, deck_2 = carry_out_normal_game(deck_1, deck_2)
    deck = deck_1 if len(deck_1) != 0 else deck_2
    return sum([value * (multiplier + 1) for multiplier, value in enumerate(reversed(deck))])


def carry_out_recursive_game(deck_1: list, deck_2: list) -> tuple:
    """
    Carry out a game of recursive combat to completion. Returns the tinner of
    the game. 0 = player 1, 1 = player 2.
    """
    deck_1 = deck_1.copy()
    deck_2 = deck_2.copy()

    history = []

    while True:
        done = is_game_done(deck_1, deck_2)
        if done:
            return (deck_1, deck_2, done)

        # Check if this state has been achieved before.
        if [deck_1, deck_2] in history:
            return (deck_1, deck_2, 1)
        history.append([deck_1, deck_2])

        # Carry out a recursive round
        player_1_plays = deck_1[0]
        player_2_plays = deck_2[0]
        deck_1 = deck_1[1:]
        deck_2 = deck_2[1:]

        # If players play cards with numbers less than the sizes of their deck,
        # enter the subgame
        if (player_1_plays <= len(deck_1)) and (player_2_plays <= len(deck_2)):
            _, _, winner = carry_out_recursive_game(deck_1[:player_1_plays], deck_2[:player_2_plays])
        else:
            # Otherwise it's a normal game
            winner = 1 if player_1_plays > player_2_plays else 2

        # Add cards to the bottom of the winners deck
        if winner == 1:
            deck_1 += [player_1_plays, player_2_plays]
        else:
            deck_2 += [player_2_plays, player_1_plays]


def part_b(deck_1: list, deck_2: list) -> int:
    """
    Play out a game of recursive combat and calculate the value of the winning
    deck.
    """
    deck_1, deck_2, winner = carry_out_recursive_game(deck_1, deck_2)
    deck = deck_1 if winner == 1 else deck_2
    return sum([value * (multiplier + 1) for multiplier, value in enumerate(reversed(deck))])


if __name__ == "__main__":
    deck_1, deck_2 = get_decks('input.txt')
    print("Part A: " + str(part_a(deck_1, deck_2)))
    deck_1, deck_2 = get_decks('input.txt')
    print("Part B: " + str(part_b(deck_1, deck_2)))
