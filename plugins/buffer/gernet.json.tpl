{
"path":"${_JAVA_PATH_}.${_NAME_}",
"gen":["com.github.osblinnikov.gernet.plugins.buffer","com.github.osblinnikov.gernet.plugins.build"],
"args": [{
  "name": "buffers",
  "type": "Object[]"
},{
  "name": "timeout_milisec",
  "type": "long"
},{
  "name": "readers_grid_size",
  "type": "int"
}],
"depends":[{
  "path":"com.github.osblinnikov.cnets.readerWriter"
},{
  "path":"com.github.osblinnikov.cnets.queue"
},{
  "path":"com.github.osblinnikov.cnets.types"
}]
}