import { useEffect, useMemo, useState } from 'react';
import { MapContainer, Marker, Polyline, Popup, TileLayer } from 'react-leaflet';
import L from 'leaflet';
import { Activity, AlertTriangle, CloudRain, Map as MapIcon, RefreshCw, Route as RouteIcon, Users } from 'lucide-react';
import { getDashboard, route, simulate } from './services/api';
import { fallback } from './data/fallbackData';

const markerIcon = (level) => L.divIcon({ className: `dot dot-${level}`, iconSize: [15, 15], iconAnchor: [7, 7] });
const roadColors = { SAFE: '#42d6b8', CAUTION: '#f0bd55', BLOCKED: '#f06b68' };

function App() {
  const [data, setData] = useState(fallback);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [scenario, setScenario] = useState('flash_flood');
  const [selected, setSelected] = useState(null);
  const [routeInfo, setRouteInfo] = useState(null);

  useEffect(() => {
    getDashboard().then(setData).catch(() => setError('Backend unavailable — showing fallback simulated data.')).finally(() => setLoading(false));
  }, []);

  const villages = data.villages || [];
  const shelters = data.shelters || [];
  const roads = data.roads || [];
  const critical = villages.filter((v) => v.risk_level === 'CRITICAL').length;
  const people = villages.filter((v) => v.risk_score >= 50).reduce((total, v) => total + v.population, 0);
  const minTime = Math.min(...villages.map((v) => v.estimated_time_to_impact || 999));
  const overall = Math.round(villages.reduce((total, v) => total + v.risk_score, 0) / villages.length);
  const ranked = useMemo(() => [...villages].sort((a, b) => b.risk_score - a.risk_score), [villages]);
  const position = (node) => {
    const village = villages.find((item) => item.id === node);
    const shelter = shelters.find((item) => item.id === node);
    return village ? [village.latitude, village.longitude] : shelter ? [shelter.latitude, shelter.longitude] : null;
  };
  const run = async () => {
    setLoading(true);
    try { const result = await simulate(scenario); setData((current) => ({ ...current, villages: result.villages })); setError(''); }
    catch { setError('Simulation requires the FastAPI backend at localhost:8000.'); }
    finally { setLoading(false); }
  };
  const selectVillage = async (village) => { setSelected(village); try { setRouteInfo(await route(village.id)); } catch { setRouteInfo(null); } };
  const routePoints = routeInfo?.route?.map(position).filter(Boolean) || [];

  return <div className="app">
    <header className="header"><div className="brand"><div className="brand-mark"><Activity size={22} /></div><div><h1>AquaSentinel</h1><div className="muted">Flash Flood Early Warning & Evacuation Intelligence</div></div></div><div className="status">● SYSTEM ONLINE · SIMULATION</div></header>
    <div className="toolbar"><button className="button primary" onClick={run} disabled={loading}><RefreshCw size={15} /> {loading ? 'Updating…' : 'Run Flood Simulation'}</button><select value={scenario} onChange={(event) => setScenario(event.target.value)}><option value="normal">Normal</option><option value="heavy_rain">Heavy Rain</option><option value="flash_flood">Flash Flood Risk</option></select><span className="muted">Last updated: just now</span></div>
    {error && <div className="error">⚠ {error}</div>}
    <section className="grid"><Metric label="Overall Flood Risk" value={`${overall}%`} detail={overall >= 75 ? 'CRITICAL' : 'ELEVATED'} alert /><Metric label="Critical Villages" value={critical} detail={`of ${villages.length} monitored`} /><Metric label="People at Risk" value={people.toLocaleString()} detail="exposure estimate" /><Metric label="Shelters Available" value={shelters.filter((s) => s.available_capacity > 0).length || 3} detail="capacity-aware" /><Metric label="Min Time-to-Impact" value={`${minTime} min`} detail="prototype estimate" /></section>
    <div className="layout"><section className="panel"><h2><MapIcon size={17} /> Live Risk Map</h2><div className="map"><MapContainer center={[10.09, 77.06]} zoom={12}><TileLayer attribution="&copy; OpenStreetMap" url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />{roads.map((road) => { const start = position(road.start_node); const end = position(road.end_node); return start && end ? <Polyline key={road.id} positions={[start, end]} color={roadColors[road.status]} dashArray={road.status === 'BLOCKED' ? '5 8' : undefined} weight={road.status === 'BLOCKED' ? 4 : 3}><Popup>{road.id} · {road.status}<br />{road.distance} km · {road.travel_time} min</Popup></Polyline> : null; })}{villages.map((village) => <Marker key={village.id} position={[village.latitude, village.longitude]} icon={markerIcon(village.risk_level)} eventHandlers={{ click: () => selectVillage(village) }}><Popup><b>{village.name}</b><br />Risk: {village.risk_score}% · {village.risk_level}<br />Rainfall: {village.rainfall}<br />River level: {village.river_level}<br />Impact: {village.estimated_time_to_impact} min<br />Priority: {village.evacuation_priority}</Popup></Marker>)}{shelters.map((shelter) => <Marker key={shelter.id} position={[shelter.latitude, shelter.longitude]}><Popup><b>{shelter.name}</b><br />Capacity: {shelter.capacity}<br />Available: {shelter.available_capacity}<br />Status: {shelter.status}</Popup></Marker>)}{routePoints.length > 1 && <Polyline positions={routePoints} color="#41d8c0" weight={6} />}</MapContainer></div>{selected && <div className="recommend"><div className="label">🚨 Recommended Action</div><h3>{selected.evacuation_priority === 'P1' ? 'EVACUATE' : 'PREPARE'} {selected.name}</h3><div>Risk <b className={selected.risk_level}>{selected.risk_score}% · {selected.risk_level}</b> · Time-to-impact <b>{selected.estimated_time_to_impact} min</b></div><div className="muted"><RouteIcon size={14} /> {routeInfo?.recommended_shelter?.name || 'Route unavailable'} · {routeInfo?.distance || '—'} km · {routeInfo?.road_warnings?.join(', ') || 'No road warnings'}</div><small className="muted">Prototype recommendation — verify with authorized emergency procedures.</small></div>}</section>
      <section className="panel"><h2><AlertTriangle size={17} /> Alert Console</h2>{data.alerts?.length ? data.alerts.map((alert) => <div className="alert-item" key={alert.id}><b className={alert.severity}>{alert.severity}</b><div>{alert.title || alert.message}</div><small className="muted">{alert.message} · SIMULATED</small></div>) : <div className="muted">No active alerts. Conditions are being monitored.</div>}<h2 style={{ marginTop: 24 }}><CloudRain size={17} /> Risk Factor Contribution</h2><div className="chart">{Object.entries(data.metrics?.feature_importance || fallback.metrics.feature_importance).slice(0, 5).map(([name, value]) => <div className="bar" style={{ height: `${Math.max(15, value * 260)}%` }} key={name}><span>{Math.round(value * 100)}%</span></div>)}</div><div className="muted">Rainfall · River · Soil · Flow · Slope</div></section></div>
    <section className="panel" style={{ marginTop: 16 }}><h2><Users size={17} /> Vulnerable Village Ranking</h2><div className="table-wrap"><table className="table"><thead><tr><th>Rank</th><th>Village</th><th>Risk</th><th>Time to Impact</th><th>Population</th><th>Priority</th><th>Action</th></tr></thead><tbody>{ranked.map((village, index) => <tr key={village.id} onClick={() => selectVillage(village)}><td>0{index + 1}</td><td><b>{village.name}</b></td><td className={`risk ${village.risk_level}`}>{village.risk_score}% · {village.risk_level}</td><td>{village.estimated_time_to_impact} min</td><td>{village.population.toLocaleString()}</td><td><span className="priority">{village.evacuation_priority}</span></td><td className={village.evacuation_priority === 'P1' ? 'CRITICAL' : 'muted'}>{village.evacuation_priority === 'P1' ? 'EVACUATE' : 'MONITOR'}</td></tr>)}</tbody></table></div></section>
    <div className="footer">SIMULATION DATA — HACKATHON PROTOTYPE · Not a real emergency-warning system or safety guarantee.</div>
  </div>;
}

function Metric({ label, value, detail, alert }) { return <div className={`metric${alert ? ' alert' : ''}`}><div className="label">{label}</div><strong>{value}</strong><span className={alert ? 'CRITICAL' : 'muted'}>{detail}</span></div>; }
export default App;
