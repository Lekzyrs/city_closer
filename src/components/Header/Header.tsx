import { useEffect, useState } from 'react'
import styles from './Header.module.css'

interface HeaderProps {
  kioskName: string
  district: string
}

export function Header({ kioskName, district }: HeaderProps) {
  const [time, setTime] = useState(new Date())

  useEffect(() => {
    const timer = setInterval(() => setTime(new Date()), 1000)
    return () => clearInterval(timer)
  }, [])

  const timeStr = time.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })
  const dateStr = time.toLocaleDateString('ru-RU', { weekday: 'long', day: 'numeric', month: 'long' })

  return (
    <header className={styles.header}>
      <div className={styles.logo}>
        <svg className={styles.logoIcon} width="32" height="32" viewBox="0 0 32 32" fill="none" aria-hidden="true">
          <rect width="32" height="32" rx="5" fill="#C8102E"/>
          <circle cx="16" cy="10.5" r="2.2" fill="white"/>
          <rect x="14" y="15" width="4" height="8.5" rx="2" fill="white"/>
        </svg>
        <div className={styles.logoText}>
          <span className={styles.logoTitle}>МОСКВА</span>
          <span className={styles.logoSub}>НАВИГАЦИЯ</span>
        </div>
      </div>

      <div className={styles.kioskInfo}>
        <div className={styles.youAreHere}>
          <span className={styles.dot} />
          <span className={styles.kioskName}>{kioskName}</span>
        </div>
        <span className={styles.kioskDistrict}>{district} · Вы здесь</span>
      </div>

      <div className={styles.timeBlock}>
        <span className={styles.time}>{timeStr}</span>
        <span className={styles.date}>{dateStr}</span>
      </div>
    </header>
  )
}
