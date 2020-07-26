import re
import logging
import mysql.connector
from selenium import webdriver
import search_helper as search
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as ec

driver: None
product_link: None
databaseConnection: None


def sql_insertion(p_dataid, p_name, p_price, p_highlights, p_rating, p_generic_name, p_img_url, p_link):
    if databaseConnection:
        try:
            cursor = databaseConnection.cursor()
            cursor.execute(
                "SELECT EXISTS(SELECT * FROM product.product_info WHERE Product_ID = '%s' AND Product_Name = '%s')" %
                (p_dataid, p_name))
            results = cursor.fetchone()
            if results[0] == 0:
                p_highlights2str = '&'.join(map(str, p_highlights))
                insert_stmt = (
                    "INSERT INTO product.product_info(Product_ID,Product_Name,Product_Price,Product_Highlights,"
                    "Product_Rating,Product_Generic_Name,Product_Img_Url,Product_Link) "
                    "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)")
                insert_data = (p_dataid, p_name, p_price, p_highlights2str, p_rating, p_generic_name, p_img_url, p_link)
                cursor.execute(insert_stmt, insert_data)
                databaseConnection.commit()
                logging.info("%s Data inserted", p_dataid)
            else:
                pass
        except Exception as e:
            logging.exception("Exception")
            databaseConnection.rollback()
            return e


def data_id_processing(link):
    find_re = "pid\=.+&l"
    d_id = re.findall(find_re, link)
    d_id = d_id[0].split("=")
    d_id = d_id[1].split("&")
    return d_id[0]


def spec_scrapping(link, data_id, generic_name):
    global highlights_ul
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
        logging.exception("Exception")
        rating = driver.find_element_by_xpath('//div[@class="hGSR34 bqXGTW"]')
        rating1 = rating.get_attribute("outerText")
        if rating is not None:
            rating1 = float(rating1)
        else:
            rating1 = float(0)
    try:
        highlights_ul = driver.find_elements_by_xpath('//div[@class="_3WHvuP"]//ul//li')
        highlights_ul1 = [item.get_attribute("outerText") for item in highlights_ul]
    except NoSuchElementException:
        logging.exception("Exception")
        highlights_ul1 = []

    try:
        img_url = driver.find_element_by_xpath('//div[@class="_3BTv9X _3iN4zu"]//img').get_attribute("src")
    except NoSuchElementException:
        logging.exception("Exception")
        img_url = driver.find_element_by_xpath('//div[@class="_3ZJShS _31bMyl"]//img').get_attribute("src")

    if data_id and name1 and price1 and generic_name:
        sql_insertion(data_id, name1, price1, highlights_ul1, rating1, generic_name, img_url, link)
        highlights = [{"highlight": item.get_attribute("outerText")} for item in highlights_ul]
        search.store_record({'Product_ID': data_id, 'Product_Name': name1, 'Product_Price': price1,
                             "Product_Generic_Name": generic_name, 'Product_Highlights': highlights,
                             'Product_Rating': rating1, 'Product_Img_Url': img_url, 'Product_Link': link})
        search.store_terms(name1)
        search.store_terms(generic_name)
        search.store_phrase(name1)
        search.store_phrase(generic_name)


