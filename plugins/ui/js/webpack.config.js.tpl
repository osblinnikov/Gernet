<%import parsing_js
from gernetHelpers import getFullName_, getClassName
p = reload(parsing_js)
p.parsingGernet(a)
%>

var path = require("path");
var webpack = require("webpack");
module.exports = {
  resolveLoader: { root: path.join(__dirname, "node_modules") },
  // This is the main file that should include all other JS files
  entry: "./src/scripts/main.coffee",
  target: "web",
  debug: true,
  // We are watching in the gulp.watch, so tell webpack not to watch
  watch: false,
  // watchDelay: 300,
  output: {
    path: path.join(__dirname, "ui", "assets"),
    publicPath: "/ui/assets/",
    // If you want to generate a filename with a hash of the content (for cache-busting)
    // filename: "main-[hash].js",
    filename: "main.js",
    chunkFilename: "[chunkhash].js"
  },
  resolve: {
    // Tell webpack to look for required files in bower and node
    modulesDirectories: ['bower_components', 'node_modules', 'dist', "${p.rootRelativePath(a).replace('/','\\\\').replace('\\','\\\\')}", "${p.rootRelativePath(a)}"],
  },
  module: {
    loaders: [
      { test: /bootstrap/, loader: 'imports?jQuery=jquery' },
      { test: /\.css/, loader: "style-loader!css-loader" },
      { test: /\.gif/, loader: "url-loader?limit=10000&minetype=image/gif" },
      { test: /\.jpg/, loader: "url-loader?limit=10000&minetype=image/jpg" },
      { test: /\.png/, loader: "url-loader?limit=10000&minetype=image/png" },
      { test: /\.woff$/,   loader: "url-loader?limit=10000&minetype=application/font-woff" },
      { test: /\.woff2(\?v=\d+\.\d+\.\d+)?$/, loader: "url-loader?limit=10000&mimetype=application/font-woff2" },
      { test: /\.ttf$/,    loader: "file-loader" },
      { test: /\.eot$/,    loader: "file-loader" },
      { test: /\.svg$/,    loader: "file-loader" },
      { test: /\.js$/, loader: "jsx-loader" },
      { test: /\.coffee$/, loader: "jsx-loader!coffee-loader" },
      { test: /\.scss$/, loader: "style!css!sass?outputStyle=expanded" },
      { test: /\.less$/, loader: "style-loader!css-loader!less-loader" }
    ],
    noParse: /\.min\.js/
  },
  plugins: [
    // If you want to minify everything
    // new webpack.optimize.UglifyJsPlugin()
  ]
};
