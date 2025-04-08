import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup
import re


# Stores that use different API endpoints
metro_stores = [
    {"merchantName": "metro", "banner": "62e3ee07ffe0e6f10778a56e",
     "subscription_key": "0a112db32b2f42588b54063b05dfbc90","merchantId": "1002","all_stores_id":[
    702,401,402,680,420,405,581,775,656,387,552,726,661,673,643,665,362,361,343,627,611,624,658,623,369,624,371,374,377,375,381,390,373,372,376,378,386,560,551,636,537,538,382,443,
    ]},
    {"merchantName": "adonis", "banner": "63fe18ec3e7cd81e86393c61",
    "subscription_key": "0a112db32b2f42588b54063b05dfbc90","merchantId": "1001","all_stores_id" :[
    21937,21943,21950,21947,10120,21947,21945,21938,21944,10120,21940,21941,101201,21948
    ]},
    {"merchantName": "superc", "banner": "6141fa7157f8c212fc19dddc",
     "subscription_key": "021027e7c41548bcba5d2315a155816b","merchantId": "1006","all_stores_id":[815,885,445,706,464,728]},
    {"merchantName": "foodbasics", "banner": "62015981ed29a2a604a206b4",
     "subscription_key": "0defd42b9de9412488327864774fbfca","merchantId":"1014","all_stores_id":[
    929,927,976,897,902,912,833,837,855,921,620,657 
    ]},
    {"merchantName": "brunet", "url": "https://www.brunet.ca/StoreLocator/StoreLocator.svc/LoadStoreInfosBH", "banner": "65ce6bcdef603354c0166764", "subscription_key": "0a112db32b2f42588b54063b05dfbc90","merchantId":"1020","all_stores_id":[]},
    {"merchantName": "jeancoutu", "url": "https://www.jeancoutu.com/StoreLocator/StoreLocator.svc/LoadStoreInfosBH", "banner": "659ed62d2212030336aff389", "subscription_key": "0a112db32b2f42588b54063b05dfbc90","merchantId":"1021","all_stores_id":[]},
]

loblaws_stores = [
    {"name": "provigo", "merchantName": "provigo", "access_token": "31c52dc6a419dc10959261a5a210fccf","merchantId":"1004"},
    {"name": "maxi", "merchantName": "maxi", "access_token": "75a33b973cc2e856dd0f2cd629d80a19","merchantId":"1005"},
    {"name": "loblaw", "merchantName": "loblaws", "access_token": "fd66ddd31b95e07b9ad2744424e9fd32","merchantId": "1009"},
    {"name": "fortinos", "merchantName": "fortinos", "access_token": "ff3274ff57f481a8fcfac9c6c968fe67","merchantId":"1010"},
    {"name": "zehrs", "merchantName": "zehrs", "access_token": "fef2a837ffeee9e5e5d02f31db81f209","merchantId":"1011"},
    {"name": "superstore", "merchantName": "realcanadiansuperstore", "access_token": "a6e07e290f469d032d54a252f7582de2","merchantId":"1012"},
    {"name": "nofrills", "merchantName": "nofrills", "access_token": "1063f92aaf17b3dfa830cd70a685a52b","merchantId":"1013"},
    ####{"name": "shoppersdrugmart", "merchantName": "shoppersdrugmart", "access_token": "1f12a442b4517171cd23ff13a2a18519","merchantId":"1015"},
    {"name": "valumart", "merchantName": "valumart", "access_token": "52a882a9661c216dead4255a669f3000","merchantId":"1016"},
    {"name": "dominion", "merchantName": "dominion", "access_token": "23d83ed8a192329f29749c3b86c707fc","merchantId":"1017"},
    {"name": "rass", "merchantName": "atlanticsuperstore", "access_token": "4d9c0561f7abbf53ad6eca20dad201c7","merchantId":"1018"},
    {"name": "independent", "merchantName": "yourindependentgrocer", "access_token": "fa31161a375478b68b2ec0f8f8edd65a","merchantId":"1019"},
]

