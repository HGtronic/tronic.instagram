import re

import requests
import torch
import transformers
from login import *
from PIL import Image
from selenium.webdriver.support.wait import WebDriverWait
from transformers import (AutoModelForCausalLM, AutoTokenizer,
                          BlipForConditionalGeneration, BlipProcessor)


def comment():
    url = input('Enter instagram account url: ')

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

                    img_url = driver.find_element(
                        By.XPATH, '//div[@class="_aagu _aato"]/div/img').get_attribute('src')

                    description = img_to_text(img_url)
                    print('description => ', description)

                    comment = create_comment_by_description(description)
                    print('comment => ', comment)

                    textarea = driver.find_element(
                        By.XPATH, '//div[@class="_akhn"]/textarea')

                    wait = WebDriverWait(driver, timeout=2, poll_frequency=.2)

                    wait.until(lambda d: textarea.send_keys(comment) or True)

                    sleep(10)

                    driver.find_element(
                        By.XPATH, '//div[@class="_akhn"]/div[2]').click()

                    sleep(5)

                    driver.find_element(
                        By.XPATH, '//div[@class="x160vmok x10l6tqk x1eu8d0j x1vjfegm"]').click()

        if new_height == last_height:
            break

        last_height = new_height

    print(str(len(posts_list)) + ' found')


def img_to_text(img_url):

    processor = BlipProcessor.from_pretrained(
        "Salesforce/blip-image-captioning-large")
    model = BlipForConditionalGeneration.from_pretrained(
        "Salesforce/blip-image-captioning-large")

    raw_image = Image.open(requests.get(
        img_url, stream=True).raw).convert('RGB')

    # unconditional image captioning
    inputs = processor(raw_image, return_tensors="pt")

    out = model.generate(**inputs)
    return processor.decode(out[0], skip_special_tokens=True)


def create_comment_by_description(description):

    model = AutoModelForCausalLM.from_pretrained(
        "tiiuae/falcon-7b-instruct").to_bettertransformer()

    tokenizer = AutoTokenizer.from_pretrained("tiiuae/falcon-7b-instruct")
    pipeline = transformers.pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        torch_dtype=torch.bfloat16,
        trust_remote_code=True,
        device_map="auto",
    )
    sequences = pipeline(
        f"Write a flirty comment on a picture that is described as following: {description}",
        max_length=200,
        do_sample=True,
        top_k=10,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
    )
    for seq in sequences:
        return re.search(r'\n(.*)', seq['generated_text']).group(1)


if __name__ == "__main__":
    comment()
