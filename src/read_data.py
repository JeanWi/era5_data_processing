import xarray as xr
import pandas as pd
import numpy as np
from metpy.calc import relative_humidity_from_dewpoint, wind_speed
from metpy.units import units
import pvlib


def roundPartial (value: float, resolution: float) -> float:
    """
    Rounds number to decimals

    Rounds to grid level of JRC dataset

    :param float value: value to round
    :param float resolution: resolution of rounding
    :return float rounded value: result value
    """
    return round (value / resolution) * resolution

def calculate_dni(data: pd.DataFrame, lon: float, lat: float) -> pd.Series:
    """
    Calculate direct normal irradiance from ghi and dhi. The function assumes that
    the ghi and dhi are given as an average value for the timestep and dni is
    calculated using the position of the sun in the middle of the timestep.

    :param pd.DataFrame data: climate data with columns ghi and dhi
    :param float lon: longitude
    :param float lat: latitude
    :return data: climate data including dni
    :rtype: pd.Series
    """
    timesteps = pd.to_datetime(data.index)
    timestep_length = pd.to_datetime(data.index[1]) - pd.to_datetime(data.index[0])
    timesteps = timesteps + (timestep_length / 2)

    zenith = pvlib.solarposition.get_solarposition(timesteps, lat, lon)
    data["dni"] = pvlib.irradiance.dni(
        data["ghi"].to_numpy(), data["dhi"].to_numpy(), zenith["zenith"].to_numpy()
    )
    data["dni"] = data["dni"].fillna(0)
    data["dni"] = data["dni"].where(data["dni"] > 0, 0)

    return data["dni"]


def convert_era5_data(filename: str, lon: float, lat: float) -> dict:
    """
    Converts era5 data to from nc file to AdOpT-NET0 compatible dataframe

    :param year:
    :param lon:
    :param lat:
    :return: Dict with longitude, latitude, dataframe
    :rtype dict
    """

    lat = roundPartial(lat, 0.25)
    lon = roundPartial(lon, 0.25)
    ds = xr.open_dataset(filename)

    time_index = ds.time.to_pandas()
    temp_air = ds.t2m.sel(longitude=lon, latitude=lat).to_numpy() - 273.15
    rh = np.array(relative_humidity_from_dewpoint(temp_air * units.celsius,
                                                  ds.d2m.sel(longitude=lon, latitude=lat).to_numpy() * units.kelvin).to(
        'percent'))
    ws = {}
    # u10 = ds.u10.sel(longitude=lon, latitude=lat).to_numpy()
    # v10 = ds.v10.sel(longitude=lon, latitude=lat).to_numpy()
    # ws['10'] = wind_speed(u10 * units.m / units.s, v10 * units.m / units.s)
    u100 = ds.u100.sel(longitude=lon, latitude=lat).to_numpy()
    v100 = ds.v100.sel(longitude=lon, latitude=lat).to_numpy()
    ws['100'] = wind_speed(u100 * units.m / units.s, v100 * units.m / units.s)
    ghi = ds.ssrd.sel(longitude=lon, latitude=lat).to_numpy() / 3600
    dhi = (ds.ssrd.sel(longitude=lon, latitude=lat).to_numpy() / 3600) - \
          (ds.fdir.sel(longitude=lon, latitude=lat).to_numpy() / 3600)
    answer = {}
    answer['longitude'] = lon
    answer['latitude'] = lat
    answer['altitude'] = 0
    answer['dataframe'] = pd.DataFrame(
        np.array([
            ghi,
            dhi,
            temp_air,
            rh
        ]).T,
        columns=['ghi', 'dhi', 'temp_air', 'rh'],
        index=time_index)

    answer['dataframe']["dni"] = calculate_dni(answer['dataframe'], lon, lat)

    for height in ws:
        answer['dataframe']['ws' + str(height)] = ws[height]

    answer['dataframe'] = answer['dataframe'].round(4)

    return answer