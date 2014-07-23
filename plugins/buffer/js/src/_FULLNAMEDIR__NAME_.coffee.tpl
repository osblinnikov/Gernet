<%import parsing_js
p = reload(parsing_js)
p.parsingGernet(a)%>
isNode = typeof module isnt "undefined" and module.exports
if isNode
  s = {}
else
  s = self

${p.importBlocks(a)}

${a.className} = s.${a.className} = s.${a.fullName_} =
  create: ->
    #dummy