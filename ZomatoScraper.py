from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd

chromepath = r'C:\Users\Jonathan\Box\ZomatoWebScraping-main\chromedriver.exe'

# Initialize Empty List that we will use to store the scraping data results
rest_name = []
rest_type = []
rest_area = []
rest_rating = []
rest_review = []
price_for_2 = []
rest_address = []
rest_phone = []
rest_info = []
rest_lat = []
rest_long = []

# Initialize Webdriver
driver = webdriver.Chrome(chromepath)

out_lst = []

# Loop Through Search Pages that we wanted
for i in range(981, 1004):
    print('Opening Search Pages ' + str(i))
    driver.get('https://www.zomato.com/jakarta/restoran?page={}'.format(i))
    print('Accessing Webpage OK \n')
    url_elt = driver.find_elements_by_class_name("result-title")

    # Loop Through Lists of Web Elements
    for j in url_elt:
        url = j.get_attribute("href")
        out_lst.append(url)

out_df = pd.DataFrame(out_lst, columns=['Website'])

out_df_nd = out_df[~out_df.duplicated(['Website'], keep='first')]


# Scrape the data by looping through entries in DataFrame
for url in out_df_nd['Website']:
    driver.get(url)
    time.sleep(6)
    print('Accessing Webpage OK')

    #Restaurant Name
    try:
        name_anchor = driver.find_element_by_tag_name('h1')
        name = name_anchor.text
        rest_name.append(name)
    except NoSuchElementException:
        name = "404 Error"
        rest_name.append(name)
        pass

    print(f'Scraping Restaurant Name - {name} - OK')

    #Restaurant Type
    rest_type_list = []
    rest_type_eltlist = driver.find_elements_by_xpath("""/html/body/div[1]/div[2]/main/div/section[3]/section/section[1]/section[1]/div/a""")


    for rest_type_anchor in rest_type_eltlist:
        rest_type_text = rest_type_anchor.text
        rest_type_list.append(rest_type_text)

    rest_type.append(rest_type_list)
    print(f'Scraping Restaurant Type - {name} - {rest_type_text} - OK')

    #Restaurant Area
    rest_area_anchor = driver.find_element_by_xpath("""/html/body/div[1]/div[2]/main/div/section[3]/section/section[1]/section[1]/a""")
    rest_area_text = rest_area_anchor.text
    rest_area.append(rest_area_text)
    print(f'Scraping Restaurant Area - {name} - {rest_area_text} - OK')

    #Restaurant Rating
    try:
        rest_rating_anchor = driver.find_element_by_xpath("""/html/body/div[1]/div[2]/main/div/section[3]/section/section[2]/section/div[1]/p""")
        rest_rating_text = rest_rating_anchor.text
    except NoSuchElementException:
        rest_rating_text = "Not Rated Yet"
        pass

    rest_rating.append(rest_rating_text)
    print(f'Scraping Restaurant Rating - {name} - {rest_rating_text} - OK')

    #Restaurant Review
    try:
        rest_review_anchor = driver.find_element_by_xpath("""/html/body/div[1]/div[2]/main/div/section[3]/section/section[2]/section/div[2]/p""")
        rest_review_text = rest_review_anchor.text
    except NoSuchElementException:
        rest_review_text = "Not Reviewed Yet"
        pass

    rest_review.append(rest_review_text)
    print(f'Scraping Restaurant Review Counts - {name} - {rest_review_text} - OK')

    #Restaurant Price for 2
    try:
        price_for_2_anchor = driver.find_element_by_xpath("""/html/body/div[1]/div[2]/main/div/section[4]/section/section/article[1]/section[2]/p[1]""")
        price_for_2_text = price_for_2_anchor.text

    except NoSuchElementException:
        price_for_2_text = "No Price Data Found"
        pass   
            
    if (price_for_2_text[0:2] == 'Rp') or (price_for_2_text[0:2] == 'No'):
        price_for_2.append(price_for_2_text)
    else:
        price_for_2_anchor = driver.find_element_by_xpath("""/html/body/div[1]/div[2]/main/div/section[4]/section/section/article[1]/section[2]/p[2]""")
        price_for_2_text = price_for_2_anchor.text

        if (price_for_2_text[0:2] == 'Rp') or (price_for_2_text[0:2] == 'No'):
            price_for_2.append(price_for_2_text)
        else:
            price_for_2_anchor = driver.find_element_by_xpath("""/html/body/div[1]/div[2]/main/div/section[4]/section/section/article[1]/section[2]/p[3]""")
            price_for_2_text = price_for_2_anchor.text
            price_for_2.append(price_for_2_text)
        
    print(f'Scraping Restaurant Price for Two - {name} - {price_for_2_text} - OK')

    #Restaurant Address
    rest_address_anchor = driver.find_element_by_xpath("""/html/body/div[1]/div[2]/main/div/section[4]/section/article/section/p""")
    rest_address_text = rest_address_anchor.text
    rest_address.append(rest_address_text)
    print(f'Scraping Restaurant Address - {rest_address_text} - OK')

    #Restaurant Phone
    rest_phone_anchor = driver.find_element_by_xpath("""/html/body/div[1]/div/main/div/section[4]/section/article/p""")
    rest_phone_text = rest_phone_anchor.text
    rest_phone.append(rest_phone_text)
    print(f'Scraping Restaurant Phone - {rest_phone_text} - OK')

    #Restaurant Additional Information
    addt_info_list = []
    try:
        addt_info_bigelt = driver.find_element_by_xpath("""/html/body/div[1]/div[2]/main/div/section[4]/section/section/article[1]/section[2]/div[3]""")
        addt_info_eltlist = addt_info_bigelt.find_elements_by_tag_name('p')
    except NoSuchElementException:
        addt_info_eltlist = ["No additional info"]
        pass

    for addt_info_anchor in addt_info_eltlist:
        if isinstance(addt_info_anchor, str):
            addt_info_text = addt_info_anchor
            addt_info_list.append(addt_info_text)
        else:
            addt_info_text = addt_info_anchor.text
            addt_info_list.append(addt_info_text)

    rest_info.append(addt_info_list)
    print(f'Scraping Restaurant Additional Info - {name} - {addt_info_text} - OK')

    print('-------------------------------------------------------------------------------------------------------------------------------------------')


driver.close()

rdf = pd.DataFrame({"Restaurant Name" : rest_name[:], "Restaurant Type" : rest_type[:], "Restaurant Area" : rest_area[:], "Restaurant Rating" : rest_rating[:], "Restaurant Review" : rest_review[:], "Price for 2" : price_for_2[:], "Restaurant Address" : rest_address[:], "Restaurant Phone" : rest_phone[:], "Additional Info" : rest_info[:]})
rdf.to_csv(r'C:\Users\Jonathan\Box\ZomatoWebScraping-main\output.csv')
