#define UNICODE
#define _UNICODE

#include <windows.h>
#include <Python.h>

static size_t strcnt(const char* s, char ch)
{
    // Returns the number of `ch` characters in the NULL terminated string `s`.

    int count = 0;

    const char* pch = s;
    while (pch = strchr(pch, ch))
    {
        count++;
        pch++;
    }

    return count;
}

static void strcat_slashes(char* dest, const char* src)
{
    // Like strcat, but also converts single backslashes to 4.
    //
    // Note that this doesn't check the buffer, you must ensure there is enough memory.

    dest = strchr(dest, 0);

    while (*src)
    {
        if (*src == '\\')
        {
            *dest++ = '\\';
            *dest++ = '\\';
            *dest++ = '\\';
        }
        *dest++ = *src++;
    }

    *dest = '\0';
}


static bool InitializePythonPath()
{
    // Set the Python path to the executable directory and the executable itself.
    //
    // I am not sure why this is necessary, but PyInitialize will hang when running as a
    // service.  It is not just because the current directory is somewhere else because it
    // doesn't hang if running on the command line from another directory.

    // REVIEW: The path already includes the executable's directory.  I didn't notice that in
    // the docs.  It is probably harmless to leave in our duplicate, but it should be checked.

    wchar_t szPath[MAX_PATH * 2 + 3];

    wchar_t szFilename[MAX_PATH];
    if (!GetModuleFileNameW(0, szFilename, MAX_PATH))
        return false;

    wcscpy_s(szPath, sizeof(szPath), szFilename);

    // Now append the directory the executable is in so we pick up the DLLs

    wchar_t* pch = &szFilename[wcslen(szFilename) - 1];
    while (pch > szFilename) {
        if (*pch == '\\') {
            *pch = '\0';
            break;
        }
        pch--;
    }
    wcscat_s(szPath, sizeof(szPath), L";");
    wcscat_s(szPath, sizeof(szPath), szFilename);
    Py_SetPath(szPath);

    return true;
}


static bool InitializePython()
{
    Py_DebugFlag             = 0;
    Py_FrozenFlag            = 1;
    Py_IgnoreEnvironmentFlag = 1;
    Py_NoSiteFlag            = 1;
    Py_OptimizeFlag          = 1;

    if (!InitializePythonPath())
        return false;

    Py_Initialize();

    // Set sys.frozen to True.
    PySys_SetObject("frozen", Py_True);
    Py_INCREF(Py_True);

    return true;
}

// The initial Python script run to configure the path so we can run code from the executable.
// It then loads the startup script from the executable to start the program.
//
// The sys module is dynamically generated when Py_Initialize is called, so we can use it and
// objects built-in to the Python DLL.  Don't use anything else, though, since the standard
// Python modules are inside the executable.

const char* szBootstrap =
    "import __kelvin__\n"
    "__kelvin__.run_main()\n"
;

static bool RunMain()
{
    return PyRun_SimpleString(szBootstrap) == 0;
}

int wmain(int argc, wchar_t* argv[], wchar_t* envp[])
{
    if (!InitializePython())
        return 1;

    PySys_SetArgv(argc, argv);

    if (!RunMain())
        return 2;

    return 0;
}

// When linked as a windows program this entry point will be used.
int CALLBACK wWinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, PWSTR lpCmdLine, int nCmdShow)
{
    if (!InitializePython())
        return 1;

    int argc;
    LPWSTR* argv = CommandLineToArgvW(lpCmdLine, &argc);
    PySys_SetArgv(argc, argv);

    if (!RunMain())
        return 2;

    return 0;
}
