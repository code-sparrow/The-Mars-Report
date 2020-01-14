#imports
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    # Visit NASA Mars News site
    url = 'https://mars.nasa.gov/news'
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    #getting title and paragraph
    news_title = soup.find('div', class_="content_title").text
    news_p = soup.find('div', class_="rollover_description_inner").text

    #------------------------------------------------------------------------

    # Visit JPL Mars Space Images site
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    time.sleep(1)

    html = browser.html
    # Create BeautifulSoup object; parse with 'html'
    soup = bs(html, 'html.parser') # --

    #midsize image actually larger than wallpaper
    link = soup.find('a', class_='button fancybox')['data-fancybox-href']
    #midsize image....need full size
    
    #string = soup.find('div', class_='carousel_items').article.get('style')
    #import re
    #string = re.sub(r"background-image: url\('", '', string)
    #link = re.sub(r"'\);", '', string)

    featured_image_url = 'https://www.jpl.nasa.gov' + link

    #------------------------------------------------------------------------

    # Visit Mars Weather Twitter acount
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    # Sometimes had None type error in twitter
    time.sleep(1)
    try:
        html = browser.html
        # Create BeautifulSoup object; parse with 'html'
        soup = bs(html, 'html.parser') # --
        mars_weather = soup.find('p', class_='TweetTextSize').text
    except Exception as e:
        print(e)
        mars_weather = "Latest Mars Weather Tweet is not Currently Available: Try scraping again in a little while."

    #------------------------------------------------------------------------

    # Visit the Mars Facts site
    url = 'https://space-facts.com/mars/'

    # Use pandas to read HTML tables into a list of DataFrame objects
    # choose first df and convert to HTML with no index or column names
    tables = pd.read_html(url)[0].to_html(index=False, header=False)

    #------------------------------------------------------------------------

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    time.sleep(1)

    html = browser.html
    soup = bs(html, 'html.parser')

    #Create List of Hemisphere names (remove "Enhanced" text)
    names = []
    for name in soup.find_all('h3'):
        names.append(name.text[:-9])

        # Find Links to click on, based on hemisphere names list
        # Click the link, find the image url, then go back and repeat
    hemisphere_image_urls = []
    for name in names:
        browser.click_link_by_partial_text(name)
        html = browser.html
        soup = bs(html, 'html.parser')

        # Find image URL
        link = 'https://astrogeology.usgs.gov' + soup.find(class_="wide-image").get('src')
        # and append to list of dicts
        hemisphere_image_urls.append({'title': name, 'img_url': link})

        # Go back to parent site
        browser.back()

    #------------------------------------------------------------------------

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "table": tables,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
