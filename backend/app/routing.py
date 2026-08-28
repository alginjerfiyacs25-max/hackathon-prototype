import networkx as nx
from .models import Village, Shelter, Road

def route_for(v: Village, shelters: list[Shelter], roads: list[Road]) -> dict:
    graph = nx.Graph()
    for road in roads:
        if road.status != 'BLOCKED': graph.add_edge(road.start_node, road.end_node, weight=road.distance + (3 if road.status == 'CAUTION' else 0), road=road)
    options=[]
    for shelter in shelters:
        if shelter.available_capacity <= 0 or v.id not in graph or shelter.id not in graph or not nx.has_path(graph, v.id, shelter.id): continue
        path=nx.shortest_path(graph, v.id, shelter.id, weight='weight'); edges=list(zip(path,path[1:])); route_roads=[graph[a][b]['road'] for a,b in edges]
        options.append((sum(r.distance for r in route_roads) + sum(3 for r in route_roads if r.status=='CAUTION'), shelter, path, route_roads))
    if not options: return {'village_id':v.id,'recommended_shelter':None,'route':[],'distance':None,'travel_time':None,'road_warnings':['No safe-capacity route available']}
    _, shelter, path, route_roads=min(options,key=lambda x:x[0])
    return {'village_id':v.id,'recommended_shelter':shelter.model_dump(),'route':path,'distance':round(sum(r.distance for r in route_roads),1),'travel_time':sum(r.travel_time for r in route_roads),'estimated_travel_time':sum(r.travel_time for r in route_roads),'road_warnings':[f'{r.id} is under caution' for r in route_roads if r.status=='CAUTION'],'route_safety':'CAUTION' if any(r.status=='CAUTION' for r in route_roads) else 'SAFE'}
