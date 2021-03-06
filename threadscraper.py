from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import substring
import sqlite3
import dateutil.parser as dparser
import datetime

db = "mygbdatabase.db"

#gets all ids for each thread
connection = sqlite3.connect(db)
cursor = connection.cursor()
cursor.execute("SELECT Thread.id FROM Thread")
pages = cursor.fetchall()

#loop, parses and inserts all relevant data into DB
for page in pages:
    url = "https://geekhack.org/index.php?topic=%s" %(page)

    # parsing webpage
    uClient = uReq(url)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")

    #get title of thread associated with id
    title = page_soup.find("div", {"class":"keyinfo"}).find("a").text
    sql = "UPDATE Thread SET thread_name = ? WHERE Thread.id = ?"
    cursor.execute(sql, (title, page[0]))

    # get all images
    imgs = page_soup.find("div", {"class":"inner"}).findAll("img")
    for img in imgs:
        # check if img is in DB
        sql = "SELECT Photo.link FROM Photo WHERE Photo.link = ?;"
        cursor.execute(sql, (img["src"],))
        numrows = int(len(cursor.fetchall()))
        # if not in DB insert into DB
        if numrows == 0:
            sql = "INSERT INTO Photo(thread_id, link) VALUES(?,?)"
            cursor.execute(sql, (page[0], img["src"]))

    # get all links
    links = page_soup.find(
        "div", {"class":"inner"}).findAll("a", {"class":"bbc_link"})
    for link in links:
        # check if link is in DB
        sql = "SELECT Link.link FROM Link WHERE Link.link = ?;"
        cursor.execute(sql,(link["href"],))
        numrows = int(len(cursor.fetchall()))
        # if not in DB insert into DB
        if numrows == 0:
            sql = "INSERT INTO Link(thread_id, link) VALUES(?,?)"
            cursor.execute(sql,(page[0], link["href"]))

    # get post date
    date_str = page_soup.find(
        "div", {"class":"keyinfo"}).find("div", {"class":"smalltext"}
    # parse date into sql YYYY-MM-DD
    date = dparser.parse(date_str).text, fuzzy=True).date()
    sql = "UPDATE Thread SET start_date = ? WHERE Thread.id = ?"
    cursor.execute(sql,(date, page[0]))

    # get starter/user
    try:
        #shorten link to user id
        starter = page_soup.find("div", {"class":"poster"}).find("a")["href"]
        starter_shortened = substring.substringByChar(
            starter_link, startChar=";", endChar = "")
        starter_id = substring.substringByChar(
            starter_link_short, startChar="=", endChar = "")[1:]
    except:
        # if guest account use 0
        starter_id = 0
    starter_name = page_soup.find(
        "div", {"class":"poster"}).find("h4").text.strip()
    # check if starter is already in my db
    sql = "SELECT Starter.id FROM Starter WHERE Starter.id = ?;"
    cursor.execute(sql,(starter_id,))
    numrows = int(len(cursor.fetchall()))
    # if not in db add to db
    if numrows == 0:
        sql = "INSERT INTO Starter(id, starter_name) VALUES(?,?)"
        cursor.execute(sql,(starter_id, starter_name))
    # add starter_id to thread table
    sql = "UPDATE Thread SET starter_id = ? WHERE Thread.id = ?"
    cursor.execute(sql,(starter_id, page[0]))

connection.commit()
connection.close()
print("done xx")
