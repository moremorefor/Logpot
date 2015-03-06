gulp        = require 'gulp'
browserSync = require 'browser-sync'
config      = require '../config'
paths        = config.path

gulp.task 'browser-sync', ->
  browserSync
    # server:
    #   baseDir: "#{paths.dest.dir}"
    # ghostMode:
    #   location: true
    proxy: "localhost:5000"
