from .models import Village

def assign_priority(v: Village) -> Village:
    exposure = min(100, v.population / 15)
    vulnerable = min(100, v.vulnerable_population / max(1, v.population) * 220)
    road_risk = 100 - v.road_accessibility
    urgency = min(100, max(0, 100 - v.estimated_time_to_impact * .7))
    score = round(.4*v.risk_score + .2*exposure + .15*vulnerable + .15*road_risk + .1*urgency, 1)
    v.priority_score = score
    v.evacuation_priority = 'P1' if score >= 70 else 'P2' if score >= 50 else 'P3' if score >= 30 else 'P4'
    v.recommended_action = {'P1': 'EVACUATE / PREPARE IMMEDIATE EVACUATION', 'P2': 'PREPARE EVACUATION', 'P3': 'MONITOR', 'P4': 'CONTINUE MONITORING'}[v.evacuation_priority]
    return v
