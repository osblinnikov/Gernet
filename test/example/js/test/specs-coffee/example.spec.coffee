

#[[[cog
#import cogging as c
#c.tpl(cog,templateFile,c.a(prefix=configFile))
#]]]

isNode = typeof module isnt "undefined" and module.exports and process and process.title != 'browser'
if isNode
  s = {}
else
  s = self

if isNode
  s.types = s.com_github_osblinnikov_cnets_types = require(__dirname + "/../../dist/com_github_osblinnikov_cnets_types/types.js")
  s.block0 = s.com_github_osblinnikov_gernet_test_block0 = require(__dirname + "/../../dist/com_github_osblinnikov_gernet_test_block0/block0.js")
  s.readerWriter = s.com_github_osblinnikov_cnets_readerWriter = require(__dirname + "/../../dist/com_github_osblinnikov_cnets_readerWriter/readerWriter.js")
  s.block4 = s.com_github_osblinnikov_gernet_test_block4 = require(__dirname + "/../../dist/com_github_osblinnikov_gernet_test_block4/block4.js")
  s.block3 = s.com_github_osblinnikov_gernet_test_block3 = require(__dirname + "/../../dist/com_github_osblinnikov_gernet_test_block3/block3.js")
  s.queue = s.com_github_osblinnikov_cnets_queue = require(__dirname + "/../../dist/com_github_osblinnikov_cnets_queue/queue.js")
  s.mapBuffer = s.com_github_osblinnikov_cnets_mapBuffer = require(__dirname + "/../../dist/com_github_osblinnikov_cnets_mapBuffer/mapBuffer.js")
  s.runnablesContainer = s.com_github_osblinnikov_cnets_runnablesContainer = require(__dirname + "/../../dist/com_github_osblinnikov_cnets_runnablesContainer/runnablesContainer.js")
  s.mapBuffer = s.com_github_osblinnikov_cnets_mapBuffer = require(__dirname + "/../../dist/com_github_osblinnikov_cnets_mapBuffer/mapBuffer.js")
  s.example = s.com_github_osblinnikov_gernet_test_example = require(__dirname + "/../../dist/com_github_osblinnikov_gernet_test_example/example.js")
#[[[end]]] (checksum: 8787152c42a486db1dbfc2906eb68c44)