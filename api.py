import requests
import urllib
import os
import csv
import pandas as pd



def get_api(url, keyword):
    print(f'----検索ワード{keyword}で楽天のECサイトにリクエストを行います----')
    result = requests.get(url)
    print('----リクエスト終了----')
    return result.json()

def extraction_item(get_api_data): # 商品名と価格のリストをdictで返す
    item_names = []
    item_prices = []
    for data in get_api_data['Items']:
        item_names.append(data['Item']['itemName'])
        item_prices.append(data['Item']['itemPrice'])
    return {
        'ItemName': item_names,
        'ItemPrice': item_prices
    }

def create_csv(items, keyword):
    print('----リクエストの結果をcsvファイルとして保存します----')
    df = pd.DataFrame(items)
    df.to_csv(f'{keyword}.csv', encoding='utf-8')
    print(f'----{keyword}.csvを"{os.getcwd()}"に保存しました----')


def main():
    while True: 
        keyword = input('検索したい商品のキーワードを入力:')
        if keyword:
            keyword_quote = urllib.parse.quote(keyword, encoding='utf-8')
            url = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706?format=json&keyword=     {}&applicationId=1019079537947262807".format(
        keyword_quote)
            break
        else:
            print('検索ワードを入力してください')
    
    # apiにリクエストを送りデータを取得
    get_api_data = get_api(url, keyword)
    
    
    # 取得したデータの商品名と価格のデータを抽出
    items = extraction_item(get_api_data)
    
    
    create_csv(items, keyword)
    


if __name__ == '__main__':
    main()
