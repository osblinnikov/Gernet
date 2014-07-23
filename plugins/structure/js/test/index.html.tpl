<%import parsing_js
from gernetHelpers import getFullName_, getClassName
p = reload(parsing_js)
p.parsingGernet(a)
dependenciesDict = dict()
for v in a.read_data["blocks"]+a.read_data["depends"]:
  dependenciesDict[v["path"]] = v %>
        %for k,v in dependenciesDict.items():
        <script type="text/javascript" src="../dist/${getFullName_(k)}/${getClassName(k)}.js"></script>
        %endfor