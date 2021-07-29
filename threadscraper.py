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
        sql = "INSERT INTO Thread(id, status_id) VALUES(?,?)"
        cursor.execute(sql,(id, status))
        connection.commit()


connection = sqlite3.connect(db)
cursor = connection.cursor()
cursor.execute("SELECT Thread.id FROM Thread")
pages = cursor.fetchall()

for page in pages:
    url = "https://geekhack.org/index.php?topic=%s" %(page)

    uClient = uReq(url)
    page_html = uClient.read()
    uClient.close()

    page_soup = soup(page_html, "html.parser")

    title = page_soup.find("div", {"class":"keyinfo"}).find("a").text
    sql = "UPDATE Thread SET thread_name = ? WHERE Thread.id = ?"
    cursor.execute(sql,(title, page[0]))
    connection.commit()

    imgs = page_soup.find("div", {"class":"inner"}).findAll("img")
    for img in imgs:
        cursor.execute("SELECT Photo.link FROM Photo WHERE Photo.link = ?;",(img["src"],))
        numrows = int(len(cursor.fetchall()))
        if numrows == 0:
            sql = "INSERT INTO Photo(thread_id, link) VALUES(?,?)"
            cursor.execute(sql,(page[0], img["src"]))
            connection.commit()

    links = page_soup.find("div", {"class":"inner"}).findAll("a", {"class":"bbc_link"})
    for link in links:
        cursor.execute("SELECT Link.link FROM Link WHERE Link.link = ?;",(link["href"],))
        numrows = int(len(cursor.fetchall()))
        if numrows == 0:
            sql = "INSERT INTO Link(thread_id, link) VALUES(?,?)"
            cursor.execute(sql,(page[0], link["href"]))
            connection.commit()

    matches = dparser.parse(page_soup.find("div", {"class":"keyinfo"}).find("div", {"class":"smalltext"}).text ,fuzzy=True)
    sql = "UPDATE Thread SET start_date = ? WHERE Thread.id = ?"
    cursor.execute(sql,(matches.date(), page[0]))
    connection.commit()
    try:
        starter_id = substring.substringByChar(substring.substringByChar(page_soup.find("div", {"class":"poster"}).find("a")["href"], startChar=";", endChar = ""), startChar="=", endChar = "")[1:]
    except:
        starter_id = 0
        print(0)
    starter_name = page_soup.find("div", {"class":"poster"}).find("a").text
    cursor = connection.cursor()
    cursor.execute("SELECT Starter.id FROM Starter WHERE Starter.id = ?;",(starter_id,))
    numrows = int(len(cursor.fetchall()))
    if numrows == 0:
        sql = "INSERT INTO Starter(id, starter_name) VALUES(?,?)"
        cursor.execute(sql,(starter_id, starter_name))
    sql = "UPDATE Thread SET starter_id = ? WHERE Thread.id = ?"
    cursor.execute(sql,(starter_id, page[0]))
    connection.commit()

connection.close()
print("done xx")
