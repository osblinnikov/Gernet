<%import parsing_c
p = reload(parsing_c)
p.parsingGernet(a)%>${p.importBlocks(a)}

#undef ${a.fullName_}_EXPORT_API
#if defined WIN32 && !defined __MINGW32__ && !defined(CYGWIN) && !defined(${(a.fullName_+"_static").upper()})
  #ifdef ${a.fullName_}_EXPORT
    #define ${a.fullName_}_EXPORT_API __declspec(dllexport)
  #else
    #define ${a.fullName_}_EXPORT_API __declspec(dllimport)
  #endif
#else
  #define ${a.fullName_}_EXPORT_API extern
#endif

struct ${a.fullName_};

${a.fullName_}_EXPORT_API
void ${a.fullName_}_init(${p.getArgs(a)});

${a.fullName_}_EXPORT_API
void ${a.fullName_}_deinit(struct ${a.fullName_} *that);

${a.fullName_}_EXPORT_API
reader ${a.fullName_}_createReader(struct ${a.fullName_} *that, int gridId);

${a.fullName_}_EXPORT_API
writer ${a.fullName_}_createWriter(struct ${a.fullName_} *that, int gridId);



typedef struct ${a.fullName_}{
  ${p.getProps(a)}
  ${p.declareBlocks(a)}