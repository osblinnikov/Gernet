isNode = typeof module isnt "undefined" and module.exports
if isNode
  s = {}
  s.Worker = require(__dirname + "/../../dist/Worker.js")
else
  s = self

describe "eval.js", ->
  it "should eval the given code", ->
    wrk = new s.Worker("/test/specs/eval.js")
    result = null
    done = false
    runs ->
      wrk.onmessage = (msg) ->
        result = msg.data
        done = true
        wrk.terminate()
        return

      wrk.postMessage ("postMessage(\"abc\")")
      return

    waitsFor (->
      done
    ), "should finish", 500
    runs ->
      expect(result).toEqual "abc"
      return

    return

  return
