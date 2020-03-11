import urllib.parse
import hashlib
import http.client
import base64
import datetime

URL_PATH = 'https://www.56zhifu.com/user/MerchantAccFileDown.do'
Content_Type = 'application/x-www-form-urlencoded'
MD5Key = '7JGHPG950BSAN3EEDU3PY46C'

current_Date_Formatted = datetime.datetime.today().strftime('%Y%m%d')
print('current date: ' + str(current_Date_Formatted))
previous_Date = datetime.datetime.today() - datetime.timedelta(days=1)
previous_Date_Formatted = previous_Date.strftime('%Y%m%d')  # format the date to yyyymmdd
print('the day before the current day:', previous_Date_Formatted)

billDate = previous_Date_Formatted
merchantId = '00000000035349'
signType = 'MD5'
version = '2.0'

param = 'billDate=' + billDate + '&' + 'merchantId=' + merchantId + '&' + 'signType=' + signType + '&' + 'version=' \
        + version + MD5Key

print('md5 param :' + param)

res = hashlib.md5(param.encode('utf-8'))

print('md5 res: ' + res.hexdigest())

data = urllib.parse.urlencode({'billDate': billDate, 'merchantId': merchantId, 'signType': signType, 'version': version,
                               'signature': res.hexdigest()})
data = data.encode('UTF-8')

print('last request data :', data)

headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/xml"}

try:
    conn = http.client.HTTPSConnection("www.56zhifu.com")
    conn.request("POST", URL_PATH, data, headers)

    response = conn.getresponse()

    print(response.status, response.reason)
    if response.status != 200:
        print(f'Failure to send !')
        print(f'Response ', response.reason)
    f = response.read()

    print('res headers:', response.getheaders())
    print('len of res :', len(f))
    # print('origin of data: \n', f)
    id = f.index(b'retCode=')
    retCode = f[id + 9: id + 13]
    id = f.index(b'billDate=')
    Date = f[id + 10: id + 18]
    id = f.index(b'filecontent=')
    content = f[id + 13: len(f) - 3]
    print('str of data: \n', retCode, Date)
    print('decode content: ', base64.b64decode(content))
    filePath = "./" + "swt-" + Date.decode('ASCII') + ".txt"
    file = open(filePath, "w")
    file.write(base64.b64decode(content).decode('utf-8'))
    file.close()
    conn.close()
except Exception as e:
    print(e)
    conn.close()
