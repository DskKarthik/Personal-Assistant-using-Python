from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
from googlesearch import search
from urllib.request import FancyURLopener
import webbrowser

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
