import ctypes
'''

# step two identify the parameters and types to be specified
# step three obtain a handle to the dll that calls this api function
# step four pass in the parameters 
# step five execute api function
'''
# handle to User32.dll to obtain MessageBox Function
user_handle = ctypes.WinDLL("User32.dll")
# handle to Kernel32.dll to obtain GetLastError() function
kernel_handle = ctypes.WinDLL("Kernel32.dll")

# Parameters to pass into MessageBox()
'''
int MessageBox(
  HWND    hWnd,
  LPCTSTR lpText,
  LPCTSTR lpCaption,
  UINT    uType
);
'''
hWnd = None
lpText = ctypes.c_char_p('Hello World')
lpCaption = ctypes.c_char_p('Message')
uType = ctypes.c_uint(0x00000001)
response = user_handle.MessageBoxW(hWnd, lpText, lpCaption, uType)
error_check = kernel_handle.GetLastError()
if error_check != 0:
    print('Error {} occured'.format(error_check))
    exit(1)
if error_check == 0:
    print('Program ran successfully')