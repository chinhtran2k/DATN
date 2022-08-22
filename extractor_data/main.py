from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import random
import pandas as pd
import numpy as np
chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("--disable-notifications")
chrome_options.add_experimental_option('useAutomationExtension', False)

list_house = []

url = 'https://nha.chotot.com/mua-ban-bat-dong-san-tp-ho-chi-minh'
driver = webdriver.Chrome(options=chrome_options, executable_path='D:/dowload/chromedriver.exe')
for i in range(1,2, 1):
    link_url_page = "https://nha.chotot.com/mua-ban-bat-dong-san-tp-ho-chi-minh?page" + str(i)
    driver.get(link_url_page)
    driver.implicitly_wait(random.randint(0,1))
    houses = driver.find_elements(By.CLASS_NAME, value="AdItem_adItem__2O28x")
    for house in houses:
        attr_house = house.get_attribute('href')
        list_house.append(attr_house.split("[")[0])
driver.quit()
df_link = pd.DataFrame({"link":list_house} )
df_link.to_csv("D:/demoDA/links_chotot.csv")
index =['DiaChi','Phuong','TinhTrangBDS','DienTich','Gia/m2','Phongngu','SoNhaVeSinh','GiayTo','TinhTrangNoiThat','SoTang','LoaiHinhNhaO','LoaiHinhDat','image_house']
# data = pd.DataFrame(index)
list_data_house =[]
for item in list_house:
    list_data = {}
    driver = webdriver.Chrome(options=chrome_options, executable_path='D:/dowload/chromedriver.exe')
    driver.get(item)
    driver.implicitly_wait(random.randint(0,1))
    tag_address_house = driver.find_element(By.CLASS_NAME , value="fz13")
    address_house = tag_address_house.text.split("Xem")[0].split(",")[-2]
    if address_house:
        list_data["DiaChi"] = address_house
    else :
        list_data["DiaChi"] = np.nan
    district_house = tag_address_house.text.split("Xem")[0].split(",")[-2]
    if district_house:
        list_data["Quan"] = district_house
    else:
        list_data["Quan"] = np.nan
    tag_house = driver.find_elements(By.CLASS_NAME , value="AdParam_adParamValue__1ayWO")
    for element in tag_house:
        attr=element.get_attribute('itemprop')
        if "property_status" == attr:
            property_status= element.text
            list_data["TinhTrangBDS"] = property_status
        elif "size" == attr:
            size = element.text
            list_data["DienTich"] = size
        elif "rooms" == attr:
            rooms = element.text
            list_data["Phongngu"] = rooms
        elif "floors" == attr:
            floors = element.text
            list_data["SoTang"]= floors
        elif "toilets" == attr:
            toilets = element.text
            list_data["PhongTam"] = toilets
        elif "furnishing_sell" == attr:
            furnishing_sell = element.text
            list_data["TinhTrangNoiThat"] = furnishing_sell
        elif "apartment_type" == attr:
            house_type = element.text
            list_data["Loai"] = house_type
        elif "property_legal_document" == attr:
            property_legal_document = element.text
            list_data["GiayTo"] = property_legal_document
        elif "direction" == attr:
            direction = element.text
            list_data["HuongCuaChinh"] = direction
        elif "balconydirection" == attr:
            balconydirection = element.text
            list_data["HuongBanCong"] = balconydirection
        elif "apartment_feature" == attr:
            apartment_feature = element.text
            list_data["DacDiem"] = apartment_feature
        elif "price_m2" == attr:
            price_m2 = element.text
            list_data["Gia/m2"] = price_m2
            # list_data["USD"] = price_m2 / 24000

        elif "property_status" not in attr:
            list_data["TinhTrangBDS"] = ""
        elif "size" not in attr:
            list_data["DienTich"] = ""
        elif "price_m2" not in attr:
            list_data["Gia/m2"] = ""
        elif "rooms" not in attr:
            list_data["Phongngu"] = ""
        elif "toilets" not in attr:
            list_data["SoNhaVeSinh"] = ""
        elif "property_legal_document" not in attr:
            list_data["GiayTo"] = ""
        elif "furnishing_sell" not in attr:
            list_data["TinhTrangNoiThat"] = ""
        elif "floors" not in attr:
            list_data["SoTang"]= ""
        elif "apartment_type" not in attr:
            list_data["Loai"] = ""
        elif "direction" not in attr:
            list_data["HuongCuaChinh"] = ""
        elif "balconydirection" not in attr:
            list_data["HuongBanCong"] = ""
        elif "apartment_feature" not in attr:
            list_data["DacDiem"] = ""
    list_data_house.append(list_data)
driver.close()
data1 = pd.DataFrame(list_data_house)
data1.to_csv("D:/demoDA/data_house_sale.csv",encoding="utf-8")



