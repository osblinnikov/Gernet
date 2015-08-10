<%import parsing_c
p = reload(parsing_c)
p.parsingGernet(a)%>#ifndef ${a.fullName_}_H
#define ${a.fullName_}_H

/*[[[cog
import cogging as c
c.tpl(cog,templateFile,c.a(prefix=configFile,module=configModule))
]]]*/
/*[[[end]]]*/

}${a.fullName_};

#endif /* ${a.fullName_}_H */