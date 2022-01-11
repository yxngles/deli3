from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer as SIA

my_url = "https://edition.cnn.com/2022/01/10/politics/joe-biden-voting-rights/index.html"
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

page_soup = soup(page_html, "html.parser")

filename = "Politico Analysis.csv"
f = open(filename, "w")
headers = ("Things,Move,Impact,Upshot,Positive Score,Negative Score,\n")
f.write(headers)

titles = []
for data in page_soup.findAll("h3", {"class": "story-text__heading-medium"}):
    data = data.text.strip()
    titles.append(data)

p = page_soup.findAll("p", {"class": "story-text__paragraph"})

The_move = []
The_impact = []
The_upshot = []
for data in p:
    if "The move:" in data.text:
        The_move.append(data.text.strip())
    if "The impact:" in data.text:
        The_impact.append(data.text.strip())
    if "The upshot:" in data.text:
        The_upshot.append(data.text.strip())

The_move_final = []
for data in The_move:
    data = data.replace("The move: ", "")
    The_move_final.append(data)

The_impact_final = []
for data in The_impact:
    data = data.replace("The impact: ", "")
    The_impact_final.append(data)

The_upshot_final = []
for data in The_upshot:
    data = data.replace("The upshot: ", "")
    The_upshot_final.append(data)

sid_obj = SIA()
pos_scores = []
neg_scores = []
for data in The_impact_final:
    score = sid_obj.polarity_scores(data)
    pos = score["pos"] * 100
    pos = round(pos, 2)
    pos_scores.append(pos)
    neg = score["neg"] * 100
    neg = round(neg, 2)
    neg_scores.append(neg)

score_specific = sid_obj.polarity_scores(The_move_final[4])
pos_specific = score_specific["pos"] * 100
pos_specific = round(pos_specific, 2)
neg_specific = score_specific["neg"] * 100
neg_specific = round(neg_specific, 2)

n = 0
o = 0
m = 0
for data in range(29):
    if n == 3:
        f.write(str(titles[n]) + "," + str(The_move_final[o].replace(",", "|")) + "," + str(
            The_move_final[o + 1].replace(",", "|")) + "," + str(The_move_final[o + 2].replace(",", "|")) + "," + str(
            pos_specific) + "," + str(neg_specific) + "\n")
        n = n + 1
        o = o + 3
    else:
        f.write(str(titles[n]) + "," + str(The_move_final[o].replace(",", "|").replace(";", "`")) + "," + str(
            The_impact_final[m].replace(",", "|").replace(";", "`")) + "," + str(
            The_upshot_final[m].replace(",", "|").replace(";", "`")) + "," + str(pos_scores[m]) + "," + str(
            neg_scores[m]) + "\n")
        n = n + 1
        o = o + 1
        m = m + 1
f.write(str(titles[-1]) + "," + str(The_move_final[-1].replace(",", "|")) + "," + str(
    The_impact_final[-1].replace(",", "|")) + "," + str(The_upshot_final[-1].replace(",", "|")) + "," + str(
    pos_scores[-1]) + "," + str(neg_scores[-1]) + "\n")
f.close()

