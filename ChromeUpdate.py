import sys, time, platform
sys.path.insert(0, './modules')

from inform_currentVersion import checkAllUsers, checkCurrUser, get_CurrentVersion
from inform_newVersion import get_page, parse_page, get_NewVersion
from get_Chrome import download_Chrome, install_Chrome


platf=platform.architecture()[0]
print('\nZdravstvuy, dorogoy drug!\n')

# Установленная версия, строка информирования, метод установки, метод проверки
userVersion, infoStr, installMethod, checkMethod=get_CurrentVersion()
print(infoStr)

#Блок условий для модифицирования ссылки загрузки
if installMethod=='allUsers':
    needsAdmin='true'
elif installMethod=='currentUser':
    needsAdmin='false'
    
if platf=='64bit':
    arch='x64-stable-statsdef_1'
    key='B6FA01EA3-136B-EBF0-7F82-89B6536B4C3F'
    tail='ChromeStandaloneSetup64.exe'
else:
    arch='stable-arch_x86-statsdef_1'
    key='BCFC4537C-7A35-A5A7-26EF-ACE9C6512C8B'
    tail='ChromeStandaloneSetup.exe'

directLink='https://dl.google.com/tag/s/appguid'\
           '%3D%7B8A69D345-D564-463C-AFF1-A69D9E530F96%7D%26iid%3D%7'+key+'%7D%26'\
           'lang%3Dru%26browser%3D4%26usagestats%3D0%26appname%3DGoogle%2520Chrome%26needsadmin%3D'+needsAdmin+'%26ap%3D' \
           +arch+'%26installdataindex%3Ddefaultbrowser/update2/installers/'+tail

print('\nChecking the latest version of Google Chrome...')
newVersion=get_NewVersion()

# Проверка, требуется ли обновление
if userVersion==newVersion:
    equalityVers=True
    print('Update is not required.\nYou already have the latest version of Google Chrome:', newVersion)
    print('Do you want to download and install this version?(y or n)')
else:
    equalityVers=False
    print('Latest stable version of Google Chrome:', newVersion)
    print('Do you want to download and install new version?(y or n)')

while True:

    choice=input()
    if choice=='y':
        print('\nDownload Link:\n', '-'*50)
        print(directLink, '\n', '-'*50)

        print('\nDownload...')
        download_Chrome(directLink)
        print('Google Chrome has successfully downloaded')

        print('\nInstall...')
        installStatus=install_Chrome(installMethod, newVersion, equalityVers)

        # Блок условий для проверки успешности установки
        if installStatus:
            # Получение значения ячейки текущей версии по ключу реестра
            # для соответствующего метода проверки
            print('Сheck...')
            if  checkMethod=='allUsers':
                installVersion=checkAllUsers()
            elif checkMethod=='currentUser':
                installVersion=checkCurrUser()
        else:
            time.sleep(80)
            installVersion=checkAllUsers()
        
        if installVersion==newVersion:
            print('Google Chrome %s successfully installed' % installVersion)
            break
        else:
            print('Sorry, something went wrong :(')
            sys.exit()

    elif choice=='n':
        print('\nDownload Link:\n', '-'*50)
        print(directLink, '\n', '-'*50)
        break
    else:
        print('Please enter only correct characters(y or n)')
        continue

print('\nGoodbye!')
