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

int main(int iargc, char *argv[]) {
   std::string command;
   char * root_path = std::getenv("SANEROOT");
   if (!root_path) {
      std::cerr << "SANEROOT not set" << std::endl;
      std::exit(-1);
   }
   std::string rootPath(root_path);
   std::string pythonDir = rootPath + "/python";
   if (iargc == 1) {
      command = std::string("python ") + pythonDir 
         + std::string("/default_tests.py");
   } else if (iargc == 2) {
      command = std::string("python ") + argv[1];
   }
   return std::system(command.c_str());
}
