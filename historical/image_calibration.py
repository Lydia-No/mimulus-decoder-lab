#!/usr/bin/env python3
import json, os, random, sys
from PIL import Image, ImageDraw
import image_only_f113r as D

W,H=2582,3787
SEED=170113
EXPECTED={
  "positive_structured":{"horizontal-repetition":"present","left-margin-discrete-repetition":"present"},
  "central_disrupted":{"horizontal-repetition":"not_detected","left-margin-discrete-repetition":"present"},
  "margin_ablated":{"horizontal-repetition":"present","left-margin-discrete-repetition":"not_detected"},
  "texture_null":{"horizontal-repetition":"not_detected","left-margin-discrete-repetition":"not_detected"}
}

def base(): return Image.new("L",(W,H),245)

def marker(draw,x,y):
    draw.line((x-24,y,x+24,y),fill=35,width=6); draw.line((x,y-24,x,y+24),fill=35,width=6)
    draw.line((x-16,y-16,x+16,y+16),fill=35,width=4); draw.line((x-16,y+16,x+16,y-16),fill=35,width=4)
    draw.line((x,y+18,x+7,y+55),fill=35,width=4)

def line_units(draw,y,rng):
    x=520
    while x<2330:
        w=rng.randint(22,70); h=rng.randint(10,18)
        draw.rectangle((x,y-h//2,x+w,y+h//2),fill=rng.randint(25,65))
        if rng.random()<.28: draw.rectangle((x+w//2,y-h//2-7,x+w//2+5,y+h//2+7),fill=35)
        x += w+rng.randint(12,32)

def structured(with_margin=True):
    rng=random.Random(SEED); im=base(); d=ImageDraw.Draw(im)
    y=360
    for _ in range(42): line_units(d,y,rng); y+=65
    if with_margin:
        for i in range(16): marker(d,250,430+i*180)
    return im

def disrupted():
    rng=random.Random(SEED); im=base(); d=ImageDraw.Draw(im)
    # Same approximate central glyph mass as the structured case, but vertical locations are independently randomized.
    for _ in range(42*28):
        x=rng.randint(520,2280); y=rng.randint(300,3300); w=rng.randint(22,70); h=rng.randint(10,18)
        d.rectangle((x,y-h//2,x+w,y+h//2),fill=rng.randint(25,65))
    for i in range(16): marker(d,250,430+i*180)
    return im

def texture_null():
    rng=random.Random(SEED); im=base(); d=ImageDraw.Draw(im)
    # Fine periodic microtexture at ~60 px vertical spacing, intentionally lacking macro text-line groups or discrete margin markers.
    for y in range(330,3330,60):
        phase=rng.randint(0,19)
        for x in range(110+phase,2350,54):
            shade=rng.randint(65,115)
            d.rectangle((x,y,x+5,y+13),fill=shade)
    return im

def claims_map(run): return {c["claimKey"]:c["proposition"] for c in run["claims"]}

def main():
    if len(sys.argv)!=2: raise SystemExit("usage: image_calibration.py OUTPUT_DIR")
    out=sys.argv[1]; os.makedirs(out,exist_ok=True)
    conditions={
      "positive_structured":structured(True),
      "central_disrupted":disrupted(),
      "margin_ablated":structured(False),
      "texture_null":texture_null()
    }
    decoders={"A2":D.decoder_a2,"B5":D.decoder_b5,"C8":D.decoder_c8}
    result={"calibration_id":"image-decoder-calibration-001","decoder_version":D.RUN_VERSION,"seed":SEED,"expected":EXPECTED,"conditions":{},"scores":{},"gate":{}}
    for name,img in conditions.items():
        img.save(os.path.join(out,name+".png"),format="PNG",optimize=False)
        result["conditions"][name]={}
        for code,fn in decoders.items():
            run=fn(img); actual=claims_map(run); expected=EXPECTED[name]
            cells={k:{"expected":expected[k],"actual":actual[k],"correct":actual[k]==expected[k]} for k in expected}
            result["conditions"][name][code]={"measurements":run["measurements"],"claims":actual,"cells":cells}
    for code in decoders:
        cells=[]
        for name in conditions:
            cells.extend(result["conditions"][name][code]["cells"].values())
        correct=sum(1 for c in cells if c["correct"])
        result["scores"][code]={"correct":correct,"total":len(cells),"passed":correct==len(cells)}
    result["gate"]={"criterion":"each decoder must classify all 8 known-answer claim-condition cells correctly","passed":all(v["passed"] for v in result["scores"].values())}
    result["boundary"]="Known-answer image calibration only. Failure blocks substantive rerun of the same decoder version on f113r; it does not alter the already frozen historical run 001."
    with open(os.path.join(out,"calibration.json"),"w") as f: json.dump(result,f,indent=2,sort_keys=True)
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=="__main__": main()
