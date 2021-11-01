import os
from urllib.parse import urlparse
import argparse

import requests
from dotenv import load_dotenv


def shorten_link(headers, link):
  url_for_shorten_link = "https://api-ssl.bitly.com/v4/shorten"
  payload = {"long_url": link}

  response = requests.post(url_for_shorten_link, json=payload, headers=headers)
  response.raise_for_status()
  return response.json()["link"]


def count_clicks(headers, link):
  parsed_link = urlparse(link)
  link_netloc_and_path = f"{parsed_link.netloc}{parsed_link.path}"
  url_for_all_clicks = "https://api-ssl.bitly.com/v4/bitlinks/"\
                       f"{link_netloc_and_path}/clicks/summary"
  response = requests.get(url_for_all_clicks, headers=headers)
  response.raise_for_status()
  return response.json()["total_clicks"]


def is_bitlink(headers, link):
  parsed_link = urlparse(link)
  link_netloc_and_path = f"{parsed_link.netloc}{parsed_link.path}"
  url_for_verification = f"https://api-ssl.bitly.com/v4/bitlinks/{link_netloc_and_path}"
  response = requests.get(url_for_verification, headers=headers)
  return response.ok

if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    description='Сокращение ссылок'
    )
  parser.add_argument('link', help=' Ваша ссылка')
  args = parser.parse_args()
  load_dotenv()
  headers = {"Authorization": f"Bearer {os.getenv('BITLY_TOKEN')}"}
  link = args.link
  if is_bitlink(headers, link):
    print(count_clicks(headers, link))
  else:
    print(shorten_link(headers, link))
