#!/usr/bin/env python3
import json, math, statistics
from collections import deque
from PIL import Image, ImageFilter

RUN_VERSION = "image-only-002.0-dev"


def otsu(img):
    hist=img.histogram()[:256]; total=sum(hist); total_sum=sum(i*n for i,n in enumerate(hist))
    wb=0; sb=0.0; best=-1.0; threshold=128
    for t in range(256):
        wb += hist[t]
        if wb == 0: continue
        wf=total-wb
        if wf == 0: break
        sb += t*hist[t]
        mb=sb/wb; mf=(total_sum-sb)/wf
        score=wb*wf*(mb-mf)**2
        if score > best: best=score; threshold=t
    return threshold


def moving_average(xs, radius):
    prefix=[0.0]
    for x in xs: prefix.append(prefix[-1]+x)
    out=[]; n=len(xs)
    for i in range(n):
        lo=max(0,i-radius); hi=min(n,i+radius+1)
        out.append((prefix[hi]-prefix[lo])/(hi-lo))
    return out


def runs(mask, merge_gap=0, min_len=1):
    found=[]; start=None
    for i,active in enumerate(mask):
        if active and start is None: start=i
        elif not active and start is not None: found.append([start,i-1]); start=None
    if start is not None: found.append([start,len(mask)-1])
    if merge_gap and found:
        merged=[found[0]]
        for a,b in found[1:]:
            if a-merged[-1][1]-1 <= merge_gap: merged[-1][1]=b
            else: merged.append([a,b])
        found=merged
    return [r for r in found if r[1]-r[0]+1 >= min_len]


def cv(xs):
    if not xs: return None
    mean=statistics.mean(xs)
    return None if mean == 0 else statistics.pstdev(xs)/mean


def claim(key, target, value, locator):
    return {"claimKey":key,"target":target,"proposition":value,"evidence":[{"layer":"SOURCE_IMAGE","locator":locator}]}


def row_longrun_score(crop, threshold, min_run=7):
    px=crop.load(); w,h=crop.size; out=[]
    for y in range(h):
        dark=0; x=0
        while x < w:
            if px[x,y] < threshold:
                start=x
                while x < w and px[x,y] < threshold: x += 1
                if x-start >= min_run: dark += x-start
            x += 1
        out.append(dark/w)
    return out


def decoder_a3(gray, fixture_id="synthetic", source_sha256=None):
    tw=1200; th=round(gray.height*tw/gray.width); im=gray.resize((tw,th),Image.Resampling.LANCZOS)
    y0,y1=round(.05*th),round(.95*th)
    values={}
    for name,x0,x1 in (("central",.18,.94),("margin",.03,.18)):
        crop=im.crop((round(x0*tw),y0,round(x1*tw),y1)); threshold=otsu(crop)
        series=moving_average(row_longrun_score(crop,threshold,7),2)
        bands=runs([v >= .006 for v in series],3,2)
        centers=[(a+b)/2 for a,b in bands]
        gaps=[centers[i]-centers[i-1] for i in range(1,len(centers))]
        values[name]={"otsu":threshold,"bandCount":len(bands),"medianGapPx":statistics.median(gaps) if gaps else None,"gapCv":cv(gaps)}
    c=values["central"]; m=values["margin"]
    horizontal=20 <= c["bandCount"] <= 60 and c["medianGapPx"] is not None and 8 <= c["medianGapPx"] <= 50 and c["gapCv"] is not None and c["gapCv"] <= .45
    margin=8 <= m["bandCount"] <= 24 and m["medianGapPx"] is not None and 35 <= m["medianGapPx"] <= 120 and m["gapCv"] is not None and m["gapCv"] <= .45
    return record("A3",fixture_id,source_sha256,values,[
        claim("horizontal-repetition","full-folio-layout","present" if horizontal else "not_detected","A3:macro-horizontal-run-bands"),
        claim("left-margin-discrete-repetition","left-margin-layout","present" if margin else "not_detected","A3:macro-margin-run-bands")
    ],["grayscale image only","long horizontal dark runs define macro ink","regular macro bands are required; fine periodic texture is excluded by minimum horizontal run length"])


