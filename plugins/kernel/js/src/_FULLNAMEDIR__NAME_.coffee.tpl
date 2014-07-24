<%import parsing_js
p = reload(parsing_js)
p.parsingGernet(a)%>
isNode = typeof module isnt "undefined" and module.exports
if isNode
  s = {}
else
  s = self

${p.importBlocks(a)}

s.${a.fullName_} =
  wrk: null
  blocks: []
  create: ->
    #constructor
    %if len(a.read_data["blocks"])==0:
    this.wrk = new s.Worker('/dist/${a.fullName_}/${a.className}.worker.js')
    %endif
    ${p.initializeBuffers(a)}