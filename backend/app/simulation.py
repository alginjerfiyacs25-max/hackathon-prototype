from copy import deepcopy

from .models import Road, Village
from .seed_data import ROADS, VILLAGES

SCENARIO_FACTORS = {
    'normal': (0.45, 0.55, 0.55, 0.45),
    'heavy_rain': (1.10, 1.08, 1.08, 1.12),
    'flash_flood': (1.45, 1.40, 1.30, 1.50),
}


def apply_scenario(scenario: str, roads: list[Road]) -> list[Village]:
    """Return fresh deterministic scenario data; repeated clicks do not compound values."""
    rain, river, soil, upstream = SCENARIO_FACTORS[scenario]
    villages = deepcopy(VILLAGES)
    for village in villages:
        village.rainfall = min(100, round(village.rainfall * rain, 1))
        village.forecast_rainfall = min(100, round(village.forecast_rainfall * rain, 1))
        village.river_level = min(100, round(village.river_level * river, 1))
        village.soil_saturation = min(100, round(village.soil_saturation * soil, 1))
        village.upstream_flow = min(100, round(village.upstream_flow * upstream, 1))
    base_roads = {road.id: road for road in deepcopy(ROADS)}
    for road in roads:
        base = base_roads[road.id]
        road.risk, road.status = base.risk, base.status
        if road.status == 'BLOCKED':
            continue
        road.risk = min(100, round(road.risk * (1 + (rain - 1) * 0.55), 1))
        road.status = 'BLOCKED' if road.risk >= 98 else 'CAUTION' if road.risk >= 35 else 'SAFE'
    return villages