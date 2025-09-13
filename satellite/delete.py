import os
import shutil

def delete_files_and_dirs(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir in dirs:
            shutil.rmtree(os.path.join(root, dir))

def delete_files_only(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            os.remove(os.path.join(root, file))

# 删除.temp、bytecode、detect-library、predict目录下所有文件和子目录
directories_to_delete = ['.temp', 'bytecode', 'detect-library', 'predict','all_contract_tac','vul']
for directory in directories_to_delete:
    delete_files_and_dirs(directory)

# 删除preprocess目录下所有文件但保留子目录
delete_files_only('preprocess')
