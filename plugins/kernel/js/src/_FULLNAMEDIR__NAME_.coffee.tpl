<%import parsing_js
p = reload(parsing_js)
p.parsingGernet(a)%>
isNode = typeof module isnt "undefined" and module.exports
if isNode
  s = {}
else
  s = self

${'\n'.join(p.importBlocks(a))}

customCallbacks = {}

s.${a.fullName_} =
  create: (${','.join(p.getargsArrStrs(a))})->
    self = this
    #constructor
    ${'\n    '.join(p.getFieldsArrStr(a))}
    %if len(a.read_data["blocks"])==0:
    wrk = new s.types.Worker('/dist/${a.fullName_}/${a.className}.worker.js')
    ${'\n    '.join(p.registerConnections(a))}
    %endif
    ${'\n    '.join(p.initializeBuffers(a))}
    ${'\n    '.join(p.initializeKernels(a))}
    self.onStart = ->
      if customCallbacks.onStart
        customCallbacks.onStart()
      ${'\n      '.join(p.syncBuffers(a))}
      %if len(a.read_data["blocks"])==0:
      wrk.postMessage({type:'start'})
      %endif
      ${'\n      '.join(p.startKernels(a))}

    self.onStop = ->
      %if len(a.read_data["blocks"])==0:
      wrk.postMessage({type:'stop'})
      %endif
      ${'\n      '.join(p.stopKernels(a))}
      if customCallbacks.onStop
        customCallbacks.onStop()