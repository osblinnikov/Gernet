path = require('path')
gulp = require('gulp')
gutil = require('gulp-util')
express = require('express')
node_static = require('node-static')
sass = require('gulp-sass')
minifyCSS = require('gulp-minify-css')
clean = require('gulp-clean')
watch = require('gulp-watch')
rev = require('gulp-rev')
tiny_lr = require('tiny-lr')
conn_lr = require("connect-livereload")
webpack = require("webpack")
sockjs = require('sockjs')
args   = require('yargs').argv

isProduction = if args.production then true else false
isTestNoRun = if args.testnorun then true else false

webpackConfig = require("./webpack.config.js")
if isProduction  # i.e. we were executed with a --production option
  webpackConfig.plugins = webpackConfig.plugins.concat(new webpack.optimize.UglifyJsPlugin())
  webpackConfig.output.filename = "main.js"
sassConfig = { includePaths : ['src/styles'] }

# paths to files in bower_components that should be copied to ui/assets/vendor
vendorPaths = ['es5-shim/es5-sham.min.js', 'es5-shim/es5-shim.min.js', 'es5-shim/es5-sham.map',
 'es5-shim/es5-shim.map']
#
# TASKS
#

gulp.task 'clean', ->
  gulp.src('ui', {read: false})
  .pipe(clean())

# main.scss should @include any other CSS you want
gulp.task 'sass', ->
  gulp.src('src/styles/main.scss')
  .pipe(sass(sassConfig).on('error', gutil.log))
  .pipe(if isProduction then minifyCSS() else gutil.noop())
  # .pipe(if isProduction then rev() else gutil.noop())
  .pipe(gulp.dest('ui/assets'))

# Some JS and CSS files we want to grab from Bower and put them in a ui/assets/vendor directory
# For example, the es5-sham.js is loaded in the HTML only for IE via a conditional comment.
gulp.task 'vendor', ->
  paths = vendorPaths.map (p) -> path.resolve("./bower_components", p)
  gulp.src(paths).pipe(gulp.dest('ui/assets/vendor'))

# Just copy over remaining assets to dist. Exclude the styles and scripts as we process those elsewhere
gulp.task 'copy', ->
  gulp.src(['src/**/*', '!src/scripts', '!src/scripts/**/*', '!src/styles', '!src/styles/**/*']).pipe(gulp.dest('ui'))

# This task lets Webpack take care of all the coffeescript and JSX transformations, defined in webpack.config.js
# Webpack also does its own uglification if we are in --production mode
gulp.task 'webpack', (callback) ->
  execWebpack(webpackConfig)
  callback()

gulp.task 'default', ['build'], ->
gulp.task 'build', ['webpack', 'sass', 'copy', 'vendor'], ->
gulp.task 'test', ['build'], ->
  if isTestNoRun
    return
  servers = createServers(4000, 35729)
  # When /src changes, fire off a rebuild
  gulp.watch ['./dist/**/*', './src/**/*','./test/specs-coffee/*'], (evt) -> gulp.run 'build'
  # When /ui changes, tell the browser to reload
  gulp.watch ['./ui/**/*'], (evt) ->
    gutil.log(gutil.colors.cyan(evt.path), 'changed')
    servers.lr.changed
      body:
        files: [evt.path]
gulp.task 'build-tests', ['build'], ->
  # Give first-time users a little help
  setTimeout ->
    gutil.log "**gulp [target] [options]*********************"
    gutil.log "* gulp              (build and run development server)"
    gutil.log "* gulp clean        (rm /ui)"
    gutil.log "* gulp build --production"
    gutil.log "*   targets: default, clean, build (aliases: build-tests, test)"
    gutil.log "*   options: --production"
    gutil.log "**********************************************"
  , 3000
#
# HELPERS
#


# Create both http server and livereload server
createServers = (port, lrport) ->
  lr = tiny_lr()
  lr.listen lrport, -> gutil.log("LiveReload listening on", lrport)

  app = false
  if port > 0
    # 1. Echo sockjs server
    sockjs_opts = sockjs_url: "http://cdn.sockjs.org/sockjs-0.3.min.js"
    sockjs_echo = sockjs.createServer(sockjs_opts)
    sockjs_echo.on "connection", (conn) ->
      conn.on "data", (message) ->
        gutil.log message
        return

      return


    # 2. Static files server
    app = express()
    app.use conn_lr()
    app.use(express.static(path.resolve("./")))
    app.listen port, ->
      gutil.log("HTTP server is listening")
      gutil.log("http://localhost:"+port+"/ui/")

    # 3. Usual http stuff
    app.get "/", (req, res) ->
      res.sendfile __dirname + "/README.md"

    sockjs_echo.installHandlers app,
      prefix: "/ws"


  lr: lr
  app: app

execWebpack = (config) ->
  webpack config, (err, stats) ->
    if (err) then throw new gutil.PluginError("execWebpack", err)
    gutil.log("[execWebpack]", stats.toString({colors: true}))