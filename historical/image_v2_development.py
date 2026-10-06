#!/usr/bin/env python3
import json, os, random, sys
from PIL import Image, ImageDraw
import image_decoders_v2 as D

W,H=2582,3787
DEV_CASES={
  "positive_a":{"kind":"structured","seed":1001,"line_spacing":58,"marker_spacing":160,"margin":True,"expected":["present","present"]},
  "positive_b":{"kind":"structured","seed":1002,"line_spacing":74,"marker_spacing":215,"margin":True,"expected":["present","present"]},
  "disrupted_a":{"kind":"disrupted","seed":1003,"marker_spacing":160,"density":1100,"expected":["not_detected","present"]},
  "disrupted_b":{"kind":"disrupted","seed":1004,"marker_spacing":215,"density":900,"expected":["not_detected","present"]},
  "margin_ablated_a":{"kind":"structured","seed":1005,"line_spacing":58,"marker_spacing":160,"margin":False,"expected":["present","not_detected"]},
  "margin_ablated_b":{"kind":"structured","seed":1006,"line_spacing":74,"marker_spacing":215,"margin":False,"expected":["present","not_detected"]},
  "texture_null_a":{"kind":"texture","seed":1007,"vspacing":47,"xspacing":43,"barw":4,"barh":11,"expected":["not_detected","not_detected"]},
  "texture_null_b":{"kind":"texture","seed":1008,"vspacing":83,"xspacing":67,"barw":7,"barh":17,"expected":["not_detected","not_detected"]}
}
KEYS=["horizontal-repetition","left-margin-discrete-repetition"]

def base(): return Image.new("L",(W,H),245)

def marker(draw,x,y):
    draw.line((x-24,y,x+24,y),fill=35,width=6); draw.line((x,y-24,x,y+24),fill=35,width=6)
    draw.line((x-16,y-16,x+16,y+16),fill=35,width=4); draw.line((x-16,y+16,x+16,y-16),fill=35,width=4)
    draw.line((x,y+18,x+7,y+55),fill=35,width=4)

def line_units(draw,y,rng):
    x=500
    while x<2320:
        w=rng.randint(18,82); h=rng.randint(9,22)
        draw.rectangle((x,y-h//2,x+w,y+h//2),fill=rng.randint(25,75))
        if rng.random()<.25: draw.rectangle((x+w//2,y-h//2-rng.randint(3,8),x+w//2+rng.randint(3,6),y+h//2+rng.randint(3,8)),fill=35)
        x += w+rng.randint(10,38)

def structured(cfg):
    rng=random.Random(cfg["seed"]); im=base(); d=ImageDraw.Draw(im); y=340
    nlines=min(46,int((3200-340)/cfg["line_spacing"]))
    for _ in range(nlines): line_units(d,y,rng); y += cfg["line_spacing"]
    if cfg["margin"]:
        nmark=min(20,int((3300-400)/cfg["marker_spacing"]))
        for i in range(nmark): marker(d,250,400+i*cfg["marker_spacing"])
    return im

def disrupted(cfg):
    rng=random.Random(cfg["seed"]); im=base(); d=ImageDraw.Draw(im)
    for _ in range(cfg["density"]):
        x=rng.randint(500,2280); y=rng.randint(300,3300); w=rng.randint(18,82); h=rng.randint(9,22)
        d.rectangle((x,y-h//2,x+w,y+h//2),fill=rng.randint(25,75))
    nmark=min(20,int((3300-400)/cfg["marker_spacing"]))
    for i in range(nmark): marker(d,250,400+i*cfg["marker_spacing"])
    return im

def texture(cfg):
    rng=random.Random(cfg["seed"]); im=base(); d=ImageDraw.Draw(im)
    for y in range(300,3350,cfg["vspacing"]):
        phase=rng.randint(0,max(1,cfg["xspacing"]//3))
        for x in range(100+phase,2360,cfg["xspacing"]):
            d.rectangle((x,y,x+cfg["barw"],y+cfg["barh"]),fill=rng.randint(60,130))
    return im

def make(cfg):
    return structured(cfg) if cfg["kind"]=="structured" else disrupted(cfg) if cfg["kind"]=="disrupted" else texture(cfg)

def main():
    if len(sys.argv)!=2: raise SystemExit("usage: image_v2_development.py OUTPUT_DIR")
    out=sys.argv[1]; os.makedirs(out,exist_ok=True)
    result={"development_id":"image-only-v2-development-001","decoder_version":D.RUN_VERSION,"cases":{},"scores":{},"gate":{}}
    for name,cfg in DEV_CASES.items():
        image=make(cfg); result["cases"][name]={"expected":dict(zip(KEYS,cfg["expected"])),"decoders":{}}
        for run in D.run_all(image,name,None):
            code=run["decoder"]["blindCode"]; actual=D.claims_map(run); expected=result["cases"][name]["expected"]
            cells={k:{"expected":expected[k],"actual":actual[k],"correct":actual[k]==expected[k]} for k in KEYS}
            result["cases"][name]["decoders"][code]={"measurements":run["measurements"],"cells":cells}
    for code in ["A3","B6","C9"]:
        cells=[]
        for case in result["cases"].values(): cells.extend(case["decoders"][code]["cells"].values())
        correct=sum(1 for c in cells if c["correct"]); result["scores"][code]={"correct":correct,"total":len(cells),"passed":correct==len(cells)}
    result["gate"]={"criterion":"all three decoder families must classify all 16 development cells correctly","passed":all(v["passed"] for v in result["scores"].values())}
    result["boundary"]="Development material only. Passing this set does not authorize historical use. The decoder implementation must be frozen before a separately generated held-out set is created and inspected."
    with open(os.path.join(out,"development.json"),"w",encoding="utf-8") as f: json.dump(result,f,indent=2,sort_keys=True)
    print(json.dumps(result,indent=2,sort_keys=True))
    if not result["gate"]["passed"]: raise SystemExit(2)

if __name__=="__main__": main()
