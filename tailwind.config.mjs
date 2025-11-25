/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './src/**/*.{astro,html,js,jsx,ts,tsx,vue,svelte,md,mdx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', 'Segoe UI', 'Helvetica', 'Arial', 'Apple Color Emoji', 'Segoe UI Emoji'],
        heading: ['"Space Grotesk"', 'Inter', 'ui-sans-serif', 'system-ui'],
      },
      colors: {
        brand: {
          teal: '#0F2A43', // Primary (legacy key 'teal')
          light: '#B9BDC2', // Support
          coral: '#B48A3C', // Accent
        },
        primary: '#0F2A43',
        support: '#B9BDC2',
        accent: '#B48A3C',
      },
    },
  },
  plugins: [],
};


