# Import Splinter, BeautifulSoup, and Pandas
import pymongo
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import sys



def scrape_all():
    # Set the executable path and initialize Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    news_title, image = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "facts": mars_facts(),
        "mar_news": mars_news(browser),
        "hemisphere_image_info": hemisphere_image(browser)
        }

    #browser.quit()
    return data


# Mars Facts
def mars_facts():
    df = pd.read_html('http://space-facts.com/mars/')[0]

    df.columns = ['Description', 'Mars']
    df.set_index('Description', inplace=True)

    return df.to_html(classes="table table-striped")

def mars_news(browser):
        # Visit the mars nasa news site
        url = 'https://redplanetscience.com/'
        browser.visit(url)

        # Optional delay for loading the page
        browser.is_element_present_by_css('div.list_text', wait_time=1)

        # Convert the browser html to a soup object and then quit the browser
        html = browser.html
        news_soup = soup(html, 'html.parser')

        slide_elem = news_soup.select_one('div.list_text')

        slide_elem.find('div', class_='content_title')

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
        news_p

        # Visit URL
        url = 'https://spaceimages-mars.com'
        browser.visit(url)

        # Find and click the full image button
        full_image_elem = browser.find_by_tag('button')[1]
        full_image_elem.click()

        # Parse the resulting html with soup
        html = browser.html
        img_soup = soup(html, 'html.parser')
        img_soup

        # find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        img_url_rel

        # Use the base url to create an absolute url
        img_url = f'https://spaceimages-mars.com/{img_url_rel}'
        img_url

        df = pd.read_html('https://galaxyfacts-mars.com')[0]
        df.head()

        df.columns=['Description', 'Mars', 'Earth']
        df.set_index('Description', inplace=True)
        df

        df.to_html()
        return news_p, img_url


def hemisphere_image(browser):
        # 1. Use browser to visit the URL
        url = 'https://marshemispheres.com/'
        browser.visit(url)

        # Parse the resulting html with soup
        html = browser.html

        #use soup to find and load into
        hemispheres = soup(html, 'html.parser')

        # using hemisphere load class item to hemi
        hemi = hemispheres.find_all("div", class_="item")

        # 2. Create a list to hold the images and titles.
        hemisphere_image_urls = []

        hemispheres_url = 'https://marshemispheres.com/'


        # 3. Write code to retrieve the image urls and titles for each hemisphere.
        new = []
        for i in hemi:
            #title
            title = i.find("h3").text
            #partial image collect like https://getbootstrap.com/docs/4.1/components/list-group/
            img1_url = i.find('a', class_='itemLink product-item')['href']
            browser.visit(hemispheres_url + img1_url)

          # image
            image_html = browser.html
            web_info = soup(image_html, "html.parser")
    
            img_url = hemispheres_url + web_info.find('img', class_='wide-image').get('src')
            # this comment does not work.
            #img_url = hemispheres_url + web_info.find("img", class_="fancy-image")["src"]
    
            hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
            hemisphere_image_urls
            new.append(hemisphere_image_urls)
        file1 = open('output.txt','w')
        file1.write(str(new))
        file1.close()
        return title, img_url


if __name__ == '__main__':
    print(scrape_all())






