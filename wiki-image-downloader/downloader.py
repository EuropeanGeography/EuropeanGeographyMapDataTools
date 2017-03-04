#!/usr/bin/env python3

import argparse
import requests
import json
import os
import logging
import urllib.request as request
from html.parser import HTMLParser

base_url = "https://en.wikipedia.org"


class MLStripper(HTMLParser):

    def error(self, message):
        pass

    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def format_api_request_for_title(title):
    api_access_url = base_url + "/w/api.php"
    params = {'action': 'query',
              'format': 'json',
              'prop': 'imageinfo',
              'titles': title,
              'utf8': '1',
              'iiprop': 'url|extmetadata',
              'iilimit': '5',
              'iiextmetadatamultilang': '1'}

    return api_access_url, params


def parse_to_expected_metadata_json(extmetadata):
    metadata = {'description': {}}
    en_present = False
    for key, value in extmetadata['ImageDescription']['value'].items():
        if key != '_type' and len(key) == 2:
            metadata['description'][key] = strip_tags(value)
            if key == "en":
                en_present = True
    if not en_present:
        logging.warning("No 'en' tag present for description! You have to add it manually!")
    metadata['author'] = strip_tags(extmetadata['Artist']['value'])
    metadata['license'] = extmetadata['LicenseShortName']['value']
    return metadata


def get_image_info_child(key, response_text):
    pages = json.loads(response_text)['query']['pages']
    page = pages[next(iter(pages))]
    return page['imageinfo'][0][key]


def download_image(url):
    req = request.urlopen(url)
    data = req.read()
    return data


def get_extension(filename: str):
    return filename.split(".")[1]


def strip_extension(filename: str):
    return filename.split(".")[0]


def get_text_after_last_slash(text):
    return text.rsplit('/', 1)[-1]


def save_data(country_code, image_data, metadata, image_name):
    directory = country_code
    if not os.path.exists(directory):
        os.makedirs(directory)
    files = os.listdir(directory)
    if len(files) == 0:
        max_number = 1
    else:
        max_number = int(max(map(strip_extension, files))) + 1

    base_path = os.path.join(directory, str(max_number))

    json_data = open(base_path + ".json", 'w+')
    json_data.write(json.dumps(metadata, sort_keys=True, indent=4, ensure_ascii=False))
    json_data.close()

    image_file = open(base_path + "." + get_extension(image_name), 'wb+')
    image_file.write(image_data)
    image_file.close()


def download_data_and_write_them_to_disk(country, url):
    page_title = get_text_after_last_slash(url)

    request_url, params = format_api_request_for_title(page_title)
    response = requests.get(request_url, params=params)
    print("Response code from server: ", response.status_code)

    # download image
    image_url = get_image_info_child("url", response.text)
    image_name = get_text_after_last_slash(image_url)
    image = download_image(get_image_info_child("url", response.text))

    # prepare metadata
    metadata = parse_to_expected_metadata_json(get_image_info_child('extmetadata', response.text))
    metadata['source_url'] = url
    metadata['original_file'] = page_title.split(':')[1]

    # write data to disc
    save_data(country, image, metadata, image_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Metadata and photo downloader from Wikipedia.')
    parser.add_argument('--url', dest='url', type=str, help='url of file which will be downloaded', required=True)
    parser.add_argument('--country', dest='country', type=str, help='country code of country to which the photo belongs',
                        required=True)
    args = parser.parse_args()
    download_data_and_write_them_to_disk(country=args.country, url=args.url)
