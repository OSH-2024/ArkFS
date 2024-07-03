import os
import shutil

# opcode:[[origin],target_folder,file/dir,name]

def my_add(opcode):
    if not opcode[0]:
        # Create a file or directory
        try:
            if opcode[2]:
                # Create a directory
                os.makedirs(os.path.join(opcode[1],opcode[3]))
            else:
                # Create a file
                with open(os.path.join(opcode[1],opcode[3]),"w") as f:
                    pass
        except Exception as e:
            print(f"Error: {e}")
            return None
                    
    else:
        # Copy but not move
        try:
            for address in opcode[0]:
                if os.path.isdir(address):
                    # Find the name of the directory
                    name = os.path.basename(address)
                    # Copy the directory to the target folder
                    if os.path.exists(os.path.join(opcode[1],name)):
                        name = name + "(1)"
                    shutil.copytree(address,os.path.join(opcode[1],name))
                elif os.path.isfile(address):
                    # Find the name of the file
                    name = os.path.basename(address)
                    # Copy the file to the target folder
                    if not os.exists(os.path.join(opcode[1],name)):
                        with open(os.path.join(opcode[1],name),"w") as f:
                            pass
                    shutil.copy(address,os.path.join(opcode[1],name))
                else:
                    pass
        except Exception as e:
            print(f"Error: {e}")
            return None
                    
                    
            
        
