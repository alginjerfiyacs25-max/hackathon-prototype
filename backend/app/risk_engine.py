from .models import Village

def clamp(value: float) -> float: return max(0.0, min(100.0, value))
def calculate_risk(v: Village) -> Village:
    factors = {'rainfall': clamp((v.rainfall * .65 + v.forecast_rainfall * .35)), 'river_level': clamp(v.river_level), 'soil_saturation': clamp(v.soil_saturation), 'slope': clamp(v.slope / 0.7), 'upstream_flow': clamp(v.upstream_flow)}
    weights = {'rainfall': .35, 'river_level': .25, 'soil_saturation': .20, 'slope': .10, 'upstream_flow': .10}
    score = round(sum(factors[k] * weights[k] for k in weights), 1)
    level = 'CRITICAL' if score >= 75 else 'HIGH' if score >= 50 else 'MODERATE' if score >= 25 else 'LOW'
    top = sorted(factors, key=factors.get, reverse=True)[:2]
    labels = {'rainfall':'rainfall', 'river_level':'river level', 'soil_saturation':'saturated soil', 'slope':'terrain slope', 'upstream_flow':'upstream flow'}
    v.risk_score, v.risk_level = score, level
    v.factor_contributions = {key: round(factors[key] * weights[key], 1) for key in weights}
    v.vulnerable_population = v.children + v.elderly + v.disabled
    v.explanation = f"{labels[top[0]].capitalize()} and {labels[top[1]]} are the primary contributors to the current risk."
    return v
