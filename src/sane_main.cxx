/** @file like_main.cxx


*/
#ifdef WIN32
#include <process.h>
#endif
#include <sstream>
#include "st_app/IApp.h"

class LikeApp : public st_app::IApp {

    void run()
    {
        std::stringstream cmd;
        std::string app("/python/menu.py");

        cmd << "python " << ::getenv("SANEROOT") << app;

        system(cmd.str().c_str());
    }
 
} app;
