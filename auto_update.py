import traceback
import requests
import time
import json
import sys
import os

def AddNewKey(data: dict, new: dict) -> dict:
    result = data.copy()
    for key,value in new.items():
        if type(value) ==  dict:
            result[key] = AddNewKey(result.get(key, {}), value)
        result.setdefault(key, value)
    return result

def CheckUpdate(filename: str, githuburl: str) -> bool:
    print(f'Checking update for {filename}...')
    try:
        if "/" in filename:
            os.makedirs("/".join(filename.split("/")[:-1]), exist_ok=True)
        for count, text in enumerate(filename[::-1]):
            if text == ".":
                filename_ = filename[:len(filename)-count-1]
                extension = filename[-count-1:]
                break
        else:
            extension = ""
        if extension in [".py", ".bat", ".txt", ".md", ".sh", ""]:
            if os.path.isfile(filename):
                with open(filename, "r", encoding='utf-8') as f:
                    current = f.read()
            else:
                github = requests.get(githuburl + filename)
                if github.status_code != 200:
                    print(f'Failed to get data for {filename}\n')
                    return None
                github.encoding = github.apparent_encoding
                github = github.text.encode(encoding='utf-8')
                with open(filename, "wb") as f:
                    f.write(github)
                with open(filename, "r", encoding='utf-8') as f:
                    current = f.read()
            github = requests.get(githuburl + filename)
            if github.status_code != 200:
                print(f'Failed to get data for {filename}\n')
                return None
            github.encoding = github.apparent_encoding
            github = github.text.encode(encoding='utf-8')
            if current.replace('\n','').replace('\r','').encode(encoding='utf-8') != github.decode().replace('\n','').replace('\r','').encode(encoding='utf-8'):
                print(f'Update found for {filename}!')
                print(f'Backuping {filename}...\n')
                if os.path.isfile(f'{filename_}_old{extension}'):
                    try:
                        os.remove(f'{filename_}_old{extension}')
                    except PermissionError:
                        print(f'Failed to remove file {filename}\n')
                        print(traceback.format_exc())
                try:
                    os.rename(filename, f'{filename_}_old{extension}')
                except PermissionError:
                    print(f'Failed to backup file {filename}\n')
                    print(traceback.format_exc())
                else:
                    with open(filename, "wb") as f:
                        f.write(github)
                    print(f'Update for {filename} done!\n')
                    return True
            else:
                print(f'No update for {filename}!\n')
                return False
        elif extension == ".json":
            if os.path.isfile(filename):
                with open(filename, "r", encoding='utf-8') as f:
                    current = json.load(f)
            else:
                github = requests.get(githuburl + filename)
                if github.status_code != 200:
                    print(f'Failed to get data for {filename}\n')
                    return None
                github.encoding = github.apparent_encoding
                github = github.text.encode(encoding='utf-8')
                with open(filename, "wb") as f:
                    f.write(github)
                try:
                    with open(filename, "r", encoding='utf-8') as f:
                        current = json.load(f)
                except json.decoder.JSONDecodeError:
                    with open(filename, "r", encoding='utf-8-sig') as f:
                        current = json.load(f)
            github = requests.get(githuburl + filename)
            if github.status_code != 200:
                print(f'Failed to get data for {filename}\n')
                return None
            github.encoding = github.apparent_encoding
            github = github.text
            
            github = json.loads(github)
            new = AddNewKey(current, github)
            if current != new:
                print(f'Update found for {filename}!')
                print(f'Backuping {filename}...\n')
                try:
                    if os.path.isfile(f'{filename_}_old{extension}'):
                        try:
                            os.remove(f'{filename_}_old{extension}')
                        except PermissionError:
                            print(f'Failed to remove file {filename_}_old{extension}')
                            print(f'{traceback.format_exc()}\n')
                    os.rename(filename, f'{filename_}_old{extension}')
                except PermissionError:
                    print(f'Failed to backup file {filename}')
                    print(f'{traceback.format_exc()}\n')
                    return None
                else:
                    with open(filename, 'w', encoding="utf-8") as f:
                        json.dump(new, f, indent=4, ensure_ascii=False)
                    print(f'Update for {filename} done!\n')
                    return True
            else:
                print(f'No update for {filename}!\n')
                return False
        elif extension == ".png":
            if os.path.isfile(filename):
                with open(filename, "rb") as f:
                    current = f.read()
            else:
                github = requests.get(githuburl + filename)
                if github.status_code != 200:
                    print(f'Failed to get data for {filename}\n')
                    return None
                github = github.content
                with open(filename, "wb") as f:
                    f.write(github)
                with open(filename, "rb") as f:
                    current = f.read()
            github = requests.get(githuburl + filename)
            if github.status_code != 200:
                print(f'Failed to get data for {filename}\n')
                return None
            github = github.content
            if current != github:
                print(f'Update found for {filename}!')
                print(f'Backuping {filename}...\n')
                if os.path.isfile(f'{filename_}_old{extension}'):
                    try:
                        os.remove(f'{filename_}_old{extension}')
                    except PermissionError:
                        print(f'Failed to remove file {filename}\n')
                        print(traceback.format_exc())
                try:
                    os.rename(filename, f'{filename_}_old{extension}')
                except PermissionError:
                    print(f'Failed to backup file {filename}\n')
                    print(traceback.format_exc())
                else:
                    with open(filename, "wb") as f:
                        f.write(github)
                    print(f'Update for {filename} done!\n')
                    return True
            else:
                print(f'No update for {filename}!\n')
                return False
        else:
            print(f'Extension {extension} not supported\n')
            return None
    except Exception:
        print("Update failed")
        print(f'{traceback.format_exc()}\n')
        return None

if "-beta" in sys.argv:
    githuburl = "https://raw.githubusercontent.com/Pasta-amongus/Bot-v1.0.2"
else:
    githuburl = "https://raw.githubusercontent.com/Pasta-amongus/Bot-v1.0.2"

if CheckUpdate("fortnitpy.py", githuburl):
    print("")
    os.chdir(os.getcwd())
    os.execv(os.sys.executable,['python', *sys.argv])

flag = False
CheckUpdate("main.py", githuburl)
if CheckUpdate("requirements.txt", githuburl):
    print("requirements.txt got updated. Run INSTALL Packages\n")
    flag = True

CheckUpdate("main.py", githuburl)
CheckUpdate("main.py", githuburl)
CheckUpdate("main.py", githuburl)
CheckUpdate("main.py", githuburl)
CheckUpdate("main.py", githuburl)
CheckUpdate("main.py", githuburl)

print("All update finished")
if flag:
    os.chdir(os.getcwd())
    os.execv(os.sys.executable,['python3', "-m", "pip", "install", "--user", "-U", "-r", "requirements.txt"])
    sys.exit(0)
