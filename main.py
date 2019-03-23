import config
import scraping
import slack_notify
import datetime

STUDENT_NUMBER = config.STUDENT_NUMBER
PASSWORD = config.PASSWORD


def run():
    try:
        scraping.process('http://180.42.83.34/yoyaku/default.htm', STUDENT_NUMBER, PASSWORD)
        print('[' + str(datetime.datetime.now()) + '] 正常に終了しました．')
    except Exception:
        import traceback
        slack_notify.send_message('```' + traceback.format_exc() + '```')
        print('[' + str(datetime.datetime.now()) + '] エラーメッセージをslackに送信しました．')


if __name__ == '__main__':
    try:
        scraping.process('http://180.42.83.34/yoyaku/default.htm', STUDENT_NUMBER, PASSWORD)
        print('[' + str(datetime.datetime.now()) + '] 正常に終了しました．')
    except Exception:
        import traceback
        slack_notify.send_message('```' + traceback.format_exc() + '```')
        print('[' + str(datetime.datetime.now()) + '] エラーメッセージをslackに送信しました．')
