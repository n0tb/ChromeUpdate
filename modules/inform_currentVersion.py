from winreg import *
import platform


# Функция проверяет, установлен ли Chrome
# в пространство для всех пользователей
def checkAllUsers():
    reg=ConnectRegistry(None,HKEY_LOCAL_MACHINE)
    try:
        if platform.architecture()[0]=='64bit':
            key=OpenKey(reg, r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Google Chrome")
        else:
            key=OpenKey(reg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Google Chrome")
    
    except FileNotFoundError:
        return False
    else:
        version=QueryValueEx(key, "DisplayVersion")
        return version[0]


# Функция проверяет, установлен ли Chrome
# в пространство для текущего пользователя
def checkCurrUser():
    reg=ConnectRegistry(None,HKEY_CURRENT_USER)
    try:
        key=OpenKey(reg, r"Software\Microsoft\Windows\CurrentVersion\Uninstall\Google Chrome")
    except:
        return False
    else:
        version=QueryValueEx(key, "DisplayVersion")
        return version[0]


# Функция на основе того, в какое пространство установлен Chrome, возврящает:
# текущую версию, строку информирования, метод установки, метод проверки
def get_CurrentVersion():
    versAllUsers=checkAllUsers()
    versCurrUser=checkCurrUser()

    if versCurrUser and not versAllUsers:
        installMethod='currentUser'
        checkMethod='currentUser'
        infoStr='You have Google Chrome '+ versCurrUser
        return versCurrUser, infoStr, installMethod, checkMethod

    # Если Chrome установлен в двух пространствах 
    # или только в пространстве для всех пользователей,
    # то необходима установка в пространсвто для всех пользователей,
    # иначе, при установке возникнет ошибка
    elif (versAllUsers and not versCurrUser) or (versAllUsers and versCurrUser):
        installMethod='allUsers'
        checkMethod='allUsers'
        infoStr='You have Google Chrome '+versAllUsers
        return versAllUsers, infoStr, installMethod, checkMethod
    
    # Если ни одно из выше описанных условий не выполнилось,
    # значит браезер не установлен.
    # Установка и проверка будут производится в пространстве
    # текущего пользователя
    else:
        installMethod='currentUser'
        checkMethod='currentUser'
        infoStr='You dont have installed Google Chrome'
        return False, infoStr, installMethod, checkMethod


if __name__=='__main__':
    currVersion, infoStr, installMethod, checkMethod=get_CurrentVersion()
    print('%s. Installation mode: %s. Check mode: %s' % (infoStr, installMethod, checkMethod))