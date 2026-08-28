from .models import Village, Shelter

def allocate(villages: list[Village], shelters: list[Shelter]) -> list[dict]:
    remaining={s.id:s.available_capacity for s in shelters}; result=[]
    for v in sorted(villages,key=lambda x:x.risk_score,reverse=True):
        need=max(0, v.population - v.population//5)
        candidates=[s for s in shelters if remaining[s.id]>0 and s.accessibility>=45]
        if not candidates: continue
        shelter=min(candidates,key=lambda s: (s.accessibility < v.road_accessibility, -remaining[s.id]))
        amount=min(need,remaining[shelter.id]); remaining[shelter.id]-=amount
        result.append({'village_id':v.id,'village':v.name,'village_name':v.name,'shelter_id':shelter.id,'shelter':shelter.name,'shelter_name':shelter.name,'allocated_people':amount,'remaining_capacity':remaining[shelter.id],'occupancy_percentage':round((shelter.capacity-remaining[shelter.id])/shelter.capacity*100,1),'route_safety':'SAFE' if shelter.accessibility >= v.road_accessibility else 'CAUTION'})
    return result
