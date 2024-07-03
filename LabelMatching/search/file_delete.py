import os
import shutil

def my_delete(target_addresses):          
    try:
        for address in target_addresses:
            if os.path.isfile(address):
                os.remove(address)
            elif os.path.isdir(address):
                shutil.rmtree(address)
            else:
                pass
    except Exception as e:
        print(f"Error: {e}")
        return None