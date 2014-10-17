<%
import sys
sys.path.insert(0, a.parserPath)
import parsing_js
p = reload(parsing_js)
p.parsingGernet(a) %>

#[[[cog
#import cogging as c
#c.tpl(cog,templateFile,c.a(prefix=configFile))
#]]]
#[[[end]]]

initOnCreate = (p)->
  console.log "initOnCreate"
  console.log p

_this.onStart = ->
  console.log "onStart"

_this.onStop = ->
  console.log "onStop"

onRun.callback = (mapBufferId, mapBufferObj) ->
  switch mapBufferId
    when 0
      console.log "onRun"
    else
      console.log "onRun, unknown buffer"

#sendMessageExample = ->
#  r = w0.writeNext()
#  if r!=null
#    r.obj = {someData:"data"}
#    w0.writeFinished()
#    receivedData = null
#  # else
#    # setTimeout(sendMessageExample,100)

#readMessageExample = ->
#  r = r0.readNext()
#  if r != null
#    receivedData = r.obj
#    r0.readFinished()
