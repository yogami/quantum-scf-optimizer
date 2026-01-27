import pandas as pd
from entsoe import EntsoePandasClient
import os
from ports.data_fetcher import DataFetcherPort

class EntsoeAdapter(DataFetcherPort):
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("ENTSOE_API_KEY")
        self.client = EntsoePandasClient(api_key=self.api_key) if self.api_key else None
        self.country_code = 'DE_LU' # Germany-Luxembourg Bidding Zone

    def fetch_installed_capacity(self, year=2025):
        if self.client:
            try:
                start = pd.Timestamp(f'{year}-01-01', tz='Europe/Brussels')
                end = pd.Timestamp(f'{year}-01-02', tz='Europe/Brussels')
                data = self.client.query_installed_generation_capacity(self.country_code, start=start, end=end)
                return data
            except Exception as e:
                print(f"⚠️ ENTSO-E API Fetch Failed: {e}. Falling back to Snapshot.")
        
        return {
            'Biomass': 9000,
            'Fossil Brown coal/Lignite': 18000,
            'Fossil Hard coal': 17000,
            'Fossil Gas': 32000,
            'Hydro Pumped Storage': 9400,
            'Hydro Water Reservoir': 1500,
            'Nuclear': 0,
            'Solar': 82000,
            'Wind Offshore': 9000,
            'Wind Onshore': 61000
        }

    def get_topology_nodes(self):
        capacity = self.fetch_installed_capacity()
        if isinstance(capacity, pd.DataFrame):
            cap_dict = capacity.iloc[0].to_dict()
        else:
            cap_dict = capacity

        nodes = [
            {"id": "50HZ_WIND_ONSHORE", "type": "GEN_WIND", "mw": cap_dict.get('Wind Onshore', 61000) * 0.40},
            {"id": "50HZ_WIND_OFFSHORE", "type": "GEN_WIND", "mw": cap_dict.get('Wind Offshore', 9000) * 0.60},
            {"id": "TENNET_WIND_OFFSHORE", "type": "GEN_WIND", "mw": cap_dict.get('Wind Offshore', 9000) * 0.40},
            {"id": "TENNET_SOLAR_BAVARIA", "type": "GEN_SOLAR", "mw": cap_dict.get('Solar', 82000) * 0.35},
            {"id": "AMPRION_GAS_FLEET", "type": "GEN_GAS", "mw": cap_dict.get('Fossil Gas', 32000) * 0.50},
            {"id": "TRANSNET_SOLAR_BW", "type": "GEN_SOLAR", "mw": cap_dict.get('Solar', 82000) * 0.15},
            {"id": "TRANSNET_PUMPED_HYDRO", "type": "STORAGE", "mw": cap_dict.get('Hydro Pumped Storage', 9400) * 0.40},
        ]
        return nodes
