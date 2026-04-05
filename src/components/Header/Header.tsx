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
        <span className={styles.logoIcon}>◈</span>
        <div className={styles.logoText}>
          <span className={styles.logoTitle}>CITY</span>
          <span className={styles.logoSub}>KIOSK</span>
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
