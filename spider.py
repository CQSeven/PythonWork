import requests
from bs4 import BeautifulSoup
import time
import json

# 设置请求头，模拟浏览器访问
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# 存储所有电影数据的列表
movies = []

# 分页抓取，每页25条，共10页
for page in range(0, 250, 25):
    url = f'https://movie.douban.com/top250?start={page}'
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 找到所有电影项
        items = soup.find_all('div', class_='item')
        
        for item in items:
            # 提取电影信息
            title = item.find('span', class_='title').text.strip()
            info = item.find('div', class_='bd').p.text.strip()
            info_parts = info.split('\n')
            year_type_country = info_parts[1].strip().split('/')
            year = year_type_country[0].strip()
            country = year_type_country[1].strip()
            movie_type = year_type_country[2].strip()
            
            director_actors = info_parts[0].strip().split('   ')
            director = director_actors[0].replace('导演:', '').strip()
            actors = director_actors[1].replace('主演:', '').strip() if len(director_actors) > 1 else ''
            
            rating = item.find('span', class_='rating_num').text.strip()
            comment_num = item.find('div', class_='star').find_all('span')[-1].text.replace('人评价', '').strip()
            quote_tag = item.find('span', class_='inq')
            quote = quote_tag.text.strip() if quote_tag else ''
            
            # 添加到电影列表
            movies.append({
                'title': title,
                'director': director,
                'actors': actors,
                'year': year,
                'country': country,
                'type': movie_type,
                'rating': rating,
                'comment_num': comment_num,
                'quote': quote
            })
        
        print(f'已抓取第 {page//25 + 1} 页')
        time.sleep(2)  # 防止频繁请求
    
    except requests.exceptions.RequestException as e:
        print(f'请求失败: {e}')
        break

# 保存到JSON文件
with open('douban_top250.json', 'w', encoding='utf-8') as f:
    json.dump(movies, f, ensure_ascii=False, indent=2)

print('数据已保存到 douban_top250.json')