def autocorr(series, lag):
    n=len(series)-lag
    if n <= 4: return 0.0
    a=series[:n]; b=series[lag:]; ma=statistics.mean(a); mb=statistics.mean(b)
    va=sum((x-ma)**2 for x in a); vb=sum((x-mb)**2 for x in b)
    if va == 0 or vb == 0: return 0.0
    return sum((a[i]-ma)*(b[i]-mb) for i in range(n))/math.sqrt(va*vb)


def gradient_series(crop, step):
    px=crop.load(); w,h=crop.size; xs=list(range(0,w,step)); out=[0.0]
    for y in range(1,h): out.append(sum(abs(px[x,y]-px[x,y-1]) for x in xs)/len(xs)/255.0)
    return out


def best_autocorr(series, lo, hi):
    vals=[(autocorr(series,lag),lag) for lag in range(lo,min(hi,len(series)-5)+1)]
    return max(vals) if vals else (0.0,None)


def column_gradient_energy(crop):
    px=crop.load(); w,h=crop.size; out=[]
    for x in range(w): out.append(sum(abs(px[x,y]-px[x,y-1]) for y in range(1,h)))
    return out


def top_fraction_concentration(values, fraction=.2):
    total=sum(values)
    if total == 0: return 0.0
    k=max(1,int(len(values)*fraction))
    return sum(sorted(values,reverse=True)[:k])/total


def decoder_b6(gray, fixture_id="synthetic", source_sha256=None):
    tw=900; th=round(gray.height*tw/gray.width); im=gray.resize((tw,th),Image.Resampling.BILINEAR); y0,y1=round(.05*th),round(.95*th)
    central=im.crop((round(.18*tw),y0,round(.94*tw),y1)).filter(ImageFilter.GaussianBlur(2.5))
    cs=gradient_series(central,2); ccorr,clag=best_autocorr(moving_average(cs,2),8,80); cmean=statistics.mean(cs)
    margin_crop=im.crop((round(.03*tw),y0,round(.18*tw),y1)).filter(ImageFilter.GaussianBlur(2.5))
    ms=gradient_series(margin_crop,1); mcorr,mlag=best_autocorr(moving_average(ms,2),20,150); concentration=top_fraction_concentration(column_gradient_energy(margin_crop),.2)
    horizontal=ccorr >= .45 and cmean >= .007 and clag is not None and clag >= 11
    margin=mcorr >= .35 and mlag is not None and 30 <= mlag <= 120 and concentration >= .70
    measurements={"centralBestAutocorrelation":ccorr,"centralBestLagPx":clag,"centralMeanBlurredGradient":cmean,"marginBestAutocorrelation":mcorr,"marginBestLagPx":mlag,"marginTop20ColumnEnergyFraction":concentration}
    return record("B6",fixture_id,source_sha256,measurements,[
        claim("horizontal-repetition","full-folio-layout","present" if horizontal else "not_detected","B6:blurred-gradient-periodicity"),
        claim("left-margin-discrete-repetition","left-margin-layout","present" if margin else "not_detected","B6:periodicity-plus-column-concentration")
    ],["grayscale image only","macro vertical-gradient periodicity must survive Gaussian smoothing","central repetition requires nontrivial blurred-gradient amplitude and non-boundary lag","margin repetition must also be horizontally concentrated rather than distributed texture"])


