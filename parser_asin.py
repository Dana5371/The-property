from asyncio.tasks import create_task, gather
import requests
from bs4 import BeautifulSoup as BS
import csv
import time
import asyncio
import aiohttp

start_time = time.time()
books_data = []


async def get_page_data(session, page):
   
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
    }  
    url = f'https://www.house.kg/kupit?page={page}'
    async with session.get(url=url, headers=headers) as responce:
    
        soup = BS(await responce.text(), 'lxml')
        catalog = soup.find('div', class_='listings-wrapper')
        aparts = catalog.find_all('div', class_='listing')
      
        
        for apart in aparts:
      
            try:
                title = apart.find('p', class_='title').text.strip()
                location = apart.find('div', class_='address').text.strip()
                price_dollar = apart.find('div', class_='price').text.strip()
                price_som = apart.find('div', class_='price-addition').text.strip()
                description = apart.find('div', class_='description').text.strip()
                link = apart.find('a').get('href')
        
            except:
                title = ''
                location = ''
                price_dollar = ''
                price_som = ''
                description = ''
                link = ''
    url_osh = 'https://www.house.kg/kupit?region=6&town=36&page={page}'
    async with session.get(url=url_osh, headers=headers) as responce:
        third = BS(await responce.text(), 'lxml')
        lists = third.find('div', class_='listings-wrapper')
        aparts_osh = lists.find_all('div', class_='listing')
        for apart in aparts_osh:
            try:
                title = apart.find('p', class_='title').text.strip()
                location = apart.find('div', class_='address').text.strip()
                price_dollar = apart.find('div', class_='price').text.strip()
                price_som = apart.find('div', class_='price-addition').text.strip()
                description = apart.find('div', class_='description').text.strip()
                link = apart.find('a').get('href')
        
            except:
                title = ''
                location = ''
                price_dollar = ''
                price_som = ''
                description = ''
                link = ''


            books_data.append({
            'title': title,
            'location': location,
            'price': f'{price_dollar},{price_som}',
            'description': description,
            'link': f'https://www.house.kg{link}'
            })
            print(books_data)
          

            

  

    

async def gahter_data():
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
    }

    url = 'https://www.house.kg/kupit'
    
    session = aiohttp.ClientSession()
    

    responce = await session.get(url=url, headers=headers)
    soup = BS(await responce.text(), 'lxml')
    tasks = []
    for page in range(1, 22):
        task = asyncio.create_task(get_page_data(session, page))
        tasks.append(task)
        
        
    await asyncio.gather(*tasks)
    await session.close()
  
    


def main():
    asyncio.run(gahter_data())
    finish = time.time()- start_time
    print(f'Time of working {finish}')

if __name__ == '__main__':
    main()

