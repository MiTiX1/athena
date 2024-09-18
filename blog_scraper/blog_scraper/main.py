import os
os.environ["SCRAPY_SETTINGS_MODULE"] = "blog_scraper.settings"  # nopep8

import logging
import crochet

from bson import ObjectId
from flask import Flask, Response, make_response, request
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.reactor import install_reactor

from blog_scraper.spiders.blog_scraper import BlogScraperSpider
from blog_scraper.settings import PORT, DEBUG
from blog_scraper.mongo_provider import collection_blogs
from blog_scraper.data_validation import (
    input_run_for_schema,
    input_run_on_demand_schema,
)


app = Flask(__name__)
process = CrawlerProcess(get_project_settings())


@crochet.wait_for(timeout=1000)
def scrape_with_crochet(config):
    return process.crawl(BlogScraperSpider, config)


@app.route("/run-on-demand", methods=["POST"])
def run_on_demand() -> Response:
    if request.method != "POST":
        return make_response("Method Not Allowed", 405)

    data = request.get_json()
    err = input_run_on_demand_schema.validate(data)
    if err:
        logging.error(f"Wrong input: {err}")
        return make_response("Bad Request", 400)

    logging.debug("starting scraping...")
    scrape_with_crochet(data)
    logging.debug("finished scraping...")
    return make_response("OK", 200)


@app.route("/run-for", methods=["POST"])
def run_for_blog() -> Response:
    if request.method != "POST":
        return make_response("Method Not Allowed", 405)

    data = request.get_json()
    err = input_run_for_schema.validate(data)
    if err:
        print(f"Wrong input: {err}")
        return make_response("Bad Request", 400)

    config = collection_blogs.find_one({"_id": ObjectId(data["blogId"])})
    if config is None:
        return make_response("No Content", 204)  # unsure if 204 is right

    print("starting scraping...")
    scrape_with_crochet(config)
    print("finished scraping...")

    return make_response("OK", 200)


if __name__ == "__main__":
    install_reactor("twisted.internet.asyncioreactor.AsyncioSelectorReactor")
    crochet.setup()
    app.run("0.0.0.0", port=PORT, debug=bool(DEBUG))
