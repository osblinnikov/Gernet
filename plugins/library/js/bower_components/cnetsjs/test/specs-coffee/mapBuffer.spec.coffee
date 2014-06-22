isNode = typeof module isnt "undefined" and module.exports
if isNode
  s = {}
  s.mapBuffer = require(__dirname + "/../../dist/mapBuffer.js")
  s.Worker = require(__dirname + "/../../dist/Worker.js")
else
  s = self

describe "mapBuffer-API", ->
  it "should define the used API", ->
    expect(s.mapBuffer).toEqual jasmine.any(Function)
    m = new s.mapBuffer()
    expect(m.dispatchMessage).toEqual jasmine.any(Function)
    expect(m.getReader).toEqual jasmine.any(Function)
    expect(m.getWriter).toEqual jasmine.any(Function)
    expect(m.readNext).toEqual jasmine.any(Function)
    expect(m.readNextWithMeta).toEqual jasmine.any(Function)
    expect(m.readFinished).toEqual jasmine.any(Function)
    expect(m.writeNext).toEqual jasmine.any(Function)
    expect(m.writeFinished).toEqual jasmine.any(Function)
    expect(m.size).toEqual jasmine.any(Function)
    expect(m.gridSize).toEqual jasmine.any(Function)
    expect(m.uniqueId).toEqual jasmine.any(Function)
    expect(m.init).toEqual jasmine.any(Function)
    expect(m.addConnection).toEqual jasmine.any(Function)
    expect(m.syncConnections).toEqual jasmine.any(Function)
    return

describe "mapBuffer-send-receive", ->
  it "should send the given message", ->
    expect(s.mapBuffer).toEqual jasmine.any(Function)
    expect(s.Worker).toEqual jasmine.any(Function)

    wrk0 = new s.Worker('/test/specs/mapBuffer.sender.js')
    wrk1 = new s.Worker('/test/specs/mapBuffer.receiver.js')
    
    mBufferToSender = new s.mapBuffer()
    mBufferToSender.init(buffersLength = 2,uniqueId = 1000,readers_grid_size = 1)
    mBufferToSender.addConnection(undefined,undefined,undefined,wrk0,dstWrkPinId = 0,dstWrGridId = 0)
    mBufferToSender.syncConnections()

    mBufferExchange = new s.mapBuffer()
    mBufferExchange.init(buffersLength = 2,uniqueId = 1001,readers_grid_size = 1)
    mBufferExchange.addConnection(wrk0,srcWrkPinId = 1,srcWrkGridId = 0,wrk1,dstWrkPinId = 0,dstWrGridId = 0)
    mBufferExchange.syncConnections()

    mBufferFromReceiver = new s.mapBuffer()
    mBufferFromReceiver.init(buffersLength = 2,uniqueId = 1002,readers_grid_size = 1)
    mBufferFromReceiver.addConnection(wrk1,srcWrkPinId = 1,srcWrkGridId = 0,undefined,undefined,undefined)
    mBufferFromReceiver.syncConnections()
    
    done = false
    result = undefined
    runs ->
      rootR1 = mBufferFromReceiver.getReader((bufId, target)->
        # console.log "recevied!!!!!!!! eeee"
        done = true
        obj = rootR1.readNext()
        if obj != null
          result = obj.obj
          console.log "successfuly read message:"+result
          rootR1.readFinished()
      )

      rootW0 = mBufferToSender.getWriter()
      obj = rootW0.writeNext()
      if obj != null
        console.log "write Next OK"
        obj.obj = "Test Should Be Passed"
        rootW0.writeFinished()

      

    waitsFor (->
      done
    ), "should finish", 2000
    
    # wrk0.postMessage({type:'stop'})
    # wrk1.postMessage({type:'stop'})

    runs ->
      expect(result).toEqual "Test Should Be Passed"
      return