stores = [
    {"merchantName": "marcheami", "url": "https://www.marcheami.ca/map-stores", "access_token": "7c9a2c8409a452ec8e9e54806370af8e","merchantId": "1022"},
    {
        "merchantName": "gianttiger",
        "merchantId": "1008",
        "access_token": "b8657ead90fc4ff25f66a8859d8d1d59",
        "url": "https://stores.gianttiger.com/api/getAutocompleteData"
    },
    {
        "merchantName": "saveonfoods",
        "merchantId": "1034",
        "access_token": "d0fb03dbaa873bf1a2e0f07cdd241951",
    },
    {
        "merchantName": "coopfood",
        "merchantId": "1035",
        "access_token": "1612256f56f9424cfd6ec29265ce14f6",
    },
    {
        "merchantName": "walmartcanada",
        "merchantId": "1007",
        "access_token": "92bcff5f7d07c3aaa4b33e2c048d7728",
    },
]

sobeys = [
    {"merchantName": "igaquebec","url": "www.iga.ca","access_token": "692be3f8ba9e9247dc13d064cb89e7f9","merchantId": "1003"},
    {"merchantName": "foodland","url": "www.foodland.ca","access_token": "07ca28af93a0585f05575bf41ce92a6d","merchantId": "1023"},
    {"merchantName": "lawtonsdrugs","url": "www.lawtons.ca","access_token": "539e1573c2e3a44ef843192293a3ea00","merchantId": "1024"},
    {"merchantName": "marchebonichoix","url": "www.bonichoix.com","access_token": "b977a402ba8d56a9d0236cdbc90f1cae","merchantId": "1025"},
    {"merchantName": "Freshco","url": "freshco.com","access_token": "881f0b9feea3693a704952a69b2a037a","merchantId": "1026"},
    {"merchantName": "safewaycanada","url": "www.safeway.ca","access_token": "41073822c1e3a003da36de785443fa0f","merchantId": "1027"},
    {"merchantName": "lesmarchstradition","url": "www.marchestradition.com","access_token": "efd43fd035f30655cb45ffa12872f2b3","merchantId": "1028"}
]

date = datetime.now().strftime("%d%m%Y")
all_store_data = []

