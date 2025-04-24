from bs4 import BeautifulSoup
import csv

# 读取合并后的文件
with open('douban.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 假设每个页面的内容以特定的分隔符开头，这里以豆瓣页面的 <ol class="grid_view"> 作为分隔依据
page_sections = html.split('<ol class="grid_view">')[1:]

all_data = []

for section in page_sections:
    section = '<ol class="grid_view">' + section
    soup = BeautifulSoup(section, 'lxml')
    movie_list = soup.find('ol', class_='grid_view').find_all('li')
    for movie in movie_list:
        # 电影名称
        title = movie.find('div', class_='hd').find('span', class_='title').get_text()
        # 评价分数
        rating_num = movie.find('div', class_='bd').find('div').find('span', class_='rating_num').get_text()
        # 评论人数
        comment_num = movie.find('div', class_='bd').find('div').find_all('span')[-1].get_text().strip('人评价')
        # 导演和主演信息
        directors_info = movie.find('div', class_='bd').find('p').get_text().strip().split('\n')[0].strip()
        directors = directors_info.split('导演: ')[1].split('主演: ')[0].strip()
        if '主演: ' in directors_info:
            actors = directors_info.split('主演: ')[1].strip()
        else:
            actors = ''
        # 上映时间、出品地、剧情类别
        info = movie.find('div', class_='bd').find('p').get_text().strip().split('\n')[1].strip()
        year = info.split('/')[0].strip()
        country = info.split('/')[1].strip()
        category = info.split('/')[2].strip()
        # 电影标题图链接
        pic = movie.find('div', class_='item').find('div', class_='pic').find('a').find('img').get('src')

        # 第一行：电影名称、评价分数、评论人数
        first_row = [title, rating_num, comment_num, '', '', '', '', '', '']
        # 第二行：导演、主演
        second_row = ['', '', '', directors, actors, '', '', '', '']
        # 第三行：上映时间、出品地、剧情类别、电影标题图链接
        third_row = ['', '', '', '', '', year, country, category, pic]

        all_data.extend([first_row, second_row, third_row])

# 将所有数据保存到 CSV 文件中
with open('douban_movies.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.writer(csvfile)
    # 写入表头
    writer.writerow(
        ['电影名称', '评价分数', '评论人数', '导演', '主演', '上映时间', '出品地', '剧情类别', '电影标题图链接'])
    writer.writerow(['', '', '', '', '', '', '', '', ''])
    writer.writerow(['', '', '', '', '', '', '', '', ''])
    # 写入数据
    writer.writerows(all_data)

print('数据抽取完成，已保存到 douban_movies.csv 文件中。')
