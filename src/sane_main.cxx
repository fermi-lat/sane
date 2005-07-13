/** @file like_main.cxx


*/
#include <string>
#include <sstream>

#ifdef WIN32
#include <process.h>
std::string pyname("python ");
#else
std::string pyname("python ");
#endif

#include "st_app/StApp.h"
#include "st_app/StAppFactory.h"

class SaneApp : public st_app::StApp {

    void run()
    {
        std::stringstream cmd;
        std::string app("/python/menu.py");

        cmd << pyname<< ::getenv("SANEROOT") << app;

        system(cmd.str().c_str());
    }
 
};

// Factory which can create an instance of the class above.
st_app::StAppFactory<SaneApp> g_factory;
