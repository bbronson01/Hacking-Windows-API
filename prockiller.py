import ctypes

''' 
ProcKiller: A Process Killer 
API needed
FindWindowA
HWND FindWindowA(
  LPCSTR lpClassName,
  LPCSTR lpWindowName
);

GetWindowThreadProcessId
DWORD GetWindowThreadProcessId(
  HWND    hWnd,
  LPDWORD lpdwProcessId
);
OpenProcess
HANDLE OpenProcess(
  DWORD dwDesiredAccess,
  BOOL  bInheritHandle,
  DWORD dwProcessId
);
TerminateProcess
'''
User32 = ctypes.WinDLL('User32.dll')
Kernel32 = ctypes.WinDLL('Kernel32.dll')
process_all_access = (0x000F0000 | 0x00100000 | 0xFFF)


# params for FindWindowA
lpClassName = None
lpWindowName = ctypes.c_char_p(input('Enter Window Name To Kill: ').encode('utf-8'))
window_handle = User32.FindWindowA(lpClassName, lpWindowName)
if window_handle == 0:
    print('Error Code Occurred Unable To Obtain A Handle {}'.format(Kernel32.GetLastError()))
else:
    print('Obtained Window Handle..')

# Params for GetWindowsThreadProcessID
'''
GetWindowThreadProcessId
DWORD GetWindowThreadProcessId(
  HWND    hWnd,
  LPDWORD lpdwProcessId */ This is being passed in as a reference to pass in a value as a reference
  use ctypes.byref (this param will auto update if the handle it correct)
);
'''
lpdwProcessId = ctypes.c_ulong()
pid = User32.GetWindowThreadProcessId(window_handle, ctypes.byref(lpdwProcessId))
if pid == 0:
    print('Error Code Occurred Unable To Get PID {}'.format(Kernel32.GetLastError()))
    exit(1)

dwDesiredAccess = ctypes.c_ulong(0x000F0000 | 0x00100000 | 0xFFF)
bInheritHandle = False
kernel32 = ctypes.WinDLL('Kernel32.dll')
hProcess = kernel32.OpenProcess(dwDesiredAccess, bInheritHandle, lpdwProcessId)
if hProcess == 0:
    print('Error Code {} Occurred Unable To Open Process'.format(kernel32.GetLastError()))

# Params To Terminate Process
'''
BOOL TerminateProcess(
  HANDLE hProcess,
  UINT   uExitCode
);
'''
uExitCode = ctypes.c_uint(1)
taskill = kernel32.TerminateProcess(hProcess, uExitCode)
if taskill == 1:
    print('Error Code {} occurred unable to kill process')
