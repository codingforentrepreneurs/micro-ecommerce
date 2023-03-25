/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{html,js}",
    "./node_modules/flowbite/**/*.js",
    "./src/**/forms.py",
  ],
  theme: {
    extend: {},
  },
  plugins: [
      require('flowbite/plugin')
  ]
}
