set(EXE_SOURCES
    "main.cpp"
)
set(EXE_INCLUDES
    "./"
)

add_executable(${EXECUTABLE_NAME} ${EXE_SOURCES})

target_include_directories(${EXECUTABLE_NAME} PUBLIC
    ${EXE_INCLUDES}
)

target_link_libraries(${EXECUTABLE_NAME}
    ${Python3_LIBRARIES}
)

if(ENABLE_WARNINGS)
    target_set_warnings(
        ${EXECUTABLE_NAME}
        ON
        OFF
    )
endif()
