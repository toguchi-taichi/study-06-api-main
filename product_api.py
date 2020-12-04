import requests
import urllib
import os
import csv
import pandas as pd

PRODUCT_NAMES = []
SALES_MIN_PRICES = []
MAX_PRICES = []


def get_api(url, keyword, page_count):
    if page_count == 1:
        print(f'----検索ワード:{keyword}で楽天の商品価格サイトにリクエストを送信し、最安値と最高値を取得します----')
    print(f'{page_count}ページ目にリクエスト送信')
    result = requests.get(url)
    return result.json()

def extraction_item(get_api_data, page_count): # 商品名、最安値、最高値をdictで返す
    for product in get_api_data['Products']:
        for k, v in product.items():
            SALES_MIN_PRICES.append(v['salesMinPrice'])
            MAX_PRICES.append(v['maxPrice'])
            PRODUCT_NAMES.append(v['productName'])
    print(f'{page_count}ページ目の最安値と最高値の情報を抽出完了')


def create_csv(items, keyword):
    print('----これまでに取得したデータをcsvファイルに保存します----')
    df = pd.DataFrame(items)
    df.to_csv(f'{keyword}.csv', index=1, encoding='utf-8')
    print(f'----{keyword}.csvを"{os.getcwd()}"に保存しました----')


def main():
    
    # リクエスト先のページ数
    page_count = 1
    
    
    while True: 
        keyword = input('検索したい商品のキーワードを入力:')
        if keyword:
            keyword_quote = urllib.parse.quote(keyword, encoding='utf-8')
            break
        else:
            print('検索ワードを入力してください')
    
    
    
    while True:
        url = f'https://app.rakuten.co.jp/services/api/Product/Search/20170426?format=json&keyword={keyword_quote}&page={page_count}&applicationId=1048602787554194311'
        
        try:
            # apiにリクエストを送りデータを取得
            get_api_data = get_api(url, keyword, page_count)
    
    
            # 取得したデータの商品名と最大・最小価格のデータを抽出
            extraction_item(get_api_data, page_count)
    
        
            page_count += 1
            
        
        except:
            print(f'{page_count}ページ目は存在しません。')
            # csvファイルの作成
            items = {
                'product_name': PRODUCT_NAMES,
                'min_price': SALES_MIN_PRICES,
                'max_price': MAX_PRICES
            }
            
            create_csv(items, keyword)
            
            break
    


if __name__ == '__main__':
    main()
