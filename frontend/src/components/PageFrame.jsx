import { Activity } from 'lucide-react';
import Navigation from './Navigation';

export default function PageFrame({ title, subtitle, children }) {
  return <div className="min-h-screen bg-ink px-4 py-5 text-slate-100 sm:px-6 lg:px-8">
    <header className="mx-auto mb-5 flex max-w-[1500px] flex-wrap items-center justify-between gap-4 border-b border-slate-700 pb-5">
      <div className="flex items-center gap-3"><div className="rounded-xl bg-aqua p-2 text-slate-950"><Activity size={22} /></div><div><h1 className="font-['Space_Grotesk'] text-xl font-bold">AquaSentinel</h1><p className="text-xs text-slate-400">{subtitle || 'Flash Flood Early Warning & Evacuation Intelligence'}</p></div></div>
      <span className="rounded-full bg-emerald-950 px-3 py-2 text-xs font-semibold text-teal-300">● SYSTEM ONLINE · SIMULATION</span>
    </header>
    <Navigation />
    <main className="mx-auto max-w-[1500px]"><div className="mb-5"><h2 className="font-['Space_Grotesk'] text-2xl font-bold">{title}</h2><p className="mt-1 text-sm text-slate-400">SIMULATION DATA — HACKATHON PROTOTYPE</p></div>{children}</main>
  </div>;
}
