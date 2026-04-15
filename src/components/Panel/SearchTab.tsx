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
        <span className={styles.searchIcon}>
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" aria-hidden="true">
            <circle cx="9" cy="9" r="5.5"/>
            <line x1="13.5" y1="13.5" x2="17" y2="17"/>
          </svg>
        </span>
        <input
          className={styles.searchInput}
          type="text"
          placeholder="Поиск мест, киосков..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          autoComplete="off"
        />
        {query && (
          <button className={styles.clearBtn} onClick={() => setQuery('')}>×</button>
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
              <span className={styles.resultIcon}>
                <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                  <rect x="2.5" y="2.5" width="13" height="13" rx="2.5"/>
                  <circle cx="9" cy="9" r="2.5"/>
                </svg>
              </span>
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
              <span className={styles.resultIcon}>
                <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                  <circle cx="9" cy="7" r="2.5"/>
                  <path d="M9 1.5C6.1 1.5 3.75 3.85 3.75 6.75c0 4.2 5.25 9.75 5.25 9.75s5.25-5.55 5.25-9.75C14.25 3.85 11.9 1.5 9 1.5z"/>
                </svg>
              </span>
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
