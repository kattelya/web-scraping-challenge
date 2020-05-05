from splinter import Browser
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
from flask import Flask, render_template
from flask_pymongo import PyMongo
import requests
import time

# transfer most of the code that you had written in ipynb to here
def scrape_url():
    executable_path = {"executable_path":"/usr/local/bin/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)

    ### Nasa Mars news - website 1 scrapped
    # Url for Nasa Mars News 
    nasa_url = "https://mars.nasa.gov/news/"
    browser.visit(nasa_url)
    #Scrape page into Soup Object 
    html = browser.html
    # parse HTML with BS 
    soup = bs(html, 'html.parser')
    browser.is_element_present_by_css("li.slide", wait_time=2)

    # parse HTML with BS 
    soup = bs(html, 'html.parser')
    browser.is_element_present_by_css("li.slide", wait_time=2)

    article = soup.select_one("li.slide div.list_text")
    title = article.find("div", class_="content_title").text
    paragraph = article.find("div", class_="article_teaser_body").text


    ### JPL Mars Space Image - Featured 
    #URL for JPL Mars Space Images
    jpl_mars_images = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_mars_images)
    #pause to make sure the webpage to load first.
    time.sleep(3)

    #retrieve background-image url -- still need to fix 
    featured_image_url = browser.links.find_by_partial_text('FULL IMAGE')
    featured_image_url.click()
    time.sleep(3)

    featured_image_url = browser.links.find_by_partial_text('more info')
    featured_image_url.click()
    time.sleep(3)
    
    #Scrape page into Soup object 
    html = browser.html
    soup = bs(html, 'html.parser')
    image_url = soup.select_one('figure.lede a img').get('src')
    website_url = "http://www.jpl.nasa.gov"
    featured_image_url = f"{website_url}{image_url}"

    ###Mars Weather





    #Mars Facts 
    #Visit Space facts website - using pd.read_html that i found online and see from people's example
    mars_fact_df = pd.read_html("https://space-facts.com/mars/")
    mars_fact_df = mars_fact_df[0]
    mars_fact_df = mars_fact_df.rename(columns = { 0 : "Description", 1 : "Values"})
    mars_fact_df
    html_table = mars_fact_df.to_html()

    ###Mars Hemispheres 
    # Visit hemispheres website through splinter module 
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    links = browser.find_by_css("a.product-item h3")

    hemisphere_image_urls = []
    for i in range(len(links)):
        hemisphere = {}
        browser.find_by_css("a.product-item h3")[i].click()
        time.sleep(3)
        sample_elem = browser.find_link_by_text('Sample').first
        hemisphere['img_url'] = sample_elem['href']
        hemisphere['title'] = browser.find_by_css("h2.title").text
        hemisphere_image_urls.append(hemisphere)
        browser.back()
    print(hemisphere_image_urls)

if __name__ == "__main__":
    scrape_url()