def components(binary):
    px=binary.load(); w,h=binary.size; seen=bytearray(w*h); out=[]; neigh=[(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]
    for y in range(h):
        for x in range(w):
            idx=y*w+x
            if seen[idx] or px[x,y] == 0: continue
            seen[idx]=1; q=deque([(x,y)]); area=0; minx=maxx=x; miny=maxy=y
            while q:
                cx,cy=q.popleft(); area += 1; minx=min(minx,cx); maxx=max(maxx,cx); miny=min(miny,cy); maxy=max(maxy,cy)
                for dx,dy in neigh:
                    nx,ny=cx+dx,cy+dy
                    if 0 <= nx < w and 0 <= ny < h:
                        ni=ny*w+nx
                        if not seen[ni] and px[nx,ny] != 0: seen[ni]=1; q.append((nx,ny))
            out.append({"area":area,"cx":(minx+maxx)/2,"cy":(miny+maxy)/2,"width":maxx-minx+1,"height":maxy-miny+1})
    return out


def cluster(values, max_gap):
    groups=[]
    for value in sorted(values):
        if not groups or value-groups[-1][-1] > max_gap: groups.append([value])
        else: groups[-1].append(value)
    return groups


def decoder_c9(gray, fixture_id="synthetic", source_sha256=None):
    tw=360; th=round(gray.height*tw/gray.width); im=gray.resize((tw,th),Image.Resampling.BOX)
    inner=im.crop((round(.02*tw),round(.04*th),round(.96*tw),round(.96*th))); threshold=otsu(inner)
    comps=components(inner.point(lambda p:255 if p < threshold else 0))
    cx0=(.18-.02)/(.96-.02)*inner.width; cx1=(.94-.02)/(.96-.02)*inner.width
    central=[c for c in comps if cx0 <= c["cx"] <= cx1 and 6 <= c["area"] <= 250 and c["width"] >= 3 and c["height"] >= 2]
    row_groups=cluster([c["cy"] for c in central],3); row_centers=[statistics.mean(g) for g in row_groups if len(g) >= 5]
    row_gaps=[row_centers[i]-row_centers[i-1] for i in range(1,len(row_centers))]
    mx1=(.18-.02)/(.96-.02)*inner.width
    margin_components=[c for c in comps if c["cx"] <= mx1 and 6 <= c["area"] <= 220 and c["width"] >= 3 and 2 <= c["height"] <= 45]
    margin_groups=cluster([c["cy"] for c in margin_components],5); margin_centers=[statistics.mean(g) for g in margin_groups]
    margin_gaps=[margin_centers[i]-margin_centers[i-1] for i in range(1,len(margin_centers))]
    row_med=statistics.median(row_gaps) if row_gaps else None; row_cv=cv(row_gaps); margin_med=statistics.median(margin_gaps) if margin_gaps else None; margin_cv=cv(margin_gaps)
    horizontal=20 <= len(row_centers) <= 60 and row_med is not None and 5 <= row_med <= 18 and row_cv is not None and row_cv <= .45
    margin=8 <= len(margin_centers) <= 24 and margin_med is not None and 15 <= margin_med <= 40 and margin_cv is not None and margin_cv <= .45
    measurements={"otsu":threshold,"componentCount":len(comps),"macroCentralComponents":len(central),"macroRowLoci":len(row_centers),"macroRowMedianGapPx":row_med,"macroRowGapCv":row_cv,"macroMarginComponents":len(margin_components),"macroMarginLoci":len(margin_centers),"macroMarginMedianGapPx":margin_med,"macroMarginGapCv":margin_cv}
    return record("C9",fixture_id,source_sha256,measurements,[
        claim("horizontal-repetition","full-folio-layout","present" if horizontal else "not_detected","C9:macro-component-row-clustering"),
        claim("left-margin-discrete-repetition","left-margin-layout","present" if margin else "not_detected","C9:macro-margin-component-loci")
    ],["grayscale image only","BOX downsampling and Otsu binarization","only macro connected components contribute","horizontal organization requires repeated multi-component row loci; margin organization requires repeated macro-component loci"])


def record(code, fixture_id, source_sha256, measurements, claims, assumptions):
    return {"runId":f"{fixture_id}-{code}","frozen":False,"decoder":{"blindCode":code,"version":RUN_VERSION,"assumptions":assumptions},"source":{"fixtureId":fixture_id,"sha256":source_sha256},"measurements":measurements,"claims":claims}


def run_all(gray, fixture_id="synthetic", source_sha256=None):
    return [decoder_a3(gray,fixture_id,source_sha256),decoder_b6(gray,fixture_id,source_sha256),decoder_c9(gray,fixture_id,source_sha256)]


def claims_map(run):
    return {c["claimKey"]:c["proposition"] for c in run["claims"]}
