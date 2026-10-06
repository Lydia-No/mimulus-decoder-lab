#!/usr/bin/env python3
import json, os, random, sys
from PIL import Image, ImageDraw
import image_decoders_v2 as D

W,H=2582,3787
KEYS=["horizontal-repetition","left-margin-discrete-repetition"]
HOLDOUT={
  "positive_c":{"kind":"structured","seed":41011,"line_spacing":62,"marker_spacing":172,"jitter":1,"margin":True,"expected":["present","present"]},
  "positive_d":{"kind":"structured","seed":41012,"line_spacing":70,"marker_spacing":198,"jitter":2,"margin":True,"expected":["present","present"]},
  "disrupted_c":{"kind":"disrupted_rect","seed":41013,"marker_spacing":172,"density":1020,"expected":["not_detected","present"]},
  "disrupted_d":{"kind":"disrupted_ellipse","seed":41014,"marker_spacing":198,"density":940,"expected":["not_detected","present"]},
  "margin_ablated_c":{"kind":"structured","seed":41015,"line_spacing":62,"marker_spacing":172,"jitter":1,"margin":False,"expected":["present","not_detected"]},
  "margin_ablated_d":{"kind":"structured","seed":41016,"line_spacing":70,"marker_spacing":198,"jitter":2,"margin":False,"expected":["present","not_detected"]},
  "texture_null_c":{"kind":"texture","seed":41017,"vspacing":54,"xspacing":59,"barw":5,"barh":14,"expected":["not_detected","not_detected"]},
  "texture_null_d":{"kind":"texture","seed":41018,"vspacing":71,"xspacing":47,"barw":9,"barh":16,"expected":["not_detected","not_detected"]},
  "marker_only":{"kind":"marker_only","seed":41019,"marker_spacing":187,"expected":["not_detected","present"]},
  "sparse_null":{"kind":"sparse_null","seed":41020,"expected":["not_detected","not_detected"]}
}


def base(): return Image.new("L",(W,H),245)

def marker(draw,x,y,variant=0):
    if variant % 2 == 0:
        draw.line((x-27,y,x+27,y),fill=38,width=7); draw.line((x,y-25,x,y+26),fill=38,width=6)
        draw.line((x-17,y-17,x+17,y+17),fill=38,width=4); draw.line((x-17,y+17,x+17,y-17),fill=38,width=4)
        draw.line((x+2,y+19,x+10,y+58),fill=38,width=4)
    else:
        draw.polygon([(x,y-29),(x+27,y),(x,y+29),(x-27,y)],outline=38,width=6)
        draw.line((x-22,y,x+22,y),fill=38,width=5); draw.line((x,y-22,x,y+48),fill=38,width=5)


