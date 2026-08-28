import { useEffect, useState } from 'react';
import { getDashboard } from '../services/api';
import { fallback } from '../data/fallbackData';
import PageFrame from '../components/PageFrame';

export default function Villages() {
  const [villages, setVillages] = useState(fallback.villages);
  useEffect(() => { getDashboard().then((data) => setVillages(data.villages)).catch(() => {}); }, []);
  return <PageFrame title="Village risk intelligence"><div className="overflow-hidden rounded-xl border border-slate-700 bg-panel"><div className="overflow-x-auto"><table className="min-w-full text-left text-sm"><thead className="bg-slate-900 text-xs uppercase text-slate-400"><tr>{['Rank', 'Village', 'Risk', 'Time to impact', 'Population', 'Priority', 'Action'].map((heading) => <th className="px-5 py-4" key={heading}>{heading}</th>)}</tr></thead><tbody>{[...villages].sort((a, b) => b.risk_score - a.risk_score).map((village, index) => <tr className="border-t border-slate-700/80" key={village.id}><td className="px-5 py-4 font-semibold">{index + 1}</td><td className="px-5 py-4 font-semibold">{village.name}</td><td className={`px-5 py-4 font-bold ${village.risk_level}`}>{village.risk_score}% · {village.risk_level}</td><td className="px-5 py-4">{village.estimated_time_to_impact} min</td><td className="px-5 py-4">{village.population.toLocaleString()}</td><td className="px-5 py-4"><span className="rounded bg-rose-950 px-2 py-1 text-xs text-rose-300">{village.evacuation_priority}</span></td><td className="px-5 py-4 text-slate-400">{village.evacuation_priority === 'P1' ? 'EVACUATE' : 'MONITOR'}</td></tr>)}</tbody></table></div></div></PageFrame>;
}
