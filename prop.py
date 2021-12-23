import requests
from bs4 import BeautifulSoup as BS
import csv

def get_html(url):
    responce = requests.get(url)
    return responce.text


def get_data(html):
    soup = BS(html, 'html5lib')
    catalog = soup.find('div', class_='row row-cols-1 row-cols-md-2 row-cols-lg-3 row-cols-xl-4')
    aparts = catalog.find_all('div', class_='property')
    for apart in aparts:
        try:
           price = apart.find('div', class_='price').text.strip()
           img = apart.find('img', class_='p-img').get('src')
           location = apart.find('div', class_='location').text.strip()
           room = apart.find('div', class_='b').text.strip()
           bathroom = apart.find('div', class_='bz').text
           square = apart.find('div', class_='a').text
        except:
            price = 'under contract'
            img = 'not found'
            location = 'not found'
            room = 'not found'
            bathroom = 'not found'
            square = 'not found'


        # try:
        #     img = apart.find('img', class_='p-img').get('src')
        # except:
        #     img = 'not found'
    
        
        # try:
        #     location = apart.find('div', class_='location').text.strip()
        # except:
        #     location = 'not found'

        # try:
        #     room = apart.find('div', class_='b').text.strip()
        # except:
        #     room = 'not found'

        # try:
        #     bathroom = apart.find('div', class_='bz').text
        # except:
        #     bathroom = 'not found'

        # try:
        #     square = apart.find('div', class_='a').text
        # except:
        #     square = 'not found'
        
        data = {
            'location': location,
            'price': price,
            'img': img,
            'description': f'room: {room}, bathroom: {bathroom}, square: {square}'
        }   

        write_to_csv(data)

def write_headers():
      with open('apart.csv', 'a') as  file:
        fieldnames = ['Location', 'Price', 'Photo', 'Description']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
def write_to_csv(data):
    with open('apart.csv', 'a') as  file:
        fieldnames = ['Location', 'Price', 'Photo', 'Description']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow({'Location': data['location'],
                        'Price': data['price'],
                        'Photo': data['img'],
                        'Description': data['description']
                        })

def main():
    with open('apart.csv', 'w') as file:pass
    write_headers()
    i = 1
    while True:
        url = (f'https://www.axcapital.ae/ru/buy/dubai/properties-for-sale?utm_source=google&utm_medium=cpc&utm_campaign=google_%7B1_axcapitalae_komercia_SNG_RUS%7D&utm_content=559444672768&utm_term=%2B%D0%B7%D0%B0%D1%80%D1%83%D0%B1%D0%B5%D0%B6%D0%BD%D0%B0%D1%8F%20%2B%D0%BD%D0%B5%D0%B4%D0%B2%D0%B8%D0%B6%D0%B8%D0%BC%D0%BE%D1%81%D1%82%D1%8C.p.c...p.%2B%D0%B7%D0%B0%D1%80%D1%83%D0%B1%D0%B5%D0%B6%D0%BD%D0%B0%D1%8F%20%2B%D0%BD%D0%B5%D0%B4%D0%B2%D0%B8%D0%B6%D0%B8%D0%BC%D0%BE%D1%81%D1%82%D1%8C&adposition=&gclid=CjwKCAiAtouOBhA6EiwA2nLKH4vieMdPrjQQDCUqkzIcjCW5cfUWuN0s8pu3UxCFeZPtR7j-8ULiihoCHr8QAvD_BwE&page={i}')
        html = get_html(url)
        catalog = BS(html, 'html5lib').findChildren('div', class_='row row-cols-1 row-cols-md-2 row-cols-lg-3 row-cols-xl-4')
        if not catalog:
            break
        (get_data(html=html))
        i += 1

if __name__ == '__main__':
    main()

