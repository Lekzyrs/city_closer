import { useState } from 'react'
import { Header } from './components/Header/Header'
import { BottomPanel } from './components/BottomPanel/BottomPanel'
import { MapView } from './components/Map/MapView'
import {
  MOCK_KIOSKS,
  MOCK_POIS,
  CURRENT_KIOSK_ID,
  CATEGORY_ICONS,
} from './data/mockData'
import type { Route, RoutePoint } from './types'
import styles from './App.module.css'

type Tab = 'nearby' | 'route' | 'search'

export default function App() {
  const [activeTab, setActiveTab] = useState<Tab>('nearby')
  const [selectedKioskId, setSelectedKioskId] = useState<string | null>(null)
  const [selectedPOIId, setSelectedPOIId] = useState<string | null>(null)
  const [activeRoute, setActiveRoute] = useState<Route | null>(null)
  const [isBuilding, setIsBuilding] = useState(false)

  const currentKiosk = MOCK_KIOSKS.find((k) => k.id === CURRENT_KIOSK_ID)!

  function handleBuildRoute(points: RoutePoint[]) {
    setIsBuilding(true)
    // Sprint 1 mock — Python routing replaces this
    setTimeout(() => {
      setActiveRoute({
        id: `route-${Date.now()}`,
        points,
        totalDistance: 0,
        estimatedTime: 0,
        segments: [],
      })
      setIsBuilding(false)
    }, 900)
  }

  function handleClearRoute() {
    setActiveRoute(null)
  }

  return (
    <div className={styles.app}>
      <Header kioskName={currentKiosk.name} district={currentKiosk.district} />

      <div className={styles.mapArea}>
        <MapView
          kiosks={MOCK_KIOSKS}
          pois={MOCK_POIS}
          currentKioskId={CURRENT_KIOSK_ID}
          activeRoute={activeRoute}
          selectedKioskId={selectedKioskId}
          onKioskClick={setSelectedKioskId}
          onPOIClick={setSelectedPOIId}
          categoryIcons={CATEGORY_ICONS}
        />
      </div>

      <BottomPanel
        kiosks={MOCK_KIOSKS}
        pois={MOCK_POIS}
        currentKioskId={CURRENT_KIOSK_ID}
        activeTab={activeTab}
        onTabChange={setActiveTab}
        selectedPOIId={selectedPOIId}
        onKioskSelect={(id) => { setSelectedKioskId(id); setActiveTab('nearby') }}
        onPOISelect={(id) => { setSelectedPOIId(id); setActiveTab('nearby') }}
        activeRoute={activeRoute}
        onBuildRoute={handleBuildRoute}
        onClearRoute={handleClearRoute}
        isBuilding={isBuilding}
      />
    </div>
  )
}
