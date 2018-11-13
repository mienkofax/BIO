CMAKE_MINIMUM_REQUIRED(VERSION 3.0.0)
PROJECT(wsq)
ADD_DEFINITIONS(-Wall -g -D__NBISLE__)

FIND_PACKAGE(PNG REQUIRED)
FIND_PACKAGE(PythonInterp)

if (PYTHONINTERP_FOUND)
	if (PYTHON_VERSION_MAJOR EQUAL 3)
		FIND_PACKAGE(Boost COMPONENTS python${PYTHON_VERSION_SUFFIX})
		FIND_PACKAGE(PythonInterp 3)
		FIND_PACKAGE(PythonLibs 3 REQUIRED)
	else()
		FIND_PACKAGE(Boost COMPONENTS python)
		FIND_PACKAGE(PythonInterp)
		FIND_PACKAGE(PythonLibs REQUIRED)
	endif()
else()
	message("Python not found")
endif()

include_directories(
	${PNG_INCLUDE_DIR}
	${PROJECT_SOURCE_DIR}/include
	${Boost_INCLUDE_DIRS}
	${PYTHON_INCLUDE_DIRS}
)

message("")
message(STATUS "PYTHON_LIBRARIES = ${PYTHON_LIBRARIES}")
message(STATUS "PYTHON_EXECUTABLE = ${PYTHON_EXECUTABLE}")
message(STATUS "PYTHON_INCLUDE_DIRS = ${PYTHON_INCLUDE_DIRS}")
message(STATUS "Boost_LIBRARIES = ${Boost_LIBRARIES}")
message("")

# FET library
file(GLOB SOURCE
	${PROJECT_SOURCE_DIR}/fet/allocfet.c
	${PROJECT_SOURCE_DIR}/fet/delfet.c
	${PROJECT_SOURCE_DIR}/fet/extrfet.c
	${PROJECT_SOURCE_DIR}/fet/freefet.c
	${PROJECT_SOURCE_DIR}/fet/lkupfet.c
	${PROJECT_SOURCE_DIR}/fet/nistcom.c
	${PROJECT_SOURCE_DIR}/fet/printfet.c
	${PROJECT_SOURCE_DIR}/fet/readfet.c
	${PROJECT_SOURCE_DIR}/fet/strfet.c
	${PROJECT_SOURCE_DIR}/fet/updatfet.c
	${PROJECT_SOURCE_DIR}/fet/writefet.c
)
add_library(fetlib SHARED ${SOURCE})

# IO_Util library
file(GLOB IO_UTIL
	${PROJECT_SOURCE_DIR}/ioutil/dataio.c
	${PROJECT_SOURCE_DIR}/ioutil/filesize.c
)
add_library(ioutillib SHARED ${IO_UTIL})

# sdf
file(GLOB JPEGL
	${PROJECT_SOURCE_DIR}/jpegl/decoder.c
	${PROJECT_SOURCE_DIR}/jpegl/encoder.c
	${PROJECT_SOURCE_DIR}/jpegl/huff.c
	${PROJECT_SOURCE_DIR}/jpegl/huftable.c
	${PROJECT_SOURCE_DIR}/jpegl/imgdat.c
	${PROJECT_SOURCE_DIR}/jpegl/ppi.c
	${PROJECT_SOURCE_DIR}/jpegl/sd4util.c
	${PROJECT_SOURCE_DIR}/jpegl/tableio.c
	${PROJECT_SOURCE_DIR}/jpegl/util.c
)
add_library(jpegllib SHARED ${JPEGL})

# saf
file(GLOB UTIL
	${PROJECT_SOURCE_DIR}/util/computil.c
	${PROJECT_SOURCE_DIR}/util/fatalerr.c
	${PROJECT_SOURCE_DIR}/util/syserr.c
)
add_library(utillib SHARED ${UTIL})

# sddg
file(GLOB WSQ
	${PROJECT_SOURCE_DIR}/wsq/cropcoeff.c
	${PROJECT_SOURCE_DIR}/wsq/decoder.c
	${PROJECT_SOURCE_DIR}/wsq/encoder.c
	${PROJECT_SOURCE_DIR}/wsq/globals.c
	${PROJECT_SOURCE_DIR}/wsq/huff.c
	${PROJECT_SOURCE_DIR}/wsq/ppi.c
	${PROJECT_SOURCE_DIR}/wsq/sd14util.c
	${PROJECT_SOURCE_DIR}/wsq/tableio.c
	${PROJECT_SOURCE_DIR}/wsq/tree.c
	${PROJECT_SOURCE_DIR}/wsq/util.c
)
add_library(wsqlib SHARED ${WSQ})

add_library(${PROJECT_NAME} SHARED wsq.cpp)
target_link_libraries(${PROJECT_NAME}
	wsqlib
	jpegllib
	fetlib
	utillib
	ioutillib
	${PNG_LIBRARY}
	${Boost_LIBRARIES}
	${PYTHON_LIBRARIES}
)

set_target_properties(${PROJECT_NAME} PROPERTIES SUFFIX .so)
set_target_properties(${PROJECT_NAME} PROPERTIES PREFIX "")
