''''

Working with undocumented APIs
example dnsapi.dll
api = DnsGetCacheDataTableEx

'''
import ctypes
from ctypes.wintypes import DWORD, HANDLE, LPWSTR

# setup the windows structure for the undocumented API
class DNS_CACHE_ENTRY(ctypes.Structure):
	_fields_ = [
	("pNext", HANDLE),
	("recName", LPWSTR),
	("wType", DWORD),
	("wDataLength", DWORD),
	("dwFalgs", DWORD),
	]

k_handle = ctypes.WinDLL("Kernel32.dll")
d_handle = ctypes.WinDLL("DNSAPI.dll")

print("[INFO] Pulling DNS Cache Data From System...")

dnsEntry = DNS_CACHE_ENTRY()
dnsEntry.wDataLength = 1024



response = d_handle.DnsGetCacheDataTable(ctypes.byref(dnsEntry))
if response == 0:
    print('Error Code {0}'.format(k_handle.GetLastError()))

dnsEntry = ctypes.cast(dnsEntry.pNext, ctypes.POINTER(DNS_CACHE_ENTRY))
while True:
    # Handle try catch for when we dont have any more entries
    try:
        print("[INFO] DNS Entry: {0} - Type: {1}".format(dnsEntry.contents.recName, dnsEntry.contents.wType))
        dnsEntry = ctypes.cast(dnsEntry.contents.pNext, ctypes.POINTER(DNS_CACHE_ENTRY))
    except:
        break
