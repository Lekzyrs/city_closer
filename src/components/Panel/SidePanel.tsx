import type { Kiosk, POI, Route, RoutePoint } from '../../types'
import { SearchTab } from './SearchTab'
import { NearbyTab } from './NearbyTab'
import { RouteTab } from './RouteTab'
import styles from './SidePanel.module.css'

type Tab = 'nearby' | 'route' | 'search'

interface SidePanelProps {
  kiosks: Kiosk[]
  pois: POI[]
  currentKioskId: string
  activeTab: Tab
  onTabChange: (tab: Tab) => void
  selectedPOIId: string | null
  onKioskSelect: (id: string) => void
  onPOISelect: (id: string) => void
  activeRoute: Route | null
  onBuildRoute: (points: RoutePoint[]) => void
  onClearRoute: () => void
  isBuilding: boolean
}

const TABS: { id: Tab; label: string; icon: string }[] = [
  { id: 'nearby', label: 'Рядом', icon: '◉' },
  { id: 'route', label: 'Маршрут', icon: '⇢' },
  { id: 'search', label: 'Поиск', icon: '⌕' },
]

export function SidePanel({
  kiosks,
  pois,
  currentKioskId,
  activeTab,
  onTabChange,
  selectedPOIId,
  onKioskSelect,
  onPOISelect,
  activeRoute,
  onBuildRoute,
  onClearRoute,
  isBuilding,
}: SidePanelProps) {
  return (
    <aside className={styles.panel}>
      {/* Tab bar */}
      <nav className={styles.tabs}>
        {TABS.map((t) => (
          <button
            key={t.id}
            className={`${styles.tab} ${activeTab === t.id ? styles.tabActive : ''}`}
            onClick={() => onTabChange(t.id)}
          >
            <span className={styles.tabIcon}>{t.icon}</span>
            <span className={styles.tabLabel}>{t.label}</span>
          </button>
        ))}
      </nav>

      {/* Active route summary strip */}
      {activeRoute && (
        <div className={styles.routeStrip}>
          <span className={styles.routeStripIcon}>⇢</span>
          <div className={styles.routeStripInfo}>
            <span className={styles.routeStripTitle}>Маршрут активен</span>
            <span className={styles.routeStripMeta}>
              {activeRoute.points.length} точки ·{' '}
              {activeRoute.totalDistance > 0
                ? `${(activeRoute.totalDistance / 1000).toFixed(1)} км · `
                : ''}
              {activeRoute.estimatedTime > 0 ? `~${activeRoute.estimatedTime} мин` : 'расчёт...'}
            </span>
          </div>
          <button className={styles.routeStripClose} onClick={onClearRoute}>
            ✕
          </button>
        </div>
      )}

      {/* Tab content */}
      <div className={styles.content}>
        {activeTab === 'nearby' && (
          <NearbyTab
            pois={pois}
            selectedPOIId={selectedPOIId}
            onPOISelect={onPOISelect}
          />
        )}
        {activeTab === 'route' && (
          <RouteTab
            kiosks={kiosks}
            currentKioskId={currentKioskId}
            onBuildRoute={onBuildRoute}
            onClearRoute={onClearRoute}
            isBuilding={isBuilding}
          />
        )}
        {activeTab === 'search' && (
          <SearchTab
            kiosks={kiosks}
            pois={pois}
            currentKioskId={currentKioskId}
            onKioskSelect={(id) => {
              onKioskSelect(id)
              onTabChange('nearby')
            }}
            onPOISelect={(id) => {
              onPOISelect(id)
              onTabChange('nearby')
            }}
          />
        )}
      </div>

      {/* "You are here" footer */}
      <div className={styles.youAreHere}>
        <span className={styles.youAreHereDot} />
        <span className={styles.youAreHereText}>
          Вы здесь · {kiosks.find((k) => k.id === currentKioskId)?.name}
        </span>
      </div>
    </aside>
  )
}
