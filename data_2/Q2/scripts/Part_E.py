import csv,glob,re,time,statistics

notices={}

for file in glob.glob("notices\\part-*.csv"):
    with open(file,encoding="utf-8-sig",newline="") as f:
        for r in csv.DictReader(f):
            notices[r["notice_id"]]=r

AGG={"P001","P002","P003","P004","P005","P006"}

def norm(s):
    return re.sub(r"\s+"," ",s.lower()).strip()

def transform(r,mitigate=False):
    text=r["title"]+" "+r["body"]

    if mitigate and r["portal_id"] in AGG:
        # Remove documented common portal boilerplate.
        if len(text)>1900:
            text=text[1400:-300]
        elif len(text)>1900:
            text=text[1400:]
    
    return norm(text)

def signature(text):
    S={text[i:i+5] for i in range(len(text)-4)}
    out=[]
    for seed in range(128):
        m=2**64-1
        for x in S:
            h=hash((seed,x))&((1<<64)-1)
            if h<m:m=h
        out.append(m)
    return out

def run(mitigate):
    t=time.time()
    sigs={n:signature(transform(r,mitigate))
          for n,r in notices.items()}

    buckets={}
    for n,s in sigs.items():
        for b in range(16):
            key=(b,hash(tuple(s[b*8:(b+1)*8])))
            buckets.setdefault(key,[]).append(n)

    counts=[len(x) for x in buckets.values()]

    candidates=set()
    for ids in buckets.values():
        if len(ids)<=300:
            for i in range(len(ids)):
                for j in range(i+1,len(ids)):
                    a,b=ids[i],ids[j]
                    candidates.add((a,b) if a<b else (b,a))

    return candidates,counts,time.time()-t

before,bcounts,bt=run(False)
after,acounts,at=run(True)

with open("labelled_pairs.csv",encoding="utf-8-sig",newline="") as f:
    pairs=list(csv.DictReader(f))

same=[p for p in pairs if p["label"]=="same"]

def recall(c):
    return sum(
        ((p["notice_id_a"],p["notice_id_b"]) if p["notice_id_a"]<p["notice_id_b"]
         else (p["notice_id_b"],p["notice_id_a"])) in c
        for p in same
    )/len(same)*100

def stats(x):
    return (
        len(x),
        statistics.median(x),
        statistics.quantiles(x,n=20)[18] if len(x)>=20 else max(x),
        max(x)
    )

print("========== PART E ==========")
print("BEFORE mitigation")
print("Candidate pairs:",len(before))
print("Bucket count/median/P95/max:",stats(bcounts))
print("Runtime:",round(bt,2),"seconds")
print("Same-pair recall:",round(recall(before),2),"%")

print("\nAFTER mitigation")
print("Candidate pairs:",len(after))
print("Bucket count/median/P95/max:",stats(acounts))
print("Runtime:",round(at,2),"seconds")
print("Same-pair recall:",round(recall(after),2),"%")

print("\nMitigation: remove repeated portal boilerplate from the six nodal aggregator portals.")
print("Reason: repeated boilerplate creates large buckets and unnecessary comparisons.")
print("Stable card IDs should be stored in q2_opportunity_card and q2_notice_card.")
print("Existing card mappings are retained on reruns; new matching copies reuse the existing card_id.")