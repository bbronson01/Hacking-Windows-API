'''
Token Privileges:

Only permissions that are currently set in memory can be enabled and disabled
Can't add a permission

Step one. Open a process and obtain a privileged handle
'''

from ctypes import *
from ctypes.wintypes import  *

'''
HWND FindWindowA(
  LPCSTR lpClassName,
  LPCSTR lpWindowName
);
'''

kernel32 = WinDLL('Kernel32.dll')
user32 = WinDLL('User32.dll')
advapi = WinDLL('Advapi32.dll')

fWindow = user32.FindWindowA(None, c_char_p(b'Task Manager'))
if fWindow == 0:
    print('Error Code {} Occurred'.format(kernel32.GetLastError()))
else:
    print('[*] Got Handle')
'''
DWORD GetWindowThreadProcessId(
  HWND    hWnd,
  LPDWORD lpdwProcessId
);
'''
lpdwProcessId = c_ulong()
getWinID = user32.GetWindowThreadProcessId(fWindow, byref(lpdwProcessId))
if lpdwProcessId == 0:
    print('[*] Error Code {} Occurred'.format(kernel32.GetLastError()))

'''
HANDLE OpenProcess(
  DWORD dwDesiredAccess,
  BOOL  bInheritHandle,
  DWORD dwProcessId
);
'''
# Access Rights
dwDesiredAccess = (0x000F0000 | 0x00100000 | 0xFFF)
bInheritHandle = None
SE_PRIVILEGE_ENABLED = 0x00000002
SE_PRIVILEGE_DISABLED = 0x00000000
# Token Access Rights
# Token Access Rights
STANDARD_RIGHTS_REQUIRED = 0x000F0000
STANDARD_RIGHTS_READ = 0x00020000
TOKEN_ASSIGN_PRIMARY = 0x0001
TOKEN_DUPLICATE = 0x0002
TOKEN_IMPERSONATION = 0x0004
TOKEN_QUERY = 0x0008
TOKEN_QUERY_SOURCE = 0x0010
TOKEN_ADJUST_PRIVILEGES = 0x0020
TOKEN_ADJUST_GROUPS = 0x0040
TOKEN_ADJUST_DEFAULT = 0x0080
TOKEN_ADJUST_SESSIONID = 0x0100
TOKEN_READ = (STANDARD_RIGHTS_READ | TOKEN_QUERY)
TOKEN_ALL_ACCESS = (STANDARD_RIGHTS_REQUIRED |
					TOKEN_ASSIGN_PRIMARY     |
					TOKEN_DUPLICATE          |
					TOKEN_IMPERSONATION      |
					TOKEN_QUERY              |
					TOKEN_QUERY_SOURCE       |
					TOKEN_ADJUST_PRIVILEGES  |
					TOKEN_ADJUST_GROUPS      |
					TOKEN_ADJUST_DEFAULT     |
					TOKEN_ADJUST_SESSIONID)

# Grab Process Handle
hProcess = kernel32.OpenProcess(dwDesiredAccess, bInheritHandle, lpdwProcessId)
if hProcess == 0:
    print('Error Code {} Occurred'.format(kernel32.GetLastError()))
else:
    print('[*] Got PID')

# Open Process Token
'''
BOOL OpenProcessToken(
  HANDLE  ProcessHandle,
  DWORD   DesiredAccess,
  PHANDLE TokenHandle
);
'''
proc_handle = hProcess
DesiredAccess = TOKEN_ALL_ACCESS
TokenHandle = c_void_p()
response = kernel32.OpenProcessToken(proc_handle, DesiredAccess, byref(TokenHandle))
if response == 0:
    print('[*] Error {} Occurred'.format(kernel32.GetLastError()))
else:
    print('[*] Got Privileged Handle')

# Check Process Privileges
'''
BOOL LookupPrivilegeValueW(
  LPCWSTR lpSystemName, //If a null string is specified, the function attempts to find the privilege name on the local system.
  LPCWSTR lpName, //A pointer to a null-terminated string that specifies the name of the privilege,
  PLUID   lpLuid //A pointer to a variable that receives the LUID by which the privilege is known on the system specified by the lpSystemName parameter.
);
'''

# LUID Structure
'''
typedef struct _LUID {
  DWORD LowPart;
  LONG  HighPart;
} LUID, *PLUID;
'''
class LUID(Structure):
    _fields_ = [
        ('LowPart', DWORD),
        ('HighPart', DWORD)
    ]

lpSystemName = None
lpName = "SEDebugPrivilege"
lpLuid = LUID()
LookupPrivileges = advapi.LookupPrivilegeValueW(lpSystemName, lpName, byref(lpLuid))
if LookupPrivileges == 0:
    print('[*] Error Code {} Occurred'.format(kernel32.GetLastError()))
