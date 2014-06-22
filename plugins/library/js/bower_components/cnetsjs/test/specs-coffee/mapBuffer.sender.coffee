importScripts( 
  '/dist/Kernel.js',
  '/dist/readerWriter.js',
  '/dist/cnetsjsTypes.js',
  '/dist/MessageChannel.js',
  '/dist/mapBuffer.js'
)

_this = new Kernel(this)

_this.onStart = ->
  console.log "onStart"

receivedData = null

onRun = (mapBufferId, mapBufferObj)->
  switch mapBufferId
    when 0
      # console.log "onRun _bufferToReadTest"
      r = readersWriters[mapBufferId].readNext()
      if r != null
        receivedData = r.obj
        readersWriters[mapBufferId].readFinished()
        onSend()
    when 1
      console.log "onRun _bufferToWriteTest"
    else
      console.log "onRun, unknown buffer"

onSend = ->
  if receivedData == null
    return
  r = readersWriters[1].writeNext()
  if r!=null
    r.obj = receivedData
    readersWriters[1].writeFinished()
    receivedData = null
  else
    setTimeout(onSend,100)

_this.onStop = ->
  console.log "onStop"

bId = 0
readersWriters = {}

_bufferToReadTest = new mapBuffer(bId, _this)
readersWriters[bId++] = _bufferToReadTest.getReader(onRun)

_bufferToWriteTest = new mapBuffer(bId, _this)
readersWriters[bId++] = _bufferToWriteTest.getWriter()