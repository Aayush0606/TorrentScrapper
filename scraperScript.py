import webbrowser
import requests
import re
from bs4 import BeautifulSoup

flag=True

def fetchLink(url):
    try:
        results=requests.get("https://www.1337xxx.to"+url)
        htmlTranslate=BeautifulSoup(results.text,'html.parser')
        tags=htmlTranslate.find_all(text="Magnet Download")
        parents=tags[0].parent
        webbrowser.open(parents['href'])
    except:
        print(url)


while flag:
    toSearch=input("Enter torrent you want to search : ")


    url=f"https://www.1337xxx.to/search/{toSearch}/1/"

    urlFetched=requests.get(url).text
    htmlTranslated=BeautifulSoup(urlFetched,'html.parser')

    try:
        myDict={}
        myLst=[]
        # None if only one page
        last=htmlTranslated.find(class_="last")
        if(last):
            last=last.a['href']
            totalPages=int(last.split('/')[-2])
            for page in range(1,totalPages+1):
                url=f"https://www.1337xxx.to/search/{toSearch}/{page}/"
                urlFetched=requests.get(url).text
                htmlTranslated=BeautifulSoup(urlFetched,'html.parser')
                tbody=htmlTranslated.tbody
                trs=tbody.contents
                trs=list(filter(lambda a: a != '\n', trs))
                for tr in trs:
                    name = tr.contents[1].find_all('a')[1].string
                    size=list(tr.contents[9])[0]
                    myDict[name]=size
                    myLst.append(tr.contents[1].find_all('a')[1]['href'])

        else:
            tbody=htmlTranslated.tbody
            trs=tbody.contents
            trs=list(filter(lambda a: a != '\n', trs))
            for tr in trs:
                name = tr.contents[1].find_all('a')[1].string
                size=list(tr.contents[9])[0]
                myDict[name]=size
                myLst.append(tr.contents[1].find_all('a')[1]['href'])

    
        index=1
        for key in myDict:
            print(index,"\t|",key,"\t|",myDict[key])
            index=index+1
        choice = int(input("Enter Your Choice?(0 to search new -1 to exit) "))
        if(choice==-1):
            flag=False
        elif(choice==0):
            flag=True
        elif(choice>index-1 or choice<1):
            print("Not a valid choice")
        else:
            fetchLink(myLst[choice-1])

    except:
        print("Not Found")
        print("1\tSearch new\n2\tExit")
        flagSetter=int(input())
        if(flagSetter==2):
            flag=False


