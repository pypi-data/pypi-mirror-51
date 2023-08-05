# - Locate Unuran library
# Defines:
#
#  UNURAN_FOUND
#  UNURAN_INCLUDE_DIR
#  UNURAN_INCLUDE_DIRS (not cached)
#  UNURAN_LIBRARIES

find_path(UNURAN_INCLUDE_DIR NAMES unuran.h HINTS ${UNURAN_DIR}/include $ENV{UNURAN_DIR}/include /usr/include)
find_library(UNURAN_LIBRARY NAMES unuran HINTS ${UNURAN_DIR}/lib $ENV{UNURAN_DIR}/lib)

set(UNURAN_INCLUDE_DIRS ${UNURAN_INCLUDE_DIR})
if(UNURAN_LIBRARY)
  set(UNURAN_LIBRARIES ${UNURAN_LIBRARY})
endif()


# handle the QUIETLY and REQUIRED arguments and set UNURAN_FOUND to TRUE if
# all listed variables are TRUE
INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(UNURAN DEFAULT_MSG UNURAN_LIBRARY UNURAN_INCLUDE_DIR)

mark_as_advanced(UNURAN_FOUND UNURAN_INCLUDE_DIR UNURAN_LIBRARY)
