/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        hyper: {
          dark: '#0f172a',
          card: '#1e293b',
          text: '#f8fafc',
          accent: '#8b5cf6', // Violet
          success: '#10b981', // Emerald
          warning: '#f59e0b', // Amber
        }
      }
    },
  },
  plugins: [],
}