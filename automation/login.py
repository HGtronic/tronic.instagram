from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()
user_name = 'type-your-username-here'
user_password = 'type-your-password-here'


def login():

    driver.get('https://www.instagram.com/')

    sleep(2)

    try:
        driver.find_element(By.XPATH, '//button[@class="_a9-- _a9_1"]').click()
    except Exception:
        print('Cookie modal not found')

    sleep(5)

    driver.find_element(
        By.XPATH, '//input[@name="username"]').send_keys(user_name)
    driver.find_element(
        By.XPATH, '//input[@name="password"]').send_keys(user_password)
    driver.find_element(
        By.XPATH, '//button[@class="_acan _acap _acas _aj1-"]').click()

    sleep(5)


if __name__ == "__main__":
    login()
