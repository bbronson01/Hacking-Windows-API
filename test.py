from ctypes import *
from ctypes.wintypes import *
import sys


# const variable
# Establish rights and basic options needed for all process declartion / iteration
TH32CS_SNAPPROCESS = 2
STANDARD_RIGHTS_REQUIRED = 0x000F0000
SYNCHRONIZE = 0x00100000
PROCESS_ALL_ACCESS = (STANDARD_RIGHTS_REQUIRED | SYNCHRONIZE | 0xFFF)
TH32CS_SNAPMODULE = 0x00000008
TH32CS_SNAPTHREAD = 0x00000004

#class MODULEENTRY32(Structure):
#    _fields_ = [ ( 'dwSize' , DWORD ) , 
#                ( 'th32ModuleID' , DWORD ),
#                ( 'th32ProcessID' , DWORD ),
#                ( 'GlblcntUsage' , DWORD ),
#                ( 'ProccntUsage' , DWORD ) ,
#                ( 'modBaseAddr' , LONG ) ,
#                ( 'modBaseSize' , DWORD ) , 
#                ( 'hModule' , HMODULE ) ,
#                ( 'szModule' , c_char * 256 ),
#                ( 'szExePath' , c_char * 260 ) ]


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


CreateToolhelp32Snapshot= windll.kernel32.CreateToolhelp32Snapshot
Process32First = windll.kernel32.Process32First
Process32Next = windll.kernel32.Process32Next
Module32First = windll.kernel32.Module32First
Module32Next = windll.kernel32.Module32Next
GetLastError = windll.kernel32.GetLastError
OpenProcess = windll.kernel32.OpenProcess
GetPriorityClass = windll.kernel32.GetPriorityClass
CloseHandle = windll.kernel32.CloseHandle


try:
    ProcessID=13604
    hModuleSnap = DWORD
    me32 = MODULEENTRY32()
    me32.dwSize = sizeof( MODULEENTRY32 )
    #me32.dwSize = 5000
    hModuleSnap = CreateToolhelp32Snapshot( TH32CS_SNAPMODULE, ProcessID )
    ret = Module32First( hModuleSnap, pointer(me32) )
    if ret == 0 :
        CloseHandle( hModuleSnap )
    global PROGMainBase
    PROGMainBase=False
    while ret :
        print(me32.modBaseAddr)
        ret = Module32Next( hModuleSnap , pointer(me32) )
    CloseHandle( hModuleSnap )



except:
    print("Error in ListProcessModules")