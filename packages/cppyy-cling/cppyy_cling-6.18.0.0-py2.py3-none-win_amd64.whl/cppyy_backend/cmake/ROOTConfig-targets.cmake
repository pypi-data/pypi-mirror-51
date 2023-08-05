# Generated by CMake

if("${CMAKE_MAJOR_VERSION}.${CMAKE_MINOR_VERSION}" LESS 2.5)
   message(FATAL_ERROR "CMake >= 2.6.0 required")
endif()
cmake_policy(PUSH)
cmake_policy(VERSION 2.6)
#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Protect against multiple inclusion, which would fail when already imported targets are added once more.
set(_targetsDefined)
set(_targetsNotDefined)
set(_expectedTargets)
foreach(_expectedTarget ROOT::vectorDict ROOT::listDict ROOT::forward_listDict ROOT::dequeDict ROOT::mapDict ROOT::map2Dict ROOT::unordered_mapDict ROOT::multimapDict ROOT::multimap2Dict ROOT::unordered_multimapDict ROOT::setDict ROOT::unordered_setDict ROOT::multisetDict ROOT::unordered_multisetDict ROOT::complexDict ROOT::Cling ROOT::Thread ROOT::Core ROOT::bindexplib ROOT::rmkdepend ROOT::MathCore ROOT::RIO ROOT::rootcling)
  list(APPEND _expectedTargets ${_expectedTarget})
  if(NOT TARGET ${_expectedTarget})
    list(APPEND _targetsNotDefined ${_expectedTarget})
  endif()
  if(TARGET ${_expectedTarget})
    list(APPEND _targetsDefined ${_expectedTarget})
  endif()
endforeach()
if("${_targetsDefined}" STREQUAL "${_expectedTargets}")
  unset(_targetsDefined)
  unset(_targetsNotDefined)
  unset(_expectedTargets)
  set(CMAKE_IMPORT_FILE_VERSION)
  cmake_policy(POP)
  return()
endif()
if(NOT "${_targetsDefined}" STREQUAL "")
  message(FATAL_ERROR "Some (but not all) targets in this export set were already defined.\nTargets Defined: ${_targetsDefined}\nTargets not yet defined: ${_targetsNotDefined}\n")
endif()
unset(_targetsDefined)
unset(_targetsNotDefined)
unset(_expectedTargets)


# Compute the installation prefix relative to this file.
get_filename_component(_IMPORT_PREFIX "${CMAKE_CURRENT_LIST_FILE}" PATH)
get_filename_component(_IMPORT_PREFIX "${_IMPORT_PREFIX}" PATH)
if(_IMPORT_PREFIX STREQUAL "/")
  set(_IMPORT_PREFIX "")
endif()

# Create imported target ROOT::vectorDict
add_library(ROOT::vectorDict SHARED IMPORTED)

set_target_properties(ROOT::vectorDict PROPERTIES
  INTERFACE_COMPILE_FEATURES "cxx_std_14"
  INTERFACE_INCLUDE_DIRECTORIES "${_IMPORT_PREFIX}/include"
  INTERFACE_LINK_LIBRARIES "ROOT::Core"
)

# Create imported target ROOT::listDict
add_library(ROOT::listDict SHARED IMPORTED)

set_target_properties(ROOT::listDict PROPERTIES
  INTERFACE_COMPILE_FEATURES "cxx_std_14"
  INTERFACE_INCLUDE_DIRECTORIES "${_IMPORT_PREFIX}/include"
  INTERFACE_LINK_LIBRARIES "ROOT::Core"
)

# Create imported target ROOT::forward_listDict
add_library(ROOT::forward_listDict SHARED IMPORTED)

set_target_properties(ROOT::forward_listDict PROPERTIES
  INTERFACE_COMPILE_FEATURES "cxx_std_14"
  INTERFACE_INCLUDE_DIRECTORIES "${_IMPORT_PREFIX}/include"
  INTERFACE_LINK_LIBRARIES "ROOT::Core"
)

# Create imported target ROOT::dequeDict
add_library(ROOT::dequeDict SHARED IMPORTED)

set_target_properties(ROOT::dequeDict PROPERTIES
  INTERFACE_COMPILE_FEATURES "cxx_std_14"
  INTERFACE_INCLUDE_DIRECTORIES "${_IMPORT_PREFIX}/include"
  INTERFACE_LINK_LIBRARIES "ROOT::Core"
)

