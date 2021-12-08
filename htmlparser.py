from html.parser import HTMLParser;
import urllib.request;
import re;
import mysql.connector
import image;

# -----------database connection-----------
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  # database="mydatabase"
)

# -----------start-----------
info = []

my_url = 'https://www.vrbo.com/vacation-rentals/cabins/usa/north-carolina'
req = urllib.request.Request(my_url, headers={'User-Agent': 'Mozila'})

with urllib.request.urlopen(req) as html:
  html_page = html.read()


class MyHTMLParser(HTMLParser):

  def __init__(self, my_tag, my_attr):
    super().__init__()
    self.my_tag = my_tag
    self.my_attr = my_attr
    self.flag = False
    self.data = []

  def handle_starttag(self, tag, attr):
    if tag == self.my_tag and all(single_attr in attr for single_attr in self.my_attr.items()):
      self.flag= True

  def handle_endtag(self, tag):
    if tag == self.my_tag:
      self.flag = False

  def handle_data(self, data):
    if self.flag == True:
      info.append(data)

#-----------get title-----------

parser = MyHTMLParser('div', {'class': 'CommonRatioCard__description'})
parser.feed(str(html_page))
hotel_title = info
info = []

#-----------get subtitle-----------
final_room = []
parser = MyHTMLParser('div', {'class': 'CommonRatioCard__subcaption'})
parser.feed(str(html_page))
description = info
info = []

#-----------splitting info-----------
for i in range (len(description)):
  temp=description[i].split(' \\xc2\\xb7 ')
  final_room.append(temp)

#-----------get price-----------
parser = MyHTMLParser('span', {'class': 'CommonRatioCard__price__amount'})
parser.feed(str(html_page))
price = info
info = []


def Find(string):
  regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
  url = re.findall(regex,string)
  return [x[0] for x in url]

#-------------------

parser = image.MyHTMLParser()
html_page = urllib.request.urlopen("https://www.vrbo.com/vacation-rentals/cabins/usa/north-carolina")
parser.query = ['script', (), 'text']
parser.feed(str(html_page.read()))

pic = ''
for im in image.images:
  x = re.search("^window.__PRELOADED_STATE__", im)
  if x:
    pic = im
    x = ''

li = re.findall(r'thumbnailUrl(.*?),', pic)

image_list = []

for i in range(18):
  image_list.append(li[i])


image_urls_r = []

flag = 1

temp = []

for url in image_list:

  if flag < 4:

    temp.append(Find(url))

  flag = flag + 1

  if flag > 3:

    flag = 1

    image_urls_r.append(temp)

    temp = []

mycursor = mydb.cursor()
mycursor.execute("SHOW DATABASES")
all_databases = []

# checking if database exixts
for x in mycursor:
  all_databases.append(x[0])

is_create = True

if 'Mueems_Hotel_DB' in all_databases:
  is_create = False

print("All databases:", all_databases)

if is_create:
  database="Mueems_Hotel_DB"
  mycursor = mydb.cursor()
  mycursor.execute("CREATE DATABASE Mueems_Hotel_DB")
  mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database= database
  )
  mycursor = mydb.cursor()
  mySql_Create_Table_Query = """CREATE TABLE Hotel_details(
    Name varchar(250) NOT NULL,
    Sleeps varchar(30),
    Bedroom varchar(30),
    Bathroom varchar(30),
    Image1 varchar(500),
    Image2 varchar(500),
    Image3 varchar(500),
    Price varchar(10),
    PRIMARY KEY (Name))
 """
  mycursor.execute(mySql_Create_Table_Query)

  for i in range(len(image_urls_r)):
    sql = "INSERT INTO Hotel_details (Name, Sleeps, Bedroom, Bathroom, Image1, Image2, Image3, Price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    val = (str(hotel_title[i]), str(final_room[i][0]), str(final_room[i][1]), str(final_room[i][2]), str(image_urls_r[i][0]), str(image_urls_r[i][1]), str(image_urls_r[i][2]), str(price[i]))
    mycursor.execute(sql, val)
    mydb.commit()
    print("1 record inserted", mycursor)

else:
  print('Database already exists')
  # mydb = mysql.connector.connect(
  # host="localhost",
  # user="root",
  # password="",
  # database= "Mueems_Hotel_DB"
  # )
  # mycursor = mydb.cursor()
  # for i in range(len(image_urls_r)):
  #   sql = "INSERT INTO Hotel_details (Name, Sleeps, Bedroom, Bathroom, Image1, Image2, Image3, Price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
  #   val = (str(hotel_title[i]), str(final_room[i][0]), str(final_room[i][1]), str(final_room[i][2]), str(image_urls_r[i][0]), str(image_urls_r[i][1]), str(image_urls_r[i][2]), str(price[i]))
  #   mycursor.execute(sql, val)
  #   mydb.commit()
  #   print("1 record inserted", mycursor)