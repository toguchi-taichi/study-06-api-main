import requests
import urllib
import os
import csv
import pandas as pd

ITEM_RANKS = []
ITEM_NAMES = []
ITEM_URLS = []

def get_api(url, keyword):
    print(f'----ジャンルID:{keyword}で楽天商品ランキングサイトにリクエストを行います----')
    result = requests.get(url)
    print('----リクエスト終了----')
    return result.json()

def extraction_item(get_api_data): # 商品名と価格のリストをdictで返す
    for data in get_api_data['Items']:
        for k, v in data.items():
            ITEM_RANKS.append(v['rank'])
            ITEM_NAMES.append(v['itemName'])
            ITEM_URLS.append(v['mediumImageUrls'][0]['imageUrl'])
    return {
        'item_rank': ITEM_RANKS,
        'item_name': ITEM_NAMES,
        'item_url': ITEM_URLS
    }

def create_csv(items, keyword):
    print('----リクエストの結果をcsvファイルとして保存します----')
    df = pd.DataFrame(items)
    df.to_csv(f'ジャンル{keyword}.csv', encoding='utf-8')
    print(f'----ジャンル{keyword}.csvを"{os.getcwd()}"に保存しました----')


def main():
    # 邦画のランキング
    keyword = 101370
        
    url = f'https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20170628?format=json&genreId={keyword}&applicationId=1048602787554194311'
        
    
    # apiにリクエストを送りデータを取得
    get_api_data = get_api(url, keyword)
    
    
    # 取得したデータの商品名と価格のデータを抽出
    items = extraction_item(get_api_data)
    
    
    create_csv(items, keyword)
    


if __name__ == '__main__':
    main()
