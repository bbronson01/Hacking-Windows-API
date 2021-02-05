# Creating a Windows Structure in Python
'''
typedef struct _PROCESS_INFORMATION {
  HANDLE hProcess;
  HANDLE hThread;
  DWORD  dwProcessId;
  DWORD  dwThreadId;
}
'''
# import ctypes, and wintypes which references the keys in the structure
import ctypes
from ctypes.wintypes import HANDLE, DWORD, LPSTR, WORD, LPBYTE

# Creating A Windows Structure
# Windows Structs in python are classes
# ctypes has a built in class for structs called ctypes.Structure that can be inherited
class PROCESS_INFORMATION(ctypes.Structure):
    # to setup a structure we need to specify the magic type called __fields__
    # we need to pass in a list of tuples with field types
    __fields__ = [
        ("hProcess", HANDLE),
        ("hTread", HANDLE),
        ("dwProcessID", DWORD),
        ("dwThreadID", DWORD)
    ]

class STARTUPINFO(ctypes.Structure):
    __fields__ = [
        ("cb", DWORD),
        ("lpReserved", LPSTR),
        ("lpDesktop", LPSTR),
        ("lpTitle", LPSTR),
        ("dwX", DWORD),
        ("dwY", DWORD),
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


