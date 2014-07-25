

#[[[cog
#import cogging as c
#c.tpl(cog,templateFile,c.a(prefix=configFile))
#]]]

isNode = typeof module isnt "undefined" and module.exports
if isNode
  s = {}
else
  s = self

if isNode
  s.block0 = s.com_github_airutech_gernet_test_block0 = require(__dirname + "/../../dist/com_github_airutech_gernet_test_block0/block0.js")
  s.block3 = s.com_github_airutech_gernet_test_block3 = require(__dirname + "/../../dist/com_github_airutech_gernet_test_block3/block3.js")
  s.queue = s.com_github_airutech_cnets_queue = require(__dirname + "/../../dist/com_github_airutech_cnets_queue/queue.js")
  s.block4 = s.com_github_airutech_gernet_test_block4 = require(__dirname + "/../../dist/com_github_airutech_gernet_test_block4/block4.js")
  s.readerWriter = s.com_github_airutech_cnets_readerWriter = require(__dirname + "/../../dist/com_github_airutech_cnets_readerWriter/readerWriter.js")
  s.runnablesContainer = s.com_github_airutech_cnets_runnablesContainer = require(__dirname + "/../../dist/com_github_airutech_cnets_runnablesContainer/runnablesContainer.js")
  s.types = s.com_github_airutech_cnets_types = require(__dirname + "/../../dist/com_github_airutech_cnets_types/types.js")
  s.mapBuffer = s.com_github_airutech_cnets_mapBuffer = require(__dirname + "/../../dist/com_github_airutech_cnets_mapBuffer/mapBuffer.js")
  s.example = s.com_github_airutech_gernet_test_example = require(__dirname + "/../../dist/com_github_airutech_gernet_test_example/example.js")
#[[[end]]] (checksum: 277148ed38513011603010334b828e7b)

describe "example-send-receive", ->
  it "should send a message", ->
    expect(s.mapBuffer.create).toEqual jasmine.any(Function)
    expect(s.example.create).toEqual jasmine.any(Function)
    unsignedArr = new Array(2)
    buffers = new Array(2)
    mBufferToSender = new s.mapBuffer.create(buffers, 1000, 1)
    exampleObj = new s.example.create(unsignedArr,mBufferToSender)

    done = false
    runs ->
      mBufferToSender.syncRegister()
      exampleObj.onStart()
      setTimeout ->
        done = true
      , 3000

    waitsFor (->
      done
    ), "should finish", 5000

