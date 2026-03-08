'use client'

import { motion } from 'framer-motion'
import { useEffect, useState } from 'react'
import { Sparkles, Users, Sword, TrendingUp, Clock } from 'lucide-react'
import Link from 'next/link'

interface Stats {
  total_teams: number
  total_equipment: number
  recent_teams_7d: number
  platform_distribution: Record<string, number>
  last_updated: string
}

export default function Home() {
  const [stats, setStats] = useState<Stats | null>(null)

  useEffect(() => {
    // 获取统计数据
    fetch('http://localhost:8181/api/stats')
      .then(res => res.json())
      .then(data => setStats(data))
      .catch(err => console.error('获取统计失败:', err))
  }, [])

  return (
    <main className="min-h-screen">
      {/* Hero Section */}
      <section className="relative h-[60vh] flex items-center justify-center overflow-hidden">
        {/* 背景动画 */}
        <div className="absolute inset-0 bg-hero-gradient" />
        <div className="absolute inset-0 opacity-30">
          {[...Array(20)].map((_, i) => (
            <motion.div
              key={i}
              className="absolute w-2 h-2 bg-ark-cyan-400 rounded-full"
              style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
              }}
              animate={{
                y: [0, -30, 0],
                opacity: [0.2, 1, 0.2],
              }}
              transition={{
                duration: 3 + Math.random() * 2,
                repeat: Infinity,
                delay: Math.random() * 2,
              }}
            />
          ))}
        </div>

        <div className="relative z-10 text-center px-4">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h1 className="font-display text-5xl md:text-7xl font-black mb-4 neon-text">
              <span className="bg-gradient-to-r from-ark-purple-400 via-ark-cyan-400 to-ark-pink-400 bg-clip-text text-transparent">
                伊冯
              </span>
              <span className="text-white"> · 配队指南</span>
            </h1>
            <p className="text-xl md:text-2xl text-gray-300 mb-2">
              明日方舟终末地
            </p>
            <p className="text-gray-400 max-w-2xl mx-auto">
              汇集 B站 · NGA · 森空岛 多平台最新攻略
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5, duration: 0.8 }}
            className="mt-8 flex gap-4 justify-center"
          >
            <Link
              href="/teams"
              className="px-8 py-3 bg-gradient-to-r from-ark-purple-600 to-ark-purple-500 rounded-full font-semibold hover:from-ark-purple-500 hover:to-ark-purple-400 transition-all shadow-lg shadow-ark-purple-500/30"
            >
              查看配队
            </Link>
            <Link
              href="/equipment"
              className="px-8 py-3 glass rounded-full font-semibold hover:bg-ark-purple-800/50 transition-all"
            >
              装备配置
            </Link>
          </motion.div>
        </div>
      </section>

      {/* 统计卡片 */}
      <section className="py-12 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <StatCard
              icon={<Users className="w-6 h-6" />}
              title="配队方案"
              value={stats?.total_teams || 0}
              color="purple"
            />
            <StatCard
              icon={<Sword className="w-6 h-6" />}
              title="装备配置"
              value={stats?.total_equipment || 0}
              color="cyan"
            />
            <StatCard
              icon={<Sparkles className="w-6 h-6" />}
              title="本周新增"
              value={stats?.recent_teams_7d || 0}
              color="pink"
            />
            <StatCard
              icon={<Clock className="w-6 h-6" />}
              title="数据更新"
              value={stats?.last_updated ? new Date(stats.last_updated).toLocaleDateString() : '--'}
              color="purple"
              isText
            />
          </div>
        </div>
      </section>

      {/* 数据来源 */}
      <section className="py-12 px-4">
        <div className="max-w-6xl mx-auto">
          <h2 className="font-display text-3xl font-bold text-center mb-8">
            <span className="bg-gradient-to-r from-ark-cyan-400 to-ark-purple-400 bg-clip-text text-transparent">
              数据来源
            </span>
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <SourceCard
              name="Bilibili"
              description="视频攻略 · UP主推荐"
              color="from-pink-500 to-rose-500"
            />
            <SourceCard
              name="NGA论坛"
              description="玩家讨论 · 精华攻略"
              color="from-ark-purple-500 to-indigo-500"
            />
            <SourceCard
              name="森空岛"
              description="官方社区 · 玩家分享"
              color="from-ark-cyan-500 to-blue-500"
            />
          </div>
        </div>
      </section>
    </main>
  )
}

function StatCard({ icon, title, value, color, isText = false }: {
  icon: React.ReactNode
  title: string
  value: number | string
  color: 'purple' | 'cyan' | 'pink'
  isText?: boolean
}) {
  const colorClasses = {
    purple: 'from-ark-purple-600 to-ark-purple-400',
    cyan: 'from-ark-cyan-500 to-ark-cyan-300',
    pink: 'from-ark-pink-500 to-ark-pink-300',
  }

  return (
    <motion.div
      whileHover={{ scale: 1.02 }}
      className="glass rounded-2xl p-6"
    >
      <div className={`w-12 h-12 rounded-xl bg-gradient-to-r ${colorClasses[color]} flex items-center justify-center mb-4`}>
        {icon}
      </div>
      <p className="text-gray-400 text-sm mb-1">{title}</p>
      <p className={`font-display text-3xl font-bold ${isText ? 'text-lg' : ''}`}>
        {value}
      </p>
    </motion.div>
  )
}

function SourceCard({ name, description, color }: {
  name: string
  description: string
  color: string
}) {
  return (
    <motion.div
      whileHover={{ scale: 1.02, y: -5 }}
      className="gradient-border p-6"
    >
      <div className={`w-full h-2 rounded-full bg-gradient-to-r ${color} mb-4`} />
      <h3 className="font-display text-xl font-bold mb-2">{name}</h3>
      <p className="text-gray-400">{description}</p>
    </motion.div>
  )
}
