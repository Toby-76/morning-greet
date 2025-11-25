import requests
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
QWEATHER_API_KEY = os.getenv("QWEATHER_API_KEY")
SHANGHAI_LOCATION = "101020200"

# proxy, use clash, port is 7890
proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890',
}
# Different API endpoints
INDICES_URL = "https://devapi.qweather.com/v7/indices/1d"
WEATHER_URL = "https://devapi.qweather.com/v7/weather/3d"

# 调用建议API
def get_weather_advice():
      """Get weather indices for Shanghai"""
      params = {
          'location': SHANGHAI_LOCATION,
          'key': QWEATHER_API_KEY,
          'type': '1,3'
      }

      response = requests.get(INDICES_URL, params=params)
      return response.json()

# 调用天气API
def get_weather_forecast():
    ''' Get temperature data '''
    params = {
        'location': SHANGHAI_LOCATION,
        'key': QWEATHER_API_KEY
    }

    response = requests.get(WEATHER_URL, params=params)
    return response.json()

# 获取日期
def get_date_from_forecast(data):
    return data['daily'][0]['fxDate']

# 获取最高温度
def get_max_temp(data):
    return data['daily'][0]['tempMax']

# 获取最低温度
def get_min_temp(data):
    return data['daily'][0]['tempMin']

# 获取天气状况
def get_weather_condition(data):
    return data['daily'][0]['textDay']

# 获取运动建议
def get_sports_advice(data):
    return data['daily'][0]['text']

# 获取穿衣建议
def get_clothes_advice(data):
    return data['daily'][1]['text']

def get_dad_work_status():
    """Calculate if dad is working today"""
    start_date = datetime(2025, 1, 30)  # Start working date
    today = datetime.now()

    # Calculate days difference
    days_since_start = (today - start_date).days

    # Check work pattern (1 work, 2 rest)
    if days_since_start % 3 == 0:
        return "上班"
    else:
        return "休息"

def get_gold_price():
    """Get gold price in USD per ounce"""
    url = "https://query1.finance.yahoo.com/v8/finance/chart/GC=F"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    response = requests.get(url, proxies=proxies, headers=headers, timeout=10)
    data = response.json()

    # Extract the current price
    return data['chart']['result'][0]['meta']['regularMarketPrice']

def get_usd_to_cny():
    """Get USD to CNY exchange rate"""
    url = "https://query1.finance.yahoo.com/v8/finance/chart/USDCNY=X"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    response = requests.get(url, proxies=proxies, headers=headers, timeout=10)
    data = response.json()

    return data['chart']['result'][0]['meta']['regularMarketPrice']

def calculate_gold_price_per_gram():
    """Calculate gold price in RMB per gram"""
    gold_usd_per_ounce = get_gold_price()
    usd_to_cny = get_usd_to_cny()

    # Convert: USD/oz → CNY/oz → CNY/gram
    gold_cny_per_ounce = gold_usd_per_ounce * usd_to_cny
    # 1 盎司金条约等于 31.1035克。 这是因为黄金交易使用的是“金衡盎司”，它不同于日常使用的“常衡盎司”
    gold_cny_per_gram = gold_cny_per_ounce / 31.1035 

    # Round to 2 decimal places
    return round(gold_cny_per_gram, 2)

def create_morning_message():
    """Combine all data into final message"""
    # Get all the data
    weather_data = get_weather_forecast()
    advice_data = get_weather_advice()

    # Format everything
    message =  f"""Hi, Toby!
今天是{get_date_from_forecast(weather_data)}
最高温度：{get_max_temp(weather_data)}°C
最低温度：{get_min_temp(weather_data)}°C
天气：{get_weather_condition(weather_data)}
运动指数：{get_sports_advice(advice_data)}
穿衣指数：{get_clothes_advice(advice_data)}
老爸今天：{get_dad_work_status()}
今日金价：{calculate_gold_price_per_gram()}元/克
"""
    return message

def main():
    
    print(create_morning_message())
    
if __name__ == "__main__":
    main()