<%
import sys
sys.path.insert(0, a.parserPath)

import parsing_c
p = reload(parsing_c)
p.parsingGernet(a)

%>

#ifndef ${a.fullName_}_H
#define ${a.fullName_}_H

/*[[[cog
import cogging as c
c.tpl(cog,templateFile,c.a(prefix=configFile))
]]]*/
/*[[[end]]]*/

}${a.fullName_};

#undef ${a.fullName_}_onCreateMacro
#define ${a.fullName_}_onCreateMacro(_NAME_) /**/

#endif /* ${a.fullName_}_H */