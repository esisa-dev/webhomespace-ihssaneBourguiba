import spwd
import bcrypt
import hashlib
import os
user_info = spwd.getspnam("ihssane")
ser_password=str(user_info.sp_pwdp)
print(hashlib.md5(str(user_info.sp_pwdp).encode('utf-8')).hexdigest())
print(hashlib.md5(str('Hafida@1968').encode('utf-8')).hexdigest())


def get_files_and_directories(path):
    files_and_dirs = []
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if os.path.isfile(file_path):
            files_and_dirs.append({
                'name': filename,
                'type': 'file',
                'size': os.path.getsize(file_path)
            })
        elif os.path.isdir(file_path):
            files_and_dirs.append({
                'name': filename,
                'type': 'directory',
                'size': 0
            })
    return files_and_dirs


print(get_files_and_directories("/home/ihssane"))