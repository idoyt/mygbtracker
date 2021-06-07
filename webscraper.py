from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import substring

# 70 is for group buys, 132 is for interest checks
gb_url = "https://geekhack.org/index.php?board=70.0" #https://geekhack.org/index.php?board=70.50
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
for i in range(0, 36):
    page_id = i-1 * 0.050
    c = f'{page_id:.3f}'
    url.append(c)
    # visit page with end of url = c
    https://geekhack.org/index.php?board=70.#c
    i += 1


    for gb in gbs:
        link = gb.div.span.a["href"]
        s = substring.substringByChar(link, startChar="&", endChar=".")
        a = substring.substringByChar(s, startChar="=", endChar=".")
        print(a[1:-1])







# https://geekhack.org/index.php?topic={id} testing


#find(div("class": "inner"))
