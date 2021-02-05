from ctypes import *
from ctypes.wintypes import *



# const variable
TH32CS_SNAPPROCESS = 2
STANDARD_RIGHTS_REQUIRED = 0x000F0000
SYNCHRONIZE = 0x00100000
PROCESS_ALL_ACCESS = (STANDARD_RIGHTS_REQUIRED | SYNCHRONIZE | 0xFFF)
TH32CS_SNAPMODULE = 0x00000008

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
lpClassName = None
lpWindowName = ctypes.c_char_p(b'Calculator')
window_handle = User32.FindWindowA(lpClassName, lpWindowName)
if window_handle == 0:
    print('Error Code Occurred Unable To Obtain A Handle {}'.format(Kernel32.GetLastError()))
else:
    print('Obtained Window Handle..')

# Params for GetWindowsThreadProcessID
lpdwProcessId = c_ulong()
pid = User32.GetWindowThreadProcessId(window_handle, byref(lpdwProcessId))
if pid == 0:
    print('Error Code Occurred Unable To Get PID {}'.format(Kernel32.GetLastError()))
    exit(1)

me32 = MODULEENTRY32()
me32.dwSize = sizeof(MODULEENTRY32)
hModuleSnap = Kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPMODULE, lpdwProcessId.value)

ret = Kernel32.Module32First(hModuleSnap, byref(me32))
if ret == 0 :
    print('Error {0} Occurred '.format(Kernel32.GetLastError()))
    Kernel32.CloseHandle( hModuleSnap )

'''
if ret == 0 :
    print('Error {0} Occurred '.format(Kernel32.GetLastError()))
    Kernel32.CloseHandle( hModuleSnap )
'''
'''
    while ret :
        print "   MODULE NAME:     %s"%             me32.szModule
        print "   executable     = %s"%             me32.szExePath
        print "   process ID     = 0x%08X"%         me32.th32ProcessID
        print "   ref count (g)  =     0x%04X"%     me32.GlblcntUsage
        print "   ref count (p)  =     0x%04X"%     me32.ProccntUsage
        print "   base address   = 0x%08X"%         me32.modBaseAddr
        print "   base size      = %d"%             me32.modBaseSize

        ret = Module32Next( hModuleSnap , pointer(me32) )

    CloseHandle( hModuleSnap )
    return True





'''



'''
process_all_access = (0x000F0000 | 0x00100000 | 0xFFF)


# params for FindWindowA
lpClassName = None
lpWindowName = ctypes.c_char_p(b'Task Manager')
window_handle = User32.FindWindowA(lpClassName, lpWindowName)
if window_handle == 0:
    print('Error Code Occurred Unable To Obtain A Handle {}'.format(Kernel32.GetLastError()))
else:
    print('Obtained Window Handle..')

# Params for GetWindowsThreadProcessID
lpdwProcessId = ctypes.c_ulong()
pid = User32.GetWindowThreadProcessId(window_handle, ctypes.byref(lpdwProcessId))
if pid == 0:
    print('Error Code Occurred Unable To Get PID {}'.format(Kernel32.GetLastError()))
    exit(1)




dwDesiredAccess = ctypes.c_ulong(0x000F0000 | 0x00100000 | 0xFFF)
bInheritHandle = False
hProcess = Kernel32.OpenProcess(dwDesiredAccess, bInheritHandle, lpdwProcessId)
if hProcess == 0:
    print('Error Code {} Occurred Unable To Open Process'.format(Kernel32.GetLastError()))

print(address)
print(hProcess)

STRLEN = 255
lpBuffer = ctypes.create_string_buffer(STRLEN)
bytes_read = 0
result = Kernel32.ReadProcessMemory(hProcess, 0x400000, lpBuffer, len(lpBuffer), bytes_read)
print(result)


dwDesiredAccess = ctypes.c_ulong(0x000F0000 | 0x00100000 | 0xFFF)
bInheritHandle = False
process = Kernel32.OpenProcess(dwDesiredAccess, bInheritHandle, lpdwProcessId)
if process == 0:
    print('Error Code {} Occurred Unable To Open Process'.format(Kernel32.GetLastError()))


STRLEN = 255
lpBuffer = ctypes.create_string_buffer(STRLEN)
bytes_read = 0
readProcMem = Kernel32.ReadProcessMemory()

for i in range(1,100):
    if readProcMem(process, hex(i), lpBuffer, STRLEN, bytes_read):
        print(lpBuffer.raw)

'''
