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

#for page in pages:
url = "https://geekhack.org/index.php?topic=107280" # %s %(page)

uClient = uReq(url)
page_html = uClient.read()
uClient.close()

page_soup = soup(page_html, "html.parser")

title = page_soup.find("div", {"class":"keyinfo"}).find("a").text
print(str(title.encode("UTF-8")))

print("\nPictures")

imgs = page_soup.find("div", {"class":"inner"}).findAll("img")
for img in imgs:
    print(img["src"])

print("\nLinks")
links = page_soup.find("div", {"class":"inner"}).findAll("a", {"class":"bbc_link"})
for link in links:
    print(link["href"])

print("\ndate")
matches = dparser.parse(page_soup.find("div", {"class":"keyinfo"}).find("div", {"class":"smalltext"}).text ,fuzzy=True)
print (matches.date())


print("\nstarter")
starter_id = substring.substringByChar(substring.substringByChar(page_soup.find("div", {"class":"poster"}).find("a")["href"], startChar=";"), startChar="=")[1:]
starter_name = page_soup.find("div", {"class":"poster"}).find("a").text
starter_img = page_soup.find("div", {"class":"poster"}).find("img",{"class":"avatar"})["src"]
print(starter_id, starter_name, starter_img)
print("done xx")
