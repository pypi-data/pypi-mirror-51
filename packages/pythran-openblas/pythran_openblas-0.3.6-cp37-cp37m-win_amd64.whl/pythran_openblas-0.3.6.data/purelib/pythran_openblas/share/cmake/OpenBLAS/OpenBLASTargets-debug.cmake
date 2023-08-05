#----------------------------------------------------------------
# Generated CMake target import file for configuration "Debug".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "OpenBLAS::OpenBLAS" for configuration "Debug"
set_property(TARGET OpenBLAS::OpenBLAS APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_target_properties(OpenBLAS::OpenBLAS PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_DEBUG "C"
  IMPORTED_LOCATION_DEBUG "${_IMPORT_PREFIX}/lib/openblas.lib"
  )

list(APPEND _IMPORT_CHECK_TARGETS OpenBLAS::OpenBLAS )
list(APPEND _IMPORT_CHECK_FILES_FOR_OpenBLAS::OpenBLAS "${_IMPORT_PREFIX}/lib/openblas.lib" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
