from scraper import scrapeNotices
from datetime_util import nowKoreaTime
import firebase

def sendMessageIfNoticeHasKeyword(notice, keywords):
    r"""
    공지사항 제목에 포함된 키워드를 찾아 해당 키워드를 토픽으로 알림을 보낸다.
    """
    for keyword in keywords:
        if keyword in notice.title:
            print(keyword, end=", ")
            firebase.sendMessage(keyword, notice.title, notice.url)

def createNewNoticeIds(notices):
    result = ""
    for notice in notices:
        result += notice.id + ','
    return result.removesuffix(',')

def runBot():
    print("-----------------------------------------------")
    print("Date: " + NOW.isoformat())

    try:
        notices = scrapeNotices()
    except Exception:
        firebase.sendErrorMessage('Scraping 실패')
        return
    previousNoticeIds = firebase.importPreviousNoticeIds()
    keywords = firebase.importSubscribedKeywords()
    
    for notice in notices:
        if notice.id in previousNoticeIds:
            break
        print('\nNew post: ' + notice.title)
        sendMessageIfNoticeHasKeyword(notice, keywords)
        
    newNoticeIds = createNewNoticeIds(notices)
    if newNoticeIds is not None and newNoticeIds != "" and previousNoticeIds != newNoticeIds:
        firebase.updateNoticeIdsDatabase(newNoticeIds)
    
    print("-----------------------------------------------")

NOW = nowKoreaTime()
WEEKDAY = NOW.weekday()
# 월 ~ 금, 9시 ~ 20시 59분 사이에서만 구동한다.
if 0 <= WEEKDAY <= 4 and 9 <= NOW.hour <= 20:
    firebase.init()
    runBot()