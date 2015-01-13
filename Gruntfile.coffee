module.exports = (grunt) ->
  pkg = grunt.file.readJSON 'package.json'
  grunt.initConfig
    pkg: pkg

    connect:
      livereload:
        options:
          port: 35792
          hostname:'*'
    
    watch:
      jade:
        files: "logpot/templates/*.jade"
        tasks: []
        options:
          livereload: true
          nospawn: true
      stylus:
        files: ['logpot/static/css/*.styl', 'logpot/static/css/**/*.styl']
        tasks: ['stylus', 'cssmin']
        options:
          livereload: true
          nospawn: true
      coffee:
        files: 'logpot/static/js/*.coffee'
        tasks: ['coffee']
        options:
          livereload: true
          nospawn: true

    stylus:
      options:
        compress: yes
      compile:
        files: [{
          expand: yes
          cwd: 'logpot/static'
          src: [ '*.styl', '**/*.styl' ]
          dest: 'logpot/static'
          ext: '.css'
        }]

    coffee:
      compile:
        files: [{
          expand: yes
          cwd: 'logpot/static'
          src: 'js/*.coffee'
          dest: 'logpot/static'
          ext: '.js'
        }]


    coffeelint:
      options:
        arrow_spacing:
          level: 'error'
        colon_assignment_spacing:
          spacing: left: 0, right: 1
          level: 'error'
        cyclomatic_complexity:
          level: 'warn'
        empty_constructor_needs_parens:
          level: 'error'
        indentation:
          value: 2
        max_line_length:
          value: 99
        newlines_after_classes:
          level: 'error'
        no_empty_functions:
          level: 'warn'
        no_empty_param_list:
          level: 'error'
        no_interpolation_in_single_quotes:
          level: 'warn'
        no_unnecessary_double_quotes:
          level: 'warn'
        no_unnecessary_fat_arrows:
          level: 'error'
        space_operators:
          level: 'warn'
      assets:
        files: [{
          expand: yes
          cwd: 'logpot/static'
          src: [ '*.coffee', '**/*.coffee' ]
        }]

    uglify:
      compile:
        files: [{
          expand: yes
          cwd: 'logpot/static'
          src: [ '*.js', '!**/*.js' ]
          dest: 'logpot/static'
        }]

    cssmin:
      compress:
        files:
          'logpot/static/css/min.css': ['logpot/static/css/style.css']

    kss: 
      options:
        includeType: 'stylus',
        # includePath: 'logpot/static/css/style.styl'
      dist: 
          files:
            'doc/styleguide/': ['logpot/static/css/']


  grunt.loadNpmTasks 'grunt-contrib-copy'
  grunt.loadNpmTasks 'grunt-contrib-jade'
  grunt.loadNpmTasks 'grunt-contrib-coffee'
  grunt.loadNpmTasks 'grunt-contrib-stylus'
  grunt.loadNpmTasks 'grunt-contrib-uglify'
  grunt.loadNpmTasks 'grunt-contrib-compress'
  grunt.loadNpmTasks 'grunt-coffeelint'
  grunt.loadNpmTasks 'grunt-notify'
  grunt.loadNpmTasks 'grunt-contrib-connect'
  grunt.loadNpmTasks 'grunt-contrib-watch'
  grunt.loadNpmTasks 'grunt-contrib-cssmin'
  grunt.loadNpmTasks 'grunt-kss'

  grunt.registerTask 'default', [
    'stylus', 'coffeelint', 'coffee', 'uglify', 'cssmin', 'connect', 'watch'
  ]

  grunt.registerTask 'styleguide', [
    'kss'
  ]
        

