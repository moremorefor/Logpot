gulp        = require 'gulp'
sass        = require 'gulp-ruby-sass'
filter      = require 'gulp-filter'
pleeease    = require 'gulp-pleeease'
browserSync = require 'browser-sync'
config      = require '../config'
paths       = config.path

gulp.task 'sass', ->
  sassOptions =
    style      : 'nested'
    sourcemap  : false
  sass "#{paths.src.sass}", sassOptions
    .pipe pleeease(
      autoprefixer:
        browsers: ['last 4 versions']
      minifier: false
    )
    .pipe filter('*.css')
    .pipe gulp.dest( "#{paths.dest.sass}" )
    .pipe browserSync.reload({stream:true})

gulp.task 'sass2', ->
  sassOptions =
    style      : 'nested'
    sourcemap  : true
  sass "#{paths.src.sass2}", sassOptions
    .pipe pleeease(
      autoprefixer:
        browsers: ['last 4 versions']
      minifier: false
    )
    .pipe filter('*.css')
    .pipe gulp.dest( "#{paths.dest.sass}" )
    .pipe browserSync.reload({stream:true})
