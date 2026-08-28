from typing import Literal
from pydantic import BaseModel, Field

RiskLevel = Literal['LOW', 'MODERATE', 'HIGH', 'CRITICAL']
RoadStatus = Literal['SAFE', 'CAUTION', 'BLOCKED']

class Village(BaseModel):
    id: str; name: str; latitude: float; longitude: float
    population: int; children: int; elderly: int; disabled: int
    elevation: float; slope: float; river_distance: float
    rainfall: float; forecast_rainfall: float; soil_saturation: float
    river_level: float; upstream_flow: float; road_accessibility: float
    risk_score: float = 0; risk_level: RiskLevel = 'LOW'
    evacuation_priority: str = 'P4'; estimated_time_to_impact: int = 999
    vulnerable_population: int = 0
    explanation: str = ''
    factor_contributions: dict[str, float] = Field(default_factory=dict)
    priority_score: float = 0
    priority_rank: int = 0
    recommended_action: str = 'CONTINUE MONITORING'

class Shelter(BaseModel):
    id: str; name: str; latitude: float; longitude: float
    capacity: int; current_occupancy: int; accessibility: float; status: str = 'OPEN'
    @property
    def available_capacity(self) -> int: return max(0, self.capacity - self.current_occupancy)

class Road(BaseModel):
    id: str; start_node: str; end_node: str; distance: float
    risk: float; status: RoadStatus; travel_time: int

class SimulationRequest(BaseModel):
    scenario: Literal['normal', 'heavy_rain', 'flash_flood'] = 'flash_flood'

class PredictRequest(BaseModel):
    rainfall: float = Field(ge=0); forecast_rainfall: float = Field(ge=0)
    soil_saturation: float = Field(ge=0, le=100); river_level: float = Field(ge=0)
    slope: float = Field(ge=0); upstream_flow: float = Field(ge=0)
    river_distance: float = Field(ge=0); elevation: float = Field(ge=0)
