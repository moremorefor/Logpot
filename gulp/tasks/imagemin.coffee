gulp             = require 'gulp'
imageminPngquant = require 'imagemin-pngquant'
config           = require '../config'
paths            = config.path

gulp.task 'imagemin', ->
  pngquantOptions =
    quality: '80-90'
    speed: 1

  gulp
    .src "#{paths.src.img}"
    .pipe imageminPngquant( pngquantOptions )()
    .pipe gulp.dest( "#{paths.dest.img}" )
