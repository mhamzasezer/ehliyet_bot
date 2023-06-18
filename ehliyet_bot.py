import logging
from os import access
from requests import Session
import time
from bs4 import BeautifulSoup

login_url = "https://www.e-license.jp/el25/pc/p01a.action"
shift_jis_code = "shift_jis"


session = Session()
headers = {
    "Host": "www.e-license.jp",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"
}
session.headers.update(headers)

user_id = "*************"
user_pass = "************"
school_id = "************"


# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True

def login():
    # Login sayfasini ac
    login_page_url="https://www.e-license.jp/el25/?abc=19PdhBo7H3o%2BbrGQYS%2B1OA%3D%3D"
    session.get(login_page_url)

    print("Login Page'i aciyoruz:")
    print("-------")

    # Login hazirliklari
    session.headers["Referer"] = login_page_url
    body_data = {
        "b.studentId": user_id,
        "b.password": user_pass,
        "method:doLogin": "ログイン",
        "b.wordsStudentNo": "教習生番号",
        "b.processCd": "",
        "b.kamokuCd": "",
        "b.schoolCd": school_id,
        "index": "",
        "server": "el25aspa",
    }


    # Logging
    print("Login yapiyoruz:")
    response = session.post(login_url, data=body_data)

    print("Logging status code: ", response.status_code)
    # print(response.content.decode(shift_jis_code))

    print("-------")


def fetch_calendar_html(page_number):
    calendar_page_url = "https://www.e-license.jp/el25/pc/p03a.action"
    calendar_type=""
    page_count = 1

    if page_number == 1:
        calendar_type = "A"
        page_count = 1
    elif page_number > 2 and page_number <= 5:
        calendar_type = "N"
        page_count = page_number-1

    # request hazirligi
    body_data = {
        "b.schoolCd": school_id,
        "b.processCd": calendar_type,
        "b.kamokuCd": "0",
        "b.lastScreenCd": "",
        "b.instructorTypeCd": "2",
        "b.dateInformationType": "",
        "b.infoPeriodNumber": "",
        "b.carModelCd": "101",
        "b.instructorCd": "0",
        "b.page": page_count,
        "b.groupCd": "1",
        "b.changeInstructorFlg": "0",
        "b.nominationInstructorCd": "0",
        "upDate": str(time.time())[:-8],
    }

    response = session.post(calendar_page_url,data=body_data)
    print("calendar data status: ", response.status_code)

    print("Checking number of page: ", page_number)
    if page_number > 5:
        print("CALENDAR DATA: ", response.content.decode(shift_jis_code))
    return response.content.decode(shift_jis_code)

def logout():
    url = "https://www.e-license.jp/el25/pc/logout.action?b.schoolCd=19PdhBo7H3o%2BbrGQYS%2B1OA%3D%3D&senisakiCd=4"
    res = session.get(url)

def find_empty_time(html_data):
    soup = BeautifulSoup(html_data, 'html.parser')
    td_html_list = soup.find_all("td", {"class": "status1"})

    date_times = []
    for td_html in td_html_list:
        tag_a = td_html.a
        onclick_str = tag_a.get("onclick")

        onclick_data = onclick_str[12:-1].replace("'", "").split(",")
        
        date = onclick_data[0]
        time_number = onclick_data[1]
        time = int(time_number)+7

        print(onclick_data, date, time)
        date_times.append((date, time))
    return date_times



#This function sends the people subbed to the line bot, messages of the available reservation dates and times.
def send_line_message(date, time):
    access_token = "********************"
    import linebot
    line_bot = linebot.LineBotApi(access_token)
    linebot.LineBotApi(access_token)
    #line_bot.broadcast(linebot.models.TextSendMessage(text=f'Ulaaa ayik ol, {date} tarihinde saat {time} bos. Ayik ol!!'))
    try: 
        line_bot.broadcast(linebot.models.TextSendMessage(text=f'Ulaaa ayik ol, {date} tarihinde saat {time} bos. Ayik ol!!'))
    except:
        print("line api error")


logout()
login()

cache_data = []
time_calculator = 0

while True:

    empty_date_times = []

    for page_number in range(1, 6):
        html_data = fetch_calendar_html(page_number)
        date_time_list = find_empty_time(html_data)
        empty_date_times += date_time_list

        if not date_time_list:
            continue

        for date_time in date_time_list:
            res_date = date_time[0]
            res_time = date_time[1]
            if (res_date, res_time) not in cache_data:
                send_line_message(res_date, res_time)
                cache_data.append((res_date, res_time))
    
    print("empty date and times: ", empty_date_times)

    # cache control
    for cached_date_time in cache_data:
        if cached_date_time not in empty_date_times:
            cache_data.remove(cached_date_time)

    print("cached_data: ", cache_data)

    print("-- sleeping 30 seconds.. \n\n")
    time.sleep(30)



