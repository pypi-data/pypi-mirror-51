/* This is file is automatically generated */
#define BUILD_ARCH "win32"
#define BUILD_NODE "DESKTOP-MAU10RK"
#define CXX "C:/Program Files (x86)/Microsoft Visual Studio/2017/Community/VC/Tools/MSVC/14.15.26726/bin/Hostx86/x86/cl.exe"
#define COMPILER "C:/Program Files (x86)/Microsoft Visual Studio/2017/Community/VC/Tools/MSVC/14.15.26726/bin/Hostx86/x86/cl.exe"
#define COMPILERVERS ""
#define MAKESHAREDLIB "cl $Opt -nologo -TP -c -nologo -IC:/Users/wlav/Test/cppyy-backend/cling/src/build/win -FIw32pragma.h -FIsehmap.h -Zc:__cplusplus -MD -GR -D_WINDOWS -DWIN32 -D_X86_ -EHsc- -W3 -wd4141 -wd4291 -wd4244 -wd4049 -D_XKEYCHECK_H -D_LIBCPP_HAS_NO_PRAGMA_SYSTEM_HEADER -DNOMINMAX -D_CRT_SECURE_NO_WARNINGS  $IncludePath $SourceFiles -Fo$ObjectFiles && bindexplib $LibName $ObjectFiles > $BuildDir\\$LibName.def && lib -nologo -MACHINE:IX86 -out:$BuildDir\\$LibName.lib $ObjectFiles -def:$BuildDir\\$LibName.def && link -nologo $ObjectFiles -DLL -out:$BuildDir\\$LibName.dll $BuildDir\\$LibName.exp -LIBPATH:%ROOTSYS%\\lib  $LinkedLibs libCore.lib kernel32.lib advapi32.lib user32.lib gdi32.lib comdlg32.lib winspool.lib && if EXIST \"$BuildDir\\$LibName.dll.manifest\" ( mt -nologo -manifest \"$BuildDir\\$LibName.dll.manifest\" \"-outputresource:$BuildDir\\$LibName.dll;2\" && del \"$BuildDir\\$LibName.dll.manifest\" )"
#define MAKEEXE "cl -nologo -TP -Iinclude -I..\\include -c $Opt -nologo -IC:/Users/wlav/Test/cppyy-backend/cling/src/build/win -FIw32pragma.h -FIsehmap.h -Zc:__cplusplus -MD -GR -D_WINDOWS -DWIN32 -D_X86_ -EHsc- -W3 -wd4141 -wd4291 -wd4244 -wd4049 -D_XKEYCHECK_H -D_LIBCPP_HAS_NO_PRAGMA_SYSTEM_HEADER -DNOMINMAX -D_CRT_SECURE_NO_WARNINGS  $IncludePath $SourceFiles && link -opt:ref  $ObjectFiles $LinkedLibs advapi32.lib -out:$ExeName  && if EXIST \"$ExeName.exe.manifest\" ( mt -nologo -manifest \"$ExeName.exe.manifest\" \"-outputresource:$ExeName.exe;1\" && del \"$ExeName.exe.manifest\" )"
#define CXXOPT "-O2"
#define CXXDEBUG "-Z7"
#define ROOTBUILD "debug"
#define LINKEDLIBS "-LIBPATH:%ROOTSYS%\\lib libCore.lib "
#define INCLUDEPATH "-I%ROOTSYS%\\include"
#define OBJEXT "obj"
#define SOEXT "dll"
