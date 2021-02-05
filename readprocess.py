from ctypes import *
from ctypes.wintypes import *

'''
typedef struct tagMODULEENTRY32 {
  DWORD   dwSize;
  DWORD   th32ModuleID;
  DWORD   th32ProcessID;
  DWORD   GlblcntUsage;
  DWORD   ProccntUsage;
  BYTE    *modBaseAddr;
  DWORD   modBaseSize;
  HMODULE hModule;
  char    szModule[MAX_MODULE_NAME32 + 1];
  char    szExePath[MAX_PATH];
} MODULEENTRY32;
'''

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

Kernel32 = WinDLL('Kernel32.dll')
User32 = WinDLL('User32.dll')


# params for FindWindowA
'''
HWND FindWindowA(
  LPCSTR lpClassName, // string to the program class
  LPCSTR lpWindowName // string to the program window name
);
'''
lpClassName = None
lpWindowName = c_char_p(b'Task Manager')
window_handle = User32.FindWindowA(lpClassName, lpWindowName)
if window_handle == 0:
    print('Error Code Occurred Unable To Obtain A Handle {}'.format(Kernel32.GetLastError()))
else:
    print('Obtained Window Handle..')

# Params for GetWindowsThreadProcessID
'''
DWORD GetWindowThreadProcessId(
  HWND    hWnd, // handle from FindWindowA
  LPDWORD lpdwProcessId
);
'''
lpdwProcessId = c_ulong()
pid = User32.GetWindowThreadProcessId(window_handle, byref(lpdwProcessId))
if pid == 0:
    print('Error Code Occurred Unable To Get PID {}'.format(Kernel32.GetLastError()))
    exit(1)


# setup for CreateToolhelp32Snapshot
# CreateToolhelp32Snapshot is used to take a snapshot of a process which we can then enumerate
'''
HANDLE CreateToolhelp32Snapshot(
  DWORD dwFlags, //The portions of the system to be included in the snapshot = TH32CS_SNAPMODULE
  DWORD th32ProcessID 
);
'''
TH32CS_SNAPMODULE = 0x00000008

me32 = MODULEENTRY32()
me32.dwSize = sizeof(MODULEENTRY32)
hModuleSnap = Kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPMODULE, lpdwProcessId.value)

ret = Kernel32.Module32First(hModuleSnap, byref(me32))
if ret == 0 :
    print('Error {0} Occurred '.format(Kernel32.GetLastError()))
    Kernel32.CloseHandle( hModuleSnap )

# setup for OpenProcess

'''
HANDLE OpenProcess(
  DWORD dwDesiredAccess,
  BOOL  bInheritHandle,
  DWORD dwProcessId
);
'''
STANDARD_RIGHTS_REQUIRED = 0x000F0000
SYNCHRONIZE = 0x00100000
PROCESS_ALL_ACCESS = (STANDARD_RIGHTS_REQUIRED | SYNCHRONIZE | 0xFFF)
bInheritHandle = False
hProcess = Kernel32.OpenProcess(PROCESS_ALL_ACCESS, bInheritHandle, lpdwProcessId)
if hProcess == 0:
    print('Error Code {} Occurred Unable To Open Process'.format(Kernel32.GetLastError()))

print('[*] Obtained Handle To Process {}'.format(hProcess))

# setup for ReadProcessMemory
'''
BOOL ReadProcessMemory(
  HANDLE  hProcess,
  LPCVOID lpBaseAddress,
  LPVOID  lpBuffer,
  SIZE_T  nSize,
  SIZE_T  *lpNumberOfBytesRead
);
'''
address = me32.modBaseAddr
STRLEN = 255
lpBuffer = create_string_buffer(STRLEN)
bytes_read = 0
print('[*] Reading Process')
print()
result = Kernel32.ReadProcessMemory(hProcess, address, lpBuffer, len(lpBuffer), bytes_read)
print(lpBuffer.raw)


