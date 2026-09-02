"""Build deterministic, deduplicated shell-balanced train/heldout recovery splits."""
import hashlib, json, random, re
from pathlib import Path
from evaluate_native_checkpoint import DEFAULT_PROMPTS

ROOT=Path(__file__).resolve().parents[1]
def norm(text): return re.sub(r"\W+", " ", text.casefold()).strip()
def main():
    source=ROOT/"evals/training/ascension_product_v159_proven_master.jsonl"
    excluded={norm(x) for x in DEFAULT_PROMPTS}
    receipt=json.loads((ROOT/"evals/receipt_truth_prompts.json").read_text(encoding="utf-8"))
    excluded.update(norm(x["prompt"]) for x in receipt)
    by={}; seen=set()
    for line in source.read_text(encoding="utf-8").splitlines():
        row=json.loads(line); key=norm(row["user"])
        if key in seen or key in excluded: continue
        if re.search(r"What Was Added|Cross-references:|Related Capabilities", row["assistant"], re.I): continue
        seen.add(key); by.setdefault(row["shell"],[]).append(row)
    rng=random.Random(3407); train=[]; held=[]
    for shell, rows in sorted(by.items()):
        rng.shuffle(rows); take=min(60,len(rows)); chosen=rows[:take]
        cut=min(max(1,round(take*.2)),take-1); held.extend(chosen[:cut]); train.extend(chosen[cut:])
    rng.shuffle(train); rng.shuffle(held)
    out=ROOT/"evals/training"
    paths={"train":out/"aerynza_balanced_recovery_train_v2.jsonl","heldout":out/"aerynza_balanced_recovery_heldout_v2.jsonl"}
    for name, rows in (("train",train),("heldout",held)):
        if paths[name].exists(): raise FileExistsError(paths[name])
        paths[name].write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in rows)+"\n",encoding="utf-8")
    print(json.dumps({n:{"records":sum(1 for _ in p.open(encoding="utf-8")),"sha256":hashlib.sha256(p.read_bytes()).hexdigest()} for n,p in paths.items()},indent=2))
if __name__=="__main__": main()
