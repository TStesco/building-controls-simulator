# created by Tom Stesco tom.s@ecobee.com

import logging

import pytest
import os

from BuildingControlsSimulator.DataClients.WeatherChannel import WeatherChannel


logger = logging.getLogger(__name__)


class TestWeatherChannel:
    @classmethod
    def setup_class(cls):
        # initialize with data to avoid pulling multiple times

        cls.weather = WeatherChannel(
            data=[],
            spec=[],
            nrel_dev_api_key=os.environ.get("NREL_DEV_API_KEY"),
            nrel_dev_email=os.environ.get("NREL_DEV_EMAIL"),
            archive_tmy3_dir=os.environ.get("ARCHIVE_TMY3_DIR"),
            archive_tmy3_meta=os.environ.get("ARCHIVE_TMY3_META"),
            archive_tmy3_data_dir=os.environ.get("ARCHIVE_TMY3_DATA_DIR"),
            ep_tmy3_cache_dir=os.environ.get("EP_TMY3_CACHE_DIR"),
            simulation_epw_dir=os.environ.get("SIMULATION_EPW_DIR"),
        )

    @classmethod
    def teardown_class(cls):
        """teardown any state that was previously setup with a call to
        setup_class.
        """
        pass

    def test_get_epw_tmy3(self):
        """
        test that preprocessing produces output file
        """
        lat = 33.481136
        lon = -112.078232
        test_fname = "USA_AZ_Phoenix-Sky.Harbor.Intl.AP.722780_TMY.epw"
        test_fpath = os.path.join(self.weather.ep_tmy3_cache_dir, test_fname)

        # remove test file if previously existing
        if os.path.exists(test_fpath):
            os.remove(test_fpath)
        fpath, fname = self.weather.get_tmy_fill_epw(lat, lon)
        assert os.path.exists(fpath)

        # epw file can be read and has correct columns
        data, meta, meta_epw_lines = self.weather.read_epw(fpath)
        cols = data.columns.to_list()

        assert cols == self.weather.epw_columns

    def test_get_nsrdb(self):
        """
        test that we can pull nsrdb data
        """
        df_solar = self.weather.get_nsrdb(47.650447, -117.464061, 2019)
        breakpoint()
        assert df_solar.shape == (17520, 5)
        assert df_solar.at[17515,'dni'] == 18.0
        assert df_solar.at[17519,'ghi'] == 4.0
