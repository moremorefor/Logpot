gulp         = require 'gulp'
sass         = require 'gulp-sass'
filter       = require 'gulp-filter'
postcss      = require 'gulp-postcss'
autoprefixer = require 'autoprefixer'
cssnano      = require 'cssnano'
sorting      = require 'postcss-sorting'
sortConfig   = require '../postcss-sorting.json'
browserSync  = require 'browser-sync'
config       = require '../config'
paths        = config.path

plugins = [
  autoprefixer(),
  cssnano({ preset: 'default' }),
  sorting(sortConfig)

]

gulp.task 'sass2', ->
  return gulp.src("#{paths.src.sass2}")
    .pipe(sass().on('error', sass.logError))
    .pipe postcss(plugins)
    .pipe gulp.dest( "#{paths.dest.sass}" )
    .pipe filter('**/*.css')
    .pipe browserSync.reload({stream:true})

gulp.task 'sass', gulp.series 'sass2', ->
  return gulp.src("#{paths.src.sass}")
    .pipe(sass().on('error', sass.logError))
    .pipe postcss(plugins)
    .pipe gulp.dest( "#{paths.dest.sass}" )
    .pipe filter('**/*.css')
    .pipe browserSync.reload({stream:true})