else:
    print('[*] We Found The LUID')



# PRIVILEGE_SET Structure
'''
typedef struct _PRIVILEGE_SET {
  DWORD               PrivilegeCount;
  DWORD               Control;
  LUID_AND_ATTRIBUTES Privilege[ANYSIZE_ARRAY];
} PRIVILEGE_SET, *PPRIVILEGE_SET;
'''
# LUID_AND_ATTRIBUTES Structure
'''
typedef struct _LUID_AND_ATTRIBUTES {
  LUID  Luid;
  DWORD Attributes;
}
'''
class LUID_AND_ATTRIBUTES(Structure):
    _fields_ = [
        ('Luid', LUID),
        ('Attributes', DWORD)
    ]

class PRIVILEGE_SET(Structure):
    _fields_ = [
        ('PrivilegeCount', DWORD),
        ('Control', DWORD),
        ('Privilege', LUID_AND_ATTRIBUTES)

    ]

# Call Check Privileges
'''
BOOL PrivilegeCheck(
  HANDLE         ClientToken, //This handle must have been obtained by opening the token of a thread impersonating the client.
  PPRIVILEGE_SET RequiredPrivileges, //A pointer to a PRIVILEGE_SET structure
  LPBOOL         pfResult
);
'''

# Setup the parameters for PrivilegeCheck
RequiredPrivileges = PRIVILEGE_SET()
RequiredPrivileges.PrivilegeCount = 1
RequiredPrivileges.Privilege = LUID_AND_ATTRIBUTES()
RequiredPrivileges.Privilege.Luid = lpLuid
RequiredPrivileges.Privilege.Attributes = SE_PRIVILEGE_ENABLED

pfResult = c_long()
PrivilegeCheck = advapi.PrivilegeCheck(TokenHandle, byref(RequiredPrivileges), byref(pfResult))
if PrivilegeCheck == 0:
    print('Error Occurred {}'.format(kernel32.GetLastError()))
else:
    print('[*] Privilege {} Found'.format(lpName))
    print('[*] Disabling Privilege')
    RequiredPrivileges.Privilege.Attributes = SE_PRIVILEGE_DISABLED

# Adjusting Token Privileges
'''
BOOL AdjustTokenPrivileges(
  HANDLE            TokenHandle, // A handle to the access token that contains the privileges to be modified.
  BOOL              DisableAllPrivileges, // If this value is TRUE, the function disables all privileges and ignores the NewState parameter. If it is FALSE, the function modifies privileges based on the information pointed to by the NewState parameter
  PTOKEN_PRIVILEGES NewState, // A pointer to a TOKEN_PRIVILEGES structure that specifies an array of privileges and their attributes
  DWORD             BufferLength,
  PTOKEN_PRIVILEGES PreviousState,
  PDWORD            ReturnLength
);
'''
# NewState Structure
'''
typedef struct _TOKEN_PRIVILEGES {
  DWORD               PrivilegeCount;
  LUID_AND_ATTRIBUTES Privileges[ANYSIZE_ARRAY];
}
'''
class TOKEN_PRIVILEGES(Structure):
    _fields_ = [
        ("PrivilegeCount", DWORD),
        ("Privileges", LUID_AND_ATTRIBUTES)
    ]

# Setup Paramaters for Adjusting Token Privileges
'''
BOOL AdjustTokenPrivileges(
  HANDLE            TokenHandle, // A handle to the access token that contains the privileges to be modified.
  BOOL              DisableAllPrivileges, // If this value is TRUE, the function disables all privileges and ignores the NewState parameter. If it is FALSE, the function modifies privileges based on the information pointed to by the NewState parameter
  PTOKEN_PRIVILEGES NewState, // A pointer to a TOKEN_PRIVILEGES structure that specifies an array of privileges and their attributes
  DWORD             BufferLength, // buffer length of NewState
  PTOKEN_PRIVILEGES PreviousState,
  PDWORD            ReturnLength
);
'''
DisableAllPrivileges = False
NewState = TOKEN_PRIVILEGES()
BufferLength = sizeof(NewState)
PreviousState = c_void_p()
ReturnLength = c_void_p()

NewState.PrivilegeCount = 1
NewState.Privileges = RequiredPrivileges.Privilege

AdjustPrivilege = advapi.AdjustTokenPrivileges(TokenHandle, DisableAllPrivileges, byref(NewState), BufferLength, byref(PreviousState), byref(ReturnLength))
if AdjustPrivilege == 0:
    print('Error Occurred {}'.format(kernel32.GetLastError()))
else:
    print('Token Flipped')