jslibs_path = [
  'jquery/dist/jquery.js'
  'bootstrap/dist/js/bootstrap.js'
  'angular/angular.js'
  'angular-animate/angular-animate.js'
  'angular-route/angular-route.js'
  'ngprogress/build/ngProgress.js'
  'angular-bootstrap/ui-bootstrap.js'
  'angular-bootstrap/ui-bootstrap-tpls.js'
]
jslibs_path = ("bower_components/#{path}" for path in jslibs_path)

csslibs_path = [
  'bootstrap/dist/css/bootstrap.css'
  'ngprogress/ngProgress.css'
]
csslibs_path = ("bower_components/#{path}" for path in csslibs_path)
csslibs_path.push 'sass/fontello.css'


module.exports = (grunt) ->
  # Project configuration.
  config =
    pkg: grunt.file.readJSON 'package.json'
    concat:
      libJs:
        files:
          'js/lib.js': jslibs_path
      libCss:
        files:
          'css/lib.css': csslibs_path
      appJs:
        files:
          'js/app.js': [
            'js/services.js', 'js/app.js', 'js/config.js',
            'js/apptmpl.js', 'js/directives.js', 'js/controllers.js',
            'js/global.js'
          ]
    coffee:
      app:
        options:
          join: true
        files:
          'js/services.js': []
          'js/directives.js': ['coffee/directives/**/*.coffee']
          'js/controllers.js': ['coffee/controllers/**/*.coffee']
          'js/config.js': ['coffee/config/**/*.coffee']
          'js/app.js': ['coffee/app.coffee']
          'js/utils.js': []
          'js/disqus.js': ['coffee/disqus.coffee']
    uglify:
      options:
        banner: '/*! <%= pkg.name %> <%= grunt.template.today("yyyy-mm-dd") %> */\n'
      app:
        options:
          sourceMap: true
          sourceMapName: 'js/app.map'
        files:
          'js/app.min.js': 'js/app.js'
      lib:
        options:
          sourceMap: true
          sourceMapName: 'js/lib.map'
        src: 'js/lib.js',
        dest: 'js/lib.min.js'
    cssmin:
      lib:
        files:
          'css/lib.min.css': ['css/lib.css']
      app:
        files:
          'css/app.min.css': ['css/app.css']
    clean:
      all: ['js', 'css']

    sass:
      build:
        files:
          'css/app.css': 'sass/app.sass'

    ngtemplates:
      'sblogApp':
        src: ['templates/*.html', 'templates/**/*.html']
        dest: 'js/apptmpl.js'
        options:
          htmlmin:
            collapseWhitespace: true
            collapseBooleanAttributes: true
          url: (url) ->
            return url.replace 'templates/', ''

  grunt.initConfig config

  # Load the plugin that provides the "uglify" task.
  grunt.loadNpmTasks 'grunt-contrib-concat'
  grunt.loadNpmTasks 'grunt-contrib-coffee'
  grunt.loadNpmTasks 'grunt-contrib-uglify'
  grunt.loadNpmTasks 'grunt-contrib-cssmin'
  grunt.loadNpmTasks 'grunt-contrib-sass'
  grunt.loadNpmTasks 'grunt-contrib-clean'
  # grunt.loadNpmTasks 'grunt-contrib-copy'
  grunt.loadNpmTasks 'grunt-angular-templates'

  # Default task(s).
  grunt.registerTask 'dev', ['ngtemplates', 'coffee', 'concat:appJs', 'uglify:app', 'sass', 'cssmin:app']
  grunt.registerTask 'default', ['ngtemplates', 'coffee', 'concat', 'uglify', 'sass', 'cssmin']
  grunt.registerTask 'all', ['clean', 'ngtemplates', 'coffee', 'sass', 'concat', 'uglify', 'cssmin']
