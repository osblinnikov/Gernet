`/** @jsx React.DOM */`

# Bring in jQuery and React as a Bower component in the global namespace
React = require("react")
FastClick = require("fastclick")
require("bootstrap")

window.addEventListener('load', ->
  FastClick.attach(document.body);
, false)

App = require("./components/App.coffee")
React.initializeTouchEvents(true)
React.render(`<App />`, document.getElementById('app'))