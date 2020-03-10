# ! -*- encoding:utf-8 -*-

import requests
import time,json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler



# 获取日志最后一行
def getline():
    WEB_LOG = open('./log.txt','rb')
    OFFS = -30
    while True :
        WEB_LOG.seek(OFFS,2)
        WEB_LOG_LINES = WEB_LOG.readlines()
        if len(WEB_LOG_LINES) > 1 :
            WEB_LOG_LASTLINE = WEB_LOG_LINES[-1]
            break
        OFFS *= 2
    WEB_LOG_LASTLINE = WEB_LOG_LASTLINE.decode('utf-8')
    return WEB_LOG_LASTLINE
# 监控日志变化

class FileEventHandler(FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)

    def on_modified(self, event):
        if not event.is_directory:

            log=getline()
            msg(log)

# 钉钉发送
def msg(line):
    token = ""
    api_url = "https://oapi.dingtalk.com/robot/send?access_token=%s" % token
    # 必备字符
    text = "预警"

    headers = {'Content-Type': 'application/json;charset=utf-8'}
    json_text = {
        "msgtype": "text",
        "text": {
            "content": '%s%s' %(text,line)
        }
    }
    print(requests.post(api_url, json.dumps(json_text), headers=headers).content)


if __name__ == '__main__':

    path = '.'
    event_handler = FileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    print('Ctrl-C 退出程序!')
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