def fetch_json(url, headers=None, method='GET', params=None):
    try:
        response = requests.request(method, url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[ERROR] Failed request to {url} — {e}")
        return None

def is_duplicate(store_data, store_id, flyer_id):
    return any(d["storeId"] == store_id and d["flyer_id"] == flyer_id for d in store_data)

def get_latest_flyer(flyers, date_key="valid_from", title_key="external_display_name"):
    weekly_keywords = ["Weekly Flyer", "Weekly eFlyer", "Weekly","Flyer"]

    # Filter matching flyers
    matching_flyers = [
        flyer for flyer in flyers
        if any(kw in flyer.get(title_key, "") for kw in weekly_keywords)
    ]

    if not matching_flyers:
        return []

    try:
        # Find latest valid_from date
        latest_date = max(datetime.fromisoformat(flyer[date_key]) for flyer in matching_flyers)
    except Exception as e:
        print(f"[WARN] Invalid flyer date format: {e}")
        return []

    # Return all flyers with that latest valid_from date
    return [
        {
            "flyer_id": flyer["id"],
            "valid_from": flyer.get("valid_from"),
            "valid_to": flyer.get("valid_to"),
        }
        for flyer in matching_flyers
        if datetime.fromisoformat(flyer[date_key]) == latest_date
    ]

def append_flyer_data(merchant_name, merchant_id, store_data):
    all_store_data.append({
        "merchantId": merchant_id,
        "merchantName": merchant_name,
        "data": store_data
    })
    print(f"✔ Appended data for {merchant_name}")

def process_metro_stores(metro_stores):
    for store in metro_stores:
        merchant_name = store["merchantName"]
        merchant_id = store["merchantId"]
        banner = store["banner"]
        subscription_key = store["subscription_key"]
        all_stores_id = store["all_stores_id"]
        store_data = []
        all_postals = []

        if merchant_name in ['brunet','jeancoutu']:
            url = store["url"]
            headers = {"accept": "application/json, text/javascript, */*; q=0.01"}
            req_type = {"marcheami": requests.get, "gianttiger": requests.get}.get(merchant_name, requests.post)

            response = req_type(url, headers=headers)
            if response.status_code != 200:
                continue
            
            data = response.json()
            for store_info in data["LoadStoreInfosBHResult"]:
                all_stores_id.append(store_info["Store"])
                all_postals.append({"postal_code": store_info["Zip_Code"].replace(" ", ""),"storeId": store_info["Store"]})

        for store_id in all_stores_id:
            flyer_url = (
                f"https://metrodigital-apim.azure-api.net/api/flyers/{store_id}/en?"
                f"date={datetime.now().strftime('%Y-%m-%d')}"
            )

            headers = {
                "accept": "application/json",
                "banner": banner,
                "ocp-apim-subscription-key": subscription_key,
                "user-agent": "Mozilla/5.0"
            }

            flyers_data = fetch_json(flyer_url, headers=headers)
            if not flyers_data:
                # print("err")
                continue

            latest_flyer = get_latest_flyer(flyers_data.get("flyers", []))
            if not latest_flyer:
                continue

            flyer_id = latest_flyer["title"]

            print(flyer_id)
            postal_code = next((data["postal_code"] for data in all_postals if data["storeId"] == store_id), "")
            if flyer_id and not is_duplicate(store_data, store_id, flyer_id):
                store_data.append({
                    "storeId": store_id,
                    "postalCode": postal_code,
                    "flyer_id": flyer_id,
                    "valid_from": latest_flyer.get("valid_from"),
                    "valid_to": latest_flyer.get("valid_to")
                })
            else:
                print(f"[SKIP] Duplicate or missing flyer for store {store_id}")

        append_flyer_data(merchant_name, merchant_id, store_data)

def process_loblaws_stores(loblaws_stores):
    base_headers = {
        "accept": "application/json, text/plain, */*",
        "x-apikey": "C1xujSegT5j3ap3yexJjqhOfELwGKYvz"
    }

    for store in loblaws_stores:
        merchant_name = store["merchantName"]
        name = store["name"]
        merchant_id = store["merchantId"]
        access_token = store["access_token"]
        store_data = []

        loc_url = f"https://api.pcexpress.ca/pcx-bff/api/v1/pickup-locations?bannerIds={name}"
        locations = fetch_json(loc_url, headers=base_headers)
        if not locations:
            continue

        for loc in locations:
            # print(loc)
            store_id = loc["storeId"]
            loc_store_id = str(int(loc["storeId"]))
            postal_code = loc["address"]["postalCode"].replace(" ", "")

            flyer_url = (
                f"https://dam.flippenterprise.net/flyerkit/publications/{merchant_name}"
                f"?locale=en&access_token={access_token}&show_storefronts=true"
                f"&postal_code={postal_code}&store_code={loc_store_id}"
            )

            flyers = fetch_json(flyer_url)
            if not flyers:
                continue

            weekly_flyers = [f for f in flyers if "Weekly Flyer" in f.get("name", "")]
            if not weekly_flyers:
                continue

            latest = max(weekly_flyers, key=lambda f: datetime.fromisoformat(f["valid_from"]))
            flyer_id = latest.get("id")
            print(flyer_id)

            if flyer_id and not is_duplicate(store_data, store_id, flyer_id):
                store_data.append({
                    "storeId": store_id,
                    "postalCode": postal_code,
                    "flyer_id": flyer_id,
                    "valid_from": latest.get("valid_from"),
                    "valid_to": latest.get("valid_to")
                })
            else:
                print(f"[SKIP] Duplicate or missing flyer for store {store_id}")

        append_flyer_data(merchant_name, merchant_id, store_data)

def process_stores(stores):

    for store in stores:
        merchant_name = store["merchantName"]
        merchant_id = store["merchantId"]
        access_token = store["access_token"]
        store_data = []

        if "url" not in store:
            continue

        url = store["url"]
        headers = {"accept": "application/json, text/javascript, */*; q=0.01"}
        req_type = {"marcheami": requests.get, "gianttiger": requests.get}.get(merchant_name, requests.post)

        response = req_type(url, headers=headers)
        if response.status_code != 200:
            continue

        data = response.json()

        flyer_headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "sec-fetch-site": "cross-site"
        }

        if merchant_name == "marcheami":
            postal_codes = [entry[2].split("//")[-1].replace(" ", "") for entry in data]
        elif merchant_name == "gianttiger":
            postal_codes = [p.replace(" ", "") for p in data.get("data", []) if len(p.strip()) <= 7]
        else:
            postal_codes = ['L5B2C9','L5V2N6','L5M4Z5','L5L5Z5','L5N8E1','L6W0A6','L4X1L4','L6X0Z8','M9C1A7','L6V4K2','L6H6M4','L6T5P9','L9T6R1','M9W3W6','L7G4B1','M6N4Z5','L6R3S9','M6L1A5','M6H4A9','M3J1N4','L7M5B4','L4K0L4','L7E2Y3','L4H3T6','L4J0A7','L7R0B4','L6A4R9','L4B4V5','M1L2L9','L9H0C2','L4S1P3','M1P4P5','L8H2V2','M1J2H1','L8E0G2','M1V5P7','L3R4M9','L9C2Z5','N1G5L4','M1B3C3','N1H1G8','L9W2E8','L6B0S1','L0R1P0','L4G0G2','L4A0K2','L9G3K9','L3Y8S4','N1R8K5','T4T1A1','T0M1V0','T0M0X0','T0C2J0','R0E1J0','R0G2B0','R0G0A2','R0G0B0','R0G0J0','R0E1J0','R0G2B0','R0G0B0','R0G0A2','R0G0J0','R0E1J0','R0G2B0','R0G0A2','R0G0B0','R0G0J0','R0E1J0','R0G2B0','R0G0A2','R0G0B0','R0G0J0'
            ]

        if not postal_codes:
            continue

        readed = []

        for postal_code in postal_codes:

            near_flyer_url = (
                f"https://dam.flippenterprise.net/flyerkit/stores/{merchant_name}"
                f"?locale=en&access_token={access_token}&postal_code={postal_code}"
            )

            near_flyers = fetch_json(near_flyer_url, headers=flyer_headers)
            
            if not near_flyers:
                # print(f"No flyers for postal code: {postal_code}")
                continue

            for near_store in near_flyers:
                store_id = near_store["merchant_store_code"]
                postal_code = near_store["postal_code"]

                if any(obj["storeId"] == store_id and obj["postalCode"] == postal_code for obj in readed):
                    continue
                readed.append({"storeId": store_id, "postalCode": postal_code})

                flyer_url = (
                    f"https://dam.flippenterprise.net/flyerkit/publications/{merchant_name}"
                    f"?locale=en&access_token={access_token}&show_storefronts=true"
                    f"&postal_code={postal_code}&store_code={store_id}"
                )

                flyers = fetch_json(flyer_url, headers=flyer_headers)

                if not flyers:
                    continue

                latest_flyer = min(flyers, key=lambda f: datetime.fromisoformat(f["valid_from"]))
                flyer_id = latest_flyer.get("id")
                print(flyer_id)

                if flyer_id and not is_duplicate(store_data, store_id, flyer_id):
                    store_data.append({
                        "storeId": store_id,
                        "postalCode": postal_code,
                        "flyer_id": flyer_id,
                        "valid_from": latest_flyer.get("valid_from"),
                        "valid_to": latest_flyer.get("valid_to")
                    })
                    print(f"🟢 Store {store_id} | Flyer {flyer_id}")
                else:
                    print(f"⚠️ Skipped duplicate or no flyer for store {store_id}")

        append_flyer_data(merchant_name, merchant_id, store_data)

