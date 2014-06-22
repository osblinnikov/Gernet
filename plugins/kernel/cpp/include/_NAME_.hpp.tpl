<%import parsing_c
p = reload(parsing_c)
p.parsingGernet(a)%>

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

class ${a.className}{
public:
  ${a.fullName_}_EXPORT_API static ${a.className}* create(${p.getConstructorArgs(a)});
  virtual void release() = 0;
  virtual void run() = 0;
  virtual void onStart() = 0;
  virtual void onStop() = 0;
  virtual com::github::airutech::cnets::runnablesContainer getRunnables() = 0;
};



