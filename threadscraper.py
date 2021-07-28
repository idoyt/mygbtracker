from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import substring, sqlite3
import dateutil.parser as dparser
import datetime

db = "mygbdatabase.db"

def update_data(id, status):
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


connection = sqlite3.connect(db)
cursor = connection.cursor()
cursor.execute("SELECT Thread.id FROM Thread")
pages = cursor.fetchall()
connection.close()

for page in pages:
url = "https://geekhack.org/index.php?topic=%s" %(page)

uClient = uReq(url)
page_html = uClient.read()
uClient.close()

page_soup = soup(page_html, "html.parser")

title = page_soup.find("div", {"class":"keyinfo"}).find("a").text
connection = sqlite3.connect(db)
cursor = connection.cursor()
sql = "UPDATE Thread SET thread_name = ? WHERE Thread.id = ?"
cursor.execute(sql,(title, page))
connection.commit()


imgs = page_soup.find("div", {"class":"inner"}).findAll("img")
for img in imgs:
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    sql = "INSERT INTO Photo(thread_id, link) VALUES(?,?)"
    cursor.execute(sql,(page, img["src"]))
    connection.commit()

links = page_soup.find("div", {"class":"inner"}).findAll("a", {"class":"bbc_link"})
for link in links:
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    sql = "INSERT INTO Link(thread_id, link) VALUES(?,?)"
    cursor.execute(sql,(page, link["href"]))
    connection.commit()

matches = dparser.parse(page_soup.find("div", {"class":"keyinfo"}).find("div", {"class":"smalltext"}).text ,fuzzy=True)
connection = sqlite3.connect(db)
cursor = connection.cursor()
sql = "UPDATE Thread SET start_date = ? WHERE Thread.id = ?"
cursor.execute(sql,(matches.date(), page))
connection.commit()

starter_id = substring.substringByChar(substring.substringByChar(page_soup.find("div", {"class":"poster"}).find("a")["href"], startChar=";", endChar = ""), startChar="=", endChar = "")[1:]
starter_name = page_soup.find("div", {"class":"poster"}).find("a").text
starter_img = page_soup.find("div", {"class":"poster"}).find("img",{"class":"avatar"})["src"]
connection = sqlite3.connect(db)
cursor = connection.cursor()
sql = "INSERT INTO Starter(id, starter_name, profile_picture) VALUES(?,?,?)"
cursor.execute(sql,(starter_id, starter_name, starter_img))
sql = "UPDATE Thread SET starter_id = ? WHERE Thread.id = ?"
cursor.execute(sql,(starter_id, page))

connection.commit()
print("done xx")
