import requests
import wget
import re
import sys

from bs4 import BeautifulSoup

def print_error(msg):
    print("scrap error: " + msg)

def check_url(url):
    url_pattern = "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"
    return re.match(url_pattern, url)

def check_filename(image_url):
    cek_url = check_url(image_url) 
    if cek_url is None:
        return print_error("The image URL is invalid")
    
    image_url = image_url.split('?')[0]
    split_url = image_url.split("/")[3:]
    return image_url, '-'.join([str(elem) for elem in split_url])
    

def fetch_image(images, tag):
    for image in images:
        get_images = image.get(tag)

        if get_images is not None:
            image_url, file_name = check_filename(get_images)
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', 'webp')):
                wget.download(image_url, "assets/" + file_name)
        else:
            return print_error("The image is invalid. Please choose a valid image file.")

def scrap(scrap_url, tag_attr):
    if scrap_url == "" or scrap_url is None:
        return print_error("Please provide a URL")
    
    get_url_image = requests.get(scrap_url, headers={"User-Agent": "Mozilla/5.0"})    
    parse_html_url = BeautifulSoup(get_url_image.text, "html.parser")
    images = parse_html_url.find_all('img')

    return fetch_image(images, tag_attr)

try:
    args = sys.argv
    
    if len(args) < 2:
        raise Exception("invalid arguments")
    
    scrap_url = args[1] 
    tag = 'src'

    if len(args) == 3:
        tag = args[2]

    scrap(scrap_url, tag)
except Exception as e:
    print_error(e)

exit(0)
