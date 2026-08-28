# Architecture

AquaSentinel is split into a React/Vite client and FastAPI service. The service owns the simulation state and exposes typed REST resources for villages, shelters, roads, risks, predictions, routes, allocations, alerts, and model metrics.

The risk engine normalizes each factor to 0–100 and applies fixed, explainable weights. Operational modules derive time-to-impact, evacuation priority, route choice, and capacity-safe allocations. A scikit-learn model module trains reproducibly on synthetic data and is replaceable with a persisted model later.

The current store is in-memory to make the hackathon demo simple; the data access boundary is isolated so SQLite/PostgreSQL/PostGIS can be introduced without changing the UI contract.