# Create imported target ROOT::mapDict
add_library(ROOT::mapDict SHARED IMPORTED)

set_target_properties(ROOT::mapDict PROPERTIES
  INTERFACE_COMPILE_FEATURES "cxx_std_14"
  INTERFACE_INCLUDE_DIRECTORIES "${_IMPORT_PREFIX}/include"
  INTERFACE_LINK_LIBRARIES "ROOT::Core"
)

# Create imported target ROOT::map2Dict
add_library(ROOT::map2Dict SHARED IMPORTED)

set_target_properties(ROOT::map2Dict PROPERTIES
  INTERFACE_COMPILE_FEATURES "cxx_std_14"
  INTERFACE_INCLUDE_DIRECTORIES "${_IMPORT_PREFIX}/include"
  INTERFACE_LINK_LIBRARIES "ROOT::Core"
)

# Create imported target ROOT::unordered_mapDict
add_library(ROOT::unordered_mapDict SHARED IMPORTED)

set_target_properties(ROOT::unordered_mapDict PROPERTIES
  INTERFACE_COMPILE_FEATURES "cxx_std_14"
  INTERFACE_INCLUDE_DIRECTORIES "${_IMPORT_PREFIX}/include"
  INTERFACE_LINK_LIBRARIES "ROOT::Core"
)

# Create imported target ROOT::multimapDict
add_library(ROOT::multimapDict SHARED IMPORTED)

set_target_properties(ROOT::multimapDict PROPERTIES
  INTERFACE_COMPILE_FEATURES "cxx_std_14"
  INTERFACE_INCLUDE_DIRECTORIES "${_IMPORT_PREFIX}/include"
  INTERFACE_LINK_LIBRARIES "ROOT::Core"
)

# Create imported target ROOT::multimap2Dict
add_library(ROOT::multimap2Dict SHARED IMPORTED)

set_target_properties(ROOT::multimap2Dict PROPERTIES
  INTERFACE_COMPILE_FEATURES "cxx_std_14"
  INTERFACE_INCLUDE_DIRECTORIES "${_IMPORT_PREFIX}/include"
  INTERFACE_LINK_LIBRARIES "ROOT::Core"
)

# Create imported target ROOT::unordered_multimapDict
add_library(ROOT::unordered_multimapDict SHARED IMPORTED)

set_target_properties(ROOT::unordered_multimapDict PROPERTIES
  INTERFACE_COMPILE_FEATURES "cxx_std_14"
  INTERFACE_INCLUDE_DIRECTORIES "${_IMPORT_PREFIX}/include"
  INTERFACE_LINK_LIBRARIES "ROOT::Core"
)

# Create imported target ROOT::setDict
add_library(ROOT::setDict SHARED IMPORTED)

set_target_properties(ROOT::setDict PROPERTIES
  INTERFACE_COMPILE_FEATURES "cxx_std_14"
  INTERFACE_INCLUDE_DIRECTORIES "${_IMPORT_PREFIX}/include"
  INTERFACE_LINK_LIBRARIES "ROOT::Core"
)

# Create imported target ROOT::unordered_setDict
add_library(ROOT::unordered_setDict SHARED IMPORTED)

set_target_properties(ROOT::unordered_setDict PROPERTIES
  INTERFACE_COMPILE_FEATURES "cxx_std_14"
  INTERFACE_INCLUDE_DIRECTORIES "${_IMPORT_PREFIX}/include"
  INTERFACE_LINK_LIBRARIES "ROOT::Core"
)

# Create imported target ROOT::multisetDict
add_library(ROOT::multisetDict SHARED IMPORTED)

set_target_properties(ROOT::multisetDict PROPERTIES
  INTERFACE_COMPILE_FEATURES "cxx_std_14"
  INTERFACE_INCLUDE_DIRECTORIES "${_IMPORT_PREFIX}/include"
  INTERFACE_LINK_LIBRARIES "ROOT::Core"
)

# Create imported target ROOT::unordered_multisetDict
add_library(ROOT::unordered_multisetDict SHARED IMPORTED)

set_target_properties(ROOT::unordered_multisetDict PROPERTIES
  INTERFACE_COMPILE_FEATURES "cxx_std_14"
  INTERFACE_INCLUDE_DIRECTORIES "${_IMPORT_PREFIX}/include"
  INTERFACE_LINK_LIBRARIES "ROOT::Core"
)

