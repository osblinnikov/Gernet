isNode = typeof module isnt "undefined" and module.exports
if isNode
  s = {}
else
  s = self

s.Kernel = (binds)->
  if typeof binds != 'array'
    binds = [binds]
  slf = this
  slf.bindObjects = binds

  slf.mapBuffers = []
  slf.isStarted = false
  slf.directPortId = undefined

  slf.addBuffer = (buf)->
    slf.mapBuffers.push(buf)

  slf.onStart = undefined
  slf.onStop = undefined

  slf.postMessage = (msg)->
    # slf.bindObjectsPostMessage[0].bind(slf.bindObjects[0])(msg)
    if slf.bindObjects[0].internalWorker
      slf.bindObjects[0].internalWorker.postMessage(msg)
    else
      slf.bindObjects[0].postMessage(msg)

  slf.onmessage = (e)->
    for i in [0...slf.bindObjects.length]
      if slf.bindObjects[i].internalWorker
        slf.bindObjects[i].internalWorker.onmessage(e)
      else
        slf.bindObjects[i].onmessage(e)

  onMessageCallback = (e)->
    # console.log "onMessageCallback "+e.data.bufId+" "+e.data.type
    if e.data.type == 'stop'
      if slf.isStarted
        slf.isStarted = false
        if slf.onStop
          slf.onStop()
        if self.close
          self.close()
        else
          console.error  "Kernel: onStop: I can't stop myself, no close() method found!"
    if typeof e.data.bufId!='undefined'
      if !slf.isStarted and e.data.type != 'create'
        if slf.onStart
          slf.onStart()
        slf.isStarted = true
      # console.log e
      if typeof slf.directPortId != 'undefined'
        e.data.portId = slf.directPortId
      slf.mapBuffers[e.data.bufId].dispatchMessage(e)

  for i in [0...slf.bindObjects.length]
    if slf.bindObjects[i].internalWorker
      slf.bindObjects[i].internalWorker.onmessage = onMessageCallback
    else
      slf.bindObjects[i].onmessage = onMessageCallback

  true

if isNode
  module.exports = s.Kernel