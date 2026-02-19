/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './src/**/*.{astro,html,js,jsx,ts,tsx,vue,svelte,md,mdx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['"DM Sans"', 'ui-sans-serif', 'system-ui', '-apple-system', 'sans-serif'],
      },
      colors: {
        navy: {
          DEFAULT: '#0B1F3A',
          light: '#162D4E',
        },
        gold: '#C9A84C',
        offwhite: '#F7F5F1',
        midgrey: '#6B7280',
        border: '#E5E0D8',
      },
      letterSpacing: {
        label: '0.15em',
        nav: '0.05em',
      },
      lineHeight: {
        body: '1.7',
      },
    },
  },
  plugins: [],
};
