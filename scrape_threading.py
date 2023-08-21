from concurrent.futures import ThreadPoolExecutor
import json
import requests
from serpapi import GoogleSearch
import pandas as pd
import datetime
BRAND_MPN=[['ELGA', 'LC140'],
 ['Eaton', 'GI3060'],
 ['Gast', 'PCA-10'],
 ['Eaton', 'EMS03D5EBD'],
 ['Hubbell', 'HBL20406'],
 ['Eaton', 'FAZ-C32-2-NA'],
 ['SMC', 'AM550C-N10B'],
 ['Hoffman', 'G280446G050'],
 ['RACO', '3704-2']]
def mpn_prices(brand_mpn):
    brd,mpn=brand_mpn.split(" ")
    result_df=[]
    not_wrk=0
    params = {
        "engine": "google",
        "q": f"{brd} {mpn}",
        "location": "Austin, Texas, United States",
        "google_domain": "google.com",
        "gl": "us",
        "hl": "en",
        "tbm": "shop",
        "api_key": "46adaed43a33d40b8fbdbae42231e10571c468acaa72b16331b3b67e66ad1800"
        }
    search = GoogleSearch(params)
    results = search.get_dict()
    try:
        if len(results["inline_shopping_results"])!=0:
            for shop_res in results["inline_shopping_results"]:
                try:
                    r=requests.get(shop_res["link"])
                    redirect_url=r.url
                except:
                    redirect_url=shop_res["link"]
                res={"mpn":mpn,"brand":brd,"price":shop_res["price"],"Product_url":redirect_url,"source":shop_res["source"],"title":shop_res["title"]}
                result_df.append(res)
        if len(results["shopping_results"])!=0:
            for shop_res in results["shopping_results"]:
                res={"mpn":mpn,"brand":brd,"price":shop_res["price"],"Product_url":shop_res["link"],"source":shop_res["source"],"title":shop_res["title"]}
                result_df.append(res)
    except:
        not_wrk+=1
        pass
    if len(result_df)>20:
        result_df=result_df[:20]
    return result_df

pool = ThreadPoolExecutor(max_workers=8)
results = list(pool.map(mpn_prices, BRAND_MPN))
current_time = datetime.datetime.now()

result_list = [element for innerList in results for element in innerList]
current_time=current_time.strftime("%d%M%S")
df = pd.DataFrame.from_dict(result_list)
df.to_csv(f"MPN_Price_{current_time}.csv",index=False)
pool.shutdown()