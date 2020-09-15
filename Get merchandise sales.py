import re
import requests
import json


def openurl(keyword, page):
    params = {'q': keyword, 'sort': 'sale-desc', 's': str(page * 44)}
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'}
    url = "https://s.taobao.com/search"
    res = requests.get(url, params=params, headers=headers)
    return res

def get_items(res):
    g_page = re.search(r'g_page_config = (.*?);\n', res.text)
    g_page_json = json.loads(g_page.group(1))
    p_items = g_page_json['mods']['itemlist']['data']['auctions']
    result = []
    for each in p_items:
        dict_items = dict.fromkeys(('title', 'raw_title', 'view_price', 'view_sales', 'comment_count', 'user_id'))
        dict_items['title'] = each['title']
        dict_items['raw_title'] = each['raw_title']
        dict_items['view_price'] = each['view_price']
        dict_items['view_sales'] = each['view_sales']
        dict_items['comment_count'] = each['comment_count']
        dict_items['user_id'] = each['user_id']
        result.append(dict_items)

    return result


def sale_num(items):
    count = 0
    for each in items:
        if '关键字' in each['raw_title']:  # 关键字处填写书的作者，或者某种商品特有的关键字
            print(each['raw_title'])
            count += int(re.search(r'\d+', each['view_sales']).group())
    return count


def main():
    keyword = input("请输入需要搜索销量的商品：")
    print(type(keyword))
    page_num = 3
    total_sale_num = 0
    for page in range(page_num):
        res = openurl(keyword, page)
        item = get_items(res)
        total_sale_num += sale_num(item)
    print('总销量为:', total_sale_num)


if __name__ == "__main__":
    main()