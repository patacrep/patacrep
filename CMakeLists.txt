cmake_minimum_required(VERSION 2.8)
PROJECT(Songbook NONE)
INCLUDE(UseLATEX.cmake)


set(TARGET naheulbeuk)
set(MAKE_SONGBOOK songbook.py)

#Dependencies
find_package(PythonInterp REQUIRED)
find_program(LILYPOND NAMES lilypond)
if(NOT ${var})
  message(STATUS "Lilypond not found")
endif()

set(SONGS_DIR "${CMAKE_CURRENT_SOURCE_DIR}/songs")
set(BOOKS_DIR "${CMAKE_CURRENT_SOURCE_DIR}/books")
set(LILYPOND_DIR "${CMAKE_CURRENT_SOURCE_DIR}/lilypond")

file(GLOB COVERS "${SONGS_DIR}/*")
#TODO: get actual song list from .sb
file(GLOB SONGS "${SONGS_DIR}/*/*.sg")
#TODO: get actual lilypond list from .sb
#file(GLOB LILYPOND_SRC "${LILYPOND_DIR}/*.ly")
file(GLOB LILYPOND_SRC "${LILYPOND_DIR}/10_sous_dans_ma_poche-2.ly")


#Process Lilypond files
foreach(file ${LILYPOND_SRC})
  get_filename_component(BASENAME "${file}" NAME_WE)
  add_custom_command(
    OUTPUT "${LILYPOND_DIR}/${BASENAME}.pdf"
    DEPENDS "${LILYPOND_DIR}/${BASENAME}.ly"
    COMMAND ${LILYPOND}
    ARGS "${LILYPOND_DIR}/${BASENAME}.ly"
    )
  # Make a list of all lilypond files
  set(LILYPOND_PDF ${LILYPOND_PDF}
    "${LILYPOND_DIR}/${BASENAME}.pdf"
    )
endforeach(file)

add_custom_command(
  OUTPUT "generated_${TARGET}.tex"
  DEPENDS "${BOOKS_DIR}/${TARGET}.sb"
  COMMAND python
  ARGS 
  "${CMAKE_CURRENT_SOURCE_DIR}/${MAKE_SONGBOOK}" 
  "-s ${BOOKS_DIR}/${TARGET}.sb -o generated_${TARGET}.tex"
  )

#UseLaTex requires relative paths
string(REPLACE "${CMAKE_CURRENT_SOURCE_DIR}" ""
  COVERS "${COVERS}"
  )

string(REPLACE "${CMAKE_CURRENT_SOURCE_DIR}" ""
  LILYPOND_SRC "${LILYPOND_SRC}"
  )

string(REPLACE "${CMAKE_CURRENT_SOURCE_DIR}" ""
  LILYPOND_DIR "${LILYPOND_DIR}"
  )

string(REPLACE "${CMAKE_CURRENT_SOURCE_DIR}" ""
  SONGS "${SONGS}"
  )


add_latex_document(
  "${TARGET}.tex"
  INPUTS
  tex/crepbook.cls
  tex/songs.sty
  tex/license-nb.tex
  tex/license-en.tex
  tex/license.tex
  tex/xstring.sty
  tex/licence.sty
  ${SONGS}
  ${LILYPOND_SRC}
  IMAGE_DIRS
  img
  ${LILYPOND_DIR}
  ${COVERS}
  DEPENDS
  ${LILYPOND_PDF}
  "generated_${TARGET}.tex"
  DEFAULT_PDF
  )