def process_sobeys_stores(sobeys):
    for store in sobeys:
        merchant_name = store["merchantName"]
        merchant_id = store["merchantId"]
        store_data = []
        base_url = store["url"]
        access_token = store["access_token"]
        store_data = []

        s_url = f"https://{base_url}/wp-content/stores/stores.json"
        s_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
        }
        response = requests.get(s_url, headers=s_headers)

        if response.status_code != 200:
            print(f"Failed to fetch store list for {merchant_name}")
            continue

        stores_data = response.json()

        for obj in stores_data:
            store_json_id = obj["ID"]
            store_url = f"https://{base_url}/wp-json/sobeys-rest-api/store_id/{store_json_id}"

            st_res = requests.get(store_url, headers=s_headers)
            if st_res.status_code != 200:
                print(f"Failed to fetch store info for ID {store_json_id}")
                continue

            try:
                store_details = st_res.json()["store_details"]
                postal_code = store_details["postal_code"].replace(" ", "")
            except (KeyError, TypeError):
                print(f"Missing or invalid data for store ID {store_json_id}")
                continue

            near_flyer_url = (
                f"https://dam.flippenterprise.net/flyerkit/stores/{merchant_name}"
                f"?locale=en&access_token={access_token}&postal_code={postal_code}"
            )
            flyer_headers = {
                "accept": "*/*",
                "accept-language": "en-US,en;q=0.9",
                "sec-fetch-site": "cross-site"
            }

            near_flyer_response = fetch_json(near_flyer_url, headers=flyer_headers)

            for near_store in near_flyer_response:
                store_id = near_store["merchant_store_code"]
                postal_code = near_store["postal_code"]  # 

                flyer_url = (
                    f"https://dam.flippenterprise.net/flyerkit/publications/{merchant_name}"
                    f"?locale=en&access_token={access_token}&show_storefronts=true"
                    f"&postal_code={postal_code}&store_code={store_id}"
                )

                flyers = fetch_json(flyer_url, headers=flyer_headers)

                flyer_objs = get_latest_flyer(flyers, date_key="valid_from", title_key="name")

                if not flyer_objs:
                    flyer_objs = get_latest_flyer(flyers, date_key="valid_from", title_key="external_display_name")

                if not flyer_objs:
                    continue

                # print(flyer_objs)

                for flyer in flyer_objs:
                    flyer_id = flyer["flyer_id"]
                    valid_from = flyer["valid_from"]
                    valid_to = flyer["valid_to"]
                    print(flyer_id)

                    if flyer_id and not is_duplicate(store_data, store_id, flyer_id):
                        store_data.append({
                            "storeId": store_id,
                            "postalCode": postal_code,
                            "flyer_id": flyer_id,
                            "valid_from": valid_from,
                            "valid_to": valid_to
                        })
                    else:
                        print(f"[SKIP] Duplicate or missing flyer for store {store_id}")


        append_flyer_data(merchant_name, merchant_id, store_data)

