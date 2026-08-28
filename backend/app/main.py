from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from . import database
from .models import SimulationRequest, PredictRequest
from .risk_engine import calculate_risk
from .time_to_impact import estimate_time
from .evacuation import assign_priority
from .routing import route_for
from .shelter_allocator import allocate
from .ml_model import train_model, get_metrics, predict_risk
from .simulation import apply_scenario

SCENARIOS={'normal':(0.55,0.65,0.7,0.6),'heavy_rain':(1.15,1.1,1.15,1.2),'flash_flood':(1.45,1.4,1.3,1.5)}

def refresh():
    for v in database.villages:
        calculate_risk(v); v.estimated_time_to_impact=estimate_time(v)['estimated_minutes']; assign_priority(v)
    return database.villages

def rank_villages():
    ordered = sorted(database.villages, key=lambda item: item.priority_score, reverse=True)
    for index, village in enumerate(ordered, 1):
        village.priority_rank = index
    return ordered
@asynccontextmanager
async def lifespan(app): refresh(); train_model(); yield
app=FastAPI(title='AquaSentinel API',version='1.0.0',lifespan=lifespan)
app.add_middleware(CORSMiddleware,allow_origins=['http://localhost:5173','http://127.0.0.1:5173'],allow_methods=['*'],allow_headers=['*'])
@app.get('/api/health')
def health(): return {'status':'ok','prototype':True,'message':'Simulation / hackathon prototype'}
@app.get('/api/villages')
def villages(): return refresh()
@app.get('/api/villages/{village_id}')
def village(village_id:str):
    item=next((v for v in refresh() if v.id==village_id),None)
    if not item: raise HTTPException(404,'Village not found')
    return item
@app.get('/api/shelters')
def shelters(): return [dict(s.model_dump(),available_capacity=s.available_capacity) for s in database.shelters]
@app.get('/api/roads')
def roads(): return database.roads
@app.get('/api/risk')
def risk():
    vs=refresh(); return {'overall_risk':round(sum(v.risk_score for v in vs)/len(vs),1),'villages':vs,'is_simulated':True}
@app.post('/api/predict')
def predict(req:PredictRequest): return predict_risk(req.model_dump())
@app.get('/api/evacuation-priority')
def priority(): return rank_villages()
@app.get('/api/routes/{village_id}')
def route(village_id:str):
    v=next((x for x in refresh() if x.id==village_id),None)
    if not v: raise HTTPException(404,'Village not found')
    return route_for(v,database.shelters,database.roads)
@app.get('/api/shelter-allocation')
def allocation(): return allocate(refresh(),database.shelters)
@app.get('/api/alerts')
def alerts():
    items = []
    for village in refresh():
        if village.risk_score >= 50:
            severity = 'CRITICAL' if village.risk_level == 'CRITICAL' else 'WARNING'
            items.append({'id': f'RISK-{village.id}', 'severity': severity, 'title': f'{village.name} risk escalation', 'message': f'{village.name} has entered {village.risk_level.lower()} flood-risk conditions.', 'timestamp': 'SIMULATED / NOW', 'village': village.name, 'recommended_action': village.recommended_action, 'simulated': True})
        if village.evacuation_priority == 'P1':
            items.append({'id': f'EVAC-{village.id}', 'severity': 'EVACUATION', 'title': 'Priority evacuation recommendation', 'message': f'P1 evacuation recommended for {village.name}.', 'timestamp': 'SIMULATED / NOW', 'village': village.name, 'recommended_action': village.recommended_action, 'simulated': True})
    for road in database.roads:
        if road.status == 'BLOCKED':
            items.append({'id': f'ROAD-{road.id}', 'severity': 'WARNING', 'title': 'Road access warning', 'message': f'Road {road.id} is currently classified as BLOCKED.', 'timestamp': 'SIMULATED / NOW', 'village': None, 'recommended_action': 'Use an alternate route', 'simulated': True})
    return items
@app.post('/api/simulate')
def simulate(req:SimulationRequest):
    database.villages = apply_scenario(req.scenario, database.roads)
    refresh(); return {'scenario':req.scenario,'villages':database.villages,'message':'Simulation state updated; all recommendations are simulated.'}
@app.get('/api/model-metrics')
def model_metrics(): return get_metrics()
@app.post('/api/train-model')
def retrain(): return train_model()
@app.post('/api/reset')
def reset(): database.reset_data(); refresh(); return {'status':'reset'}
