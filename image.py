from html.parser import HTMLParser;
import urllib.request;
import re;

my_url = 'https://www.vrbo.com/vacation-rentals/cabins/usa/north-carolina'
req = urllib.request.Request(my_url, headers={'User-Agent': 'Mozila'})

with urllib.request.urlopen(req) as html:
  html_page = html.read()

#get images
images = []
class MyHTMLParser(HTMLParser):
    
    query = []

    result = {}

    def handle_starttag(self, tag, attrs):
        self.result['name'] = tag
        self.result['attr'] = attrs
       
    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
          tag = self.query[0]
          attr = self.query[1]
          text = self.query[-1]

          if not len(attr):
            try:
              if self.result['name'] == tag:
                images.append(data)
                #print(data)
            except:
              pass
          else:
            pass

