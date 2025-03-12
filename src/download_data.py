import cdsapi

def download_era5_climate_data(area: list, year: int, filename: str):
    """
    Downloads data from era5 api

    :param list area: in the format [lat1, lon1, lat2, lon2]
    :param year: Climate year to use
    :param filename: filename to save it as
    :return:
    """
    cds_client = cdsapi.Client()

    cds_client.retrieve(
        'reanalysis-era5-single-levels',
        {
            'product_type': 'reanalysis',
            'format': 'netcdf',
            'variable': [
                "100u",  # 100m_u-component_of_wind
                "100v",  # 100m_v-component_of_wind
                # "fsr",  # forecast_surface_roughness
                # "sp",  # surface_pressure
                "fdir",  # total_sky_direct_solar_radiation_at_surface
                "ssrd",  # surface_solar_radiation_downwards
                "2t",  # 2m_temperature
                "2d", # 2m_dewpoint_temperature
                # "10u",  # 10m_u-component_of_wind
                # "10v",  # 10m_v-component_of_wind
            ],
            'year': year,
            'month': [
                '01', '02', '03',
                '04', '05', '06',
                '07', '08', '09',
                '10', '11', '12',
            ],
            'day': [
                '01', '02', '03',
                '04', '05', '06',
                '07', '08', '09',
                '10', '11', '12',
                '13', '14', '15',
                '16', '17', '18',
                '19', '20', '21',
                '22', '23', '24',
                '25', '26', '27',
                '28', '29', '30',
                '31',
            ],
            'time': [
                '00:00', '01:00', '02:00',
                '03:00', '04:00', '05:00',
                '06:00', '07:00', '08:00',
                '09:00', '10:00', '11:00',
                '12:00', '13:00', '14:00',
                '15:00', '16:00', '17:00',
                '18:00', '19:00', '20:00',
                '21:00', '22:00', '23:00',
            ],
            'area': area,
        },
        filename)