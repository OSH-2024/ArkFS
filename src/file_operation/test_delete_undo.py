import os
import send2trash

def my_delete(target_addresses):          
    try:
        if len(target_addresses) == 0:
            pass
        else:
            for address in target_addresses:
                if os.path.isfile(address):
                    send2trash.send2trash(address)
                elif os.path.isdir(address):
                    send2trash.send2trash(address)
                else:
                    pass
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 2
    
my_delete(["E:\\Codefield\\CODE_C\\Git\\ArkFS\\src\\file_operation\\test.txt"])