import { useState } from 'react'
import type { Kiosk, POI } from '../../types'
import styles from './Panel.module.css'

interface SearchTabProps {
  kiosks: Kiosk[]
  pois: POI[]
  onKioskSelect: (id: string) => void
  onPOISelect: (id: string) => void
  currentKioskId: string
}

export function SearchTab({ kiosks, pois, onKioskSelect, onPOISelect, currentKioskId }: SearchTabProps) {
  const [query, setQuery] = useState('')

  const q = query.toLowerCase()
  const filteredKiosks = q
    ? kiosks.filter(
        (k) =>
          k.id !== currentKioskId &&
          (k.name.toLowerCase().includes(q) || k.district.toLowerCase().includes(q))
      )
    : []
  const filteredPOIs = q
    ? pois.filter(
        (p) =>
          p.name.toLowerCase().includes(q) ||
          p.description.toLowerCase().includes(q) ||
          p.tags.some((t) => t.toLowerCase().includes(q))
      )
    : []

  const hasResults = filteredKiosks.length > 0 || filteredPOIs.length > 0

  return (
    <div className={styles.tabContent}>
      <div className={styles.searchInputWrap}>
        <span className={styles.searchIcon}>⌕</span>
        <input
          className={styles.searchInput}
          type="text"
          placeholder="Поиск мест, киосков..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          autoComplete="off"
        />
        {query && (
          <button className={styles.clearBtn} onClick={() => setQuery('')}>
            ✕
          </button>
        )}
      </div>

      {!query && (
        <p className={styles.hint}>Введите название места или достопримечательности</p>
      )}

      {query && !hasResults && (
        <p className={styles.hint}>Ничего не найдено по запросу «{query}»</p>
      )}

      {filteredKiosks.length > 0 && (
        <div className={styles.section}>
          <div className={styles.sectionLabel}>Киоски</div>
          {filteredKiosks.map((k) => (
            <button key={k.id} className={styles.resultRow} onClick={() => onKioskSelect(k.id)}>
              <span className={styles.resultIcon}>◈</span>
              <div className={styles.resultInfo}>
                <span className={styles.resultName}>{k.name}</span>
                <span className={styles.resultSub}>{k.district}</span>
              </div>
              {!k.isOnline && <span className={styles.offlineBadge}>офлайн</span>}
            </button>
          ))}
        </div>
      )}

      {filteredPOIs.length > 0 && (
        <div className={styles.section}>
          <div className={styles.sectionLabel}>Места</div>
          {filteredPOIs.map((p) => (
            <button key={p.id} className={styles.resultRow} onClick={() => onPOISelect(p.id)}>
              <span className={styles.resultIcon}>📍</span>
              <div className={styles.resultInfo}>
                <span className={styles.resultName}>{p.name}</span>
                <span className={styles.resultSub}>{p.description}</span>
              </div>
              {p.distance != null && (
                <span className={styles.distanceBadge}>{(p.distance / 1000).toFixed(1)} км</span>
              )}
            </button>
          ))}
        </div>
      )}
    </div>
  )
}
