/** @file like_main.cxx


*/
#include <string>
#include <sstream>

#ifdef WIN32
#include <process.h>
std::string pyname("python ");
#else
std::string pyname("python2.3 ");
#endif

#include "st_app/IApp.h"

class LikeApp : public st_app::IApp {

    void run()
    {
        std::stringstream cmd;
        std::string app("/python/menu.py");

        cmd << pyname<< ::getenv("SANEROOT") << app;

        system(cmd.str().c_str());
    }
 
} app;
