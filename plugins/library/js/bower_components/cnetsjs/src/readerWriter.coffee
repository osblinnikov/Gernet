isNode = typeof module isnt "undefined" and module.exports
if isNode
  s = {}
else
  s = self

reader = (bufKernParam)->
  self = this
  self.buffer = bufKernParam
  self.readNextWithMeta = ()->
    if not self.buffer
      return {}
    #todo: add here special code for debuging data flow
    return self.buffer.target.readNextWithMeta(self.buffer)

  self.readNext = ()->
    if not self.buffer
      return 0
    #todo: add here special code for debuging data flow
    return self.buffer.target.readNext(self.buffer)

  self.readFinished = ->
    if not self.buffer
      return 0
    #todo: add here special code for debuging data flow
    return self.buffer.target.readFinished(self.buffer)

  self.size = ->
    if not self.buffer
      return 0
    return self.buffer.target.size(self.buffer)

  self.getGridId = ->
    if not self.buffer
      return 0
    return self.buffer.target.gridId

  self.timeout = ->
    if not self.buffer
      return 0
    return self.buffer.target.timeout(self.buffer)

  self.gridSize = ->
    if not self.buffer
      return 0
    return self.buffer.target.gridSize(self.buffer)

  self.uniqueId = ->
    if not self.buffer
      return 0
    return self.buffer.target.uniqueId(self.buffer)

  self.addSelector = (linkCont)->
    if not self.buffer
      return -1
    return self.buffer.target.addSelector(self.buffer, linkCont)
  true

writer = (bufKernParam)->
  self = this
  self.buffer = bufKernParam
  self.writeNext = (make_timeout)->
    if not self.buffer
      return 0
    #todo: add here special code for debuging data flow
    return self.buffer.target.writeNext(self.buffer, make_timeout)

  self.writeFinished = ->
    if not self.buffer
      return 0
    #todo: add here special code for debuging data flow
    return self.buffer.target.writeFinished(self.buffer)

  self.size = ->
    if not self.buffer
      return 0
    return self.buffer.target.size(self.buffer)

  self.getGridId = ->
    if not self.buffer
      return 0
    return self.buffer.target.gridId

  self.timeout = ->
    if not self.buffer
      return 0
    return self.buffer.target.timeout(self.buffer)

  self.gridSize = ->
    if not self.buffer
      return 0
    return self.buffer.target.gridSize(self.buffer)

  self.uniqueId = ->
    if not self.buffer
      return 0
    return self.buffer.target.uniqueId(self.buffer)

  self.copy = ->
    return new writer(self.buffer.copy())
  true

s.readerWriter =
  reader: reader
  writer: writer

if isNode
  module.exports = 
    reader: reader
    writer: writer