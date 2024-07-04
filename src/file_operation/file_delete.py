import os
import shutil

def my_delete(target_addresses):          
    try:
        if len(target_addresses) == 0:
            pass
        else:
            for address in target_addresses:
                if os.path.isfile(address):
                    os.remove(address)
                elif os.path.isdir(address):
                    shutil.rmtree(address)
                else:
                    pass
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 2