#!/usr/bin/env python3
"""Poker hand evaluator demo."""

from pokr.evaluator import evaluate_hand, parse_hand


def main():
    print("=== Poker Hand Evaluator Demo ===
")

    hands = [
        "As Ks Qs Js Ts",   # Royal flush
        "9h 8h 7h 6h 5h",  # Straight flush
        "As Ah Ad Ac Ks",   # Four of a kind
        "Ks Kh Kd 9s 9h",  # Full house
        "2h 5h 8h Jh Kh",  # Flush
        "5s 6h 7d 8c 9s",  # Straight
        "7s 7h 7d Ks 2c",  # Trips
        "Ks Kh 9s 9h 2c",  # Two pair
        "As Ah Kd Qc Js",  # Pair
        "As Kh Qd Jc 9s",  # High card
    ]

    for h in hands:
        cards = parse_hand(h)
        result = evaluate_hand(cards)
        print(f"  {h:30s} -> {result.rank.name}")


if __name__ == "__main__":
    main()
