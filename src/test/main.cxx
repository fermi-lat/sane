/**
 * @file main.cxx
 * @brief Driver for running the Science Tools system tests scripts
 *
 * @author J. Chiang <jchiang@slac.stanford.edu>
 *
 * $Header$
 */

#include <cstdlib>
#include <string>

int main(int iargc, char *argv[]) {
   std::string command;
   std::string rootPath = std::getenv("SANEROOT");
   std::string pythonDir = rootPath + "/python";
   if (iargc == 1) {
      command = std::string("python ") + pythonDir 
         + std::string("/default_tests.py");
   } else if (iargc == 2) {
      command = std::string("python ") + argv[1];
   }
   std::system(command.c_str());
}
