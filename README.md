# **_The Mars Report_**

A web application that scrapes multiple websites for Mars-related information using a Flask powered backend that stores the data in a mongoDB collection and displays the latest information in a single HTML page.

<img src="Images/mission_to_mars.png" width="60%">  


## Data Sources and Technologies  
* <a href="https://mars.nasa.gov/news/" target="_blank">NASA Mars News Site</a>  
* <a href="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars" target="_blank">JPL Mars Space Images</a>  
* <a href="https://twitter.com/marswxreport?lang=en" target="_blank">Mars Weather Twitter Account</a> 
* <a href="https://space-facts.com/mars/" target="_blank">Mars Facts Table from Space-Facts site</a> 
* <a href="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars" target="_blank">Mars Hemispheres Images from USGS Astrogeology site</a>  
* MongoDB, Python, Pandas, PyMongo, BeautifulSoup, Splinter, Flask, ChromeDriver, HTML, CSS, Bootstrap  

## Backend  
A [Flask App](Missions_to_Mars/app.py)  
* connects to the Mongo database using PyMongo  
* The home route gets the latest mongoDB collection and renders the [HTML template](Missions_to_Mars/templates/index.html)     
* injecting the data into the HTML  
* A scrape route runs the web scraping functions, updates the mongoDB collection with the freshly scraped text data, and redirects back to the home route, where the HTML template is re-rendered     

## Web Scraping
* Initial testing of the web scraping was done in a [Jupyter Notebook](Missions_to_Mars/mission_to_mars.ipynb)
* The [web scraping module](Missions_to_Mars/scrape_mars.py) is ran when the user clicks the button at the top of the page
* First, a Browser istance is created with Splinter using the Chrome driver 
* As each URL is visited with the browser instance, the HTML is passed to and parsed with BeautifulSoup  
&nbsp;&nbsp;&nbsp;&nbsp;`browser.visit(url)`&nbsp;&nbsp;&nbsp;&nbsp;`html = browser.html`&nbsp;&nbsp;&nbsp;&nbsp;`soup = bs(html, "html.parser")`  
* In each case, the HTML in the "soup" object is navigated, and the appropriate text is extracted
* typically based on tags and classes, for example `soup.find('div', class_="article_teaser_body").text`
* This approach failed only with Twitter, where strictly Splinter and regular expressions were used. Such that:

```python
con = browser.find_by_tag('div')
for s in con:
    x = re.findall('InSight[^<]*hPa', s.html, flags=re.S)
    if x:
        mars_weather = x[0]
        break
```
* Finally, a dictionary is created with all of the scraped text (example below), and returned to the scrape route in the Flask app where the mongoDB collection is updated and the app is redirected to the home route

```python
mars_data = {
    "news_title": news_title,
    "news_p": news_p,
    "featured_image_url": featured_image_url,
    "mars_weather": mars_weather,
    "table": tables,
    "hemisphere_image_urls": hemisphere_image_urls
}
```   

## Frontend  
The frontend is a simple HTML template, with Bootstrap, rendered by the Flask app. The record in the mongoDB collection is used the fill the HTML page. The Jumbotron at the top contains a button the user can click on to run the scraping functions, update the mongoDB with new data, and refill the page. 
## Results  

An example of the webpage is pictured below. To run it yourself locally, copy the repository to your computer and run the Python script [app.py](Missions_to_Mars/app.py) from the command-line. Then visit the local url `http://127.0.0.1:5000/` in your browser.  

<img src="Missions_to_Mars/images/webpage.png">
