import json
from pip._vendor.distlib.compat import raw_input
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from KomplettProduct import KomplettProduct
from dotenv import load_dotenv

URL = "http://www.Komplett.dk/"

# Uses the env file to declare the local path of the chromedriver.
path = load_dotenv('CHROMEDRIVER_PATH')


options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome(path,
                          chrome_options=options)
search_input = str(raw_input("What are you looking for?\n:"))

driver.get(URL)
element = driver.find_element_by_xpath('//*[@id="caasSearchInput"]')
element.send_keys(search_input)
element.send_keys(Keys.ENTER)

productsArray = []


def price_toNumber(price):
    price = price.split("$")[1]
    try:

        price = price.split("\n")[0] + "." + price.split("\n")[1]

    except:
        Exception()
    try:

        price = price.split(",")[0] + "." + price.split("\n")[1]
    except:
        Exception()
    return float(price)


hits = 100
while True:
    try:
        driver.get(driver.current_url + "&hits=" + str(hits))

    except:
        Exception()
    counter = 0
    for i in driver.find_elements_by_xpath('//*[@id="MainContent"]/div/div[2]/div[2]/div[2]/form'):
        print(counter)
        for element in i.find_elements_by_xpath('//div/div'):
            should_add = True
            name = ""
            price = ""
            link = ""
            try:
                name = i.find_elements_by_tag_name('h2')[counter].text
                print(name)

            except:
                should_add = False
            product = KomplettProduct(name, price, link)
            if should_add:
                productsArray.append(product)
            counter += 1
            if counter == 5:
                break
    print(counter)
    break




cheapest_product = KomplettProduct("", "", "")
expensive_product = KomplettProduct("", "", "")

for product in productsArray:
    if product.price < cheapest_product.price:
        product = cheapest_product
    elif product.price > expensive_product.price:
        product = expensive_product

with open('KomplettProducts.json', 'w') as json_file:
    data = {"Products": []}
    for products in productsArray:
        data["Products"].append(products.serialize())
    json.dump(data, json_file, sort_keys=True, indent=4)




print(json.dumps(cheapest_product.serialize(), indent=4, sort_keys=True))
print(json.dumps(expensive_product.serialize(), indent=4, sort_keys=True))

#driver.get(cheapest_product.link)

