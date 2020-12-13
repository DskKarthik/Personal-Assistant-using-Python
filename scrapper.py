from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
from googlesearch import search
from urllib.request import FancyURLopener
import webbrowser
import urllib

class AppURLopener(FancyURLopener):
    version = "Mozilla/5.0"

def serch_price(query):

    for url in search(query, tld='co.in', stop=10):
        if "amazon" in url:
            amazon_result,found = amazon_scrapper(url)
            if found:
                return amazon_result,url
            else:
                return "Not Found"
            
        if "flipkart" in url:
            fk_result, found = flipkart_scrapper(url)
            return fk_result, url 

def amazon_scrapper(url):

    price = {
        "MRP": "",
        "Amazon price" : ""
    }

    found=True

    html_src = urlopen(url)
    soup=BeautifulSoup(html_src, 'html.parser')

    try:
        price_block=soup.find('div', id="unifiedPrice_feature_div", class_="celwidget")
    except:
        found=False
    else:

        try:
            price["MRP"] = price_block.tr.find('span', class_="priceBlockStrikePriceString a-text-strike").text
        except:
            price["MRP"]="Not Mentioned"

        try:
            price["Amazon price"] = price_block.find('span', id="priceblock_saleprice").text
        except:
            try:
                price["Amazon price"] = price_block.find('span', id="priceblock_ourprice").text
            except:
                price["Amazon price"] = "Not Mentioned"
    
    return price, found

def flipkart_scrapper(url):


    price={ 
        'MRP' : '',
        'Flipkart price': ''
     }

    found=True

    html_src=urlopen(url)
    soup=BeautifulSoup(html_src, 'html.parser')

    try:
        price_block=soup.find('div',class_="_29OxBi")
    except:
        found=False
    else:
        try:
            price["MRP"] = price_block.find('div',class_="_3auQ3N _1POkHg").get_text()
        except:
            price["MRP"] = "Not Mentioned"
        try:
            price["Flipkart price"] = price_block.find('div',class_="_1vC4OE _3qQ9m1").get_text()
        except:
            price["Flipkart price"] = "Not Mentioned"
    
    return price, found

    
def IMDb_Scrapper(url):
    """
    Gets Summary of IMDb
    """
    html=urlopen(url)
    soup=BeautifulSoup(html,"html.parser")
        
    page=soup.find('div',id="main_top",class_="main")
        
    title_block=page.find('div',class_="titleBar").find('div',class_="title_wrapper")
    title=title_block.find('h1',class_="").get_text().replace("\xa0",'..').split('..')[0]
    year=title_block.h1.span.text
        
    print("_"*40,'\n')
        
    print("Film :",title,"  ",year,'\n')
        
    sub_text=title_block.find('div',class_="subtext").text.replace('\n','',15).replace(' ','',100).replace('|',' | ',15)
        
    print(sub_text,'\n')
        
    rating_block=page.find('div',class_="ratingValue")
    rating=rating_block.strong.get_text()
        
    print("Rating : ",rating,'/10 ','\n')
        
    full_page=soup.find('div',id="content-2-wide",class_="flatland")
    story_block=full_page.find('div',class_="article",id="titleStoryLine")
    story_line=story_block.find('div',class_="inline canwrap").p.span.get_text()
        
    print(story_line.strip(),'\n')
        
    details_block=full_page.find('div',class_="article",id="titleDetails")
        
    print("Details:")
    for i in details_block.find_all('div',class_="txt-block"):
        try:
            print(i.h4.text,i.a.text,sep=" : ")
        except:
            pass
    '''
    engine.say(title+", "+year+", "+sub_text)
    engine.say("Rating, "+rating+" out of 10")
    engine.runAndWait()'''

    return title+" "+year+" "+sub_text+". Rating, "+rating+" out of 10."

def get_stock_price(query):
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers={'User-Agent':user_agent,}

    for i in search(query, tld='co.in', stop=20):
        if 'finance.yahoo' in i:
            url = i
            break
    
    #url = "https://in.finance.yahoo.com/quote/BHARTIARTL.NS"
    request=urllib.request.Request(url,None,headers) #The assembled request
    response = urllib.request.urlopen(request)

    html = response.read()
    soup = BeautifulSoup(html, "html.parser")
    page = soup.find('div', id="mrt-node-Lead-3-QuoteHeader")

    price = page.find('span', class_="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)").text
    change = page.find('span', class_="Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($negativeColor)").text

    return price, change

