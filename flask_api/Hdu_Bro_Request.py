import requests
import json
from PIL import Image
from io import BytesIO
import base64
import execjs
import re

def crack_code(img_stream):
    '''通过API自动识别验证码'''
    appcode = 'b50ca5defc40421ba05f24e2c13b94d7'  # 过期后需要更换
    api = 'http://codevirify.market.alicloudapi.com/icredit_ai_image/verify_code/v1'
    data = {
        'IMAGE': img_stream,
        'IMAGE_TYPE': 0
    }
    api_header = {
        'Authorization': 'APPCODE '+appcode,
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    }
    r = requests.post(api,data, headers=api_header)
    auto_crack_code = json.loads(r.text).get('VERIFY_CODE_ENTITY').get('VERIFY_CODE')
    return auto_crack_code

def crack_code_baidu(img_stream):
    access_token = '24.e93d7918167521a4bfd9dbae8bc8d299.2592000.1577504016.282335-17872543'
    api = 'https://aip.baidubce.com/rest/2.0/ocr/v1/numbers'
    kw = {'access_token':access_token}
    data = {'image': img_stream,}
    api_header = {'Content-Type': 'application/x-www-form-urlencoded'}
    r = requests.post(api, data, params=kw, headers=api_header)
    return r.json()
    
def login(u,p):
    url = 'https://cas.hdu.edu.cn/cas/login'
    kw = {'state':'', 'service': 'https://skl.hdu.edu.cn/api/cas/login?index='}
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    }
    r1 = requests.get(url, params=kw, headers=headers)
    lt = re.findall(r'\w{2}-\d{6}-\w{30}-\w{3}', r1.text)[0]
    execution = re.findall(r'e\d+s\d+', r1.text)[0]
    # 调用des.js进行rsa加密
    js_str = ''
    with open('./static/des.js', 'r') as f:
        for line in f.readlines():
            js_str += line
    ctx = execjs.compile(js_str)
    rsa = ctx.call('strEnc', u+p+lt,'1','2','3')
    ul = len(u)
    pl = len(p)
    post_data = {
        'rsa': rsa,
        'ul': ul,
        'pl': pl,
        'lt': lt,
        'execution': execution,
        '_eventId': 'submit'
    }
    r2 = requests.post('https://cas.hdu.edu.cn/cas/login?state=&service=https%3A%2F%2Fskl.hdu.edu.cn%2Fapi%2Fcas%2Flogin%3Findex%3D',post_data)
    print(r2.request.headers)
    print(r2.request.body)
    print(r2.headers)
    print(r2.status_code)

class Hdu_Bro_Request():
    def __init__(self, token):
        self.token = token
        self.headers = self.init_headers(self.token)

    def init_headers(self, token):
        headers = {
        'Host': 'skl.hdu.edu.cn',
        'Origin': 'https://skl.hduhelp.com',
        'Referer': 'https://skl.hduhelp.com/',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
        'X-Auth-Token': token,
        }
        return headers

    def get_user_info(self, ):
        '''获取用户信息
        Return dict_keys(['id', 'userName', 'userType', 'unitId', 'unitCode', 'unitName', 'grade', 'classNo', 'sex', 'major', 'roleList'])
        '''
        url = 'https://skl.hdu.edu.cn/api/userinfo?type='
        r = requests.get(url, headers=self.headers)
        userinfo = r.json()
        return userinfo

    def get_course(self, startTime):
        url = 'https://skl.hdu.edu.cn/api/course?startTime='
        kw = {'startTime':startTime}
        r = requests.get(url, params=kw, headers=self.headers)
        print(r.text)
        #course_list = r.json()['list']
        #course_names = [(course['courseName'],course['weekDay']) for course in course_list]
        #print(course_names)

    def code_check_in(self, signin_code):
        url = 'https://skl.hdu.edu.cn/api/checkIn/code-check-in'
        kw = {'code':signin_code}
        r = requests.get(url, params=kw, headers=self.headers)
        return r.status_code

    def create_code_img(self, ):
        '''Return 二进制流图片'''
        url = 'https://skl.hdu.edu.cn/api/checkIn/create-code-img'
        r = requests.get(url, headers=self.headers)
        '''
        img = Image.open(BytesIO(r.content))
        img.show()
        '''
        img_stream = base64.b64encode(r.content).decode("utf-8")
        return img_stream

    def valid_code(self, code):
        '''
        Return r.status_code
                200 签到成功
                400 验证码错误
                401 签到码无效
        '''
        url = 'https://skl.hdu.edu.cn/api/checkIn/valid-code'
        kw = {'code':code}
        r = requests.get(url, params=kw, headers=self.headers)
        return r.status_code
    
