gulp        = require 'gulp'
coffee      = require 'gulp-coffee'
plumber     = require 'gulp-plumber'
browserSync = require 'browser-sync'
config      = require '../config'
paths       = config.path

gulp.task 'coffee', ->
  gulp
    .src "#{paths.src.coffee}"
    .pipe plumber()
    .pipe coffee()
    .pipe gulp.dest("#{paths.dest.coffee}")
    .pipe browserSync.reload({stream:true})