def line_units(draw,y,rng):
    x=485
    while x<2335:
        w=rng.randint(20,88); h=rng.randint(10,23)
        shade=rng.randint(28,82)
        if rng.random()<.35:
            draw.rounded_rectangle((x,y-h//2,x+w,y+h//2),radius=max(2,h//4),fill=shade)
        else:
            draw.rectangle((x,y-h//2,x+w,y+h//2),fill=shade)
        if rng.random()<.20: draw.line((x+w//2,y-h//2-5,x+w//2,y+h//2+6),fill=40,width=rng.randint(3,6))
        x += w+rng.randint(11,36)


def structured(cfg):
    rng=random.Random(cfg["seed"]); im=base(); d=ImageDraw.Draw(im); y=350
    nlines=min(45,int((3190-350)/cfg["line_spacing"]))
    for _ in range(nlines):
        jy=y+rng.randint(-cfg["jitter"],cfg["jitter"]); line_units(d,jy,rng); y += cfg["line_spacing"]
    if cfg["margin"]:
        nmark=min(19,int((3290-410)/cfg["marker_spacing"]))
        for i in range(nmark): marker(d,248,410+i*cfg["marker_spacing"],i)
    return im


def disrupted_rect(cfg):
    rng=random.Random(cfg["seed"]); im=base(); d=ImageDraw.Draw(im)
    for _ in range(cfg["density"]):
        x=rng.randint(490,2300); y=rng.randint(310,3290); w=rng.randint(20,88); h=rng.randint(10,23)
        d.rectangle((x,y-h//2,x+w,y+h//2),fill=rng.randint(28,82))
    nmark=min(19,int((3290-410)/cfg["marker_spacing"]))
    for i in range(nmark): marker(d,248,410+i*cfg["marker_spacing"],i)
    return im


def disrupted_ellipse(cfg):
    rng=random.Random(cfg["seed"]); im=base(); d=ImageDraw.Draw(im)
    for _ in range(cfg["density"]):
        x=rng.randint(490,2300); y=rng.randint(310,3290); w=rng.randint(22,80); h=rng.randint(10,25)
        d.ellipse((x,y-h//2,x+w,y+h//2),fill=rng.randint(30,90))
    nmark=min(19,int((3290-410)/cfg["marker_spacing"]))
    for i in range(nmark): marker(d,248,410+i*cfg["marker_spacing"],i)
    return im


def texture(cfg):
    rng=random.Random(cfg["seed"]); im=base(); d=ImageDraw.Draw(im)
    for y in range(305,3350,cfg["vspacing"]):
        phase=rng.randint(0,max(1,cfg["xspacing"]//2))
        for x in range(100+phase,2370,cfg["xspacing"]):
            shade=rng.randint(62,138)
            if rng.random()<.5: d.rectangle((x,y,x+cfg["barw"],y+cfg["barh"]),fill=shade)
            else: d.ellipse((x,y,x+cfg["barw"],y+cfg["barh"]),fill=shade)
    return im


def marker_only(cfg):
    im=base(); d=ImageDraw.Draw(im); nmark=min(19,int((3290-410)/cfg["marker_spacing"]))
    for i in range(nmark): marker(d,248,410+i*cfg["marker_spacing"],i)
    return im


def sparse_null(cfg):
    rng=random.Random(cfg["seed"]); im=base(); d=ImageDraw.Draw(im)
    for _ in range(240):
        x=rng.randint(120,2350); y=rng.randint(250,3400); w=rng.randint(3,18); h=rng.randint(3,15)
        if rng.random()<.5: d.rectangle((x,y,x+w,y+h),fill=rng.randint(55,145))
        else: d.ellipse((x,y,x+w,y+h),fill=rng.randint(55,145))
    return im


def make(cfg):
    return {
      "structured":structured,
      "disrupted_rect":disrupted_rect,
      "disrupted_ellipse":disrupted_ellipse,
      "texture":texture,
      "marker_only":marker_only,
      "sparse_null":sparse_null
    }[cfg["kind"]](cfg)


def main():
    if len(sys.argv)!=2: raise SystemExit("usage: image_v2_holdout.py OUTPUT_DIR")
    out=sys.argv[1]; os.makedirs(out,exist_ok=True)
    result={"holdout_id":"image-only-v2-heldout-001","decoder_version":D.RUN_VERSION,"cases":{},"scores":{},"gate":{}}
    for name,cfg in HOLDOUT.items():
        image=make(cfg); expected=dict(zip(KEYS,cfg["expected"])); result["cases"][name]={"expected":expected,"decoders":{}}
        for run in D.run_all(image,name,None):
            code=run["decoder"]["blindCode"]; actual=D.claims_map(run)
            cells={k:{"expected":expected[k],"actual":actual[k],"correct":actual[k]==expected[k]} for k in KEYS}
            result["cases"][name]["decoders"][code]={"measurements":run["measurements"],"cells":cells}
    for code in ["A3","B6","C9"]:
        cells=[]
        for case in result["cases"].values(): cells.extend(case["decoders"][code]["cells"].values())
        correct=sum(1 for c in cells if c["correct"]); result["scores"][code]={"correct":correct,"total":len(cells),"passed":correct==len(cells)}
    result["gate"]={"criterion":"all three frozen decoder families must classify all 20 held-out cells correctly","passed":all(v["passed"] for v in result["scores"].values())}
    result["boundary"]="Held-out synthetic transport gate. Decoder thresholds were frozen before this generator was added. Failure blocks historical use of this candidate version; success permits only a separately preregistered historical run."
    with open(os.path.join(out,"holdout.json"),"w",encoding="utf-8") as f: json.dump(result,f,indent=2,sort_keys=True)
    print(json.dumps(result,indent=2,sort_keys=True))
    if not result["gate"]["passed"]: raise SystemExit(2)

if __name__=="__main__": main()
