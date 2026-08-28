import { useEffect, useState } from 'react';
import { AlertTriangle } from 'lucide-react';
import { getDashboard } from '../services/api';
import PageFrame from '../components/PageFrame';

export default function Alerts() {
  const [alerts, setAlerts] = useState([]);
  useEffect(() => { getDashboard().then((data) => setAlerts(data.alerts)).catch(() => {}); }, []);
  return <PageFrame title="Alert console" subtitle="Simulated operator recommendations"><div className="space-y-3">{alerts.map((alert) => <article className="flex gap-4 rounded-xl border border-slate-700 bg-panel p-5" key={alert.id}><AlertTriangle className="shrink-0 text-rose-400" /><div className="min-w-0 flex-1"><div className="flex flex-wrap items-center gap-3"><b className={alert.severity}>{alert.severity}</b><span className="text-xs text-slate-500">{alert.timestamp || 'SIMULATED / NOW'}</span></div><h3 className="mt-2 font-semibold">{alert.title || 'Risk alert'}</h3><p className="text-sm text-slate-400">{alert.message}</p><p className="mt-2 text-xs text-teal-300">Recommended: {alert.recommended_action || 'Review conditions'}</p></div><div className="flex shrink-0 gap-2"><button className="button">Approve</button><button className="button">Dismiss</button></div></article>)}{!alerts.length && <p className="rounded-xl border border-slate-700 bg-panel p-5 text-slate-400">No active alerts.</p>}</div><p className="mt-5 text-xs text-slate-500">Operator buttons are simulated only. No SMS, email, or emergency notification is sent.</p></PageFrame>;
}
