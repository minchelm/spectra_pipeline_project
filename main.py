from pipeline_spectra import pipeline_spectra
from pipeline_plotting import pipeline_plotting


df_crism, df_ratio = pipeline_spectra(
    "CRISM_spectra.csv",
    normalize=True,
    restrict=[1, 2.6],
    continuum=True,
    ratio=10,
)
df_lab = pipeline_spectra(
    "lab_spectra.csv",
    normalize=True,
    restrict=[1, 2.6],
    interpolate=df_crism["Wavelength"],
    continuum=True,
)
pipeline_plotting(df_lab, df_crism, df_ratio)
