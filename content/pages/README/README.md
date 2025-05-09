title: README
Slug: readme
pageorder: 3

 
#TESS Transients

This webpage hosts TESS light curve data for transients reported to
the Transient Name Server ([wis-tns.org](https://www.wis-tns.org/))
that were also observed in TESS full frame images.

As of September 2022, TESS full frame images (FFIs) are released every
seven days as a High Level Science Product
([TICA](https://archive.stsci.edu/hlsp/tica)) on the
[MAST](https://archive.stsci.edu/). To capitalize on the rapid
release of data, we are extracting light curves for transients
reproted to TNS every 7 days and posting reduced data products here.

Only transients discovered in the TESS field of view while TESS was
observing are presented. We plan to add prediscovery light curves in
the future.  A subset of confirmed supernovae per sector is also
available.

##How to get the data

Light curves are organized by sector. For a given sector, you can see
all the light curves by navigating to that sector's webpage.

Above each figure is a link to a text file with the light curve data.

To find a specific transient, you need to know which sector it was
observed in. You can use a tool like
[tess-point](https://github.com/christopherburke/tess-point) to find
which sector a given transient was observed in based on its RA and Dec.

There is also an API to download individual light curves, for example
`wget
https://tess.mit.edu/public/tesstransients/light_curves/lc_2022sfe_cleaned
`. In
this case, you only need to know the IAU designation of the transient
(replace "2022sfe" with the IAU designation). A GET request returns
the data as a string.

For bulk downloads, you may prefer to visit [the bulk
downloads page]({filename}../lc_bulk/lc_bulk.md). However, the data
are also under version contol through [this github
repo](https://github.com/mmfausnaugh/lc_bulk), which you can use to
access older versions of the data and/or keep local copies synced with
the most up-to-date version.

##Light Curve Files

Light curves are saved as text files, with 10 columns and two header
lines. The header lines start with the `#` character.

###Header

- The first line is labeld "reference_flux:" and gives the
flux calibration offset measured from the reference image in units of
counts per second (see [Flux Calibration](#flux-calibration)
below). This number can be subtracted from the `cts_per_s` column to
get the original differential light curve.

- The second line gives
the labels for the columns. Many libraries can use this line to put
names/labels/tags on the data structure. For example, with `numpy` you
can do `d = np.genfromtext('lc_2022sfe_cleaned',skip_header=1,
names=True)` and you will be able to access the timestamps and flux
light curve with `d['BTJD']`, `d['cts_per_s']`, etc. (The
`skip_header=1` is necessary to ignore the reference_flux line.)

###Columns
|Label| Description|
|---|---|
|`BTJD`| Barycentric TESS Julian Date. Corrected for light travel time to solar system barycenter, based on TNS coordinates. TESS Julian date is JD - 2457000.|
|`TJD`|  TESS Julian date, equal to JD - 2457000. The barycenter correction is given by `BTJD - TJD`. The time system is TDB, but at the position of the TESS spacecraft (and therefore differs from geocentric TDB by a small light travel time).|
|`cts_per_s`| Flux light curve in counts per second (photoelectrons per second).|
|`e_cts_per_s`| Uncertainty in `cts_per_s` (1-sigma).|
|`mag`| Light curve in TESS magnitudes (see [Flux Calibration](#flux-calibration)).|
|`e_mag`| Uncertainty in `mag` (1-sigma). A value of `99.9` marks a 3-sigma upper limit.|
|`bkg`| Local background in differential counts.|
|`bkg_model`| Model of potential systematic errors from the background correction. In some cases, `cts_per_s - bkg_model` is a more reliable measurement of the transient light curve. See [Background Model](#background-model) for details.|
|`bkg2`| Residual background in the photometric aperture. These data points are used to derive `bkg_model` (see [Background Model](#background-model)), which allows the user to experiment with their own correction model.|
| `e_bkg2`| Uncertainty in `bkg2` (1-sigma).|


##Image Processing and Light Curves

We use image subtraction and forced PSF photometry to produce the
light curves. We are using a slightly customized version of the [ISIS
](http://www2.iap.fr/users/alard/package.html) software package.

For image subtraction, we build a reference image from 20 images with
low backgrounds. The reference image is essentially a clipped
median. Starting in 2022 September, the 20 images are from the first 7
days of a TESS observing sector, because this time period coresponds
to the first downlink of TESS data in each sector. Image subtraction
is performed every 7 days, and begins as soon as the FFIs are publicly
available at MAST.

We use the coordinates reported to TNS for forced photometry on each
transient. We fit models of the pixel-response function ([available on
MAST](https://archive.stsci.edu/missions/tess/models/prf_fitsfiles/))
to the differential flux of the transient in each subtracted
image. Uncertainties are estimated from photon statistics (source +
background) in the original calibrated image. There is evidence that
these uncertainties are underestimated by a factor of 1.2 to 2.0,
depending on the brightness of the source and the surroudning scene.

More details are in [Fausnaugh et
al. 2021](https://ui.adsabs.harvard.edu/abs/2021ApJ...908...51F/abstract)
and [Fausnaugh et al. 2023](https://ui.adsabs.harvard.edu/abs/2023ApJ...956..108F/abstract).

##Flux Calibration

To convert a differential flux light curve (delta-counts per second
from subtracted images) to a flux-calibrated light curve (magnitudes),
we estimate the flux of the source in the reference image. The flux in
the reference image is added as a fixed offset to the differential
light curve to obtain a flux light curve in units of counts per
second. This flux light curve is given in the `cts_per_s` column in the
light curve files. The reference image flux is given in the file
headers. To convert to magnitudes, we use the formula in the TESS
instrument handbook, `-2.5log10(cts_per_s) + 20.44`. The zeropoint has
an uncertainty of 0.05 mag.

The advantage of this approach is that the magnitude units are easy to
understand, and can be easily converted to physical units: (2416
Jy)\*10^(-0.4\*Tmag). This formula uses the Vega-mag zeropoint for
Cousins I-band, which the TESS photometric system is defined to match.

There are two major disadvantages with this approach.

First, absolute photometry in TESS images is very
uncertain. Uncertainty in the reference image flux is typically 20%,
and can be greater than 100% for faint sources at 18th magnitude and
fainter.

The main issue is that it is difficult to estimate the correct
background level due to the the large TESS pixels and high stellar
density. There is evidence that background corrections estimated by
traditional techniques tend to be overestimate, resulting in
underestimated source fluxes. For example, the TESS mission pipeline
applies an ad hoc correction for overestimated backgrounds (described
in section 4.2 of [this data release note
document](https://archive.stsci.edu/missions/tess/doc/tess_drn/tess_sector_27_drn38_v02.pdf)).
Crowding from nearby stars that contaminate the photometric aperture
also affects the flux calibration. We iteratively fit models of the
PSF to the reference image in the vicinity of the transient to help
mitigate crowding. However, this procedure is also highly uncertain
and contributes to the large uncertainty in the reference image flux.

The second disadvantage of our flux calibration procedure is that it
includes host galaxy flux in the light curve of extragalactic
transients. For example, bright supernova may appear to peak at 13th
or 14th TESS magnitude, but only because the integrated host galaxy
light dominates the flux in the reference image.

For these cases, users should identify the light curve baseline and
shift the light curve so that the baseline is forced to zero flux. We
have chosen not to do this because identifying a suitable baseline is
not always obvious, and may not be desirable for CVs, stellar flares,
or unusual variability from other sources.

Users can also recover the original differential light curve by
subtracting the `reference_flux` value in the light curve file
headers from the `cts_per_s` column.

Lastly, users can calibrate the TESS `cts_per_s` light curve to match
a light curve in physical units (such as from ASAS-SN, ATLAS, or ZTF)
by fitting for a shift and scale factor. The TESS filter spans 600 nm
to 1,000 nm, and so there may be non-negligble color terms when
comparing to light cures in other filters.


##Upper limits

When converting to magnitudes, we only use data points with
signal-to-noise ratio = `cts_per_s/e_cts_per_s > 3.0`. Points with a
signal-to-noise ratio below 3, including all negative fluxes, are
converted to magnitude upper limits with the formula
`-2.5log10(3*e_cts_per_s) + 20.44`. Negative fluxes are due to either
an overestimated background or statistical noise that fluctuates
below the background level. Upper limits are marked in the light curve
files by setting the magnitude uncertainty to `99.9`.

For low backgrounds, a typical 3-sigma limiting magnitude is about
19.6 in 30 minutes (secotrs 1--26), 19.0 in 10 minutes (sectors
27--55), and 18.4 in 200 seconds (sector 56 and later).

##Background Model

The main systematic error in these light curves are caused by
time-variable scattered light from the Earth and Moon when they are
above the TESS sunshade. In the worst cases, the sky background is
brighter than 14th TESS magnitude per pixel, while the early time
transient light curves are often fainter than 19–21st magnitude. When
the background is this high, the background corrections must have a
relative uncertainty less than 0.1% to isolate the transient signal. In
practice, we have found that strong glints with high-frequency spatial
features are the most difficult systematic error to remove.

We provide an estimate of residual background errors in the
photometric aperture in the `bkg_model` column of the light curve
files. Subtracting this columns from the `cts_per_s` light curve, in
some cases, can improve the light curve.  We show the background model
as a purple line in the figures for each light curve, and the
"background-model corrected" light curve (converted to magnitudes) in
the bottom panel of each figure.

To produce the `bkg_model` column, we filter the subtracted images to
remove point sources such as the transient and nearby variable
stars. We used a median filter with a width of 100 pixels, and we
applied the filter to the subtracted images first column-by-column and
then row-by-row. We then produced the "background model" light curve
by rerunning forced photometry on the filtered images at the position
of the transient. The results of the forced photometry, and its
uncertainty, are given in the `bkg2` and `e_bkg2` columns of the light
curve files. Finally, we take a running median of the `bkg2` column to
reduce the statistical noise to produce the `bkg_model` columns.

Further details are in [Fausnaugh et al. 2023](https://ui.adsabs.harvard.edu/abs/2023ApJ...956..108F/abstract).

