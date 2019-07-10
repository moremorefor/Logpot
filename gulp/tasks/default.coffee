gulp        = require 'gulp'
browserSync = require 'browser-sync'

gulp.task 'default', gulp.series(
  'del',
  gulp.parallel(
    'sass', 'coffee', 'copy'
  ),
  'browser-sync',
  'watch'
)