from lxml import html
import requests
import re
page = requests.get('http://www.profixio.com/fx/serieoppsett.php?t=Korpen_SERIE_AVD5836&k=LS5836&p=1')
hm = html.fromstring(page.content)
tr = hm.xpath('//*[@id="main-col"]/div[3]/div[1]/div[2]/table/tr/td/text()')
row = 0
col = 0
game=[]
total=[]
for l in tr:
  game.append(l)
  col += 1
  if col == 6:
    total.append(game)
    game = []
    row += 1
    col = 0
for a in total:
  # regexpa ut match och status
  m = re.search('(^[0-9][0-9]\:[0-9][0-9]$)', a[0])
  if m:
    if len(a) == 6:
      print a