def process_longos():
    merchant_name = "longos"
    merchant_id = "1031"
    access_token = "5b4ad9bb0148449f25dbb0b76b976c1b"
    store_data = []

    store_url = "https://api.longos.com/ggcommercewebservices/v2/groceryGatewaySpa/stores"
    store_params = {
        "fields": "stores(displayName,name,address(FULL),openingHours(FULL),geoPoint(FULL),holidayHours(FULL),merchantStoreCode,pickupButtonStoreFinderState,showNewBadgeAtStore)",
        "lang": "en",
        "curr": "CAD",
        "defaultStoreName": "Longos Leaside Pickup"
    }
    store_headers = {
        "accept": "application/json, text/plain, */*",
        "user-agent": "Mozilla/5.0"
    }

    data = fetch_json(store_url, headers=store_headers, params=store_params)
    if not data:
        print("❌ Failed to fetch Longos store data")
        return

    for store in data.get('stores', []):
        store_id = store.get('merchantStoreCode')
        postal_code = store.get('address', {}).get('postalCode')
        if not store_id or not postal_code:
            continue

        flyer_url = "https://dam.flippenterprise.net/flyerkit/publications/longos"
        flyer_params = {
            "locale": "en",
            "access_token": access_token,
            "show_storefronts": "true",
            "postal_code": postal_code,
            "store_code": store_id
        }
        flyer_headers = {
            "accept": "*/*",
            "referer": "https://www.longos.com/"
        }

        flyers = fetch_json(flyer_url, headers=flyer_headers, params=flyer_params)
        if not flyers:
            continue

        latest_flyer = get_latest_flyer(flyers)
        flyer_id = latest_flyer.get("id") if latest_flyer else None

        if flyer_id and not is_duplicate(store_data, store_id, flyer_id):
            store_data.append({
                "storeId": store_id,
                "postalCode": postal_code,
                "flyer_id": flyer_id,
                "valid_from": latest_flyer.get("valid_from"),
                "valid_to": latest_flyer.get("valid_to")
            })
            print(f"🟢 Store {store_id} | Flyer {flyer_id}")
        else:
            print(f"⚠️ Skipping duplicate or no flyer for store {store_id}")

    append_flyer_data(merchant_name, merchant_id, store_data)

