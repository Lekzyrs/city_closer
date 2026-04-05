export interface LatLng {
  lat: number
  lng: number
}

export interface Kiosk {
  id: string
  name: string
  position: LatLng
  district: string
  isOnline: boolean
}

export interface POI {
  id: string
  name: string
  category: POICategory
  position: LatLng
  description: string
  distance?: number // meters from current kiosk
  imageUrl?: string
  tags: string[]
}

export type POICategory =
  | 'attraction'
  | 'museum'
  | 'park'
  | 'restaurant'
  | 'transport'
  | 'shopping'
  | 'hotel'

export interface RoutePoint {
  kioskId: string
  kioskName: string
  position: LatLng
  order: number
}

export interface Route {
  id: string
  points: RoutePoint[]
  totalDistance: number // meters
  estimatedTime: number // minutes
  segments?: LatLng[][] // path geometry from routing API
}

export interface SearchResult {
  id: string
  name: string
  type: 'kiosk' | 'poi'
  position: LatLng
  description?: string
}

// API response shapes — will be filled by Go/Python backends
export interface ApiResponse<T> {
  data: T
  status: 'ok' | 'error'
  message?: string
}
