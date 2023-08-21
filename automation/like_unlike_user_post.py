from login import *


def like_unlike_user_post():

    url = input('Enter instagram account url: ')
    action = ''
    while action not in {'like', 'unlike'}:
        action = input('Enter action (like/unlike): ').lower()

    login()

    driver.get(url)

    sleep(5)

    last_height = driver.execute_script("return document.body.scrollHeight")

    posts_list = []

    while True:

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

        sleep(10)

        new_height = driver.execute_script("return document.body.scrollHeight")

        main_div = driver.find_element(
            By.XPATH, '//article[@class="x1iyjqo2"]')

        rows = main_div.find_elements(By.XPATH, '//div[@class="_ac7v  _al3n"]')

        for row in rows:
            sleep(10)

            for post in row.find_elements(By.XPATH, '//div[@class="_aabd _aa8k  _al3l"]'):

                post_link = post.find_element(
                    By.TAG_NAME, 'a').get_attribute('href')

                if post_link not in posts_list:

                    posts_list.append(post_link)
                    post.click()

                    sleep(5)

                    heart_button = driver.find_element(
                        By.XPATH, '//span[@class="_aamw"]/div/div/span')

                    if action == 'like' and heart_button.find_element(By.TAG_NAME, 'svg').get_attribute('fill') == 'rgb(245, 245, 245)':
                        heart_button.click()

                    if action == 'unlike' and heart_button.find_element(By.TAG_NAME, 'svg').get_attribute('fill') != 'rgb(245, 245, 245)':
                        heart_button.click()

                    driver.find_element(
                        By.XPATH, '//div[@class="x160vmok x10l6tqk x1eu8d0j x1vjfegm"]').click()

        if new_height == last_height:
            break

        last_height = new_height

    print(str(len(posts_list)) + ' found')


if __name__ == "__main__":
    like_unlike_user_post()
