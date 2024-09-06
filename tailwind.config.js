/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/templates/app/**/*.html',
	'./static/src/**/*.css',
	'./node_modules/daisyui/**/*.js',
    // Add paths to other apps if necessary
  ],
  theme: {
    extend: {},
  },
  plugins: [
  //require("@tailwindcss/typography"),
  require('daisyui'),
  require('flowbite/plugin'),
  //require('@tailwindcss/forms'),
  ],
	daisyui: {
    themes: ["cupcake", "dark", "cmyk"],
  },
};