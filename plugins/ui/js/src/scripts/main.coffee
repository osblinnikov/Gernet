`/** @jsx React.DOM */`

# Bring in jQuery and React as a Bower component in the global namespace
require("script!react/react-with-addons.js")
require("script!jquery/jquery.js")
require("script!bootstrap/dist/js/bootstrap.js")
require("script!fastclick/lib/fastclick.js")
require("script!json2/json2.js")
require("script!lodash/dist/lodash.js")

require("!style!css!less!../styles/main.less")
require("!style!css!less!../styles/app.less")

window.addEventListener('load', ->
  FastClick.attach(document.body);
, false)


App = require("./components/App.coffee")
React.initializeTouchEvents(true);
React.renderComponent(`<App />`, document.getElementById('app'))