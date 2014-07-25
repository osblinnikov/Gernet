<%
import sys
sys.path.insert(0, a.parserPath)
import parsing_js
p = reload(parsing_js)
p.parsingGernet(a)
%>
${a.read_data["path"]}
===

<!--[[[cog
import cogging as c
c.tpl(cog,templateFile,c.a(prefix=configFile))
]]]-->
<!--[[[end]]]-->