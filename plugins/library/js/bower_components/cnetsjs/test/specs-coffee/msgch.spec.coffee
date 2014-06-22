isNode = typeof module isnt "undefined" and module.exports
if isNode
  s = {}
  s.MessageChannel = require(__dirname + "/../../dist/MessageChannel.js")
  s.Worker = require(__dirname + "/../../dist/Worker.js")
else
  s = self

describe "MessageChannel-API", ->
  it "should define the used API", ->
    expect(s.MessageChannel).toEqual jasmine.any(Function)
    ch = new s.MessageChannel()
    expect(ch.port1).toEqual jasmine.any(Object)
    expect(ch.port2).toEqual jasmine.any(Object)
    return

describe "MessageChannel-send", ->
  it "should send the given message", ->
    expect(s.MessageChannel).toEqual jasmine.any(Function)
    expect(s.Worker).toEqual jasmine.any(Function)
    ch = new s.MessageChannel()
    wrk1 = new s.Worker("/test/specs/msgch.sender.js")

    wrk1.postMessage("",[ch.port1])
    wrk2 = new s.Worker("/test/specs/msgch.receiver.js")
    wrk2.postMessage("",[ch.port2])
    result = null
    done = false
    runs ->
      wrk2.onmessage = (msg) ->
        result = msg.data
        done = true
        wrk2.terminate()
        return
        
      wrk1.postMessage ("abc")
      return

    waitsFor (->
      done
    ), "should finish", 2000
    runs ->
      expect(result).toEqual "abc"
      return