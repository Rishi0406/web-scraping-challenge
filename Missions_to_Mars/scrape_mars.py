from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import time

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():

    mars_dic = {}
    browser = init_browser()

#NASA Mars News
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(10)
    html = browser.html
    soup = bs(html, 'html.parser')
    news_title = soup.find("div", class_= "bottom_gradient").text
    news_p = soup.find("div", class_= "article_teaser_body").text
    mars_dic['news_title'] = news_title
    mars_dic['news_p'] = news_p

#JPL Mars Space Images - Featured Image
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    time.sleep(10)
    html = browser.html
    image_soup = bs(html, 'html.parser')
    base_url = image_soup.find("a",id="jpl_logo")["href"]
    img_url = image_soup.find("a",id="full_image")["data-fancybox-href"]
    featured_image_url = "https:"+base_url+img_url[1:]
    mars_dic['featured_image_url'] = featured_image_url

#Mars Facts
    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)
    time.sleep(10)
    html = browser.html
    facts = pd.read_html(facts_url)
    mars_facts = facts[0]
    facts_htmltable = mars_facts.to_html(header = False, index = False)
    table = facts_htmltable.replace('\n', '')
    mars_dic['mars_facts'] = table

#Mars Hemispheres
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    time.sleep(5)
    html = browser.html
    hemispheres_soup = bs(html, 'html.parser')
    hemispheres = hemispheres_soup.find_all('div', class_='item')
    base_url='https://astrogeology.usgs.gov'
    hemisphere_image_urls=[]
    for item in hemispheres:
        titles=item.find("h3").text
        titles=titles.strip("Enhanced")
        link=item.find('a', class_="itemLink product-item")['href']
        image_link=base_url+link
        browser.visit(image_link)
        time.sleep(10)
        html = browser.html
        soup = bs(html, "html.parser")
        records = soup.find("div", class_="downloads")
        image_url = records.find("a")["href"]
        hemisphere_image_urls.append({"title": titles, "img_url": image_url})
    mars_dic['hemisphere_image_urls'] = hemisphere_image_urls

    browser.quit()

    return mars_dic

if __name__ == "__main__":
        result = scrape()
        print(result)