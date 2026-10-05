#!/usr/bin/env python3
import hashlib, json, math, os, statistics, sys
from collections import deque
from PIL import Image

EXPECTED_SHA256 = "ad748f9012b174be520b7ac837fdadf913e49a696323920ca655ecf5474afb5c"
FIXTURE_ID = "voynich-f113r"
RUN_VERSION = "image-only-001.0"

def sha256_file(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()

def otsu(img):
    hist=img.histogram()[:256]; total=sum(hist); total_sum=sum(i*n for i,n in enumerate(hist))
    wb=0; sb=0.0; best=-1.0; threshold=128
    for t in range(256):
        wb += hist[t]
        if wb==0: continue
        wf=total-wb
        if wf==0: break
        sb += t*hist[t]
        mb=sb/wb; mf=(total_sum-sb)/wf
        score=wb*wf*(mb-mf)**2
        if score>best: best=score; threshold=t
    return threshold

def moving_average(xs,radius):
    prefix=[0.0]
    for x in xs: prefix.append(prefix[-1]+x)
    out=[]; n=len(xs)
    for i in range(n):
        lo=max(0,i-radius); hi=min(n,i+radius+1)
        out.append((prefix[hi]-prefix[lo])/(hi-lo))
    return out

def runs(mask,merge_gap=0,min_len=1):
    found=[]; start=None
    for i,active in enumerate(mask):
        if active and start is None: start=i
        elif not active and start is not None: found.append([start,i-1]); start=None
    if start is not None: found.append([start,len(mask)-1])
    if merge_gap and found:
        merged=[found[0]]
        for a,b in found[1:]:
            if a-merged[-1][1]-1<=merge_gap: merged[-1][1]=b
            else: merged.append([a,b])
        found=merged
    return [r for r in found if r[1]-r[0]+1>=min_len]

def cv(xs):
    if not xs: return None
    m=statistics.mean(xs)
    return None if m==0 else statistics.pstdev(xs)/m

def row_dark_fraction(crop,threshold,step=1):
    px=crop.load(); w,h=crop.size; denom=len(range(0,w,step)); out=[]
    for y in range(h):
        dark=sum(1 for x in range(0,w,step) if px[x,y]<threshold)
        out.append(dark/denom)
    return out

def claim(key,target,value,locator):
    return {"claimKey":key,"target":target,"proposition":value,"evidence":[{"layer":"SOURCE_IMAGE","locator":locator}]}

def decoder_a2(gray):
    tw=1200; th=round(gray.height*tw/gray.width); im=gray.resize((tw,th),Image.Resampling.LANCZOS)
    y0,y1=round(.05*th),round(.95*th)
    central=im.crop((round(.18*tw),y0,round(.94*tw),y1)); t=otsu(central)
    s=moving_average(row_dark_fraction(central,t),2); bands=runs([v>=.012 for v in s],4,2)
    centers=[(a+b)/2 for a,b in bands]; gaps=[centers[i]-centers[i-1] for i in range(1,len(centers))]
    med=statistics.median(gaps) if gaps else None; gapcv=cv(gaps)
    horizontal=len(bands)>=20 and med is not None and 12<=med<=90 and gapcv is not None and gapcv<=.90
    margin=im.crop((round(.03*tw),y0,round(.18*tw),y1)); mt=otsu(margin)
    ms=moving_average(row_dark_fraction(margin,mt),2); mruns=runs([v>=.010 for v in ms],5,2)
    mc=[(a+b)/2 for a,b in mruns]; mg=[mc[i]-mc[i-1] for i in range(1,len(mc))]; mmed=statistics.median(mg) if mg else None
    margin_repeat=8<=len(mruns)<=35 and mmed is not None and 25<=mmed<=180
    return {"runId":"f113r-image-A2","frozen":True,"decoder":{"blindCode":"A2","version":RUN_VERSION,"assumptions":["grayscale source image only","global Otsu threshold within each declared crop","horizontal organization appears as repeated row-projection bands","left-margin repetition appears as separated row-projection bands in the declared margin crop"]},"source":{"fixtureId":FIXTURE_ID,"sha256":EXPECTED_SHA256},"preprocessing":{"representation":"LANCZOS grayscale resize","width":tw,"centralCrop":[.18,.05,.94,.95],"marginCrop":[.03,.05,.18,.95]},"measurements":{"centralOtsu":t,"centralBandCount":len(bands),"centralMedianGapPx":med,"centralGapCv":gapcv,"marginOtsu":mt,"marginBandCount":len(mruns),"marginMedianGapPx":mmed},"claims":[claim("horizontal-repetition","full-folio-layout","present" if horizontal else "not_detected","A2:central-row-projection"),claim("left-margin-discrete-repetition","left-margin-layout","present" if margin_repeat else "not_detected","A2:margin-row-projection")]}

def autocorr(series,lag):
    n=len(series)-lag
    if n<=4: return 0.0
    a=series[:n]; b=series[lag:]; ma=statistics.mean(a); mb=statistics.mean(b)
    va=sum((x-ma)**2 for x in a); vb=sum((x-mb)**2 for x in b)
    if va==0 or vb==0: return 0.0
    return sum((a[i]-ma)*(b[i]-mb) for i in range(n))/math.sqrt(va*vb)

def gradient_series(crop,step):
    px=crop.load(); w,h=crop.size; xs=list(range(0,w,step)); out=[0.0]
    for y in range(1,h): out.append(sum(abs(px[x,y]-px[x,y-1]) for x in xs)/len(xs)/255.0)
    return out

def best_autocorr(series,lo,hi):
    vals=[(autocorr(series,lag),lag) for lag in range(lo,min(hi,len(series)-5)+1)]
    return max(vals) if vals else (0.0,None)

def decoder_b5(gray):
    tw=900; th=round(gray.height*tw/gray.width); im=gray.resize((tw,th),Image.Resampling.BILINEAR); y0,y1=round(.05*th),round(.95*th)
    central=im.crop((round(.18*tw),y0,round(.94*tw),y1)); ccorr,clag=best_autocorr(moving_average(gradient_series(central,2),2),8,80)
    margin=im.crop((round(.03*tw),y0,round(.18*tw),y1)); mcorr,mlag=best_autocorr(moving_average(gradient_series(margin,1),2),20,150)
    horizontal=ccorr>=.10; margin_repeat=mcorr>=.08 and mlag is not None
    return {"runId":"f113r-image-B5","frozen":True,"decoder":{"blindCode":"B5","version":RUN_VERSION,"assumptions":["grayscale source image only","no binarization","repeated organization appears as autocorrelation in vertical-gradient energy","central and left-margin regions are evaluated separately"]},"source":{"fixtureId":FIXTURE_ID,"sha256":EXPECTED_SHA256},"preprocessing":{"representation":"BILINEAR grayscale resize plus vertical-gradient energy","width":tw,"centralCrop":[.18,.05,.94,.95],"marginCrop":[.03,.05,.18,.95]},"measurements":{"centralBestAutocorrelation":ccorr,"centralBestLagPx":clag,"marginBestAutocorrelation":mcorr,"marginBestLagPx":mlag},"claims":[claim("horizontal-repetition","full-folio-layout","present" if horizontal else "not_detected","B5:central-gradient-autocorrelation"),claim("left-margin-discrete-repetition","left-margin-layout","present" if margin_repeat else "not_detected","B5:margin-gradient-autocorrelation")]}

def components(binary):
    px=binary.load(); w,h=binary.size; seen=bytearray(w*h); out=[]; neigh=[(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]
    for y in range(h):
        for x in range(w):
            idx=y*w+x
            if seen[idx] or px[x,y]==0: continue
            seen[idx]=1; q=deque([(x,y)]); area=0; minx=maxx=x; miny=maxy=y
            while q:
                cx,cy=q.popleft(); area+=1; minx=min(minx,cx); maxx=max(maxx,cx); miny=min(miny,cy); maxy=max(maxy,cy)
                for dx,dy in neigh:
                    nx,ny=cx+dx,cy+dy
                    if 0<=nx<w and 0<=ny<h:
                        ni=ny*w+nx
                        if not seen[ni] and px[nx,ny]!=0: seen[ni]=1; q.append((nx,ny))
            out.append({"area":area,"cx":(minx+maxx)/2,"cy":(miny+maxy)/2,"width":maxx-minx+1,"height":maxy-miny+1})
    return out

def decoder_c8(gray):
    tw=360; th=round(gray.height*tw/gray.width); im=gray.resize((tw,th),Image.Resampling.BOX)
    inner=im.crop((round(.02*tw),round(.04*th),round(.96*tw),round(.96*th))); t=otsu(inner); binary=inner.point(lambda p:255 if p<t else 0); comps=components(binary)
    cx0=(.18-.02)/(.96-.02)*inner.width; cx1=(.94-.02)/(.96-.02)*inner.width
    central=[c for c in comps if cx0<=c["cx"]<=cx1 and 2<=c["area"]<=250]; bins=72; counts=[0]*bins
    for c in central: counts[min(bins-1,max(0,int(c["cy"]/inner.height*bins)))]+=1
    active=[i for i,n in enumerate(counts) if n>=4]; horizontal=len(active)>=20
    mx1=(.18-.02)/(.96-.02)*inner.width
    margin=[c for c in comps if c["cx"]<=mx1 and 4<=c["area"]<=220 and 2<=c["width"]<=30 and 2<=c["height"]<=45]
    loci=[]
    for cy in sorted(c["cy"] for c in margin):
        if not loci or cy-loci[-1]>5: loci.append(cy)
        else: loci[-1]=(loci[-1]+cy)/2
    lg=[loci[i]-loci[i-1] for i in range(1,len(loci))]; lmed=statistics.median(lg) if lg else None
    margin_repeat=8<=len(loci)<=35 and lmed is not None and 5<=lmed<=45
    return {"runId":"f113r-image-C8","frozen":True,"decoder":{"blindCode":"C8","version":RUN_VERSION,"assumptions":["grayscale source image only","BOX downsampling followed by Otsu binarization","horizontal organization is inferred from connected-component centroid occupancy across vertical bins","left-margin repetition is inferred from repeated component loci under fixed geometry bounds"]},"source":{"fixtureId":FIXTURE_ID,"sha256":EXPECTED_SHA256},"preprocessing":{"representation":"BOX grayscale resize plus connected-component geometry","width":tw,"innerCrop":[.02,.04,.96,.96],"verticalBins":bins},"measurements":{"otsu":t,"componentCount":len(comps),"centralCandidateComponents":len(central),"activeVerticalBins":len(active),"marginCandidateComponents":len(margin),"marginCollapsedLoci":len(loci),"marginMedianGapPx":lmed},"claims":[claim("horizontal-repetition","full-folio-layout","present" if horizontal else "not_detected","C8:component-centroid-occupancy"),claim("left-margin-discrete-repetition","left-margin-layout","present" if margin_repeat else "not_detected","C8:margin-component-geometry")]}

def main():
    if len(sys.argv)!=3: raise SystemExit("usage: image_only_f113r.py IMAGE OUTPUT_DIR")
    image_path,outdir=sys.argv[1:3]; digest=sha256_file(image_path)
    if digest!=EXPECTED_SHA256: raise SystemExit(f"source hash mismatch: {digest}")
    os.makedirs(outdir,exist_ok=True)
    with Image.open(image_path) as src:
        if src.format!="JPEG": raise SystemExit(f"expected JPEG, got {src.format}")
        gray=src.convert("L"); all_runs=[decoder_a2(gray),decoder_b5(gray),decoder_c8(gray)]
    for r in all_runs:
        with open(os.path.join(outdir,r["decoder"]["blindCode"]+".json"),"w",encoding="utf-8") as f: json.dump(r,f,indent=2,sort_keys=True)
    with open(os.path.join(outdir,"run-set.json"),"w",encoding="utf-8") as f: json.dump({"fixtureId":FIXTURE_ID,"sourceSha256":EXPECTED_SHA256,"runVersion":RUN_VERSION,"blindCodes":[r["decoder"]["blindCode"] for r in all_runs],"boundary":"Image-only structural observations. No transcription, language model, semantic key, translation, or decipherment hypothesis is available to these decoders."},f,indent=2,sort_keys=True)
    print(json.dumps({"runs":[{"code":r["decoder"]["blindCode"],"measurements":r["measurements"],"claims":r["claims"]} for r in all_runs]},indent=2,sort_keys=True))

if __name__=="__main__": main()
