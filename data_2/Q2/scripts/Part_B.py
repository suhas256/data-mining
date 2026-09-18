import csv, glob, re, math

notices = {}

for file in glob.glob("notices\\part-*.csv"):
    with open(file, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            notices[r["notice_id"]] = r

def norm(s):
    return re.sub(r"\s+", " ", s.lower()).strip()

def shingles(s):
    s = norm(s)
    return {s[i:i+5] for i in range(len(s)-4)}

def exact(a,b):
    A,B=shingles(a),shingles(b)
    return len(A&B)/len(A|B) if A|B else 1.0

# 128-hash MinHash
def signature(s):
    S=shingles(s)
    sig=[]
    for seed in range(128):
        m=2**64-1
        for x in S:
            h=hash((seed,x)) & ((1<<64)-1)
            if h<m: m=h
        sig.append(m)
    return sig

with open("labelled_pairs.csv", encoding="utf-8-sig", newline="") as f:
    pairs=list(csv.DictReader(f))

errors=[]

for p in pairs:
    a=notices[p["notice_id_a"]]
    b=notices[p["notice_id_b"]]

    ta=a["title"]+" "+a["body"]
    tb=b["title"]+" "+b["body"]

    e=exact(ta,tb)
    sa=signature(ta)
    sb=signature(tb)
    estimate=sum(x==y for x,y in zip(sa,sb))/128

    errors.append(abs(e-estimate))

print("========== PART B ==========")
print("Labelled pairs:",len(pairs))
print("MinHash size: 128")
print("Accuracy target: 95% of pairs within absolute error 0.10")
print("Mean absolute error:",round(sum(errors)/len(errors),4))
print("Maximum absolute error:",round(max(errors),4))
print("Within 0.05:",round(sum(e<=0.05 for e in errors)/len(errors)*100,2),"%")
print("Within 0.10:",round(sum(e<=0.10 for e in errors)/len(errors)*100,2),"%")
print()
print("Decision: use 128 hash values.")
print("Reason: reduced representation saves space while keeping similarity estimation error small.")