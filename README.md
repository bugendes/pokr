# Poker Hand Evaluator

A Texas Hold'em poker hand evaluator that determines the best 5-card hand from 5-7 cards, using combinatorial enumeration with rank-count pattern matching.

## How It Works

Given 5-7 cards, the evaluator tries all C(n,5) combinations and scores each 5-card hand:

1. **Flush check:** All 5 cards share the same suit?
2. **Straight check:** 5 consecutive ranks? (Includes the A-2-3-4-5 "wheel.")
3. **Count pattern:** Tally ranks by frequency. The pattern determines:
   - (4,1) → Four of a Kind
   - (3,2) → Full House
   - (3,1,1) → Three of a Kind
   - (2,2,1) → Two Pair
   - (2,1,1,1) → One Pair
   - (1,1,1,1,1) → High Card

4. **Comparison:** Hands are compared by (hand_rank, kickers) tuple. Kickers break ties within the same rank.

**Royal Flush** is just an Ace-high Straight Flush — handled as a special case for clarity.

## Complexity

| Operation | Time | Notes |
|-----------|------|-------|
| 5-card eval | O(1) | Fixed work |
| Best of 7 | O(C(7,5)) = O(21) | Enumerate all combos |

## Applications

**Poker Bots:** Real-time hand evaluation during play. Must be fast — bots evaluate thousands of hands per second for Monte Carlo simulation.

**Equity Calculators:** Tools like PokerStove, Equilab enumerate all possible boards to compute win probability.

**Hand History Analysis:** PokerTracker, Hold'em Manager replay hands and evaluate each street.

**Game Theory:** Computing Nash equilibrium strategies requires evaluating hands across ranges.
