from .models import Village

def estimate_time(v: Village) -> dict:
    urgency = v.river_level * .42 + v.upstream_flow * .28 + v.rainfall * .20 + v.soil_saturation * .10
    minutes = round(max(15, min(180, 150 - urgency - v.slope * .15 - max(0, 3 - v.river_distance) * 8)))
    confidence = 'High' if urgency > 75 else 'Medium' if urgency > 45 else 'Low'
    return {'estimated_minutes': minutes, 'confidence_level': confidence, 'is_simulated': True, 'explanation': 'High upstream flow and rising river level are reducing the estimated warning window.' if urgency > 65 else 'Prototype estimate based on current simulated conditions.'}
