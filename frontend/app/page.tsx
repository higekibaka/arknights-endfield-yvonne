'use client'

import { motion } from 'framer-motion'
import { useEffect, useState } from 'react'
import { Sparkles, Users, Sword, Clock, ExternalLink } from 'lucide-react'
import Link from 'next/link'

interface Stats {
  total_teams: number
  total_equipment: number
  recent_teams_7d: number
  platform_distribution: Record<string, number>
  last_updated: string
}

interface TeamComposition {
  id: number
  name: string
  characters: Array<{ name: string; role?: string }>
  source_platform: string
  author?: string
  rating: number
  created_at: string
}

const API_BASE = 'http://localhost:8181'

export default function Home() {
  const [stats, setStats] = useState<Stats | null>(null)
  const [teams, setTeams] = useState<TeamComposition[]>([])
  const [loadingTeams, setLoadingTeams] = useState(true)

  useEffect(() => {
    // 获取统计 + 最新配队（首页最小闭环）
    Promise.all([
      fetch(`${API_BASE}/api/stats`).then(res => res.json()),
      fetch(`${API_BASE}/api/teams?limit=3`).then(res => res.json()),
    ])
      .then(([statsData, teamsData]) => {
        setStats(statsData)
        setTeams(Array.isArray(teamsData) ? teamsData : [])
      })
      .catch(err => {
        console.error('首页数据获取失败:', err)
      })
      .finally(() => {
        setLoadingTeams(false)
      })
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

      {/* 最新配队 */}
      <section className="py-6 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="flex items-center justify-between mb-6">
            <h2 className="font-display text-3xl font-bold">
              <span className="bg-gradient-to-r from-ark-purple-400 to-ark-cyan-400 bg-clip-text text-transparent">
                最新配队
              </span>
            </h2>
            <Link href="/teams" className="text-ark-cyan-300 hover:text-ark-cyan-200 text-sm inline-flex items-center gap-1">
              查看全部 <ExternalLink className="w-4 h-4" />
            </Link>
          </div>

          {loadingTeams ? (
            <div className="glass rounded-2xl p-8 text-center text-gray-400">加载中...</div>
          ) : teams.length === 0 ? (
            <div className="glass rounded-2xl p-8 text-center text-gray-400">
              暂无配队数据，先去执行一次抓取或导入示例数据。
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {teams.map(team => (
                <TeamCard key={team.id} team={team} />
              ))}
            </div>
          )}
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

function TeamCard({ team }: { team: TeamComposition }) {
  const topCharacters = team.characters?.slice(0, 4) || []

  return (
    <motion.div
      whileHover={{ scale: 1.02, y: -4 }}
      className="glass rounded-2xl p-5 border border-white/10"
    >
      <div className="flex items-center justify-between mb-3">
        <span className="text-xs px-2 py-1 rounded-full bg-ark-purple-600/40 text-ark-purple-200">
          {team.source_platform}
        </span>
        <span className="text-xs text-amber-300">★ {team.rating.toFixed(1)}</span>
      </div>

      <h3 className="font-display text-lg font-bold mb-3 line-clamp-2">{team.name}</h3>

      <div className="flex flex-wrap gap-2 mb-4">
        {topCharacters.map((character, idx) => (
          <span key={`${character.name}-${idx}`} className="text-xs px-2 py-1 rounded bg-white/10 text-gray-200">
            {character.name}
            {character.role ? ` · ${character.role}` : ''}
          </span>
        ))}
      </div>

      <div className="text-xs text-gray-400 flex items-center justify-between">
        <span>{team.author || '匿名作者'}</span>
        <span>{new Date(team.created_at).toLocaleDateString()}</span>
      </div>
    </motion.div>
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
