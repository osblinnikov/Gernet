@onmessage = (code) ->
  eval code.data
  return