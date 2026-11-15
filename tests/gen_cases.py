import json, random, sys
from fractions import Fraction as F
def hu(x):  # half-up to integer, x >= 0
    return int((x*2 + 1) // 2)
def tier_segs(days, r1, r2, r3):
    if days <= 90: return [(days, r1)]
    if days <= 180: return [(90, r1), (days-90, r2)]
    if days <= 365: return [(days, r2)]
    return [(days, r3)]
EDGE = [0, 1, 89, 90, 91, 179, 180, 181, 364, 365, 366, 400]
random.seed(7); cases=[]
for i in range(80000):
    P = random.choice([str(random.randint(1,999999)), f"{random.randint(1,99999)}.{random.randint(0,99):02d}"])
    rate = random.choice(["1","1.25","1.5","1.75","2","1.1","0.9","18","12.5","24","1.333"])
    basis = random.choice(["monthly","annual"]); method = random.choice(["daily","m30"])
    tiered = i >= 60000
    days = random.choice(EDGE) if tiered and random.random() < 0.3 else random.randint(0, 1500)
    dtype = random.choice(["amount","percent","final", None])
    Pp = F(P)*100; R = F(rate)
    tiers = None
    if tiered:
        tiers = dict(r1=random.choice(["1","0.75","1.25"]), r2=random.choice(["1.5","1.75","2"]), r3=random.choice(["2","2.5","3"]))
        interest = sum(hu(Pp*F(r)*d/3000) for d, r in tier_segs(days, F(tiers["r1"]), F(tiers["r2"]), F(tiers["r3"])))
    else:
        yearly = R if basis=="annual" else R*12; monthly = R if basis=="monthly" else R/12
        interest = hu(Pp*yearly*days/36500) if method=="daily" else hu(Pp*monthly*days/3000)
    sub = int(Pp) + interest
    disc = None; after = sub
    if dtype=="amount": disc = str(random.randint(0, 5000)); after = sub - min(sub, int(F(disc)*100))
    elif dtype=="percent": disc = random.choice(["5","2.5","10","0.75","33.33"]); after = sub - hu(sub*F(disc)/100)
    elif dtype=="final": disc = f"{max(0, sub//100 - random.randint(0,500))}"; after = int(F(disc)*100)
    roundOn = random.random()<0.6 and dtype!="final"
    total = hu(F(after,100))*100 if roundOn and after>=0 else after
    cases.append(dict(principal=P, rate=float(rate) if rate!="1.333" else 1.333, basis=basis, method=method, days=days, dtype=dtype or "amount", discount=disc, roundOn=roundOn, tiers=tiers, exp=[interest, sub, after, total]))
json.dump(cases, open(sys.argv[1],"w"))
print(len(cases), "cases")
