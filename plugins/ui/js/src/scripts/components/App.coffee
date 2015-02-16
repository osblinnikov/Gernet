`/** @jsx React.DOM */`

React = require("react")

App = React.createClass
  
  render: () ->
    `(
      <div className="container">
        Hello World!
        <span className="glyphicon glyphicon-search" aria-hidden="true"></span>
        <div className="btn-group" role="group" aria-label="...">
          <button type="button" className="btn btn-default">1</button>
          <button type="button" className="btn btn-default">2</button>

          <div className="btn-group" role="group">
            <button type="button" className="btn btn-default dropdown-toggle" data-toggle="dropdown" aria-expanded="false">
              Dropdown
              <span className="caret"></span>
            </button>
            <ul className="dropdown-menu" role="menu">
              <li><a href="#">Dropdown link</a></li>
              <li><a href="#">Dropdown link</a></li>
            </ul>
          </div>
        </div>
      </div>
    )`

module.exports = App