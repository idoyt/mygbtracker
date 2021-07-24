from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import substring, sqlite3

db = "mygbdatabase.db"

# 70 is for group buys, 132 is for interest checks
root_url = "https://geekhack.org/index.php?board=70.0"
#opening up connection, grabbing the page
uClient = uReq(root_url)
page_html = uClient.read()
uClient.close()

def add_id(id, status):
    '''add data to table'''
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    cursor.execute("SELECT Thread.id FROM Thread WHERE Thread.id = ?;",(id,))
    numrows = int(len(cursor.fetchall()))
    if numrows == 0:
        cursor = connection.cursor()
        # inserts data into the database where collumn names = champion, cost, etc
        sql = "INSERT INTO Thread(id, status_id) VALUES(?,?)"
        # replaces the ?'s with user inputs
        cursor.execute(sql,(id, status))
        connection.commit()


#html parsing
page_soup = soup(page_html, "html.parser")
paging = page_soup.find("div",{"class":"pagesection"}).find("div",{"class":"pagelinks"}).findAll("a",{"class":"navPages"})
last_page = paging[len(paging)-2].text
last_pages = (int(last_page)*50)-50

pages = list(range(0,int(last_pages)+1, 50))
for page in pages:
    url = "https://geekhack.org/index.php?board=70.%s" %(page)

    uClient = uReq(url)
    page_html = uClient.read()
    uClient.close()

    page_soup = soup(page_html, "html.parser")

    gbs = page_soup.findAll("td", {"class":"subject windowbg2"})
    for gb in gbs:
        link = gb.div.span.a["href"]
        s = substring.substringByChar(link, startChar="&", endChar=".")
        a = substring.substringByChar(s, startChar="=", endChar=".")
        status = 2
        id = int(a[1:-1])
        add_id(id, status)

print("done xx")
