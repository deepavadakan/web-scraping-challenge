from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()

    # JPL Mars Space Images - Featured Image

    # USe Splinter to navigate to the JPL Featured Space Image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(1)

    # Find the link to featured image
    browser.links.find_by_partial_text('FULL IMAGE').click()

    # Find link to large size image
    browser.links.find_by_partial_text('more info').click()
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # find the featured image
    featured_image_url = "https://www.jpl.nasa.gov/" + soup.find('img', class_='main_image')['src']
    featured_image_desc = soup.find('img', class_='main_image')['title']

    # Mars Hemispheres

    # Use Splinter to navigate to the JPL Featured Space Image
    jpl_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(jpl_url)

    jpl_html = browser.html
    soup = BeautifulSoup(jpl_html, 'html.parser')

    # create empty list for images and titles
    hemisphere_image_urls = []

    lists = soup.find_all('div', class_='item')

    # Find the 4 hemisphere images and titles
    for item in lists:
        
        # Retrieve h3 element that contains title
        title = item.find('h3').text
        print(title)
        
        # Click on link to full size image
        browser.click_link_by_partial_text(title)
        
        # HTML object
        html = browser.html

        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html, 'html.parser')

        # Retrieve list element that contain image
        # Retrieve list element that contain image
        li_element = soup.find_all('li')
        image_url = li_element[0].find('a')['href']
        print(image_url)
        
        # append title, image_url as dict to list
        hemisphere_image_urls_dict = {}
        hemisphere_image_urls_dict["title"] = title
        hemisphere_image_urls_dict["image_url"] = image_url
        hemisphere_image_urls.append(hemisphere_image_urls_dict)
        
        # go back to the main page
        browser.back()


    # NASA Mars News

    # URL of page to be scraped
    mars_news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    # Use Splinter to navigate to the Mars Latest news page
    browser.visit(mars_news_url)

    # wait for the Mars ne page to load, retrive the Mars table
    
    # Mars Facts
    spacefacts_url = 'https://space-facts.com/mars/'

    # Use Panda's `read_html` to parse the url
    tables = pd.read_html(spacefacts_url)

    # Find the Mars facts table and convert to pandas dataframe
    mars_df = tables[0]
    mars_df.columns = ["", "Mars"]
    mars_df.set_index("", inplace=True)

    # Convert the table to html
    mars_facts_html = mars_df.to_html()

    # retrieve the html from the latest Mars news page
    mars_news_html = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(mars_news_html, 'html.parser')
    # find the latest News Title and Paragraph Text
    mars_news = soup.find('div', class_='list_text')

    news_title = mars_news.find('div', class_='content_title').text
    news_p = mars_news.find('div', class_='article_teaser_body').text
    print(news_title)
    print(news_p)

    # Close the browser after scraping
    browser.quit()

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "featured_image_desc":featured_image_desc,
        "mars_facts_html": mars_facts_html,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    # Return results
    return mars_data
