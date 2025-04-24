import requests

# 定义请求的 URL
urls = [
    "https://movie.douban.com/top250",
    " https://movie.douban.com/top250?start=25&filter=",
    " https://movie.douban.com/top250?start=50&filter=",
    " https://movie.douban.com/top250?start=75&filter=",
    " https://movie.douban.com/top250?start=100&filter=",
    " https://movie.douban.com/top250?start=125&filter=",
    " https://movie.douban.com/top250?start=150&filter=",
    " https://movie.douban.com/top250?start=175&filter=",
    " https://movie.douban.com/top250?start=200&filter=",
    " https://movie.douban.com/top250?start=225&filter=",

]

# 设置请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}

# 设置代理
proxies = {
    "http": None,
    "https": None
}

try:
    with open("douban.html", "w", encoding="utf-8") as f:
        for url in urls:
            try:
                # 发送请求
                response = requests.get(url=url, headers=headers, proxies=proxies)
                # 检查响应状态码
                response.raise_for_status()

                # 将页面内容写入文件
                f.write(response.text)
                print(f"页面 {url} 的内容已成功追加到 douban.html 文件中。")
            except requests.exceptions.HTTPError as http_err:
                print(f"HTTP 错误发生在 {url}: {http_err}")
            except requests.exceptions.RequestException as req_err:
                print(f"请求错误发生在 {url}: {req_err}")
            except Exception as err:
                print(f"发生未知错误在 {url}: {err}")
except Exception as e:
    print(f"文件操作出现错误: {e}")