def process_farmboy():
    merchant_name = "farmboy"
    merchant_id = "1032"
    access_token = "633f9e9fe2eae3e7b4a811dd9690ac4b"

    store_data = []

    store_url = "https://www.farmboy.ca/accessible-store-listing/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Connection": "keep-alive"
    }

    try:
        response = requests.get(store_url, headers=headers)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Failed to fetch Farm Boy store page: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    wrapper = soup.find('div', class_='fb_store_location_wrapper')
    if not wrapper:
        print("❌ Store wrapper not found")
        return
    
    

    for store in wrapper.find_all('div', recursive=False):
        address_div = store.find_all('div')[0]
        address = address_div.get_text(strip=True).replace("Address:", "").strip()
        postal_code = address.split(",")[-1].strip().replace(" ", "")
        store_id = address.split(',')[1].strip().split(" ")[0] if address.startswith("Unit") else address.split(" ")[0]


        nearby_url = f"https://dam.flippenterprise.net/flyerkit/stores/{merchant_name}"
        params = {
            "locale": "en",
            "access_token": access_token,
            "postal_code": postal_code
        }
        flyer_headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "sec-fetch-site": "cross-site"
        }

        nearby_stores = fetch_json(nearby_url,headers=flyer_headers, params=params)
        if not nearby_stores:
            print(f"⚠️ No nearby flyer data for {postal_code}")
            continue

        for near in nearby_stores:
            pcode = near["postal_code"]
            sid = near["merchant_store_code"]
            # print(sid)

            flyer_url = f"https://dam.flippenterprise.net/flyerkit/publications/{merchant_name}"
            flyer_params = {
                "locale": "en",
                "access_token": access_token,
                "show_storefronts": "true",
                "postal_code": pcode,
                "store_code": sid
            }

            flyers = fetch_json(flyer_url,headers=flyer_headers, params=flyer_params)
            if not flyers:
                print(f"No flyers for {pcode}")
                continue
            # print(flyers)

            latest_flyers = get_latest_flyer(flyers, date_key="valid_from", title_key="name")
            if not latest_flyers:
                latest_flyers = get_latest_flyer(flyers, date_key="valid_from", title_key="external_display_name")
                continue

            if not latest_flyers:
                continue
            # print(latest_flyer)
            flyer_list = latest_flyers if isinstance(latest_flyers, list) else [latest_flyers]

            for flyer in flyer_list:
                flyer_id = flyer.get('flyer_id')
                print(flyer_id)

                if flyer_id and not is_duplicate(store_data, sid, flyer_id):
                    store_data.append({
                        "storeId": sid,
                        "postalCode": pcode,
                        "flyer_id": flyer_id,
                        "valid_from": flyer.get("valid_from"),
                        "valid_to": flyer.get("valid_to")
                    })
                    print(f"🟢 Store {sid} | Flyer {flyer_id}")
                else:
                    print(f"⚠️ Skipped duplicate or no flyer for store {sid}")

    append_flyer_data(merchant_name, merchant_id, store_data)

def process_giant_tiger():
    merchant_name = "gianttiger"
    merchant_id = "1008"
    access_token = "b8657ead90fc4ff25f66a8859d8d1d59"
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "sec-ch-ua": "\"Chromium\";v=\"134\", \"Not:A-Brand\";v=\"24\", \"Google Chrome\";v=\"134\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-requested-with": "XMLHttpRequest"
    }

    postal_url = "https://stores.gianttiger.com/api/getAutocompleteData"
    postal_data = fetch_json(postal_url, headers=headers)
    postal_codes = postal_data.get("data", []) if postal_data else []

    store_data = []
    seen = []

    for postal_code in postal_codes:
        if len(postal_code) > 7:
            continue

        clean_postal = postal_code.replace(" ", "")
        nearby_url = f"https://dam.flippenterprise.net/flyerkit/stores/{merchant_name}"
        params = {
            "locale": "en",
            "access_token": access_token,
            "postal_code": clean_postal
        }

        stores = fetch_json(nearby_url, headers=headers, params=params)
        if not stores:
            continue

        for store in stores:
            store_id = store["merchant_store_code"]
            pcode = store["postal_code"]

            if any(obj["storeId"] == store_id and obj["postalCode"] == pcode for obj in seen):
                continue
            seen.append({"storeId": store_id, "postalCode": pcode})

            flyer_url = f"https://dam.flippenterprise.net/flyerkit/publications/{merchant_name}"
            flyer_params = {
                "locale": "en",
                "access_token": access_token,
                "show_storefronts": "true",
                "postal_code": pcode,
                "store_code": store_id
            }

            flyers = fetch_json(flyer_url, headers=headers, params=flyer_params)
            if not flyers:
                continue

            latest_flyer = get_latest_flyer(flyers)
            flyer_id = latest_flyer.get("id") if latest_flyer else None

            if flyer_id and not is_duplicate(store_data, store_id, flyer_id):
                store_data.append({
                    "storeId": store_id,
                    "postalCode": pcode,
                    "flyer_id": flyer_id,
                    "valid_from": latest_flyer.get("valid_from"),
                    "valid_to": latest_flyer.get("valid_to")
                })
                print(f"🟢 Store {store_id} | Flyer {flyer_id}")
            else:
                print(f"⚠️ Skipped duplicate or no flyer for store {store_id}")

    append_flyer_data(merchant_name, merchant_id, store_data)

