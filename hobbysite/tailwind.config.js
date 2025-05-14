module.exports = {
    content: [
      './templates/**/*.html',  // This will scan your Django templates
      './static/**/*.js',       // This is for JS files in the static folder if you use Tailwind in JS

    ],
    theme: {
      extend: {
        fontFamily: {
          audiowide: ['Audiowide', 'sans-serif'],
          wadik: ['Wadik']
        },
      },
    },
    plugins: [],
  }