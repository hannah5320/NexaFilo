import os
import shutil

def move_file_safe(base_path, file_path, target_path):

    # Extract filename
    file_name = os.path.basename(file_path)

    src = file_path
    dst = os.path.join(target_path, file_name)

    if not os.path.exists(src):
        print(f"File not found: {src}")
        return

    try:
        shutil.move(src, dst)
        print(f"Moved: {file_name}")
    except Exception as e:
        print(f"Error moving {file_name}: {e}")