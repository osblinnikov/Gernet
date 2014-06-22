isNode = typeof module isnt "undefined" and module.exports
if isNode
  s = {}
  s.Worker = require(__dirname + "/../../dist/Worker.js")
else
  s = self

describe "WebWorker-API", ->
  it "should define the used API", ->
    expect(s.Worker).toEqual jasmine.any(Function)
    wrk = new s.Worker("/test/specs/eval.js")
    expect(wrk.postMessage).toEqual jasmine.any(Function)
    expect(wrk.terminate).toEqual jasmine.any(Function)
    wrk.terminate()
    return

  # if isNode
  #   it "should terminate correctly", ->
  #     wrk = new Worker(__dirname + "/../../dist/eval.js")
  #     done = false
  #     runs ->
  #       wrk.process.on "exit", ->
  #         done = true
  #         return

  #       wrk.terminate()
  #       return

  #     waitsFor (->
  #       done
  #     ), "terminating correctly", 500
  #     return

  return
