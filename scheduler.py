import schedule
import time
import datetime

import main


def job():
    NOWTIME = datetime.datetime.now()
    # サイトのメンテナンスの時間は停止
    print('現在の時刻：　' + str(NOWTIME.time()))
    if NOWTIME.time() > datetime.time(3, 55) and NOWTIME.time() < datetime.time(5, 35):
        print('サイトが停止中です．')
        return

    print("\n I'm working...")
    main.run()

# schedule.every().seconds.do(job)
schedule.every(1).minutes.do(job)
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)