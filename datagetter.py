from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import substring
import sqlite3
import dateutil.parser as dparser
import datetime

# OPENING CONNECTION TO DB
db = "mygbdatabase.db"
connection = sqlite3.connect(db)
cursor = connection.cursor()

# 70 = group buy 132 = interest check
boards = ["70","132"]
for board in boards:
    root_url = "https://geekhack.org/index.php?board=%s" %(board)
    #opening up connection, grabbing the page
    uClient = uReq(root_url)
    page_html = uClient.read()
    uClient.close()

    #html parsing
    page_soup = soup(page_html, "html.parser")
    #getting last page in the pagination thing
    paging = page_soup.find("div",{"class":"pagesection"})
             .find("div",{"class":"pagelinks"})
             .findAll("a",{"class":"navPages"})
    #the end of link increases by 50 every time you go next page. *50 to get last link
    last_page = paging[len(paging)-2].text
    last_pages = (int(last_page)*50)-50

    #loop through to get all pages
    pages = list(range(0,int(last_pages)+1, 50))
    for page in pages:
        url = "https://geekhack.org/index.php?board=70.%s" %(page)

        #gets the page with all the links
        uClient = uReq(url)
        page_html = uClient.read()
        uClient.close()

        page_soup = soup(page_html, "html.parser")

        # find all classed subject windowbg2 which is where the link is.
        gbs = page_soup.findAll("td", {"class":"subject windowbg2"})
        for gb in gbs:
            link = gb.div.span.a["href"]
            #slice the link until i get the thread id
            s = substring.substringByChar(link, startChar="&", endChar=".")
            a = substring.substringByChar(s, startChar="=", endChar=".")
            # change to 3 for interest check, 2 for gb
            if
            status = 2
            id = int(a[1:-1])
            sql = "SELECT Thread.id FROM Thread WHERE Thread.id = ?;"
            cursor.execute(,(id,))
            numrows = int(len(cursor.fetchall()))
            if numrows == 0:
                # inserts data into the database
                sql = "INSERT INTO Thread(id, status_id) VALUES(?,?)"
                cursor.execute(sql,(id, status))

#gets all ids for each thread
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

# DOWNLOAD ALL IMAGES
#gets all the photo links
connection = sqlite3.connect(db)
cursor = connection.cursor()
sql = "SELECT Photo.id, Photo.link FROM Photo"
something = cursor.execute(sql)
results = something.fetchall()
connection.close()

# loops through the links, downloads them, naming them as the id in the database
for i in results:
    try:
        x = urllib.request.urlretrieve(i[1], f"static/images/{i[0]}.jpg")
    except Exception as e:
        # print it, see which imgs did not download
        print(i)

connection.commit()
connection.close()
print("done xx")
