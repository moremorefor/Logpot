srcDir = 'logpot/static_src'
destDir = 'logpot/static'

path =
  src:
    dir    : srcDir
    sass   : srcDir + '/css/app.sass'
    sass2  : srcDir + '/css/admin.sass'
    html   : srcDir + '/*.html'
    img    : srcDir + '/img/*'
    coffee : './' + srcDir + '/js/*.coffee'
    bower  : srcDir + '/bower_components/**/*'
  dest:
    dir    : destDir
    sass   : destDir + '/css'
    html   : destDir
    img    : destDir + '/img'
    coffee : destDir + '/js'
  watch:
    sass   : srcDir + '/**/*.sass'
    scss   : srcDir + '/**/*.scss'
    coffee : srcDir + '/**/*.coffee'
    html   : srcDir + '/**/*.html'
    png    : srcDir + '/**/*.png'
    jpg    : srcDir + '/**/*.jpg'
    gif    : srcDir + '/**/*.gif'

module.exports =
  path: path
