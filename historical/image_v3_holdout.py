#!/usr/bin/env python3
import json, os, random, sys
from PIL import Image, ImageDraw
import image_decoders_v3 as D
import image_v2_holdout as G

W,H=2582,3787
KEYS=["horizontal-repetition","left-margin-discrete-repetition"]
HOLDOUT={
  "positive_e":{"kind":"structured","seed":73001,"line_spacing":61,"marker_spacing":155,"jitter":3,"margin":True,"expected":["present","present"]},
  "positive_f":{"kind":"structured","seed":73002,"line_spacing":77,"marker_spacing":235,"jitter":3,"margin":True,"expected":["present","present"]},
  "disrupted_e":{"kind":"disrupted_rect","seed":73003,"marker_spacing":155,"density":980,"expected":["not_detected","present"]},
  "disrupted_f":{"kind":"disrupted_ellipse","seed":73004,"marker_spacing":235,"density":860,"expected":["not_detected","present"]},
  "margin_ablated_e":{"kind":"structured","seed":73005,"line_spacing":61,"marker_spacing":155,"jitter":3,"margin":False,"expected":["present","not_detected"]},
  "margin_ablated_f":{"kind":"structured","seed":73006,"line_spacing":77,"marker_spacing":235,"jitter":3,"margin":False,"expected":["present","not_detected"]},
  "texture_null_e":{"kind":"texture","seed":73007,"vspacing":63,"xspacing":73,"barw":6,"barh":15,"expected":["not_detected","not_detected"]},
  "texture_null_f":{"kind":"texture","seed":73008,"vspacing":87,"xspacing":41,"barw":8,"barh":19,"expected":["not_detected","not_detected"]},
  "marker_only_e":{"kind":"marker_only","seed":73009,"marker_spacing":205,"expected":["not_detected","present"]},
  "irregular_margin_null":{"kind":"irregular_margin","seed":73010,"expected":["not_detected","not_detected"]},
  "vertical_margin_rule_null":{"kind":"vertical_margin_rules","seed":73011,"expected":["not_detected","not_detected"]},
  "mixed_sparse_null":{"kind":"mixed_sparse","seed":73012,"expected":["not_detected","not_detected"]}
}


def irregular_margin(cfg):
    rng=random.Random(cfg["seed"]); im=Image.new("L",(W,H),245); d=ImageDraw.Draw(im)
    ys=[]; y=360
    # Deliberately non-periodic gaps, all concentrated in the margin column.
    gaps=[91,247,133,319,78,211,166,287,104,352,145,226,83,301]
    for gap in gaps:
        y += gap
        if y>3350: break
        ys.append(y)
    for i,y in enumerate(ys): G.marker(d,248,y,i)
    # a few unrelated central marks so blankness itself is not the cue
    for _ in range(90):
        x=rng.randint(600,2250); yy=rng.randint(350,3300)
        d.rectangle((x,yy,x+rng.randint(8,28),yy+rng.randint(4,12)),fill=rng.randint(70,135))
    return im


def vertical_margin_rules(cfg):
    rng=random.Random(cfg["seed"]); im=Image.new("L",(W,H),245); d=ImageDraw.Draw(im)
    for x in (170,210,255,300,338):
        d.line((x,330,x+rng.randint(-3,3),3330),fill=rng.randint(35,80),width=rng.randint(3,7))
    for _ in range(70):
        x=rng.randint(650,2200); y=rng.randint(350,3300)
        d.ellipse((x,y,x+rng.randint(5,18),y+rng.randint(5,18)),fill=rng.randint(75,145))
    return im


def mixed_sparse(cfg):
    rng=random.Random(cfg["seed"]); im=Image.new("L",(W,H),245); d=ImageDraw.Draw(im)
    for _ in range(330):
        if rng.random()<.28: x=rng.randint(100,430)
        else: x=rng.randint(480,2350)
        y=rng.randint(260,3400); w=rng.randint(3,24); h=rng.randint(3,18)
        if rng.random()<.5: d.rectangle((x,y,x+w,y+h),fill=rng.randint(55,150))
        else: d.ellipse((x,y,x+w,y+h),fill=rng.randint(55,150))
    return im


def make(cfg):
    kind=cfg["kind"]
    if kind=="structured": return G.structured(cfg)
    if kind=="disrupted_rect": return G.disrupted_rect(cfg)
    if kind=="disrupted_ellipse": return G.disrupted_ellipse(cfg)
    if kind=="texture": return G.texture(cfg)
    if kind=="marker_only": return G.marker_only(cfg)
    if kind=="irregular_margin": return irregular_margin(cfg)
    if kind=="vertical_margin_rules": return vertical_margin_rules(cfg)
    if kind=="mixed_sparse": return mixed_sparse(cfg)
    raise ValueError(kind)


def main():
    if len(sys.argv)!=2: raise SystemExit("usage: image_v3_holdout.py OUTPUT_DIR")
    out=sys.argv[1]; os.makedirs(out,exist_ok=True)
    result={"holdout_id":"image-only-v3-heldout-001","decoder_version":D.RUN_VERSION,"cases":{},"scores":{},"gate":{}}
    for name,cfg in HOLDOUT.items():
        image=make(cfg); expected=dict(zip(KEYS,cfg["expected"])); result["cases"][name]={"expected":expected,"decoders":{}}
        for run in D.run_all(image,name,None):
            code=run["decoder"]["blindCode"]; actual=D.claims_map(run)
            cells={k:{"expected":expected[k],"actual":actual[k],"correct":actual[k]==expected[k]} for k in KEYS}
            result["cases"][name]["decoders"][code]={"measurements":run["measurements"],"cells":cells}
    for code in ["A3","B7","C9"]:
        cells=[]
        for case in result["cases"].values(): cells.extend(case["decoders"][code]["cells"].values())
        correct=sum(1 for c in cells if c["correct"])
        result["scores"][code]={"correct":correct,"total":len(cells),"passed":correct==len(cells)}
    result["gate"]={"criterion":"all three frozen decoder families must classify all 24 fresh held-out cells correctly","passed":all(v["passed"] for v in result["scores"].values())}
    result["boundary"]="Fresh prospective v3 synthetic holdout. Failure blocks historical use; success permits only a separately preregistered historical run using the unchanged decoder blob."
    with open(os.path.join(out,"holdout.json"),"w",encoding="utf-8") as f: json.dump(result,f,indent=2,sort_keys=True)
    print(json.dumps(result,indent=2,sort_keys=True))
    if not result["gate"]["passed"]: raise SystemExit(2)

if __name__=="__main__": main()
