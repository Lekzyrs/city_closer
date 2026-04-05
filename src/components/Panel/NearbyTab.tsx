import { useState } from 'react'
import type { POI } from '../../types'
import { CATEGORY_LABELS, CATEGORY_ICONS } from '../../data/mockData'
import styles from './Panel.module.css'

type FilterCategory = POI['category'] | 'all'

interface NearbyTabProps {
  pois: POI[]
  selectedPOIId: string | null
  onPOISelect: (id: string) => void
}

const FILTERS: { value: FilterCategory; label: string }[] = [
  { value: 'all', label: 'Всё' },
  { value: 'attraction', label: '🏛 Памятники' },
  { value: 'museum', label: '🎨 Музеи' },
  { value: 'park', label: '🌳 Парки' },
  { value: 'restaurant', label: '🍽 Еда' },
  { value: 'transport', label: '🚇 Транспорт' },
  { value: 'shopping', label: '🛍 Шопинг' },
]

export function NearbyTab({ pois, selectedPOIId, onPOISelect }: NearbyTabProps) {
  const [filter, setFilter] = useState<FilterCategory>('all')

  const filtered = filter === 'all' ? pois : pois.filter((p) => p.category === filter)
  const sorted = [...filtered].sort((a, b) => (a.distance ?? 9999) - (b.distance ?? 9999))

  return (
    <div className={styles.tabContent}>
      {/* Category filters */}
      <div className={styles.filterRow}>
        {FILTERS.map((f) => (
          <button
            key={f.value}
            className={`${styles.filterChip} ${filter === f.value ? styles.filterChipActive : ''}`}
            onClick={() => setFilter(f.value)}
          >
            {f.label}
          </button>
        ))}
      </div>

      {/* POI list */}
      <div className={styles.poiList}>
        {sorted.map((poi) => (
          <button
            key={poi.id}
            className={`${styles.poiCard} ${selectedPOIId === poi.id ? styles.poiCardActive : ''}`}
            onClick={() => onPOISelect(poi.id)}
          >
            <div className={styles.poiEmoji}>{CATEGORY_ICONS[poi.category]}</div>
            <div className={styles.poiBody}>
              <div className={styles.poiName}>{poi.name}</div>
              <div className={styles.poiDesc}>{poi.description}</div>
              <div className={styles.poiMeta}>
                <span className={styles.categoryTag}>{CATEGORY_LABELS[poi.category]}</span>
                {poi.distance != null && (
                  <span className={styles.distance}>
                    {poi.distance < 1000
                      ? `${poi.distance} м`
                      : `${(poi.distance / 1000).toFixed(1)} км`}
                  </span>
                )}
              </div>
            </div>
          </button>
        ))}
      </div>

      {sorted.length === 0 && (
        <p className={styles.hint}>Нет мест в этой категории поблизости</p>
      )}
    </div>
  )
}
