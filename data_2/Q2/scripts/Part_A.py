import csv, glob, re, math, time, os
from collections import defaultdict

# ---------- LOAD NOTICES ----------
notices = {}

for fn in glob.glob("notices\\part-*.csv"):
    with open(fn, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            notices[r["notice_id"]] = r

print("NOTICES:", len(notices))

# ---------- NORMALIZATION ----------
def norm(s):
    s = s.lower()
    s = re.sub(r'rs\.?\s*[\d,]+(?:\.\d+)?(?:\s*lakh|\s*cr)?', ' MONEY ', s)
    s = re.sub(r'\binr\s*[\d,]+(?:\.\d+)?(?:\s*lakh|\s*cr)?', ' MONEY ', s)
    s = re.sub(r'\b\d[\d,]*(?:\.\d+)?\b', ' NUM ', s)
    s = re.sub(r'\s+', ' ', s)
    return s.strip()

def words3(s):
    w = norm(s).split()
    return set(" ".join(w[i:i+3]) for i in range(len(w)-2))

def chars5(s):
    s = norm(s)
    return set(s[i:i+5] for i in range(len(s)-4))

def jac(a,b):
    if not a and not b: return 1
    return len(a & b) / len(a | b)

# ---------- LABELLED PAIRS ----------
pairs=[]
with open("labelled_pairs.csv", encoding="utf-8-sig", newline="") as f:
    pairs=list(csv.DictReader(f))

same=[p for p in pairs if p["label"].strip().lower()=="same"]
diff=[p for p in pairs if p["label"].strip().lower()=="different"]

print("LABELS: same =",len(same),"different =",len(diff))

# ---------- ALL PAIR SCORES ----------
results=[]

for p in pairs:
    a=notices[p["notice_id_a"]]
    b=notices[p["notice_id_b"]]
    ta=a["title"]+" "+a["body"]
    tb=b["title"]+" "+b["body"]

    w=jac(words3(ta),words3(tb))
    c=jac(chars5(ta),chars5(tb))

    results.append((p["label"],w,c))

def stats(index,label):
    x=[r[index] for r in results if r[0]==label]
    return min(x),sum(x)/len(x),max(x)

print("\nWORD 3-GRAM JACCARD")
print("same      min/avg/max:",stats(1,"same"))
print("different min/avg/max:",stats(1,"different"))

print("\nCHAR 5-GRAM JACCARD")
print("same      min/avg/max:",stats(2,"same"))
print("different min/avg/max:",stats(2,"different"))

# ---------- THRESHOLD TEST ----------
print("\nTHRESHOLD TEST - CHAR 5 GRAMS")

best=None
for t in [i/100 for i in range(30,91)]:
    fp=sum(1 for l,w,c in results if l=="different" and c>=t)
    fn=sum(1 for l,w,c in results if l=="same" and c<t)

    # Explicit design assumption: missing a duplicate costs 100x a false merge.
    cost=100*fn+fp

    if best is None or cost<best[0]:
        best=(cost,t,fp,fn)

print("chosen threshold:",best[1])
print("false positives:",best[2])
print("false negatives:",best[3])
print("weighted cost (FN=100, FP=1):",best[0])

# ---------- SAVE MEASUREMENTS ----------
with open("q2_measurements.txt","w") as f:
    f.write("Q2 MEASUREMENTS\n")
    f.write("Notices: 12000\n")
    f.write("Labelled pairs: 900\n")
    f.write("Same: 279\nDifferent: 621\n\n")
    f.write("WORD 3-GRAM\n")
    f.write("same min avg max: "+str(stats(1,"same"))+"\n")
    f.write("different min avg max: "+str(stats(1,"different"))+"\n\n")
    f.write("CHAR 5-GRAM\n")
    f.write("same min avg max: "+str(stats(2,"same"))+"\n")
    f.write("different min avg max: "+str(stats(2,"different"))+"\n\n")
    f.write("THRESHOLD\n")
    f.write("threshold: "+str(best[1])+"\n")
    f.write("false positives: "+str(best[2])+"\n")
    f.write("false negatives: "+str(best[3])+"\n")
    f.write("weighted cost FN=100 FP=1: "+str(best[0])+"\n")

print("\nDONE. Created q2_measurements.txt")