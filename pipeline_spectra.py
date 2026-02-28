import pandas as pd
import numpy as np
from scipy.spatial import ConvexHull, savgol_filter


def pipeline_spectra(
    csv,
    normalize=False,
    restrict=False,
    interpolate=False,
    continuum=False,
    ratio=False,
):
    """
    This function is a pipeline that converts a .csv file containing wavelength
    vs. reflectance to a dataframe ready to be plotted to compare to other
    spectra.
    It has five modular steps that are applicable to spectral analysis.
    - normalize_spectra: normalizes each column of spectra by dividing by
        the max value in each.
    - restrict_spectra: modifies the starting and ending wavelength range
    - interpolate_spectra: normalizes the amount of points in each spectra.
        particularly useful when resolution of samples are extremely different.
    - remove_continuum_spectra: removes the background trend of reflectance for
        ease of comparing
    - ratio_spectra: after being given a spectra, divides the rest of the
    spectra. Useful for removing common general effects like an atmosphere.
    """
    df = pd.read_csv(csv)
    if normalize:
        df = normalize_spectra(df)
    if restrict:
        df = restrict_spectra(df, restrict[0], restrict[1])
    if interpolate is not False:
        df = interpolate_spectra(df, interpolate)
    if continuum:
        df = remove_continuum_spectra(df)
    if ratio:
        df_ratio = ratio_spectra(df, ratio)
        return df, df_ratio
    return df


def restrict_spectra(df, start, stop):
    # cuts DataFrame by start/stop, also resets index.
    return df[
        (df["Wavelength"] >= start) & (df["Wavelength"] <= stop)
    ].reset_index(drop=True)


def normalize_spectra(df):
    # iterates through spectra, divides by max value in column
    for column in df.columns:
        if column != "Wavelength":
            df[column] = df[column].div(max(df[column]), axis=0)
    return df


def interpolate_spectra(df, interpolate):
    # iterates through spectra, interpolates initial spectras
    # by secondary spectra.
    df_interpolated = pd.DataFrame()
    df_interpolated["Wavelength"] = interpolate
    for column in df.columns:
        if column != "Wavelength":
            df_interpolated[column] = np.interp(
                interpolate, df["Wavelength"], df[column]
            )
    return df_interpolated


def ratio_spectra(df, ratio):
    # same as normalize_spectra, except not max value. mean spectra.
    df_ratio = df.copy()
    for column in df_ratio:
        if column != "Wavelength":
            df_ratio[column] = df_ratio[column].div(df[str(ratio)], axis=0)
    return df_ratio


def remove_continuum_spectra(df):
    # converts wavelength and spectra in df to 2D points. finds the vertices of
    # the convext hull ( upper envelope of reflectance), divides all values by
    # that to remove the continuum. also applies savgol filter.
    x = df["Wavelength"].values
    for column in df.columns:
        if column != "Wavelength":
            y = df[column].values
            y = savgol_filter(y, window_length=11, polyorder=3)
            points = np.column_stack((x, y))
            hull = ConvexHull(points)
            hull_points = points[hull.vertices]
            hull_points = hull_points[np.argsort(hull_points[:, 0])]
            continuum = np.interp(x, hull_points[:, 0], hull_points[:, 1])
            df[column] = y / continuum
    return df
