"""Tests for poker hand evaluator."""

import pytest
from pokr.evaluator import evaluate_hand, parse_hand, HandRank


class TestPoker:
    def test_royal_flush(self):
        hand = parse_hand("As Ks Qs Js Ts")
        result = evaluate_hand(hand)
        assert result.rank == HandRank.ROYAL_FLUSH

    def test_straight_flush(self):
        hand = parse_hand("9h 8h 7h 6h 5h")
        result = evaluate_hand(hand)
        assert result.rank == HandRank.STRAIGHT_FLUSH

    def test_four_of_a_kind(self):
        hand = parse_hand("As Ah Ad Ac Ks")
        result = evaluate_hand(hand)
        assert result.rank == HandRank.FOUR_OF_A_KIND

    def test_full_house(self):
        hand = parse_hand("Ks Kh Kd 9s 9h")
        result = evaluate_hand(hand)
        assert result.rank == HandRank.FULL_HOUSE

    def test_flush(self):
        hand = parse_hand("2h 5h 8h Jh Kh")
        result = evaluate_hand(hand)
        assert result.rank == HandRank.FLUSH

    def test_straight(self):
        hand = parse_hand("5s 6h 7d 8c 9s")
        result = evaluate_hand(hand)
        assert result.rank == HandRank.STRAIGHT

    def test_wheel_straight(self):
        hand = parse_hand("As 2h 3d 4c 5s")
        result = evaluate_hand(hand)
        assert result.rank == HandRank.STRAIGHT

    def test_three_of_a_kind(self):
        hand = parse_hand("7s 7h 7d Ks 2c")
        result = evaluate_hand(hand)
        assert result.rank == HandRank.THREE_OF_A_KIND

    def test_two_pair(self):
        hand = parse_hand("Ks Kh 9s 9h 2c")
        result = evaluate_hand(hand)
        assert result.rank == HandRank.TWO_PAIR

    def test_one_pair(self):
        hand = parse_hand("As Ah Kd Qc Js")
        result = evaluate_hand(hand)
        assert result.rank == HandRank.ONE_PAIR

    def test_high_card(self):
        hand = parse_hand("As Kh Qd Jc 9s")
        result = evaluate_hand(hand)
        assert result.rank == HandRank.HIGH_CARD

    def test_seven_cards(self):
        hand = parse_hand("As Ah Ad Ks Kh 2c 3d")
        result = evaluate_hand(hand)
        assert result.rank == HandRank.FULL_HOUSE

    def test_comparison(self):
        r1 = evaluate_hand(parse_hand("As Ah Ad Ks Qs"))
        r2 = evaluate_hand(parse_hand("Ks Kh Kd As Qs"))
        assert r1 > r2 or (r1.rank.value, r1.kickers) > (r2.rank.value, r2.kickers)
