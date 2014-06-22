isNode = typeof module isnt "undefined" and module.exports
if isNode
  s = {}
  s.mapBuffer = require(__dirname + "/../../dist/mapBuffer.js")
  s.Worker = require(__dirname + "/../../dist/Worker.js")
  s.Kernel = require(__dirname + "/../../dist/Kernel.js")
else
  s = self

describe "mapBuffer-send-receive-perf-multi", ->
  it "should send many messages during 3 seconds", ->
    expect(s.mapBuffer).toEqual jasmine.any(Function)
    expect(s.Worker).toEqual jasmine.any(Function)

    wrk0 = new s.Worker('/test/specs/mapBufferPerfMulti.sender.js')
    wrk1 = new s.Worker('/test/specs/mapBufferPerfMulti.sender.js')
    wrk2 = new s.Worker('/test/specs/mapBufferPerfMulti.sender.js')

    mBufferToSender = new s.mapBuffer()
    mBufferToSender.init(buffersLength = 200,uniqueId = 1006,readers_grid_size = 3, grid_id = 0)
    mBufferToSender.addConnection(undefined,undefined,undefined,wrk0,dstWrkPinId = 0,dstWrGridId = 0)
    mBufferToSender.addConnection(undefined,undefined,undefined,wrk1,dstWrkPinId = 0,dstWrGridId = 1)
    mBufferToSender.addConnection(undefined,undefined,undefined,wrk2,dstWrkPinId = 0,dstWrGridId = 2)
    mBufferToSender.syncConnections()

    mBufferFromSender = new s.mapBuffer()
    mBufferFromSender.init(buffersLength = 200,uniqueId = 1007,readers_grid_size = 1, grid_id = 0)
    mBufferFromSender.addConnection(wrk0,srcWrkPinId = 1,srcWrkGridId = 0,undefined,undefined,undefined)
    mBufferFromSender.addConnection(wrk1,srcWrkPinId = 1,srcWrkGridId = 1,undefined,undefined,undefined)
    mBufferFromSender.addConnection(wrk2,srcWrkPinId = 1,srcWrkGridId = 2,undefined,undefined,undefined)
    mBufferFromSender.syncConnections()

    done = false
    
    runs ->
      
      startTime = new Date().getTime()
      nextTickTime = startTime + 1000
      fps = 0
      errorsCntr = 0

      rootR1 = mBufferFromSender.getReader((bufId, target)->
        # console.log "recv"
        obj = rootR1.readNextWithMeta()
        if obj.data != null
          # console.log obj.writer_grid_id
          fps++
          curTime = new Date().getTime()
          if curTime > nextTickTime
            console.log "fps: "+fps+", failed writes:"+errorsCntr
            nextTickTime += 1000
            errorsCntr = 0
            fps = 0
          rootR1.readFinished()
      )



      requestAnimFrame = (->
        requestAnimationFrame = undefined
        if typeof window!= 'undefined'
          requestAnimationFrame = window.requestAnimationFrame or window.webkitRequestAnimationFrame or window.mozRequestAnimationFrame
        return requestAnimationFrame or (callback) ->
          setTimeout callback, 0
          return
      )()

      
      senderFunc = ->
        curTime = new Date().getTime()
        if curTime > startTime + 3000
          done = true
          return
        obj = rootW0.writeNext()
        if obj != null
          # console.log "send"
          rootW0.writeFinished()
          # senderFunc()
        else
          errorsCntr++
        #   requestAnimFrame senderFunc
      rootW0 = mBufferToSender.getWriter(senderFunc)
      for i in [0...buffersLength*2]
        senderFunc()

    waitsFor (->
      done
    ), "should finish", 5000