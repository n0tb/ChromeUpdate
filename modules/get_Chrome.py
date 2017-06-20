import os, urllib.request, getpass
import  subprocess, ctypes, sys, time
from inform_currentVersion import checkAllUsers


user=getpass.getuser()
sysDrive=os.environ['systemdrive']

def download_Chrome(link):
    try:
        os.mkdir(sysDrive+'\\Users\\'+user+'\\ChromeUpdate')
    except FileExistsError:
        pass
    
    os.chdir(sysDrive+'\\Users\\'+user+'\\ChromeUpdate')
    try:
        urllib.request.urlretrieve(link, 'ChromeStandaloneSetup.exe')
    except urllib.error.URLError:
        print('Error:( Could not connect to the server.\n' \
            'Check your network connection or download link.')
        sys.exit()
    else:
        return True

 
def install_Chrome(installMethod, newVersion, equalityVers):

    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    # Если выполняется от имени администратора,
    # или есть возможность установить в пронстранство текущего пользователя
    if is_admin() or installMethod=='currentUser':
        proc=subprocess.Popen([r'ChromeStandaloneSetup.exe', ' /silent', ' /install'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        error=proc.communicate()[1]
        if error:
            print('Error:', error)
            sys.exit()
        else:
            return True
    
    # Иначе, для установки, необходимо повысить привелегии, вызвав окно UAC.
    # В противном случае, при установке вызовится ошибка
    else:
        command=os.getcwd()+'\\ChromeStandaloneSetup.exe'
        param='/silent /install'
        ctypes.windll.shell32.ShellExecuteW(None, "runas", command, param, None, 0)
        
        # Т.к. после запуска команды runas, скрипт продолжит выполнение,
        # необходимо предоставить врем на установку браузера.
        # Сложно выполнить проверку, когда версии были равны, 
        # поэтому в этом случае функция установка, спустя 80c ожидания, всегда возвращает True 
        if equalityVers:
            time.sleep(80)
            return True
            
        # Иначе, если версии изначально были не равны,
        # то по истечению 50с проверяется значение ячейки версии в реестре
        else:
            time.sleep(50)
            installVersion=checkAllUsers() 
            
            if installVersion==newVersion:
                return True
            else:
                return False


if __name__=='__main__':
    link='https://dl.google.com/tag/s/appguid'\
         '%3D%7B8A69D345-D564-463C-AFF1-A69D9E530F96%7D%26iid%3D%7B6FA01EA3-136B-EBF0-7F82-89B6536B4C3F%7D%26'\
         'lang%3Dru%26browser%3D4%26usagestats%3D0%26appname%3DGoogle%2520Chrome%26needsadmin%3Dfalse%26ap%3D' \
         'x64-stable-statsdef_1%26installdataindex%3Ddefaultbrowser/update2/installers/ChromeStandaloneSetup64.exe'
    
    installMethod='currentUser'
    print('Download...')
    download_Chrome(link)
    print('Install...')
    install_Chrome(installMethod, '59.0.3071.104', 'false')