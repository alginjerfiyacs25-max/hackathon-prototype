import { NavLink } from 'react-router-dom';
import { Bell, Building2, LayoutDashboard, MapPinned } from 'lucide-react';

const links = [
  { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/villages', label: 'Villages', icon: MapPinned },
  { to: '/shelters', label: 'Shelters', icon: Building2 },
  { to: '/alerts', label: 'Alerts', icon: Bell },
];

export default function Navigation() {
  return <nav className="mx-auto mb-5 flex max-w-[1500px] flex-wrap items-center gap-2 rounded-xl border border-slate-700/70 bg-slate-900/80 p-2 shadow-lg" aria-label="Primary navigation">
    {links.map(({ to, label, icon: Icon }) => <NavLink key={to} to={to} className={({ isActive }) => `flex items-center gap-2 rounded-lg px-4 py-2 text-sm font-semibold transition ${isActive ? 'bg-aqua text-slate-950' : 'text-slate-300 hover:bg-slate-800 hover:text-white'}`}><Icon size={16} />{label}</NavLink>)}
  </nav>;
}
