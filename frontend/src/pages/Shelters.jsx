import { useEffect, useState } from 'react';
import { getDashboard } from '../services/api';
import PageFrame from '../components/PageFrame';

export default function Shelters() {
  const [shelters, setShelters] = useState([]);
  useEffect(() => { getDashboard().then((data) => setShelters(data.shelters)).catch(() => {}); }, []);
  return <PageFrame title="Shelter capacity"><div className="grid gap-4 md:grid-cols-3">{shelters.map((shelter) => { const occupancy = Math.round(((shelter.capacity - shelter.available_capacity) / shelter.capacity) * 100); return <article className="rounded-xl border border-slate-700 bg-panel p-5" key={shelter.id}><div className="mb-4 flex items-start justify-between"><div><p className="text-xs uppercase text-slate-500">{shelter.id}</p><h3 className="mt-1 text-lg font-semibold">{shelter.name}</h3></div><span className="rounded-full bg-emerald-950 px-2 py-1 text-xs text-teal-300">{shelter.status}</span></div><div className="mb-2 flex justify-between text-sm"><span>Occupancy</span><b>{occupancy}%</b></div><div className="h-2 rounded-full bg-slate-800"><div className="h-2 rounded-full bg-aqua" style={{ width: `${occupancy}%` }} /></div><dl className="mt-5 grid grid-cols-2 gap-3 text-sm"><div><dt className="text-slate-500">Capacity</dt><dd>{shelter.capacity}</dd></div><div><dt className="text-slate-500">Available</dt><dd className="text-teal-300">{shelter.available_capacity}</dd></div></dl></article>; })}</div>{!shelters.length && <p className="rounded-xl border border-slate-700 bg-panel p-5 text-slate-400">Loading shelter data…</p>}</PageFrame>;
}
