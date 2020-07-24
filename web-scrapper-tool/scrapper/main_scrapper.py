from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import search_helper as search
import re
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)

# driver Instance
driver = webdriver.Chrome(executable_path="../extra/chromedriver.exe",
                          options=chrome_options)


def data_id_processing(link):
    find_re = "pid\=.+&l"
    d_id = re.findall(find_re, link)
    d_id = d_id[0].split("=")
    d_id = d_id[1].split("&")
    return d_id[0]


def spec_scrapping(link, data_id, generic_name):
    global database
    driver.get(link)
    driver.implicitly_wait(5)
    price = driver.find_element_by_xpath('//div[@class="_1vC4OE _3qQ9m1"]')
    price1 = price.get_attribute("outerText")
    exp = r"[^0-9]"
    price1 = re.sub(exp, "", price1)
    price1 = int(price1)

    name = driver.find_element_by_xpath('//span[@class="_35KyD6"]')
    name1 = name.get_attribute("outerText")

    try:
        rating = driver.find_element_by_xpath('//div[@class="hGSR34"]')
        rating1 = rating.get_attribute("outerText")
    except NoSuchElementException:
        try:
            rating = driver.find_element_by_xpath('//div[@class="hGSR34 bqXGTW"]')
            rating1 = rating.get_attribute("outerText")
        except Exception:
            rating1 = "N/A"
    try:
        highlights_ul = driver.find_elements_by_xpath('//div[@class="_3WHvuP"]//ul//li')
        highlights_ul1 = [{"highlight": item.get_attribute("outerText")} for item in highlights_ul]
    except NoSuchElementException:
        highlights_ul1 = []

    try:
        img_url = driver.find_element_by_xpath('//div[@class="_3BTv9X _3iN4zu"]//img').get_attribute("src")
    except NoSuchElementException:
        img_url = driver.find_element_by_xpath('//div[@class="_3ZJShS _31bMyl"]//img').get_attribute("src")

    search.store_record({'Product_ID': data_id, 'Product_Name': name1, 'Product_Price': price1,
                         "Product_Generic_Name": generic_name, 'Product_Highlights': highlights_ul1,
                         'Product_Rating': rating1, 'Product_Img_Url': img_url, 'Product_Link': link})
    search.store_terms(name1)
    search.store_terms(generic_name)
    search.store_phrase(name1)
    search.store_phrase(generic_name)
    return


def checking_origin(link):
    flag = False
    value = data_id_processing(link)
    driver.get(link)
    try:
        WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH, '//button[text()="Read More"]')))
        read_more_btn = driver.find_element_by_xpath('//button[text()="Read More"]').click()
        try:
            manufacturing_info_btn = driver.find_element_by_class_name("_39XK9P")
            manufacturing_info_btn.click()
            origin_country_text = driver.find_elements_by_xpath('.//span[contains(@class,"_3hjvBW")]')
            product_origin = [i.get_attribute("outerText") for i in origin_country_text]
            if "india" in product_origin[1].lower():
                print("Indian Product 1")
                flag = True
                spec_scrapping(link, value, product_origin[0])
            else:
                print("Non Indian Product 1")
        except NoSuchElementException:
            origins = driver.find_elements_by_xpath('//div[@class="_2RngUh"]//ul//li//ul//li')
            origin = [i.get_attribute("outerText") for i in origins]
            if len(origin) == 1:
                print("Non Indian Product 2")
            elif origin[1].lower() == "india":
                print("Indian Product 2")
                flag = True
                spec_scrapping(link, value, origin[0])
            else:
                print("Non Indian Product 2")
    except TimeoutException:
        product_more_info = driver.find_element_by_xpath('//div[@class="col col-11-12 ft8ug2"]').click()
        try:
            read_more_btn = driver.find_element_by_xpath('//button[text()="Read More"]').click()
            try:
                manufacturing_info_btn = driver.find_element_by_class_name("_22-mFc").click()
                origin_country_text = driver.find_elements_by_xpath('.//span[contains(@class,"_3hjvBW")]')
                product_origin = [i.get_attribute("outerText") for i in origin_country_text]
                if "india" in product_origin[1].lower():
                    print("Indian Product 3")
                    flag = True
                    spec_scrapping(link, value, product_origin[0])
                else:
                    print("Non Indian Product 3")
            except NoSuchElementException:
                origins = driver.find_elements_by_xpath('//div[@class="col col-9-12 _1BMpvA"]')
                origin = [i.get_attribute("outerText") for i in origins]
                if origin[17].lower() == "india":
                    print("Indian Product 4")
                    flag = True
                    spec_scrapping(link, value, origin[16])
                else:
                    print("Non Indian Product 4")
            except Exception:
                print("Error Occured 2")
        except NoSuchElementException:
            manufacturing_info_btn = driver.find_element_by_class_name("_22-mFc").click()
            origin_country_text = driver.find_elements_by_xpath('.//span[contains(@class,"_3hjvBW")]')
            product_origin = [i.get_attribute("outerText") for i in origin_country_text]
            if "india" in product_origin[1].lower():
                print("Indian Product 5")
                flag = True
                spec_scrapping(link, value, product_origin[0])
            else:
                print("Non Indian Product 5")

    return


def get_product_link(main_product_url):
    try:
        driver.get(main_product_url)
        try:
            WebDriverWait(driver, 10).until(
                ec.visibility_of_element_located((By.XPATH, '//a[contains(@class,"_31qSD5")]')))
            productlink = driver.find_elements_by_xpath('//a[contains(@class,"_31qSD5")]')
            product_link = [i.get_attribute("href") for i in productlink]
            for x in range(len(product_link)):
                print(x)
                checking_origin(product_link[x])
            driver.get(main_product_url)
            try:
                next_page_link = driver.find_element_by_xpath(
                    '//link[contains(@id,"next-page-link-tag")]').get_attribute("href")
                get_product_link(next_page_link)
            except Exception as e:
                print("Last Page 24")
                return

        except TimeoutException:
            WebDriverWait(driver, 10).until(
                ec.visibility_of_element_located((By.XPATH, '//a[contains(@class,"Zhf2z-")]')))
            productlink = driver.find_elements_by_xpath('//a[contains(@class,"Zhf2z-")]')
            product_link = [i.get_attribute("href") for i in productlink]
            for x in range(len(product_link)):
                print(x)
                checking_origin(product_link[x])
            driver.get(main_product_url)
            try:
                next_page_link = driver.find_element_by_xpath(
                    '//link[contains(@id,"next-page-link-tag")]').get_attribute("href")
                get_product_link(next_page_link)
            except Exception as e:
                print("Last Page 40")
                return
    except Exception as e:
        print("Last Page Error\n", e)
    return


# Main Code

search_query = 'tv'
url = "https://www.flipkart.com/search?q=" + search_query

# get_product_link(url)
