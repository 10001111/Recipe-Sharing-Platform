/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#ff6b6b',
          dark: '#ee5a6f',
        },
        secondary: {
          DEFAULT: '#4ecdc4',
        },
        text: {
          DEFAULT: '#333',
          light: '#666',
        },
        bg: {
          DEFAULT: '#f8f9fa',
        },
        card: {
          DEFAULT: '#ffffff',
        },
        border: {
          DEFAULT: '#e0e0e0',
        },
      },
      boxShadow: {
        'card': '0 2px 8px rgba(0, 0, 0, 0.1)',
        'card-hover': '0 4px 16px rgba(0, 0, 0, 0.15)',
      },
    },
  },
  plugins: [],
}

