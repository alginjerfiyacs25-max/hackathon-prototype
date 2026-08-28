import axios from 'axios';
const api=axios.create({baseURL:import.meta.env.VITE_API_URL||'http://localhost:8000/api',timeout:4000});
export const getDashboard=async()=>{const [v,s,r,a,m]=await Promise.all([api.get('/villages'),api.get('/shelters'),api.get('/roads'),api.get('/alerts'),api.get('/model-metrics')]);return {villages:v.data,shelters:s.data,roads:r.data,alerts:a.data,metrics:m.data}};
export const simulate=async scenario=>(await api.post('/simulate',{scenario})).data;
export const route=async id=>(await api.get(`/routes/${id}`)).data;
export default api;
