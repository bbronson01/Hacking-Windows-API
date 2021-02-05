import winstructs_
import ctypes


'''
BOOL CreateProcessW(
  LPCWSTR               lpApplicationName,
  LPWSTR                lpCommandLine,
  LPSECURITY_ATTRIBUTES lpProcessAttributes,
  LPSECURITY_ATTRIBUTES lpThreadAttributes,
  BOOL                  bInheritHandles,
  DWORD                 dwCreationFlags,
  LPVOID                lpEnvironment,
  LPCWSTR               lpCurrentDirectory,
  LPSTARTUPINFOW        lpStartupInfo,
  LPPROCESS_INFORMATION lpProcessInformation
);
'''
k_handle = ctypes.WinDLL('Kernel32.dll')


lpApplicationName = u"c:\\Windows\\System32\\cmd.exe"
command = "c:\\Windows\\System32\\cmd.exe /c c:\\Windows\\System32\\ping.exe 127.0.0.1 "
lpCommandLine = ctypes.c_wchar_p(command)
lpProcessAttributes = None
lpThreadAttributes = None
bInheritHandles = None
dwCreationFlags = 0x00000010
lpEnvironment = None
lpCurrentDirectory = None
lpStartupInfo = winstructs_.STARTUPINFO()
lpStartupInfo.cb = ctypes.sizeof(lpStartupInfo)
lpStartupInfo.dwFlags = 0x1
lpStartupInfo.wShowWindow = 0x1
lpProcessInformation = winstructs_.PROCESS_INFORMATION()

response = k_handle.CreateProcessW(lpApplicationName, lpCommandLine, lpProcessAttributes, lpThreadAttributes, bInheritHandles, dwCreationFlags,
                        lpEnvironment, lpCurrentDirectory, ctypes.byref(lpStartupInfo), ctypes.byref(lpProcessInformation))

if response == 0:
    print('Error Code {} occurred'.format(k_handle.GetLastError()))
else:
    print('operation completed successfully')
