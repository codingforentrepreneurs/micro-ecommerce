/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    "./src/**/*.{html,js}",
    "./node_modules/flowbite/**/*.js",
    // "./src/products/forms.py"
    "./src/**/forms.py",   
  ],
  theme: {
    extend: {},
  },
  plugins: [
      require('flowbite/plugin')
  ]
}
