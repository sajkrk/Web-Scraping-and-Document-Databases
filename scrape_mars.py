def scrape():
    import requests
    from bs4 import BeautifulSoup as bs
    # importing splinter and setting the path as chromedriver
    from splinter import Browser
    import pandas as pd
    # Accessing the webpage
    result = requests.get("https://mars.nasa.gov/news/")


    # 200 response means that the website is accessible
    print(result.status_code)

    # Checking the HTTP header of website to verify that we are in the correct page
    print(result.headers)

    # storing the page content of the website to a variable
    source = result.content
    #print(source)

    # using BeautifulSoup module to parse and process the source
    soup = bs(source, 'lxml')

    #print(soup.prettify())

    # Now, the page source has been processed via BeautifulSoup, we can access the information directly from it
    news_title = soup.title.text
    print(news_title)

    # printing the paragraph text
    news_p = soup.body.find_all('p')[0].text

#    for paragraph in news_p:
#        print(paragraph.text)
    
    #JPL MARS SPACE IMAGES - FEATURED IMAGE
    executable_path = {"executable_path": "chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)

    # finding the image url for the current image
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)

    # finding the image url to the full size .jpg image
    browser.click_link_by_partial_text("FULL IMAGE")
    expand = browser.find_by_css('a.fancybox-expand')
    expand.click()
    html = browser.html
    soup = bs(html, 'html.parser')
    img = soup.find('img', class_='fancybox-image')['src']
    #print(img)

    # passing the path to view the actual image
    featured_image_url = f'https://www.jpl.nasa.gov{img}'
    
    # MARS WEATHER
    weather_url = 'https://twitter.com/marswxreport?lang=en'

    response = requests.get(weather_url)
    soup = bs(response.text, 'html.parser')

    # print(soup.prettify())

    # printing the content 
    contents = soup.find_all('div', class_='content')
    #contents

    # using for loop to find the weather container in a list
    mars_weather = []

    for content in contents:
        tweet = content.find('div', class_='js-tweet-text-container').text
        mars_weather.append(tweet)
        #print(mars_weather)

        # printing the latest weather and saving into variable
        mars_weather = mars_weather[0]
        print(mars_weather)

        # USING PANDAS TO SCRAPE THE TABLE CONTAINING FACTS 

        facts_url = 'https://space-facts.com/mars/'
        table = pd.read_html(facts_url) 

        table[1]

        facts_df = table[1]
        facts_df.columns = ["Facts", "Value"]
        facts_df.set_index("Facts")
        #facts_df

        # USING PANDAS TO CONVERT DATA INTO HTML TABLE STRING
        facts_html = facts_df.to_html()
        facts_html

        #facts_html = facts_html.replace("\n", " ")
        #facts_html 

        # MARS HEMISPHERE

        # Cerberus Hemisphere 
        url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
        response = requests.get(url)
        soup = bs(response.text, 'html.parser')
        
        #print(soup.prettify())

        c_image = soup.find_all('div', class_='wide-image-wrapper')
        print(c_image)

        for image in c_image:
            c_pic = image.find('li')
            full_pic = c_pic.find('a')['href']
            #print(full_pic)
    
            c_title = soup.find('h2', class_='title').text
            #print(c_title)

            Cerberus_hem = {"Title": c_title, "url": full_pic}
            print(Cerberus_hem)

            # Schiaparelli Hemisphere
            url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
            response = requests.get(url)
            soup = bs(response.text, 'html.parser')

            #print(soup.prettify())

            s_image = soup.find_all('div', 'wide-image-wrapper')
            print(s_image)

            for image in s_image:
                s_pic = image.find('li')
                #print(s_pic)
                full_pic = s_pic.find('a')['href']
                #print( full_pic)
    
                s_title = soup.find('h2', class_='title').text
                #print(s_title)

                s_hem = {"Title": s_title, "url": full_pic}
                print(s_hem)

                # Syrtis Major Hemisphere
                url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
                response = requests.get(url)
                soup = bs(response.text, 'html.parser')

                #print(soup.prettify())

                sm_image = soup.find_all('div', 'wide-image-wrapper')
                print(sm_image)
                
                for image in sm_image:
                    sm_pic = image.find('li')
                    #print(sm_pic)
                    full_pic = sm_pic.find('a')['href']
                    #print(full_pic)
    
                    sm_title = soup.find('h2', class_='title').text
                    #print(sm_title)

                    sm_hem = {"Title": sm_title, "url": full_pic}
                    print(sm_hem)

                    # Valles Marineris Hemisphere
                    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'
                    response = requests.get(url)
                    soup = bs(response.text, 'html.parser')

                    #print(soup.prettify())

                    v_image = soup.find_all('div', 'wide-image-wrapper')
                    print(v_image)

                    for image in v_image:
                        v_pic = image.find('li')
                        #print(v_pic)
                        full_pic = v_pic.find('a')['href']
                        #print(full_pic)
    
                        v_title = soup.find('h2', class_='title').text
                        #print(v_title)

                        vm_hem = {"Title": v_title, "url": full_pic}
                        print(vm_hem)

                        hemisphere_image_urls = [Cerberus_hem, s_hem, sm_hem, vm_hem]
                        hemisphere_image_urls
                        
                        results = {
                            "news_title": news_title,
                            "news_p": news_p,
                            "featured_image_url": featured_image_url,
                            "mars_weather" : mars_weather,
                            "facts_html":  facts_html,
                            "hemisphere_image_url": hemisphere_image_urls,
                        }
                        return results
                        