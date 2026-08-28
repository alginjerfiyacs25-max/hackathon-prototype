import React from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import 'leaflet/dist/leaflet.css';
import './index.css';
import Navigation from './components/Navigation';
import Dashboard from './pages/Dashboard';
import Villages from './pages/Villages';
import Shelters from './pages/Shelters';
import Alerts from './pages/Alerts';

function RoutedApp() {
	return <BrowserRouter><Routes>
		<Route path="/" element={<Navigate to="/dashboard" replace />} />
		<Route path="/dashboard" element={<><Navigation /><Dashboard /></>} />
		<Route path="/villages" element={<Villages />} />
		<Route path="/shelters" element={<Shelters />} />
		<Route path="/alerts" element={<Alerts />} />
		<Route path="*" element={<Navigate to="/dashboard" replace />} />
	</Routes></BrowserRouter>;
}

createRoot(document.getElementById('root')).render(<React.StrictMode><RoutedApp /></React.StrictMode>);
