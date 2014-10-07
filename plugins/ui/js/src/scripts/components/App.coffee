`/** @jsx React.DOM */`

SetIntervalMixin = require("./SetIntervalMixin.coffee")

App = React.createClass
  getDefaultProps: ->
    return

  mixins: [SetIntervalMixin]

  getInitialState: ->
    orientation = window.orientation
    orientation = 0 unless orientation
    state = _.merge({previousOrientation: orientation}, @getDimensions())
    return state

  getDimensions: ->
    try
      node = $(@getDOMNode()).parent()
      parentNode = 
        innerHeight: node.height()
        innerWidth: node.width()
    catch
      parentNode = window
      
    style: 
      height: if parentNode.innerHeight then parentNode.innerHeight else 768
      width: if parentNode.innerWidth then parentNode.innerWidth else 1024
      
  updateDimensions: ->
    @setState _.merge(@state, @getDimensions())

  checkOrientation: ->
    orientation = window.orientation
    orientation = 0 unless orientation
    if orientation isnt @state.previousOrientation
      @state.previousOrientation = orientation
      @updateDimensions()

  componentDidMount: ->
    window.addEventListener "resize", @updateDimensions
    window.addEventListener "orientationchange", @updateDimensions
    @setInterval @checkOrientation, 2000
    @updateDimensions()

  componentWillUnmount: ->
    window.removeEventListener "resize", @updateDimensions
    window.removeEventListener "orientationchange", @updateDimensions
  
  render: () ->
    `(
      <div style={this.state.style} className="container">
        Hello World!
      </div>
    )`

module.exports = App