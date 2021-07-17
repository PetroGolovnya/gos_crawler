#!/usr/bin/python3

import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


if not os.path.exists('passport'):
    os.makedirs('passport')
path = os.path.join(os.getcwd(), 'passport', 'passport.txt')

driver = webdriver.Firefox()
driver.get("https://www.gosuslugi.ru/")
elem = driver.find_element_by_xpath("//a[text()='Личный кабинет']")
elem.click()

driver.implicitly_wait(5)
elem = driver.find_element_by_name("login")
elem.send_keys("+7(922)2232233")
elem = driver.find_element_by_name("password")
elem.send_keys("password")
elem.send_keys(Keys.RETURN)

wait = WebDriverWait(driver, 20)
wait.until(EC.invisibility_of_element_located((By.ID, 'start-app-loader')))
link = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Документы и данные"]')))
link.click()

with open(path, 'w') as writer:
    rows = driver.find_elements_by_css_selector('lk-rf-passport-card#passport section div.content lk-doc-card-row')
    for row in rows:
        try:
            name = row.find_element_by_css_selector('lk-doc-card-row div:nth-child(1) div.text-help:nth-child(1)')
            value = row.find_element_by_css_selector('lk-doc-card-row div:nth-child(1) div.text-plain.mt-4:nth-child(2)')
            writer.write(f'{name.text} - {value.text}\n')
        except:
            value = row.find_element_by_css_selector('lk-doc-card-row h5.title-h5')
            writer.write(f'Паспорт РФ - {value.text}\n')

driver.close()
