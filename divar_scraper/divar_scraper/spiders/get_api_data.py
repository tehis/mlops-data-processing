import requests

#1680773374663766

def get_api_data(last_post_date=16807747371033382, post_category='vehicles', city_number=1):
    url = 'https://api.divar.ir/v8/web-search/{city_number}/{post_category}'.format(
        city_number=city_number,
        post_category=post_category
    )

    headers = {
        'Content-Type': 'application/json'
    }

    json = {"json_schema": {"category": {"value": post_category}},
            "last-post-date": last_post_date}
    res = requests.post(url, json=json, headers=headers)

    data = res.json()

    posts_data = []
    for post in data['web_widgets']['post_list']:
        posts_data.append(
            {
                'title': post['data']['title'],
                'token': post['data']['token'],
                'image_count': post['data']['image_count'],
                'city': post['data']['action']['payload']['web_info']['city_persian'],
                'district': post['data']['action']['payload']['web_info']['district_persian'],
                'top_description_text': post['data']['top_description_text'],
                'price': post['data']['middle_description_text'],
                'bottom_description_text': post['data']['bottom_description_text'],
                'category': post_category
            }
        )

    return posts_data
