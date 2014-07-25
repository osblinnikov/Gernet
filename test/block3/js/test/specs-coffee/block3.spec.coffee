

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
  s.types = s.com_github_airutech_cnets_types = require(__dirname + "/../../dist/com_github_airutech_cnets_types/types.js")
  s.selector = s.com_github_airutech_cnets_selector = require(__dirname + "/../../dist/com_github_airutech_cnets_selector/selector.js")
  s.readerWriter = s.com_github_airutech_cnets_readerWriter = require(__dirname + "/../../dist/com_github_airutech_cnets_readerWriter/readerWriter.js")
  s.mapBuffer = s.com_github_airutech_cnets_mapBuffer = require(__dirname + "/../../dist/com_github_airutech_cnets_mapBuffer/mapBuffer.js")
  s.runnablesContainer = s.com_github_airutech_cnets_runnablesContainer = require(__dirname + "/../../dist/com_github_airutech_cnets_runnablesContainer/runnablesContainer.js")
  s.block3 = s.com_github_airutech_gernet_test_block3 = require(__dirname + "/../../dist/com_github_airutech_gernet_test_block3/block3.js")
#[[[end]]] (checksum: f0c8e02f59fbee2d1a8a9d8d213a9795)