<%
import sys
sys.path.insert(0, a.parserPath)

import parsing_c
p = reload(parsing_c)
p.parsingGernet(a)

%>

#ifndef ${a.fullName_}_IMPL_H
#define ${a.fullName_}_IMPL_H

${a.nameSpaceDeclarationBegin}
/*[[[cog
import cogging as c
c.tpl(cog,templateFile,c.a(prefix=configFile))
]]]*/
/*[[[end]]]*/

};
${a.nameSpaceDeclarationEnd}

#endif /* ${a.fullName_}_IMPL_H */