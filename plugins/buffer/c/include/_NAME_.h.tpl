<%import parsing_c
p = reload(parsing_c)
p.parsingGernet(a)%>${p.importBlocks(a)}

#undef ${a.fullName_}_EXPORT_API
#if defined WIN32 && !defined __MINGW32__ && !defined(CYGWIN) && !defined(${a.fullName_}_STATIC)
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
reader ${a.fullName_}_getReader(struct ${a.fullName_} *that, void* container, int grid_id);

${a.fullName_}_EXPORT_API
writer ${a.fullName_}_getWriter(struct ${a.fullName_} *that, void* container, int grid_id);

${a.fullName_}_EXPORT_API
void ${a.fullName_}_initialize(struct ${a.fullName_} *that);

${a.fullName_}_EXPORT_API
void ${a.fullName_}_deinitialize(struct ${a.fullName_} *that);

${a.fullName_}_EXPORT_API
void ${a.fullName_}_onKernels(struct ${a.fullName_} *that);

#undef ${a.fullName_}_onCreateMacro
#define ${a.fullName_}_onCreateMacro(_NAME_) /**/

${p.getContainerClass(a)}
${p.getReaderWriter(a)}

${p.getConstructor(a)}

typedef struct ${a.fullName_}{
  ${p.getProps(a)}
  ${p.declareBlocks(a)}