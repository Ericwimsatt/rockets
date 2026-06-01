# Module-level functions replacing the Evaluator class. Instantiates lookupTable once, then uses it forever.
# Can be problematic if the memory cost of keeping lookupTable always in memory is too high but reduces footguns

import itertools
from typing import Sequence

from .card import Card
from .lookup import LookupTable

HAND_LENGTH = 2
BOARD_LENGTH = 5

lookupTable = LookupTable()


def evaluate(hand: list[int], board: list[int]) -> int:
    all_cards = hand + board
    return hand_size_map[len(all_cards)](all_cards)


def _five(cards: Sequence[int]) -> int:
    # if flush
    if cards[0] & cards[1] & cards[2] & cards[3] & cards[4] & 0xF000:
        handOR = (cards[0] | cards[1] | cards[2] | cards[3] | cards[4]) >> 16
        prime = Card.prime_product_from_rankbits(handOR)
        return lookupTable.flush_lookup[prime]

    # otherwise
    else:
        prime = Card.prime_product_from_hand(cards)
        return lookupTable.unsuited_lookup[prime]


def _six(cards: Sequence[int]) -> int:
    minimum = LookupTable.MAX_HIGH_CARD

    for combo in itertools.combinations(cards, 5):
        score = _five(combo)
        if score < minimum:
            minimum = score

    return minimum


def _seven(cards: Sequence[int]) -> int:
    minimum = LookupTable.MAX_HIGH_CARD

    for combo in itertools.combinations(cards, 5):
        score = _five(combo)
        if score < minimum:
            minimum = score

    return minimum


hand_size_map = {
    5: _five,
    6: _six,
    7: _seven
}


def get_rank_class(hr: int) -> int:
    if hr >= 0 and hr <= LookupTable.MAX_ROYAL_FLUSH:
        return LookupTable.MAX_TO_RANK_CLASS[LookupTable.MAX_ROYAL_FLUSH]
    elif hr <= LookupTable.MAX_STRAIGHT_FLUSH:
        return LookupTable.MAX_TO_RANK_CLASS[LookupTable.MAX_STRAIGHT_FLUSH]
    elif hr <= LookupTable.MAX_FOUR_OF_A_KIND:
        return LookupTable.MAX_TO_RANK_CLASS[LookupTable.MAX_FOUR_OF_A_KIND]
    elif hr <= LookupTable.MAX_FULL_HOUSE:
        return LookupTable.MAX_TO_RANK_CLASS[LookupTable.MAX_FULL_HOUSE]
    elif hr <= LookupTable.MAX_FLUSH:
        return LookupTable.MAX_TO_RANK_CLASS[LookupTable.MAX_FLUSH]
    elif hr <= LookupTable.MAX_STRAIGHT:
        return LookupTable.MAX_TO_RANK_CLASS[LookupTable.MAX_STRAIGHT]
    elif hr <= LookupTable.MAX_THREE_OF_A_KIND:
        return LookupTable.MAX_TO_RANK_CLASS[LookupTable.MAX_THREE_OF_A_KIND]
    elif hr <= LookupTable.MAX_TWO_PAIR:
        return LookupTable.MAX_TO_RANK_CLASS[LookupTable.MAX_TWO_PAIR]
    elif hr <= LookupTable.MAX_PAIR:
        return LookupTable.MAX_TO_RANK_CLASS[LookupTable.MAX_PAIR]
    elif hr <= LookupTable.MAX_HIGH_CARD:
        return LookupTable.MAX_TO_RANK_CLASS[LookupTable.MAX_HIGH_CARD]
    else:
        raise Exception("Inavlid hand rank, cannot return rank class")


def class_to_string(class_int: int) -> str:
    return LookupTable.RANK_CLASS_TO_STRING[class_int]


def get_five_card_rank_percentage(hand_rank: int) -> float:
    return float(hand_rank) / float(LookupTable.MAX_HIGH_CARD)


def hand_summary(board: list[int], hands: list[list[int]]) -> None:
    assert len(board) == BOARD_LENGTH, "Invalid board length"
    for hand in hands:
        assert len(hand) == HAND_LENGTH, "Invalid hand length"

    line_length = 10
    stages = ["FLOP", "TURN", "RIVER"]

    for i in range(len(stages)):
        line = "=" * line_length
        print("{} {} {}".format(line, stages[i], line))

        best_rank = 7463  # rank one worse than worst hand
        winners = []
        for player, hand in enumerate(hands):

            # evaluate current board position
            rank = evaluate(hand, board[:(i + 3)])
            rank_class = get_rank_class(rank)
            class_string = class_to_string(rank_class)
            percentage = 1.0 - get_five_card_rank_percentage(rank)  # higher better here
            print("Player {} hand = {}, percentage rank among all hands = {}".format(player + 1, class_string, percentage))

            # detect winner
            if rank == best_rank:
                winners.append(player)
                best_rank = rank
            elif rank < best_rank:
                winners = [player]
                best_rank = rank

        # if we're not on the river
        if i != stages.index("RIVER"):
            if len(winners) == 1:
                print("Player {} hand is currently winning.\n".format(winners[0] + 1))
            else:
                print("Players {} are tied for the lead.\n".format([x + 1 for x in winners]))

        # otherwise on all other streets
        else:
            hand_result = class_to_string(get_rank_class(evaluate(hands[winners[0]], board)))
            print()
            print("{} HAND OVER {}".format(line, line))
            if len(winners) == 1:
                print("Player {} is the winner with a {}\n".format(winners[0] + 1, hand_result))
            else:
                print("Players {} tied for the win with a {}\n".format([x + 1 for x in winners], hand_result))
