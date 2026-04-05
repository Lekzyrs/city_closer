/**
 * Vite dev proxy routes:
 *   /api/*      → localhost:8080
 *   /routing/*  → localhost:8000
 */

import type { Kiosk, POI, Route, SearchResult, ApiResponse } from "../types";

const GO_API = "/api/v1";
const PY_API = "/routing/v1";

async function get<T>(url: string): Promise<T> {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${url}`);
  const json: ApiResponse<T> = await res.json();
  if (json.status === "error") throw new Error(json.message ?? "API error");
  return json.data;
}

// ── Kiosks ──────────────────────────────────────────────────────────────────

export const kioskService = {
  getAll: () => get<Kiosk[]>(`${GO_API}/kiosks`),
  getById: (id: string) => get<Kiosk>(`${GO_API}/kiosks/${id}`),
  create: (payload: Omit<Kiosk, "id">) =>
    fetch(`${GO_API}/kiosks`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    }).then((r) => r.json()),
  update: (id: string, payload: Partial<Kiosk>) =>
    fetch(`${GO_API}/kiosks/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    }).then((r) => r.json()),
  delete: (id: string) => fetch(`${GO_API}/kiosks/${id}`, { method: "DELETE" }),
};

// ── Points of Interest ───────────────────────────────────────────────────────

export const poiService = {
  getNearby: (lat: number, lng: number, radius = 1000) =>
    get<POI[]>(`${GO_API}/pois?lat=${lat}&lng=${lng}&radius=${radius}`),
  getById: (id: string) => get<POI>(`${GO_API}/pois/${id}`),
};

// ── Routing (Python) ─────────────────────────────────────────────────────────

export const routingService = {
  buildRoute: (pointIds: string[]) =>
    fetch(`${PY_API}/route`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ kiosk_ids: pointIds }),
    }).then((r) => r.json() as Promise<Route>),
};

// ── Search ───────────────────────────────────────────────────────────────────

export const searchService = {
  query: (q: string) =>
    get<SearchResult[]>(`${GO_API}/search?q=${encodeURIComponent(q)}`),
};
