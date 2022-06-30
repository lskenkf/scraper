from datetime import date
import json
import time
import unidecode
from utilities.utility_function import *


def get_max_page_num():
    url = 'https://www.immoberlin.de/home/page/1/'
    soup = get_soup(url)
    hrefs = soup.find_all('div', {'class':'pagination'})[0].find_all('a')
    hrefs = [keep_integers(h['href']) for h in hrefs]
    max_page_num = max(hrefs)
    return max_page_num

def update_json(json_dict, num_page):

    object_makler = 'immoberlin.de'
    current_date = str(date.today())
    url = f'https://www.immoberlin.de/home/page/{num_page}/'
    soup = get_soup(url)
    object_list = soup.find_all('div', {'class': 'detail forhome'})

    for object in object_list:

        object_href = object.find_all('a')[0]['href']
        object_index  = keep_integers(object.find_all('a')[0]['class'][1])

        object_soup = get_soup(object_href)
        title_price = object_soup.find_all('div', {'class': 'wrap clearfix'})[1]
        title = title_price.find_all('h4', {'class': 'title'})[0].text
        location = title.split('-')[0]
        object_location = location.strip()
        price = title_price.find_all('h5', {'class': 'price'})[0].text
        price = price.split('-')
        object_price = keep_integers(price[0])
        try:
            object_type = keep_characters(price[1].strip())
        except:
            object_type = None
        if object_price == 0:
            pass
        else:
            object_image_links = object_soup.find(class_='slides').find_all('img')
            object_image_links = [el['src'] for el in object_image_links]
            object_description = object_soup.find_all('div', {'class':'content clearfix'})[0].text
            object_description = refine_string(object_description)
            print(object_description)
            object_features = object_soup.find_all('ul', {'class': 'arrow-bullet-list clearfix'})[0].find_all('li')
            object_features = [refine_string(feature.text) for feature in object_features]
            print(object_features)
            space_room = object_soup.find('div', {'class': 'property-meta clearfix'})
            space_room = space_room.find_all('span')[:-1]
            space_room = [keep_integers(refine_string(el.text)) for el in space_room]
            object_living_space = space_room[0]
            try:
                object_num_room = space_room[1]
            except:
                object_num_room = None

            object_key = current_date + '_' + object_makler + '_' + str(object_index)
            object_value = {
                'object_price': object_price,
                'object_type': object_type,
                'object_href': str(object_href),
                'object_location': object_location,
                'object_description': object_description,
                'object_features': str(object_features),
                'object_living_space': object_living_space,
                'object_num_room': object_num_room,
                'object_image_links': str(object_image_links),
                'object_makler': object_makler,
                'object_dae': current_date,
                'object_index': object_index
            }

            json_dict[object_key] = object_value

    #time.sleep(10)
    return json_dict


if __name__ == "__main__":

    json_dict = {}
    max_page_num = get_max_page_num()

    for page_num in range(1,2):#max_page_num):
        print(page_num)
        json_dict = update_json(json_dict, page_num)

    import json

    with open('result.json', 'w') as fp:
        json.dump(json_dict, fp)

    print(json_dict)

