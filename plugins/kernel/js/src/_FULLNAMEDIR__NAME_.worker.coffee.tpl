<%import parsing_js
p = reload(parsing_js)
p.parsingGernet(a)%>

${p.importScripts(a)}

onRun =
  callback: ->
    #dummy

_this = new Dispatcher(this)

props = undefined
_this.onCreate = (_props)->
  props = _props
  if initOnCreate
    initOnCreate(_props)

${p.createWorkerBuffers(a)}

