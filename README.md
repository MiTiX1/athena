# Blog Scraper

This is a web scraping tool designed to collect blog posts from various websites. It utilizes Scrapy to handle the scraping process and stores the scraped data in a MongoDB database. The scraper can be configured to handle both static and dynamic pages using Selenium where necessary.

## Features

- Scrapes blog content such as titles, text, links, and publish dates.
- Supports scraping dynamic content using Selenium.
- Configurable via JSON-based blog configurations.
- Stores scraped data in MongoDB for easy retrieval and analysis.

## Installation

Set up you mongodb instance. And add the connection URL to the .env file.

```sh
git clone https://github.com/MiTiX1/athena.git
```

```sh
cd blog_scraper
poetry install
```

## Blog Configuration Document model

The blog scraper uses a configuration file for each blog, specifying how to extract content. Below is a sample document model for configuring a blog:

```json
{
    "name": "???",
    "isSelenium": false,
    "lang": "???",
    "startUrl": "???",
    "selectors": {
      "link": "???",
      "title": {
        "cssSelector": "???"
      },
      "text": {
        "cssSelector": "???"
      },
      "date": {
        "cssSelector": "???"
      }
    },
    "isDeleted": false
  }
```

## Running the app

```sh
poetry run main.py
```
