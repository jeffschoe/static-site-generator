import os
import shutil


def copy_static(src, dst): # static, public
    if not os.path.exists(src):
        raise Exception(f"Exception: {src} does not exist")
    if os.path.exists(dst):
        shutil.rmtree(dst)
        print(f"deleted: {dst}")
    os.makedirs(dst, exist_ok = True)
    print(f"mkdir: {dst}")
    
    for name in os.listdir(src): # for each subdir/file in src
        src_path = os.path.join(src, name)
        dst_path = os.path.join(dst, name)
        if os.path.isdir(src_path): # if src_path is a dir, need to recurse
            copy_static(src_path, dst_path)
        else: # is a file
            parent = os.path.dirname(dst_path)
            if not os.path.exists(parent):
                os.makedirs(parent, exist_ok=True)
                print(f"mkdir: {parent}")
            shutil.copy(src_path, dst_path)
            print(f"copied: {src_path} -> {dst_path}")