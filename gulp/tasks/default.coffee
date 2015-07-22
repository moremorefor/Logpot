gulp        = require 'gulp'
browserSync = require 'browser-sync'
runSequence = require 'run-sequence'

gulp.task 'default', ['del'], ->
  runSequence(
    ['sass', 'coffee', 'copy'],
    'browser-sync',
    'watch'
  )
