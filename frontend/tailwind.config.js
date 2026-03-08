/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // 主题色彩 - 科幻霓虹风格
        'ark-dark': '#0a0a0f',
        'ark-purple': {
          900: '#1a0b2e',
          800: '#2d1b4e',
          700: '#4c1d95',
          600: '#5b21b6',
          500: '#7c3aed',
          400: '#8b5cf6',
          300: '#a78bfa',
        },
        'ark-cyan': {
          500: '#06b6d4',
          400: '#22d3ee',
          300: '#67e8f9',
        },
        'ark-pink': {
          500: '#ec4899',
          400: '#f472b6',
          300: '#f9a8d4',
        },
      },
      fontFamily: {
        'display': ['Orbitron', 'sans-serif'],
        'body': ['Inter', 'sans-serif'],
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic': 'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
        'hero-gradient': 'linear-gradient(135deg, #1a0b2e 0%, #2d1b4e 50%, #0a0a0f 100%)',
      },
      animation: {
        'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
        'float': 'float 6s ease-in-out infinite',
      },
      keyframes: {
        glow: {
          '0%': { boxShadow: '0 0 5px #7c3aed, 0 0 10px #7c3aed' },
          '100%': { boxShadow: '0 0 20px #7c3aed, 0 0 30px #7c3aed, 0 0 40px #06b6d4' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-20px)' },
        },
      },
    },
  },
  plugins: [],
}
