<%import parsing_js
from gernetHelpers import getFullName_, getClassName
p = reload(parsing_js)
p.parsingGernet(a)
%>

path = require('path')
gulp = require('gulp')
gutil = require('gulp-util')
express = require('express')
node_static = require('node-static')
less = require('gulp-less')
# minifyCSS = require('gulp-minify-css')
del = require('del')
watch = require('gulp-watch')
tiny_lr = require('tiny-lr')
conn_lr = require("connect-livereload")
webpack = require("webpack")
#sockjs = require('sockjs')
args   = require('yargs').argv
LessPluginCleanCSS = require('less-plugin-clean-css') 
lessPlugins = []

isProduction = if args.production then true else false
isTestNoRun = if args.testnorun then true else false


webpackConfig = require("./webpack.config.js")

http = require('http')
React = require('react')
fs = require('fs')
erequire = require('enhanced-require')(module, webpackConfig)

App = undefined
Styles = ""
indexHtml = "index.html is not loaded, contact administrator please"
mainJs = ""


if isProduction
  webpackConfig.plugins = webpackConfig.plugins.concat(new webpack.optimize.UglifyJsPlugin(opts))

getWebPackConfig = (target)->
  webpackConfig.target = target
  if webpackConfig.target == 'node'
    webpackConfig.entry = "./src/scripts/components/App.coffee"
    webpackConfig.output.path = path.join(__dirname, "server", "assets")
  else
    webpackConfig.entry = "./src/scripts/main.coffee"
    webpackConfig.output.path = path.join(__dirname, "ui", "assets")
  return webpackConfig

if isProduction  # i.e. we were executed with a --production option
  lessPlugins = lessPlugins.concat(new LessPluginCleanCSS({ advanced: true }))
  opts =
    mangle: true
    compress:
      sequences: true
      dead_code: true
      conditionals: true
      booleans: true
      unused: true
      if_return: true
      join_vars: true
      drop_console: true
      drop_debugger: true
      warnings: false

# sassConfig = { includePaths : ['src/styles'] }

# paths to files in bower_components that should be copied to ui/assets/vendor
vendorPaths = ['es5-shim/es5-sham.min.js', 'es5-shim/es5-shim.min.js', 'es5-shim/es5-sham.map',
 'es5-shim/es5-shim.map']
#
# TASKS
#

gulp.task 'clean', (cb)->
  del(['ui'], cb)

# main.scss should @include any other CSS you want
# gulp.task 'sass', ->
#   gulp.src('src/styles/main.scss')
#   .pipe(sass(sassConfig).on('error', gutil.log))
#   .pipe(if isProduction then minifyCSS() else gutil.noop())
#   # .pipe(if isProduction then rev() else gutil.noop())
#   .pipe(gulp.dest('ui/assets'))

# Some JS and CSS files we want to grab from Bower and put them in a ui/assets/vendor directory
# For example, the es5-sham.js is loaded in the HTML only for IE via a conditional comment.
gulp.task 'vendor', ->
  paths = vendorPaths.map (p) -> path.resolve("./node_modules", p)
  gulp.src(paths).pipe(gulp.dest('ui/assets/vendor'))

# Just copy over remaining assets to dist. Exclude the styles and scripts as we process those elsewhere
gulp.task 'copy', ->
  gulp.src(['src/**/*', '!src/scripts', '!src/scripts/**/*', '!src/styles', '!src/styles/**/*']).pipe(gulp.dest('ui'))

gulp.task 'less', ->
  gulp.src('src/styles/main.less').pipe(less({plugins: lessPlugins, paths: [ path.join(__dirname,'node_modules'), path.join(__dirname, "${p.rootRelativePath(a)}") ]})).pipe(gulp.dest('./ui/styles'))

# This task lets Webpack take care of all the coffeescript and JSX transformations, defined in webpack.config.js
# Webpack also does its own uglification if we are in --production mode
gulp.task 'webpack', (callback) ->
  execWebpack(getWebPackConfig('web'))
  #execWebpack(getWebPackConfig('node'))
  callback()

gulp.task 'default', ['build'], ->
gulp.task 'build', ['webpack', 'copy', 'vendor', 'less'], ->
gulp.task 'test', ['build'], ->
  if isTestNoRun
    return
  servers = createServers(4000, 35729)
  # When /src changes, fire off a rebuild
  gulp.watch ['./dist/**/*', './src/**/*','./test/specs-coffee/*'], ['build']
  # When /ui changes, tell the browser to reload
  gulp.watch ['./ui/**/*'], (evt) ->
    gutil.log(gutil.colors.cyan(evt.path), 'changed')

    App = React.createFactory(erequire(path.join(__dirname, 'src', 'scripts', 'components', 'App.coffee')))
    indexHtml = fs.readFileSync(path.join(__dirname, 'src', 'index.html'), 'utf-8')
    Styles = fs.readFileSync(path.join(__dirname, 'ui', 'styles', 'main.css'), 'utf-8')
    mainJs = fs.readFileSync(path.join(__dirname, 'ui', 'assets', 'main.js'), 'utf-8')

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
    # sockjs_opts = sockjs_url: "http://cdn.sockjs.org/sockjs-0.3.min.js"
    # sockjs_echo = sockjs.createServer(sockjs_opts)
    # sockjs_echo.on "connection", (conn) ->
    #  conn.on "data", (message) ->
    #    gutil.log message
    #    return
    #
    #  return


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

    # sockjs_echo.installHandlers app,
    #   prefix: "/ws"

    renderServer = http.createServer((req, res) ->
      if req.url == '/assets/main.js'
        res.setHeader 'Content-Type', 'text/javascript'
        res.end mainJs
      else if req.url == '/styles/main.css'
        res.setHeader 'Content-Type', 'text/css'
        res.end Styles
      else if req.url.indexOf('/node_modules') == 0
        res.end fs.readFileSync(req.url.substring(1))
      else
        if App
          markup = React.renderToString(App())
          html = indexHtml.replace('<p>If you can see this, something is broken (or JS is not enabled)..</p>', markup)
        else
          html = "Server side Application is not loaded, please contact administrator"
        res.setHeader 'Content-Type', 'text/html'
        res.end html
      # The http server listens on port 3000
      return
    ).listen port+1
    gutil.log("Render Server listening")
    gutil.log("http://localhost:"+(port+1)+"/")

  lr: lr
  app: app
  renderServer: renderServer

execWebpack = (config) ->
  webpack config, (err, stats) ->
    if (err) then throw new gutil.PluginError("execWebpack", err)
    gutil.log("[execWebpack]", stats.toString({colors: true}))