from treys.card import Card
from treys import evaluation
from treys.deck import Deck


# create a card
card = Card.new('Qh')

# create a board and hole cards
board = [
    Card.new('2h'),
    Card.new('2s'),
    Card.new('Jc'),
    Card.new('As'),
    Card.new('Kc')
]
hand = [
    Card.new('Qs'),
    Card.new('Th')
]

# pretty print cards to console
Card.print_pretty_cards(board)
Card.print_pretty_cards(hand)

# and rank your hand
rank = evaluation.evaluate(hand, board)
class_ = evaluation.get_rank_class(rank)
print("{} {}".format(rank, evaluation.class_to_string(class_)))
print()

# or for random cards or games, create a deck
print("Dealing a new hand...")
deck = Deck()
board = deck.draw(5)
player1_hand = deck.draw(2)
player2_hand = deck.draw(2)

print("The board:")
Card.print_pretty_cards(board)

print("Player 1's cards:")
Card.print_pretty_cards(player1_hand)

print("Player 2's cards:")
Card.print_pretty_cards(player2_hand)

p1_score = evaluation.evaluate(player1_hand, board)
p2_score = evaluation.evaluate(player2_hand, board)

# bin the scores into classes
p1_class = evaluation.get_rank_class(p1_score)
p2_class = evaluation.get_rank_class(p2_score)

# or get a human-friendly string to describe the score
print("Player 1 hand rank = {} {}".format(p1_score, evaluation.class_to_string(p1_class)))
print("Player 2 hand rank = {} {}".format(p2_score, evaluation.class_to_string(p2_class)))

# or just a summary of the entire hand
hands = [player1_hand, player2_hand]
evaluation.hand_summary(board, hands)
