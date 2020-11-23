import requests
from requests.compat import quote_plus
from django.shortcuts import render
from bs4 import BeautifulSoup
from . import models

# Create your views here.


BASE_BWD_URL = 'https://www.beforward.jp/stocklist/sortkey=n/keyword={}'


def home(request):
    return render(request, 'scrapbase.html')


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_BWD_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')

    listings = soup.find_all('tr', {'class': 'stocklist-row'})
    final_listings = []

    for post in listings:
        if post.find('a', {'class': 'vehicle-url-link'}):
            post_title = post.find('img').get('alt')
            # print(post_title)
            post_url = post.find(
                'a', {'class': 'vehicle-url-link'}).get('href')
            post_price = post.find('span', {'class': 'price'}).text
            # print(post_price)
            post_price2 = post_price.replace('$', '')
            post_price3 = post_price2.replace(',', '')
            post_price_fin = post_price3
            trial = int(post_price_fin)
            post_price_final = trial * 2525
            # print(post_url)

            # print(post_price_final)
            post_image_url = post.find('img').get('src')
            # print(post_url)
            # print(post_price_fin)

            # print(post_image_url)

            final_listings.append(
                (post_title, post_url, post_price_final, post_image_url))

    # print(final_url)

    # print(data)

    stuff_for_frontend = {'search': search,
                          'final_listings': final_listings,
                          }

    return render(request, 'scrapping/new_search.html', stuff_for_frontend)


def car_details(request, name):
    url = request.get_full_path()
    print(url)
    bare_url = url.replace('/scrap/car_details/', '')
    befhm = 'https://www.beforward.jp'
    final_url = befhm + bare_url
    # print(final_url)
    # print(bare_url)
    response = requests.get(final_url)
    data = response.text
    data2 = data.replace(
        ' * [Manufacture Year/month] is provided by database provider. BE FORWARD shall not be responsible for any loss, damages and troubles caused by this information.', '')
    soup = BeautifulSoup(data2, features='html.parser')
    # print(soup.prettify())
    images_bare = soup.find('div', {'id': 'gallery'})
    images = str(images_bare)
    main_img_url = soup.find('img', {'id': 'mainImage'}).get('src')
    # print(main_img_url)
    features = soup.find_all('table', {'class': 'specification'})
    table_rows = []

    for table in soup.find_all('table', {'class': 'specification'}):
        for row in table.find_all('tr'):
            print(row)
            table_rows.append(row.prettify())

    '''
    for table in soup.find_all('table', {'class': 'specification'}):
        for tr in table.find_all('tr'):
            count = count + 1
            th = tr.find('th').get_text()
            td = tr.find('td').get_text()
            table_heads.append(th)
            table_data.append(td)
    '''
    # print(images)
    #  print(features)
    #context = {images, features}

    imgs = []
    for tag in soup.find_all('div', {'id': 'gallery'}):
        for img in tag.find_all('a'):
            imgs_url = img.get('href')
            imgs.append(imgs_url)

    price = soup.find('span', {'class': 'ip-usd-price'})
    context = {
        'imgs': imgs, 'features': features, 'main_img_url': main_img_url, 'table_rows': table_rows, 'price': price, }
    return render(request, 'scrapping/car_details.html', context)


'''
    for post in listings:
        if post.find('span', {'class': 'model-title'}):
            post_title = post.find('span', {'class': 'model-title'}).text
            print(post_title)
            post_url = post.find('a').get('href')
            post_price = post.find('p', {'class': 'bold red'}).text
            print(post_price)
            post_price2 = post_price.replace('$', '')
            post_price3 = post_price2.replace(',', '')
            post_price_fin = post_price3
            trial = int(post_price_fin)
            post_price_final = trial * 2525
            print(post_url)

            print(post_price_fin)
            post_image_url = post.find('img').get('src')
            # print(post_url)
            # print(post_price_fin)

            # print(post_image_url)

            final_listings.append(
                (post_title, post_url, post_price_final, post_image_url))

    # print(final_url)

    # print(data)

    stuff_for_frontend = {'search': search,
                          'final_listings': final_listings,
                          }
                        '''
