from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)


@app.route('/')
def index():
    url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EA%B3%A0%EC%96%91%EB%8F%99+%EB" \
          "%82%A0%EC%94%A8&oquery=%EB%82%A0%EC%94%A8&tqi=UJOCsdp0J14ssK%2BjZL0ssssstcN-517573 "
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    # 현재 00℃ (최저 00℃ / 최고 00℃)
    now_temp = soup.find("span", attrs={"class": "todaytemp"}).get_text()
    now_temp = int(now_temp)  # 현재 온도 int형으로 변경
    min_temp = soup.find("span", attrs={"class": "min"}).get_text()
    max_temp = soup.find("span", attrs={"class": "max"}).get_text()
    # 맑음, 어제보다 00˚ 낮아요
    compare = soup.find("p", attrs={"class": "cast_txt"}).get_text()
    # 체감 온도 00˚
    wind_chill = soup.find("span", attrs={"class": "sensible"}).get_text()
    mornig_rain_r = soup.find("span", attrs={"class": "point_time morning"}).get_text().strip()
    afternoon_rain_r = soup.find("span", attrs={"class": "point_time afternoon"}).get_text().strip()

    if 28 <= now_temp:
        image=1
    elif 23 <= now_temp <= 27:
        image=2
    elif 20 <= now_temp <= 22:
        image=3
    elif 17 <= now_temp <= 19:
        image=4
    elif 12 <= now_temp <= 16:
        image=5
    elif 9 <= now_temp <= 11:
        image=6
    elif 5 <= now_temp <= 8:
        image=7
    else:
        image=8


    return render_template('index.html', now_temp=now_temp, min_temp=min_temp, max_temp=max_temp, compare=compare,
                           wind_chill=wind_chill, mornig_rain_r=mornig_rain_r, afternoon_rain_r=afternoon_rain_r, image_file="image/{}.jpg".format(image) )


@app.route('/search', methods=['GET'])
def search():
    where = request.args.get('region')
    url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query={}+날씨".format(where)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    now_temp = soup.find("span", attrs={"class": "todaytemp"}).get_text()
    now_temp = int(now_temp)  # 현재 온도 int형으로 변경
    min_temp = soup.find("span", attrs={"class": "min"}).get_text()
    max_temp = soup.find("span", attrs={"class": "max"}).get_text()
    # 맑음, 어제보다 00˚ 낮아요
    compare = soup.find("p", attrs={"class": "cast_txt"}).get_text()
    # 체감 온도 00˚
    wind_chill = soup.find("span", attrs={"class": "sensible"}).get_text()
    mornig_rain_r = soup.find("span", attrs={"class": "point_time morning"}).get_text().strip()
    afternoon_rain_r = soup.find("span", attrs={"class": "point_time afternoon"}).get_text().strip()

    if 28 <= now_temp:
        image=1
    elif 23 <= now_temp <= 27:
        image=2
    elif 20 <= now_temp <= 22:
        image=3
    elif 17 <= now_temp <= 19:
        image=4
    elif 12 <= now_temp <= 16:
        image=5
    elif 9 <= now_temp <= 11:
        image=6
    elif 5 <= now_temp <= 8:
        image=7
    else:
        image=8

    return render_template('search.html', now_temp=now_temp, min_temp=min_temp, max_temp=max_temp, compare=compare,
                           wind_chill=wind_chill, mornig_rain_r=mornig_rain_r, afternoon_rain_r=afternoon_rain_r, image_file="image/{}.jpg".format(image), where=where)

@app.errorhandler(500)
def internal_server_error(error):
    return "검색할 수 없는 지역입니다."


if __name__ == '__main__':
    app.run()
