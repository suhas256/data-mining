import csv, glob, re, math, time

notices={}

for file in glob.glob("notices\\part-*.csv"):
    with open(file,encoding="utf-8-sig",newline="") as f:
        for r in csv.DictReader(f):
            notices[r["notice_id"]]=r

def norm(s):
    return re.sub(r"\s+"," ",s.lower()).strip()

def shingles(s):
    s=norm(s)
    return {s[i:i+5] for i in range(len(s)-4)}

def sig(s):
    S=shingles(s)
    out=[]
    for seed in range(128):
        m=2**64-1
        for x in S:
            h=hash((seed,x))&((1<<64)-1)
            if h<m:m=h
        out.append(m)
    return out

start=time.time()
sigs={}

for i,(nid,r) in enumerate(notices.items()):
    sigs[nid]=sig(r["title"]+" "+r["body"])

bands=16
rows=8
buckets={}

for nid,s in sigs.items():
    for b in range(bands):
        key=(b,hash(tuple(s[b*rows:(b+1)*rows])))
        buckets.setdefault(key,[]).append(nid)

candidates=set()

for ids in buckets.values():
    if len(ids)<=300:
        for i in range(len(ids)):
            for j in range(i+1,len(ids)):
                candidates.add((ids[i],ids[j]))

with open("labelled_pairs.csv",encoding="utf-8-sig",newline="") as f:
    pairs=list(csv.DictReader(f))

survive=[]
for p in pairs:
    a=p["notice_id_a"]
    b=p["notice_id_b"]
    key=(a,b) if a<b else (b,a)
    survive.append((p["label"],key in candidates))

print("========== PART C ==========")
print("MinHash: 128")
print("LSH: 16 bands x 8 rows")
print("Candidate pairs:",len(candidates))
print("Runtime:",round(time.time()-start,2),"seconds")

same=[x for x in survive if x[0]=="same"]
diff=[x for x in survive if x[0]=="different"]

print("Same-pair candidate recall:",
      round(sum(x[1] for x in same)/len(same)*100,2),"%")

print("Different pairs surviving:",
      round(sum(x[1] for x in diff)/len(diff)*100,2),"%")

print("Operating point: 16 bands x 8 rows")
print("This gives high survival probability for genuinely similar notices while avoiding all-pairs comparison.")