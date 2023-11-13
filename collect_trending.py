import requests
from bs4 import BeautifulSoup
import argparse as arg
import json

URL_OF_MONTREALGAZZETE = "https://montrealgazette.com/category/news/"
HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'}

def get_trending_stories():

    links = []

    page = requests.get(URL_OF_MONTREALGAZZETE, headers=HEADERS)
    soup = BeautifulSoup(page.content, "html.parser")
    trendings = soup.find("ol",class_="list-widget__content list-unstyled")
    trendings = trendings.find_all("li")
    
    for trend in trendings:
        article = trend.find("a", href=True)
        link = URL_OF_MONTREALGAZZETE[:27] + article["href"]
        links.append(link)

    return links

def get_articles_info(link):

    article_info = {"title": "",
                    "publication_date": "",
		            "author": "",
		            "blurb": ""}

    page = requests.get(link, headers=HEADERS)
    soup = BeautifulSoup(page.content, "html.parser")
    header = soup.find("div",class_="article-header__detail__texts")
    article_info["title"] = header.find("h1",id="articleTitle").text
    article_info["blurb"] = header.find("p",class_="article-subtitle").text

    if header.find("span",class_="published-by__author") == None:
        article_info["author"] = header.find("div",id="wire-company-name").text
    else:
        article_info["author"] = header.find("span",class_="published-by__author").text

    article_info["publication_date"] = header.find("span",class_="published-date__since").text

    return article_info

def main():
    parser = arg.ArgumentParser()

    parser.add_argument("-o","--output_file", required=True,help="output json file")
    args = parser.parse_args()

    articles = []

    links = get_trending_stories()

    for link in links:
        article = get_articles_info(link)
        articles.append(article)

    with open(args.output_file, "w") as file:
        json.dump(articles,file,indent=4)

    
if "__main__" == __name__:
    main()