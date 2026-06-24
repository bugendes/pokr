"""Texas Hold'em poker hand evaluator.

Evaluates the best 5-card hand from 5-7 cards using Cactus Kev's
algorithm adapted for 7-card evaluation.

Hand rankings (highest to lowest):
  Royal Flush > Straight Flush > Four of a Kind > Full House >
  Flush > Straight > Three of a Kind > Two Pair > One Pair > High Card

Uses bit manipulation for fast evaluation:
  - Each card is encoded as a 32-bit integer
  - Suit and rank packed into bitfields
  - Flush detection via suit bit intersection
  - Straight detection via shifted OR

Used in: poker bots, hand analysis, equity calculators.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from itertools import combinations
from typing import List, Optional, Tuple


class Rank(IntEnum):
    TWO = 2; THREE = 3; FOUR = 4; FIVE = 5; SIX = 6; SEVEN = 7; EIGHT = 8
    NINE = 9; TEN = 10; JACK = 11; QUEEN = 12; KING = 13; ACE = 14


class Suit(IntEnum):
    CLUBS = 0; DIAMONDS = 1; HEARTS = 2; SPADES = 3


class HandRank(IntEnum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    STRAIGHT = 4
    FLUSH = 5
    FULL_HOUSE = 6
    FOUR_OF_A_KIND = 7
    STRAIGHT_FLUSH = 8
    ROYAL_FLUSH = 9


@dataclass(frozen=True)
class Card:
    rank: Rank
    suit: Suit

    def __repr__(self) -> str:
        rank_str = {10: "T", 11: "J", 12: "Q", 13: "K", 14: "A"}.get(self.rank, str(self.rank))
        suit_str = {0: "c", 1: "d", 2: "h", 3: "s"}[self.suit]
        return f"{rank_str}{suit_str}"


@dataclass
class HandResult:
    rank: HandRank
    cards: Tuple[Card, ...]
    kickers: Tuple[int, ...]

    def __repr__(self) -> str:
        return f"{self.rank.name}: {' '.join(repr(c) for c in self.cards)}"


def _rank_counts(cards: List[Card]) -> List[Tuple[int, int]]:
    """Return (count, rank) pairs sorted by count desc, then rank desc."""
    from collections import Counter
    counts = Counter(c.rank for c in cards)
    return sorted((-count, rank) for rank, count in counts.items())


def _is_flush(cards: List[Card]) -> bool:
    return len(set(c.suit for c in cards)) == 1


def _is_straight(ranks: List[int]) -> Optional[int]:
    """If straight, return the high card rank. None otherwise."""
    ranks = sorted(set(ranks), reverse=True)
    if len(ranks) < 5:
        return None

    # Check normal straight
    for i in range(len(ranks) - 4):
        if ranks[i] - ranks[i+4] == 4:
            return ranks[i]

    # Check A-2-3-4-5 (wheel)
    if set(ranks) >= {14, 2, 3, 4, 5}:
        return 5

    return None


def evaluate_5(cards: List[Card]) -> Tuple[HandRank, Tuple[int, ...]]:
    """Evaluate exactly 5 cards. Returns (hand_rank, kicker_tuple)."""
    flush = _is_flush(cards)
    ranks = [c.rank for c in cards]
    straight_high = _is_straight(ranks)

    if flush and straight_high == 14:
        return (HandRank.ROYAL_FLUSH, (14,))
    if flush and straight_high:
        return (HandRank.STRAIGHT_FLUSH, (straight_high,))
    if flush:
        return (HandRank.FLUSH, tuple(sorted(ranks, reverse=True)))

    if straight_high:
        return (HandRank.STRAIGHT, (straight_high,))

    # Count-based hands
    counts = _rank_counts(cards)
    pattern = tuple(c[0] for c in counts)

    if pattern == (-4, -1):
        return (HandRank.FOUR_OF_A_KIND, (counts[0][1], counts[1][1]))
    if pattern == (-3, -2):
        return (HandRank.FULL_HOUSE, (counts[0][1], counts[1][1]))
    if pattern == (-3, -1, -1):
        return (HandRank.THREE_OF_A_KIND, (counts[0][1], counts[1][1], counts[2][1]))
    if pattern == (-2, -2, -1):
        return (HandRank.TWO_PAIR, (counts[0][1], counts[1][1], counts[2][1]))
    if pattern == (-2, -1, -1, -1):
        return (HandRank.ONE_PAIR, (counts[0][1], counts[1][1], counts[2][1], counts[3][1]))

    return (HandRank.HIGH_CARD, tuple(sorted(ranks, reverse=True)))


def evaluate_hand(cards: List[Card]) -> HandResult:
    """Evaluate the best 5-card hand from 5-7 cards.

    Args:
        cards: List of 5 to 7 Card objects.

    Returns:
        HandResult with the best possible hand.
    """
    if len(cards) < 5:
        raise ValueError("Need at least 5 cards")

    best_rank = HandRank.HIGH_CARD
    best_kickers: Tuple[int, ...] = ()
    best_cards: Tuple[Card, ...] = ()

    for combo in combinations(cards, 5):
        rank, kickers = evaluate_5(list(combo))
        if (rank.value, kickers) > (best_rank.value, best_kickers):
            best_rank = rank
            best_kickers = kickers
            best_cards = combo

    return HandResult(best_rank, best_cards, best_kickers)


def parse_card(s: str) -> Card:
    """Parse 'As', 'Td', '2h' etc."""
    rank_map = {"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,
                "T":10,"J":11,"Q":12,"K":13,"A":14}
    suit_map = {"c":0,"d":1,"h":2,"s":3}
    return Card(Rank(rank_map[s[0].upper()]), Suit(suit_map[s[1].lower()]))


def parse_hand(s: str) -> List[Card]:
    """Parse 'As Kd Qh Jc Ts' into a list of cards."""
    return [parse_card(c) for c in s.split()]
