cmake_minimum_required(VERSION 3.1)
project(apriltag)

find_package(OpenCV QUIET)

include_directories(.)
aux_source_directory(common COMMON_SRC)
set(APRILTAG_SRCS apriltag.c apriltag_pose.c apriltag_quad_thresh.c)

set(CMAKE_BUILD_TYPE Release)

# Library
file(GLOB TAG_FILES ${PROJECT_SOURCE_DIR}/tag*.c)
set_source_files_properties(SOURCE ${TAG_FILES} PROPERTIES COMPILE_FLAGS -O0)
add_library(${PROJECT_NAME} SHARED ${APRILTAG_SRCS} ${COMMON_SRC} ${TAG_FILES})
if (MSVC)
    # FindThreads will not find pthread.h with MSVC so we use pthreads-win
    # winmm is necessary for __imp_timeGetTime
    set(PTHREADS_WIN ${PROJECT_SOURCE_DIR}/thirdparty/pthreads-win)
    include_directories(${PTHREADS_WIN}/include)
    add_definitions(-DHAVE_STRUCT_TIMESPEC)
    target_link_libraries(${PROJECT_NAME} ${PTHREADS_WIN}/lib/x64/pthreadVC2.lib winmm)
else()
    find_package(Threads REQUIRED)
    target_link_libraries(${PROJECT_NAME} Threads::Threads m)
endif()

set_target_properties(${PROJECT_NAME} PROPERTIES SOVERSION 3 VERSION 3.1.0)

include(GNUInstallDirs)
target_include_directories(${PROJECT_NAME} PUBLIC
    "$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/>"
    "$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/common>"
    "$<INSTALL_INTERFACE:$<INSTALL_PREFIX>/${CMAKE_INSTALL_INCLUDEDIR}>/apriltag")

set_target_properties(${PROJECT_NAME} PROPERTIES
    ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_INSTALL_LIBDIR}
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_INSTALL_LIBDIR}
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_INSTALL_LIBDIR} # for windows dll
    C_STANDARD 99
)

# install library
install(TARGETS ${PROJECT_NAME} EXPORT apriltag
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_LIBDIR} # for windows dll
)
