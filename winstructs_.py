# Import the required module to handle Windows API Calls
from ctypes import *

# Import Python -> Windows Types from ctypes
from ctypes.wintypes import *

# Grab a handle to kernel32.dll
k_handle = WinDLL("Kernel32.dll")


# Structure for Startup Info
class STARTUPINFO(Structure):
    _fields_ = [
        ("cb", DWORD),
        ("lpReserved", LPWSTR),
        ("lpDesktop", LPWSTR),
        ("lpTitle", LPWSTR),
        ("dwX", DWORD),
        ("dxY", DWORD),
        ("dwXSize", DWORD),
        ("dwYSize", DWORD),
        ("dwXCountChars", DWORD),
        ("dwYCountChars", DWORD),
        ("dwFillAttribute", DWORD),
        ("dwFlags", DWORD),
        ("wShowWindow", WORD),
        ("cbReserved2", WORD),
        ("lpReserved2", LPBYTE),
        ("hStdInput", HANDLE),
        ("hStdOutput", HANDLE),
        ("hStdError", HANDLE),
    ]


# Structure for Process Info
class PROCESS_INFORMATION(Structure):
    _fields_ = [
        ("hProcess", HANDLE),
        ("hThread", HANDLE),
        ("dwProcessId", DWORD),
        ("dwThreadId", DWORD),
    ]

# Structure for DNS CACHE Entry
class DNS_CACHE_ENTRY(Structure):
    _fields_ = [
        ("pNext", HANDLE),
        ("recName", LPWSTR),
        ("wType", DWORD),
        ("wDataLength", DWORD),
        ("dwFlags", DWORD),
    ]

# Module Entry 32 Structure
class MODULEENTRY32(Structure):
    _fields_ = [( 'dwSize' , DWORD ) ,
                ( 'th32ModuleID' , DWORD ),
                ( 'th32ProcessID' , DWORD ),
                ( 'GlblcntUsage' , DWORD ),
                ( 'ProccntUsage' , DWORD ) ,
                ( 'modBaseAddr' , POINTER(BYTE) ) ,
                ( 'modBaseSize' , DWORD ) ,
                ( 'hModule' , HMODULE ) ,
                ( 'szModule' , c_char * 256 ),
                ( 'szExePath' , c_char * 260 ) ]
