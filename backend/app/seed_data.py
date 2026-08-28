from .models import Village, Shelter, Road

VILLAGES = [
 Village(id='V1', name='Kallar', latitude=10.088, longitude=77.061, population=850, children=120, elderly=90, disabled=24, elevation=920, slope=38, river_distance=1.8, rainfall=72, forecast_rainfall=84, soil_saturation=68, river_level=62, upstream_flow=58, road_accessibility=78),
 Village(id='V2', name='Munnar East', latitude=10.091, longitude=77.075, population=1200, children=170, elderly=130, disabled=36, elevation=1120, slope=44, river_distance=2.5, rainfall=58, forecast_rainfall=76, soil_saturation=61, river_level=54, upstream_flow=52, road_accessibility=66),
 Village(id='V3', name='Hillview', latitude=10.105, longitude=77.048, population=650, children=88, elderly=72, disabled=20, elevation=980, slope=56, river_distance=1.1, rainfall=88, forecast_rainfall=94, soil_saturation=82, river_level=78, upstream_flow=84, road_accessibility=55),
 Village(id='V4', name='Valley Point', latitude=10.073, longitude=77.052, population=1500, children=210, elderly=155, disabled=48, elevation=790, slope=27, river_distance=0.7, rainfall=92, forecast_rainfall=98, soil_saturation=88, river_level=86, upstream_flow=91, road_accessibility=42),
 Village(id='V5', name='Upper Hills', latitude=10.115, longitude=77.082, population=500, children=70, elderly=50, disabled=12, elevation=1380, slope=62, river_distance=3.8, rainfall=42, forecast_rainfall=55, soil_saturation=45, river_level=39, upstream_flow=35, road_accessibility=88),
]
SHELTERS = [
 Shelter(id='S1', name='Civic School Shelter', latitude=10.098, longitude=77.066, capacity=600, current_occupancy=120, accessibility=92),
 Shelter(id='S2', name='Munnar Sports Complex', latitude=10.062, longitude=77.078, capacity=1000, current_occupancy=280, accessibility=86),
 Shelter(id='S3', name='Upper Hills Community Hall', latitude=10.126, longitude=77.071, capacity=800, current_occupancy=90, accessibility=74),
]
ROADS = [
 Road(id='R1', start_node='V1', end_node='S1', distance=3.2, risk=18, status='SAFE', travel_time=8),
 Road(id='R2', start_node='V2', end_node='S1', distance=2.4, risk=38, status='CAUTION', travel_time=9),
 Road(id='R3', start_node='V3', end_node='S2', distance=4.1, risk=72, status='CAUTION', travel_time=16),
 Road(id='R4', start_node='V4', end_node='S2', distance=3.8, risk=91, status='BLOCKED', travel_time=15),
 Road(id='R5', start_node='V4', end_node='S1', distance=4.8, risk=76, status='CAUTION', travel_time=20),
 Road(id='R6', start_node='V5', end_node='S3', distance=2.1, risk=12, status='SAFE', travel_time=7),
 Road(id='R7', start_node='V3', end_node='S3', distance=5.6, risk=31, status='CAUTION', travel_time=22),
 Road(id='R8', start_node='V2', end_node='S3', distance=6.2, risk=14, status='SAFE', travel_time=24),
]