def checking_origin(link):
    value = data_id_processing(link)
    driver.get(link)
    try:
        WebDriverWait(driver, 0).until(ec.visibility_of_element_located((By.XPATH, '//button[text()="Read More"]')))
        driver.find_element_by_xpath('//button[text()="Read More"]').click()
        try:
            manufacturing_info_btn = driver.find_element_by_class_name("_39XK9P")
            manufacturing_info_btn.click()
            origin_country_text = driver.find_elements_by_xpath('.//span[contains(@class,"_3hjvBW")]')
            product_origin = [i.get_attribute("outerText") for i in origin_country_text]
            for origin in product_origin:
                if "india" in origin.lower() and len(origin) == 5:
                    spec_scrapping(link, value, product_origin[0])
        except NoSuchElementException:
            logging.exception("Exception")
            origins = driver.find_elements_by_xpath('//div[@class="_2RngUh"]//ul//li//ul//li')
            if len(origins) > 0:
                origin = [i.get_attribute("outerText") for i in origins]
                for o in origin:
                    if "india" in o and len(o) == 5:
                        spec_scrapping(link, value, origin[0])
    except TimeoutException:
        logging.exception("Exception")
        try:
            driver.find_element_by_xpath('//div[@class="col col-11-12 ft8ug2"]').click()
            try:
                driver.find_element_by_xpath('//button[text()="Read More"]').click()
                try:
                    driver.find_element_by_class_name("_22-mFc").click()
                    origin_country_text = driver.find_elements_by_xpath('.//span[contains(@class,"_3hjvBW")]')
                    if len(origin_country_text) > 0:
                        product_origin = [i.get_attribute("outerText") for i in origin_country_text]
                        if len(product_origin) > 0:
                            for o in product_origin:
                                if "india" in o.lower() and len(o) == 5:
                                    spec_scrapping(link, value, product_origin[0])
                except NoSuchElementException:
                    logging.exception("Exception")
                    origins = driver.find_elements_by_xpath('//div[@class="col col-9-12 _1BMpvA"]')
                    if len(origins) > 0:
                        origin = [i.get_attribute("outerText") for i in origins]
                        if len(origin) > 0:
                            if origin[len(origin) - 1].lower() == "india" and len(origin[len(origin) - 1].lower()) == 5:
                                spec_scrapping(link, value, origin[len(origin) - 2])
            except NoSuchElementException:
                logging.exception("Exception")
                try:
                    driver.find_element_by_class_name("_22-mFc").click()
                    origin_country_text = driver.find_elements_by_xpath('.//span[contains(@class,"_3hjvBW")]')
                    if len(origin_country_text):
                        product_origin = [i.get_attribute("outerText") for i in origin_country_text]
                        if len(product_origin) > 0:
                            for o in product_origin:
                                if "india" in o.lower() and len(o) == 5:
                                    spec_scrapping(link, value, product_origin[0])
                except NoSuchElementException:
                    logging.exception("Exception")
        except Exception as e:
            logging.exception("Exception")
            return e


def get_product_link(main_product_url):
    global product_link
    try:
        driver.get(main_product_url)
        elements = driver.find_elements_by_xpath('//a[contains(@class,"_31qSD5")]')
        if elements:
            product_link = [i.get_attribute("href") for i in elements]
            for x in range(len(product_link)):
                print(x)
                checking_origin(product_link[x])
        else:
            elements = driver.find_elements_by_xpath('//a[contains(@class,"Zhf2z-")]')
            if elements:
                product_link = [i.get_attribute("href") for i in elements]
                for x in range(len(product_link)):
                    print(x)
                    checking_origin(product_link[x])
            else:
                products_links = driver.find_elements_by_xpath('//a[contains(@class,"_3dqZjq")]')
                product_link = [i.get_attribute("href") for i in products_links]
                for x in range(len(product_link)):
                    print(x)
                    checking_origin(product_link[x])
        try:
            next_page_link = driver.find_element_by_xpath('//link[contains(@id,"next-page-link-tag")]'). \
                get_attribute("href")
            get_product_link(next_page_link)
        except Exception as e:
            logging.exception("Last Page Exception")
            print("Last Page")
            return e
    except Exception as e:
        logging.exception("Last Page Error Exception")
        print("Last Page Error")
        return e


def scrape(product):
    url = "https://www.flipkart.com/search?q=" + product
    global databaseConnection, driver
    databaseConnection = mysql.connector.connect(
        host="localhost", user="root", password="Hellobrother@9327", database="product")
    # Chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(executable_path="../extra/chromedriver.exe", options=chrome_options)
    get_product_link(url)
    databaseConnection.close()


if __name__ == '__main__':
    logging.basicConfig(filename='logs', filemode='w', format='%(name)s : %(levelname)s : %(asctime)s: %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S')
