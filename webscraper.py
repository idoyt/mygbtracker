from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

# 70 is for group buys, 132 is for interest checks
gh_urls = {"gb": "https://geekhack.org/index.php?board=70.0", "ic": "https://geekhack.org/index.php?board=132.0"}
#opening up connection, grabbing the page
uClient = uReq(f"{gh_urls["gb"]}")
page_html = uClient.read()
uClient.close()

#html parsing
page_soup = soup(page_html, "html.parser")

#grabs each thread
gbs = page_soup.findAll("td", {"class":"subject windowbg2"})
isgb = gbs[].text

if [GB] in isgb:
        filename = "links.csv"
        f = open(filename, "w")

        header = "link \n"

        f.write(header)

        for gb in gbs:
            link = gb.div.span.a["href"]
            f.write(link + "\n")

        f.close
else:
    print("not a group buy")

# https://geekhack.org/index.php?topic={id} testing
