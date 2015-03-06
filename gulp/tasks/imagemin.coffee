gulp     = require 'gulp'
imagemin = require 'gulp-imagemin'
config   = require '../config'
paths    = config.path

gulp.task 'imagemin', ->
  imageminOptions =
    optimizationLevel: 7

  gulp
    .src "#{paths.src.img}"
    .pipe imagemin( imageminOptions )
    .pipe gulp.dest( "#{paths.dest.img}" )
