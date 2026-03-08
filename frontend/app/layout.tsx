import './globals.css'
import type { Metadata } from 'next'
import { Inter, Orbitron } from 'next/font/google'

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' })
const orbitron = Orbitron({ 
  subsets: ['latin'], 
  variable: '--font-orbitron',
  weight: ['400', '700', '900']
})

export const metadata: Metadata = {
  title: '明日方舟终末地 - 伊冯配队指南',
  description: '汇集B站、NGA、森空岛等多平台伊冯配队攻略，提供最新角色组合、装备配置与输出手法',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="zh-CN" className="dark">
      <body className={`${inter.variable} ${orbitron.variable} font-sans bg-ark-dark text-white`}>
        {children}
      </body>
    </html>
  )
}
