/**
 * @file main.cxx
 * @brief Driver for running the Science Tools system tests scripts
 *
 * @author J. Chiang <jchiang@slac.stanford.edu>
 *
 * $Header$
 */

#include <cstdlib>
#include <iostream>
#include <string>

#include "st_facilities/Environment.h"

int main(int iargc, char *argv[]) {
   std::string command;
   std::string rootPath = st_facilities::Environment::packagePath("sane");
   if (rootPath == "") {
      std::cerr << "Unable to determine sane root directory" << std::endl;
      std::exit(-1);
   }
   std::string pythonDir = rootPath + "/python/tests";
   if (iargc == 1) {
      command = std::string("python ") + pythonDir 
         + std::string("/default_tests.py");
   } else if (iargc == 2) {
      command = std::string("python ") + argv[1];
   }
   if (std::system(command.c_str()) != 0) {
      return 1;
   }
}
