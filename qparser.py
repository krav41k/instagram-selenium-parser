from selenium.webdriver.common.keys import Keys
from seleniumwire import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time


def main():
    path = 'bin / browsermob - proxy'
    driver = webdriver.Chrome()
    driver.get("https://www.instagram.com/")
    delay = 5  # seconds
    action_chain = ActionChains(driver)

    # auth
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//input')))
    except TimeoutException:
        print("Loading took too much time!")

    login_field = driver.find_element_by_xpath("//input[@name='username']")
    password_field = driver.find_element_by_xpath("//input[@name='password']")
    submit_button = driver.find_elements_by_xpath("//button")
    login_field.send_keys("#LOGIN#")
    password_field.send_keys("#PATHWORD#")
    submit_button[0].click()

    # wait for auth
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'coreSpriteKeyhole')))
    except TimeoutException:
        print("Loading took too much time!")

    # redirect to target page
    driver.get("https://www.instagram.com/_victoria___alexandrovna_/")

    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//a[text()=' followers']")))
    except TimeoutException:
        print("Loading took too much time!")

    driver.find_element_by_xpath("//a[text()=' followers']").click()

    # wait for account list
    try:
        WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@class, '_0imsa ')]")))
    except TimeoutException:
        print("Loading took too much time!")

    scroll_element = driver.find_element_by_class_name('isgrP')
    print(scroll_element)
    scroll_pos = 1

    anchor_store = []
    cycle = True
    while cycle:
        title_anchors = driver.find_elements_by_xpath("//a[contains(@class, '_0imsa ')]")
        print(title_anchors)
        print(anchor_store)
        if title_anchors == anchor_store:
            cycle = False
            break
        else:
            new_anchors = [item for item in title_anchors if item not in anchor_store]
            anchor_store = title_anchors
            chain_loader(driver, new_anchors)
            driver.execute_script("document.getElementsByClassName('isgrP')[0].scroll(0, " + str(scroll_pos * 1000) + ");")
            scroll_pos += 1
            time.sleep(4)
            # if scroll_pos == 15:
            #     time.sleep(600)
            # else:
            #     time.sleep(5)

    time.sleep(2)

    counter = 0

    for request in driver.requests:
        if request.response and request.url.find('info') > 0:
            counter += 1
            print(
                request.url,
                request.response.body
            )
    print(counter)

    # driver.find_element_by_xpath("error")


def chain_loader(driver, title_anchors):
    for title_anchor in title_anchors:
        ActionChains(driver).move_to_element(title_anchor).perform()
        time.sleep(1)


if __name__ == "__main__":
    main()
