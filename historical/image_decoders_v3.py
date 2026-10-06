#!/usr/bin/env python3
import statistics
from PIL import ImageFilter
import image_decoders_v2 as V2

RUN_VERSION = "image-only-003.0-dev"


def retag(run):
    run["decoder"]["version"] = RUN_VERSION
    return run


def decoder_a3(gray, fixture_id="synthetic", source_sha256=None):
    return retag(V2.decoder_a3(gray, fixture_id, source_sha256))


def decoder_b7(gray, fixture_id="synthetic", source_sha256=None):
    tw=900
    th=round(gray.height*tw/gray.width)
    im=gray.resize((tw,th),V2.Image.Resampling.BILINEAR)
    y0,y1=round(.05*th),round(.95*th)

    central=im.crop((round(.18*tw),y0,round(.94*tw),y1)).filter(ImageFilter.GaussianBlur(2.5))
    cs=V2.gradient_series(central,2)
    ccorr,clag=V2.best_autocorr(V2.moving_average(cs,2),8,80)
    cmean=statistics.mean(cs)
    central_lag_fraction=(clag/central.height) if clag is not None else None

    margin_crop=im.crop((round(.03*tw),y0,round(.18*tw),y1)).filter(ImageFilter.GaussianBlur(2.5))
    ms=V2.gradient_series(margin_crop,1)
    # Search a broad range, then evaluate periodic scale relative to crop height rather than an absolute pixel ceiling.
    max_margin_lag=max(30,min(round(.20*margin_crop.height),margin_crop.height-6))
    mcorr,mlag=V2.best_autocorr(V2.moving_average(ms,2),20,max_margin_lag)
    concentration=V2.top_fraction_concentration(V2.column_gradient_energy(margin_crop),.2)
    margin_lag_fraction=(mlag/margin_crop.height) if mlag is not None else None

    horizontal=(
        ccorr >= .45 and cmean >= .007 and
        central_lag_fraction is not None and central_lag_fraction >= .009
    )
    margin=(
        mcorr >= .35 and concentration >= .70 and
        margin_lag_fraction is not None and .020 <= margin_lag_fraction <= .180
    )

    measurements={
        "centralBestAutocorrelation":ccorr,
        "centralBestLagPx":clag,
        "centralLagFraction":central_lag_fraction,
        "centralMeanBlurredGradient":cmean,
        "marginBestAutocorrelation":mcorr,
        "marginBestLagPx":mlag,
        "marginLagFraction":margin_lag_fraction,
        "marginTop20ColumnEnergyFraction":concentration
    }
    return {
        "runId":f"{fixture_id}-B7",
        "frozen":False,
        "decoder":{
            "blindCode":"B7",
            "version":RUN_VERSION,
            "assumptions":[
                "grayscale image only",
                "macro vertical-gradient periodicity must survive Gaussian smoothing",
                "central repetition requires nontrivial blurred-gradient amplitude and non-boundary relative lag",
                "margin repetition requires horizontal concentration and a periodic scale expressed relative to crop height rather than a fixed absolute upper pixel bound"
            ]
        },
        "source":{"fixtureId":fixture_id,"sha256":source_sha256},
        "measurements":measurements,
        "claims":[
            V2.claim("horizontal-repetition","full-folio-layout","present" if horizontal else "not_detected","B7:relative-scale-blurred-gradient-periodicity"),
            V2.claim("left-margin-discrete-repetition","left-margin-layout","present" if margin else "not_detected","B7:relative-scale-periodicity-plus-column-concentration")
        ]
    }


def decoder_c9(gray, fixture_id="synthetic", source_sha256=None):
    return retag(V2.decoder_c9(gray, fixture_id, source_sha256))


def run_all(gray, fixture_id="synthetic", source_sha256=None):
    return [decoder_a3(gray,fixture_id,source_sha256),decoder_b7(gray,fixture_id,source_sha256),decoder_c9(gray,fixture_id,source_sha256)]


def claims_map(run):
    return {c["claimKey"]:c["proposition"] for c in run["claims"]}