# Create imported target ROOT::complexDict
add_library(ROOT::complexDict SHARED IMPORTED)

set_target_properties(ROOT::complexDict PROPERTIES
  INTERFACE_COMPILE_FEATURES "cxx_std_14"
  INTERFACE_INCLUDE_DIRECTORIES "${_IMPORT_PREFIX}/include"
  INTERFACE_LINK_LIBRARIES "ROOT::Core"
)

# Create imported target ROOT::Cling
add_library(ROOT::Cling SHARED IMPORTED)

set_target_properties(ROOT::Cling PROPERTIES
  INTERFACE_COMPILE_FEATURES "cxx_std_14"
  INTERFACE_INCLUDE_DIRECTORIES "${_IMPORT_PREFIX}/include"
  INTERFACE_LINK_LIBRARIES "ROOT::Core;ROOT::RIO"
)

# Create imported target ROOT::Thread
add_library(ROOT::Thread SHARED IMPORTED)

set_target_properties(ROOT::Thread PROPERTIES
  INTERFACE_COMPILE_FEATURES "cxx_std_14"
  INTERFACE_INCLUDE_DIRECTORIES "${_IMPORT_PREFIX}/include"
  INTERFACE_LINK_LIBRARIES "ROOT::Core"
)

# Create imported target ROOT::Core
add_library(ROOT::Core SHARED IMPORTED)

set_target_properties(ROOT::Core PROPERTIES
  INTERFACE_COMPILE_FEATURES "cxx_std_14"
  INTERFACE_INCLUDE_DIRECTORIES "${_IMPORT_PREFIX}/include"
)

# Create imported target ROOT::bindexplib
add_executable(ROOT::bindexplib IMPORTED)

# Create imported target ROOT::rmkdepend
add_executable(ROOT::rmkdepend IMPORTED)

# Create imported target ROOT::MathCore
add_library(ROOT::MathCore SHARED IMPORTED)

set_target_properties(ROOT::MathCore PROPERTIES
  INTERFACE_COMPILE_FEATURES "cxx_std_14"
  INTERFACE_INCLUDE_DIRECTORIES "${_IMPORT_PREFIX}/include"
  INTERFACE_LINK_LIBRARIES "ROOT::Core"
)

# Create imported target ROOT::RIO
add_library(ROOT::RIO SHARED IMPORTED)

set_target_properties(ROOT::RIO PROPERTIES
  INTERFACE_COMPILE_FEATURES "cxx_std_14"
  INTERFACE_INCLUDE_DIRECTORIES "${_IMPORT_PREFIX}/include"
  INTERFACE_LINK_LIBRARIES "ROOT::Core;ROOT::Thread"
)

# Create imported target ROOT::rootcling
add_executable(ROOT::rootcling IMPORTED)

if(CMAKE_VERSION VERSION_LESS 2.8.12)
  message(FATAL_ERROR "This file relies on consumers using CMake 2.8.12 or greater.")
endif()

# Load information for each installed configuration.
get_filename_component(_DIR "${CMAKE_CURRENT_LIST_FILE}" PATH)
file(GLOB CONFIG_FILES "${_DIR}/ROOTConfig-targets-*.cmake")
foreach(f ${CONFIG_FILES})
  include(${f})
endforeach()

# Cleanup temporary variables.
set(_IMPORT_PREFIX)

# Loop over all imported files and verify that they actually exist
foreach(target ${_IMPORT_CHECK_TARGETS} )
  foreach(file ${_IMPORT_CHECK_FILES_FOR_${target}} )
    if(NOT EXISTS "${file}" )
      message(FATAL_ERROR "The imported target \"${target}\" references the file
   \"${file}\"
but this file does not exist.  Possible reasons include:
* The file was deleted, renamed, or moved to another location.
* An install or uninstall procedure did not complete successfully.
* The installation package was faulty and contained
   \"${CMAKE_CURRENT_LIST_FILE}\"
but not all the files it references.
")
    endif()
  endforeach()
  unset(_IMPORT_CHECK_FILES_FOR_${target})
endforeach()
unset(_IMPORT_CHECK_TARGETS)

# This file does not depend on other imported targets which have
# been exported from the same project but in a separate export set.

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
cmake_policy(POP)
