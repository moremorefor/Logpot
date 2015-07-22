gulp        = require 'gulp'
browserSync = require 'browser-sync'
config      = require '../config'
paths        = config.path

gulp.task 'copy', ['imagemin'], ->
  gulp
    .src [ "#{paths.src.html}", "#{paths.src.img}", "#{paths.src.bower}" ], { base: "#{paths.src.dir}" }
    .pipe gulp.dest( "#{paths.dest.dir}" )
    .pipe browserSync.reload({stream:true})
