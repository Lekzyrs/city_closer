/**
 * Sprint 1 mock data — removed once Go/Python APIs are live.
 */

import type { Kiosk, POI } from '../types'

export const CURRENT_KIOSK_ID = 'kiosk-01'

export const MOCK_KIOSKS: Kiosk[] = [
  {
    id: 'kiosk-01',
    name: 'Красная площадь',
    district: 'Центр',
    position: { lat: 55.7539, lng: 37.6208 },
    isOnline: true,
  },
  {
    id: 'kiosk-02',
    name: 'Арбат',
    district: 'Центр',
    position: { lat: 55.7494, lng: 37.5943 },
    isOnline: true,
  },
  {
    id: 'kiosk-03',
    name: 'Парк Горького',
    district: 'Центр',
    position: { lat: 55.7297, lng: 37.6011 },
    isOnline: true,
  },
  {
    id: 'kiosk-04',
    name: 'ВДНХ',
    district: 'Север',
    position: { lat: 55.8264, lng: 37.6402 },
    isOnline: false,
  },
  {
    id: 'kiosk-05',
    name: 'Воробьёвы горы',
    district: 'Запад',
    position: { lat: 55.7082, lng: 37.5588 },
    isOnline: true,
  },
]

export const MOCK_POIS: POI[] = [
  {
    id: 'poi-01',
    name: 'Кремль',
    category: 'attraction',
    position: { lat: 55.752, lng: 37.6174 },
    description: 'Главная крепость страны, символ Москвы',
    distance: 350,
    tags: ['история', 'архитектура', 'UNESCO'],
  },
  {
    id: 'poi-02',
    name: 'ГУМ',
    category: 'shopping',
    position: { lat: 55.7546, lng: 37.6218 },
    description: 'Исторический торговый центр',
    distance: 120,
    tags: ['шопинг', 'история'],
  },
  {
    id: 'poi-03',
    name: 'Исторический музей',
    category: 'museum',
    position: { lat: 55.7553, lng: 37.6177 },
    description: 'Крупнейший исторический музей России',
    distance: 280,
    tags: ['музей', 'история', 'культура'],
  },
  {
    id: 'poi-04',
    name: 'Александровский сад',
    category: 'park',
    position: { lat: 55.752, lng: 37.6115 },
    description: 'Городской парк у стен Кремля',
    distance: 420,
    tags: ['парк', 'прогулка'],
  },
  {
    id: 'poi-05',
    name: 'Храм Василия Блаженного',
    category: 'attraction',
    position: { lat: 55.7525, lng: 37.6231 },
    description: 'Собор XVI века — визитная карточка Москвы',
    distance: 180,
    tags: ['история', 'архитектура', 'религия', 'UNESCO'],
  },
]

export const CATEGORY_LABELS: Record<POI['category'], string> = {
  attraction: 'Достопримечательность',
  museum: 'Музей',
  park: 'Парк',
  restaurant: 'Ресторан',
  transport: 'Транспорт',
  shopping: 'Шопинг',
  hotel: 'Отель',
}

export const CATEGORY_ICONS: Record<POI['category'], string> = {
  attraction: 'Д',
  museum: 'М',
  park: 'П',
  restaurant: 'Р',
  transport: 'Т',
  shopping: 'Ш',
  hotel: 'О',
}
