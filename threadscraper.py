from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import substring, sqlite3
import dateutil.parser as dparser
import datetime

db = "mygbdatabase.db"

#grabs all ids i got in linkscraper.py
connection = sqlite3.connect(db)
cursor = connection.cursor()
cursor.execute("SELECT Thread.id FROM Thread")
pages = cursor.fetchall()

#loops through all the ids
for page in pages:
    url = "https://geekhack.org/index.php?topic=%s" %(page)

    uClient = uReq(url)
    page_html = uClient.read()
    uClient.close()

    page_soup = soup(page_html, "html.parser")

    #get title update database entry
    title = page_soup.find("div", {"class":"keyinfo"}).find("a").text
    sql = "UPDATE Thread SET thread_name = ? WHERE Thread.id = ?"
    cursor.execute(sql,(title, page[0]))
    # get all images, update database
    imgs = page_soup.find("div", {"class":"inner"}).findAll("img")
    for img in imgs:
        cursor.execute("SELECT Photo.link FROM Photo WHERE Photo.link = ?;",(img["src"],))
        numrows = int(len(cursor.fetchall()))
        if numrows == 0:
            sql = "INSERT INTO Photo(thread_id, link) VALUES(?,?)"
            cursor.execute(sql,(page[0], img["src"]))
    # get all links, update database
    links = page_soup.find("div", {"class":"inner"}).findAll("a", {"class":"bbc_link"})
    for link in links:
        cursor.execute("SELECT Link.link FROM Link WHERE Link.link = ?;",(link["href"],))
        numrows = int(len(cursor.fetchall()))
        if numrows == 0:
            sql = "INSERT INTO Link(thread_id, link) VALUES(?,?)"
            cursor.execute(sql,(page[0], link["href"]))
    # get post date, update database
    matches = dparser.parse(page_soup.find("div", {"class":"keyinfo"}).find("div", {"class":"smalltext"}).text ,fuzzy=True)
    sql = "UPDATE Thread SET start_date = ? WHERE Thread.id = ?"
    cursor.execute(sql,(matches.date(), page[0]))

    # insert it into the database
    try:
        starter_id = substring.substringByChar(substring.substringByChar(page_soup.find("div", {"class":"poster"}).find("a")["href"], startChar=";", endChar = ""), startChar="=", endChar = "")[1:]
    except:
        # if guest account use 0
        starter_id = 0
    starter_name = page_soup.find("div", {"class":"poster"}).find("h4").text.strip()
    # check if starter is already in my db
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
