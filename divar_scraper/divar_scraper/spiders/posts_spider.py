import time
import scrapy
from .get_api_data import get_api_data
import csv


url = 'https://divar.ir/v/-/{post_token}'


categories =[
    'light', 'laptops', 'refrigerator-freezer', 'offices', 'watches'
]


class PostsSpider(scrapy.Spider):
    name = "posts"

    def __init__(self, *args, **kwargs):
        super(PostsSpider, self).__init__(*args, **kwargs)

        self._posts_data = []
        self.start_urls = self._generate_urls()
        self._post_index = 0
        self._file_name = 'posts.csv'
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        print('len:', len(self._posts_data))
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

    def parse(self, response):
        self._posts_data[self._post_index]['brand'] = self._extract_brand(response)

        self._posts_data[self._post_index]['description'] = \
            response.css("div").get()

        with open(self._file_name, 'a') as file:
            if self._post_index == 0:
                self._create_file()
            writer = csv.DictWriter(
                file, fieldnames=self._posts_data[0].keys()
            )
            writer.writerow(self._posts_data[self._post_index])
            print('index:', self._post_index)

        self._post_index += 1
        # yield {'cats': category}

    def _generate_urls(self):
        urls = []

        for category in ['vehicles']:
            if category == 'light':
                n_pages = 5
            elif category == 'laptops':
                n_pages = 2
            elif category == 'refrigerator-freezer':
                n_pages = 2
            elif category == 'offices':
                n_pages = 3
            elif category == 'watches':
                n_pages = 2

            for city_number in range(1, 26):
                for _ in range(n_pages):
                    time.sleep(1)
                    retrieved_posts_data = get_api_data(
                        last_post_date=1667468224366943, post_category=category,
                        city_number=city_number
                    )
                    self._posts_data.extend(retrieved_posts_data)
                    for post in retrieved_posts_data:
                        urls.append(url.format(post_token=post['token']))

        return urls

    def _create_file(self):
        with open(self._file_name, 'w', newline='') as file:
            writer = csv.DictWriter(
                file, fieldnames=self._posts_data[0].keys()
            )
            writer.writeheader()

    def _extract_brand(self, response):
        post_fields = response.css(
            "div.kt-unexpandable-row__title-box p.kt-unexpandable-row__title::text"
        ).getall()

        for field in post_fields:
            if 'برند' in field:
                brand = response.css(
                    "div.kt-unexpandable-row__value-box a.kt-unexpandable-row__action::text"
                ).getall()[-1]
                if brand:
                    return brand
                return response.css(
                    "div.kt-unexpandable-row__value-box p.kt-unexpandable-row__value::text"
                ).getall()[-1]
