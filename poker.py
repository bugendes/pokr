import random
from collections import Counter
from itertools import combinations
RV={r:i for i,r in enumerate(["2","3","4","5","6","7","8","9","10","J","Q","K","A"])}
def hr(h):
    r=sorted([RV[c[0]] for c in h],reverse=True); s=[c[1] for c in h]
    ct=Counter(r); f=sorted(ct.values(),reverse=True)
    fl=len(set(s))==1; st=max(r)-min(r)==4 and len(set(r))==5
    if fl and st: return (8,r)
    if f==[4,1]: return (7,r)
    if f==[3,2]: return (6,r)
    if fl: return (5,r)
    if st: return (4,r)
    if f==[3,1,1]: return (3,r)
    if f==[2,2,1]: return (2,r)
    if f==[2,1,1,1]: return (1,r)
    return (0,r)
N={0:"High Card",1:"Pair",2:"Two Pair",3:"Trips",4:"Straight",5:"Flush",6:"Full House",7:"Quads",8:"SF"}
def main():
    random.seed(42); print("POKER + MONTE CARLO")
    h=[("A","spades"),("K","spades"),("Q","spades"),("J","spades"),("10","spades")]
    print(f"  Royal flush: {N[hr(h)[0]]}")
    dk=[(r,s) for s in ["h","d","c","sp"] for r in RV]
    wins=0; hole=[("A","spades"),("K","spades")]
    for _ in range(5000):
        random.shuffle(dk); b=dk[:5]; o=dk[5:7]
        m=max(combinations(list(hole)+b,5),key=hr); t=max(combinations(list(o)+b,5),key=hr)
        if hr(m)>hr(t): wins+=1
    print(f"  AKs win: {wins/5000*100:.1f}%")
if __name__=="__main__": main()
