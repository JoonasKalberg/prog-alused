class Card:
    """A card in a poker game."""

    def __init__(self, value, suit):
        """Initialize Card."""
        self.value = value
        self.suit = suit

    def __repr__(self):
        """
        Return a string representation of the card.

        "{value} of {suit}"
        "2 of hearts" or "Q of spades"
        """
        return f"{self.value} of {self.suit}"


class Hand:
    """The hand in a poker game."""

    suits = ["diamonds", "clubs", "hearts", "spades"]
    values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

    def __init__(self):
        """Initialize Hand."""
        self.cards = []

    def can_add_card(self, card: Card) -> bool:
        """
        Check for card validity.

        Can only add card if:
        - A card with the same suit and value is not already being held.
        - The player is holding less than five cards.
        - The card has both a valid value and a valid suit.
        """
        return (
            card.value in self.values
            and card.suit in self.suits
            and len(self.cards) < 5
            and card not in self.cards
        )

    def add_card(self, card: Card):
        """
        Add a card to hand.

        Before adding a card, you would have to check if it can be added.
        """
        if self.can_add_card(card):
            self.cards.append(card)
        else:
            raise ValueError("Cannot add the card to the hand.")

    def can_remove_card(self, card: Card):
        """
        Check if a card can be removed from hand.

        The only consideration should be that the card is already being held.
        """
        return card in self.cards

    def remove_card(self, card: Card):
        """
        Remove a card from hand.

        Before removing the card, you would have to check if it can be removed.
        """
        if self.can_remove_card(card):
            self.cards.remove(card)
        else:
            raise ValueError("Cannot remove the card from the hand.")

    def get_cards(self):
        """Return a list of cards as objects."""
        return self.cards

    def is_straight(self):
        """
        Determine if the hand is a straight.

        A straight hand will have all cards in the order of value.
        Sorting will help you here as the order will vary.

        Examples:
        4 5 6 7 8
        K J 10 Q A

        For the sake of simplicity - A 2 3 4 5 will not be tested.
        You can always consider A to be the highest-ranked card.
        """
        sorted_values = sorted([self.values.index(card.value) for card in self.cards])
        return sorted_values[-1] - sorted_values[0] == 4 and len(set(sorted_values)) == 5

    def is_flush(self):
        """
        Determine if the hand is a flush.

        In a flush hand, all cards are of the same suit. Their numeric value is not important here.
        """
        return len(set(card.suit for card in self.cards)) == 1

    def is_straight_flush(self):
        """
        Determine if the hand is a straight flush.

        Such a hand is both a straight and a flush at the same time.
        """
        return self.is_straight() and self.is_flush()

    def is_full_house(self):
        """
        Determine if the hand is a full house.

        A full house will have three cards of one value and two cards of a second value.
        """
        values_count = [self.values.count(card.value) for card in self.cards]
        return sorted(values_count) == [2, 3]

    def is_four_of_a_kind(self):
        """
        Determine if there are four cards of the same value in hand.
        """
        values_count = [self.values.count(card.value) for card in self.cards]
        return 4 in values_count

    def is_three_of_a_kind(self):
        """
        Determine if there are three cards of the same value in hand.
        """
        values_count = [self.values.count(card.value) for card in self.cards]
        return 3 in values_count

    def is_pair(self):
        """
        Determine if there are two cards of the same value in hand.
        """
        values_count = [self.values.count(card.value) for card in self.cards]
        return 2 in values_count

    def get_hand_type(self):
        """
        Return a string representation of the hand.

        Return None (or nothing), if there are fewer than five cards in hand.
        """
        if len(self.cards) < 5:
            return None

        if self.is_straight_flush():
            return "straight flush"
        elif self.is_flush():
            return "flush"
        elif self.is_straight():
            return "straight"
        elif self.is_full_house():
            return "full house"
        elif self.is_four_of_a_kind():
            return "four of a kind"
        elif self.is_three_of_a_kind():
            return "three of a kind"
        elif self.is_pair():
            return "pair"
        else:
            return "high card"

    def __repr__(self):
        """
        Return a string representation of the hand.

        I got a {type} with cards: {card list}
        I got a straight with cards: 2 of diamonds, 4 of spades, 5 of clubs, 3 of diamonds, 6 of hearts

        If a hand type cannot be yet determined, return a list of cards as so:

        I'm holding {cards}
        I'm holding 2 of diamonds, 4 of spades.

        Order of the cards is not important.
        """
        if self.get_hand_type() is not None:
            return f"I got a {self.get_hand_type()} with cards: {', '.join(map(str, self.cards))}"
        else:
            return f"I'm holding {', '.join(map(str, self.cards))}"


if __name__ == "__main__":
    hand = Hand()
    cards = [Card("2", "diamonds"), Card("4", "spades"), Card("5", "clubs"), Card("3", "diamonds"), Card("6", "hearts")]
    [hand.add_card(card) for card in cards]
    assert hand.get_hand_type() == "straight"

    hand = Hand()
    cards = [Card("10", "diamonds"), Card("2", "diamonds"), Card("A", "diamonds"), Card("6", "diamonds"),
             Card("9", "diamonds")]
    [hand.add_card(card) for card in cards]
    assert hand.get_hand_type() == "flush"

    hand = Hand()
    cards = [Card("A", "hearts"), Card("A", "clubs"), Card("A", "spades"), Card("A", "diamonds"),
             Card("9", "diamonds")]
    [hand.add_card(card)]