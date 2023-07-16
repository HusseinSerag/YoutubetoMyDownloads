import os
import re
from IPython.display import Audio
def get_download_path():
    if os.name == 'nt':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    else:
        return os.path.join(os.path.expanduser('~'), 'downloads')
    

def makefile():
    download = get_download_path()
    saved = os.path.join(download,"MyDownloads")
    if os.path.exists(saved):
        return saved
    else:
        os.mkdir(saved)
        return saved
    
def audiovideo(type):
    path = makefile()
    if type == 'audio':
        saved = os.path.join(path,'MyAudios')
        if os.path.exists(saved):
            return saved
        else:
            os.mkdir(saved)
            return saved
    else:
        saved = os.path.join(path,'MyVideos')
        if os.path.exists(saved):
            return saved
        else:
            os.mkdir(saved)
            return saved



        
def findfile(name):
    download = get_download_path()
    saved = os.path.join(download,"MyAudios")
    link = os.path.join(saved , name)
    return link


def check_password_pattern(password):
    is_password = re.search(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$" , password)
    if is_password :
        return True
    else:
        return False

def check_email_pattern(email):
    is_email = re.search(r"^[A-z0-9]+@([A-z0-9])+\.(\w)+" , email)
        
    if is_email:
        return True
    else:
        return False



