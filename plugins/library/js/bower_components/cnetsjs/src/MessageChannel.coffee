isNode = typeof module isnt "undefined" and module.exports
if isNode
  s = {}
else
  s = self

MessagePort = (anotherPort)->
  slf = this
  slf.anotherPort = anotherPort
  if slf.anotherPort
    slf.anotherPort.anotherPort = slf
  slf.isClosed = false
  listenersSize = 0
  listeners = {}
  listenersWithCapture = {}
  findListener = (type,listener, useCapture)->
    l = listeners[""+useCapture]
    if not l
      return false

    for i,v of l
      if v == type
        for t,tv of v
          if tv == listener
            return [i,t]
    return false

  slf.addEventListener = (type, listener, useCapture)->
    if slf.isClosed
      return
    if !findListener(type, listener, useCapture)
      l = listeners[""+useCapture]
      if not l
        l = listeners[""+useCapture] = {}
      if !l[type]
        l[type] = []
      l[type].push(listener)
      listenersSize++

  slf.removeEventListener = (type, listener, useCapture)->
    if slf.isClosed
      return
    r = findListener(type, listener, useCapture)
    if !r
      return
    listeners[""+useCapture][r[0]].splice(r[1], 1)
    listenersSize--
    if listeners[""+useCapture][r[0]].length == 0
      delete listeners[""+useCapture][r[0]]


  slf.dispatchEvent = (evt, pfResult)->
    # console.log "dispatchEvent slf.isClosed "+slf.isClosed
    if slf.isClosed
      return
    type = evt.type
    # console.log "dispatchEvent to host"
    if type == 'message' and "function" is typeof slf.onmessage
      # console.log "onMessage ok"
      slf.onmessage(evt)
    # else
      # console.log "no on message"
    if listenersSize <= 0
      return
    for useCapture,l of listeners
      if useCapture=="false" and not pfResult
        continue
      # console.log "dispatchEvent "+useCapture
      # l = listeners[useCapture]#for capturing
      for i,v of l
        if i == type
          for t,tv of v
            console.log tv
            tv(this,evt)

  slf.start = ->
    slf.isClosed = false

  slf.close = ->
    slf.isClosed = true

  slf.postMessage = (msg, ports)->
    slf.anotherPort.dispatchEvent({data:msg,ports:ports, type:'message'},true)
  true

if !s.MessageChannel
  s.MessageChannelArtificial = true
  s.MessageChannel = ->
    slf = this
    slf.port1 = new MessagePort(undefined)
    slf.port2 = new MessagePort(slf.port1)
    true
  if isNode
    module.exports = s.MessageChannel