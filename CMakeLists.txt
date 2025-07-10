#### gtburst ####

set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)

add_executable(test_sane src/test/main.cxx)
target_link_libraries(test_sane PRIVATE dataSubselector Likelihood evtbin rspgen st_app)

#### install ####
install(DIRECTORY data/ DESTINATION ${FERMI_INSTALL_REFDATADIR}/sane)
install(DIRECTORY python/ DESTINATION ${FERMI_INSTALL_PYTHON})
