<%import parsing_js
p = reload(parsing_js)
p.parsingGernet(a)%>
isNode = typeof module isnt "undefined" and module.exports and process and process.title != 'browser'
if isNode
  s = {}
else
  s = self

${'\n'.join(p.importBlocks(a))}

s.${a.fullName_} =
  create: ${p.getargsStr(a)}->
    that = this
    ${p.getProps(a)}
    #dummy