# Then call:
process_metro_stores(metro_stores)
process_loblaws_stores(loblaws_stores)
process_sobeys_stores(sobeys)
process_stores(stores)
# process_longos()
process_farmboy()


seen = set()
deduplicated_store_data = []

for entry in all_store_data:
    merchantName = entry["merchantName"]
    merchantId = entry["merchantId"]
    unique_data = []

    for store in entry["data"]:
        key = (merchantName, store["storeId"])
        if key not in seen:
            seen.add(key)
            unique_data.append(store)
    
    deduplicated_store_data.append({
        "merchantId": merchantId,
        "merchantName": merchantName,
        "data": unique_data
    })

# Save all data to JSON file
output_file = f"flyer_id.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(deduplicated_store_data, f, indent=4, ensure_ascii=False)

print(f"All responses saved to {output_file}")





        # flyer_url = f"https://{url}/wp-json/sobeys-rest-api/flyer/store_id/{storeId}"

        # flyer_headers = {
        #     "accept": "application/json",
        #     "referer": f"https://{url}/flyer/",
        #     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        #     "sec-fetch-site": "same-origin",
        #     "sec-fetch-mode": "cors",
        #     "sec-fetch-dest": "empty",
        # }


        # flyer_response = requests.get(flyer_url, headers=flyer_headers)

        # if flyer_response.status_code != 200:
        #     print("error :",flyer_response.status_code)
        #     continue

        # flyers = flyer_response.json()
        # print("Flyers fetched successfully!",flyers)

        # flyerId = ""
        # if flyers:
        #     # Get latest flyer
        #     latest_flyer = min(flyers,
        #                         key=lambda flyer: datetime.fromisoformat(flyer["valid_from"])
        #                     )

        #     flyerId = latest_flyer.get("id")
        #     valid_to = latest_flyer.get("valid_to")
        #     valid_from = latest_flyer.get("valid_from")
        #     postal_code = latest_flyer.get("postal_code").replace(" ","")
            # print(f"Flyer ID: {flyerId}")
        




# flyerId = ""
#         if isinstance(flyers, list):
#             weekly_flyers = [flyer for flyer in flyers if "Weekly" in flyer.get("name") or "Weekly" in flyer.get("") ]
#             if weekly_flyers:
#                 latest_flyer = max(weekly_flyers, key=lambda flyer: datetime.fromisoformat(flyer["valid_from"]))
#                 flyer_id = latest_flyer.get("id")
#                 valid_to = latest_flyer.get("valid_to")
#                 valid_from = latest_flyer.get("valid_from")
#                 postal_code = latest_flyer.get("postal_code").replace(" ","")
#                 print(f"Flyer ID: {flyerId}")
# external_display_name
# fetch("https://www.superc.ca/en/find-shopping-store", {
#   "headers": {
#     "accept": "*/*",
#     "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
#     "sec-ch-ua": "\"Chromium\";v=\"134\", \"Not:A-Brand\";v=\"24\", \"Google Chrome\";v=\"134\"",
#     "sec-ch-ua-mobile": "?0",
#     "sec-ch-ua-platform": "\"Windows\"",
#     "x-requested-with": "XMLHttpRequest"
#   },
#   "referrer": "https://www.superc.ca/en/flyer",
#   "referrerPolicy": "strict-origin-when-cross-origin",
#   "body": "postalCode=&city=Gatineau",
#   "method": "POST",
#   "mode": "cors",
#   "credentials": "omit"
# });









