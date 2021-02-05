import ctypes


'''
HANDLE CreateToolhelp32Snapshot(
  DWORD dwFlags,
  DWORD th32ProcessID
);

HANDLE OpenProcess(
  DWORD dwDesiredAccess,
  BOOL  bInheritHandle,
  DWORD dwProcessId
);


'''

# DesiredAccess = FULL Permisions
# obtaining full access permisions
process_all_access = (0x000F0000 | 0x00100000 | 0xFFF)

dwDesiredAccess = ctypes.c_ulong(process_all_access)
bInheritHandle = ctypes.c_long(False)
dwProcessId = ctypes.c_ulong(int(input('Enter Process ID: ')))
print()
kernel32 = ctypes.WinDLL('Kernel32.dll')

response = kernel32.OpenProcess(dwDesiredAccess, bInheritHandle, dwProcessId)
error_code = kernel32.GetLastError()
if error_code != 0:
    print(error_code)
