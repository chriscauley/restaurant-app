const alt_colors = ['bg', 'bg-alt', 'text', 'text-alt', 'border']

const colors = {}
alt_colors.forEach(c => (colors[c] = `var(--${c})`))

module.exports = {
  purge: false,
  theme: {
    extend: { colors },
    screens: {
      sm: '640px',
      md: '768px',
      lg: '1024px',
      xl: '1280px',
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
