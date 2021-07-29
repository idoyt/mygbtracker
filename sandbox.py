import substring
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup


url = "https://geekhack.org/index.php?topic=26702"

uClient = uReq(url)
page_html = uClient.read()
uClient.close()

page_soup = soup(page_html, "html.parser")
try:
    x = substring.substringByChar(substring.substringByChar(page_soup.find("div", {"class":"poster"}).find("a")["href"], startChar=";", endChar = ""), startChar="=", endChar = "")[1:]
    print(1)
except:
    print("0")
