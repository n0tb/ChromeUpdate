import urllib.request,  re, sys
from bs4 import BeautifulSoup

# Функция загрузки HTML кода страницы
def get_page(url):
    try:
        page=urllib.request.urlopen(url)
    except urllib.error.URLError:
        print('Error:( Could not connect to the server.\n' \
            'Check your network connection or link to ', url)
        sys.exit()

    else:
        return page.read()

# Функция поиска ссылки на последний пост с релизом
# стабильной версии Chrome на настольные платформы
def parse_page(html):    
    soup=BeautifulSoup(html, 'html5lib')
    tagA=soup.find('a', attrs={'title':'Stable Channel Update for Desktop'})
    if tagA:
        link=tagA.get('href')
        return link
    
    # Если на первой странице не найдена ссылка с соответствующим заголовком,
    # то вызовается рекурсивно функция parse_page(get_page(urlPreviousPage)),
    # в каторую передаётся HTML код предыдущей страницы c постами
    else:
        tagPreviousPage=soup.find('a', 'blog-pager-older-link')
        if tagPreviousPage:
            urlPreviousPage=tagPrevioustPage.get('href')
            return parse_page(get_page(urlPreviousPage))
        else:
            print('Eror:( Element "blog-pager-older-link" not found. The element may have changed.')
            sys.exit()

# Функция производит поиск ссылки, в заголовке которой
# указан номер последней версии
def get_NewVersion():
    
    # linkReleasePost—ссылка на последний пост с релизом
    # стабильной версии Chrome для настольных платформ
    linkReleasePost=parse_page(get_page('https://chromereleases.googleblog.com/search/label/Stable%20updates'))
    
    # Получить HTML код этого поста
    html=get_page(linkReleasePost)
    soup=BeautifulSoup(html, 'html5lib')
    
    #Получить содержимое контейнера, тем сымым уменьшить область поиска 
    textPage=soup.body.find('div', attrs={'itemprop':'articleBody'})
    if textPage:
        textPage=textPage.text
        # поиск совподения текста при помощи регудярного выражения
        match=re.search(r'https://chromium\.googlesource\.com/chromium/src/\+log.{1,}?pretty=fuller&amp;n=1000', textPage)
    else:
        print('Eror:( Element "itemprop:articleBody" not found. The element may have changed.')
        sys.exit()
    
    # Если совпадение есть, выделить номер версии
    if match:
        rawString=re.search(r'\.\..{1,}\?', match.group(0)).group(0)
        newVersion=rawString[2:-1]
        return newVersion
    else:
        print('Error:( Link "https://chromium\.googlesource\.com/chromium/src/\+log.d.d.d.d?pretty=fuller&amp;n=1000" not found.'\
            'Maybe the link format was changed.')
        sys.exit()
    

if __name__=='__main__':
    newVersion=get_NewVersion()
    print('Latest version of Google Chrome:', newVersion)
