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
    sourcemap  : true
  sass "#{paths.src.sass}", sassOptions
    .pipe pleeease(
      autoprefixer:
        browsers: ['last 4 versions']
      minifier: false
    )
    .pipe gulp.dest( "#{paths.dest.sass}" )
    .pipe filter('**/*.css')
    .pipe browserSync.reload({stream:true})
