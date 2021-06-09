from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import substring

#reddit
gb_url = "https://www.reddit.com/r/MechGroupBuys"
#opening up connection, grabbing the page
uClient = uReq(gb_url)
page_html = uClient.read()
uClient.close()

#html parsing
page_soup = soup(page_html, "html.parser")

#grabs each thread
gbs = page_soup.findAll("td", {"class":"subject windowbg2"})

url = []
i = 0

    for gb in gbs:
        link = gb.div.span.a["href"]
        s = substring.substringByChar(link, startChar="&", endChar=".")
        a = substring.substringByChar(s, startChar="=", endChar=".")
        print(a[1:-1])
