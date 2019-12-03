from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, timeit

class Hdu_Bro_Driver():
    def __init__(self, headless=False):
        self.init_driver(headless)

    def init_driver(self, headless=False):
        '''初始化ChromeDriver'''
        start = timeit.default_timer()
        # 初始化webdriver
        option = webdriver.ChromeOptions()
        option.add_argument('disable-infobars')
        # 模拟iPhone X登陆
        mobileEmulation = {'deviceName': 'iPhone 7'}
        option.add_experimental_option('mobileEmulation', mobileEmulation)
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        if headless:
            option.add_argument('--headless') # 无界面化.
            option.add_argument('--disable-gpu') # 配合上面的无界面化.
            option.add_argument('--window-size=1366,768') # 设置窗口大小, 窗口大小会有影响.
            option.add_argument('--no-sandbox') # 沙盒模式
        self.driver = webdriver.Chrome(options=option)
        end = timeit.default_timer()
        print('ChromeDriver初始化完成 ...\t(初始化用时: %s Seconds)' % (end-start))

    def find_element(self, locator, timeout=10):
        '''定位方法封装成函数'''
        element = WebDriverWait(self.driver, timeout).until(lambda x: x.find_element(*locator))
        return element

    def find_elements(self, locator, timeout=10):
        '''定位方法封装成函数'''
        elements = WebDriverWait(self.driver, timeout).until(lambda x: x.find_elements(*locator))
        return elements

    def login(self, student_num, passwd):
        '''模拟自动登陆数字杭电'''
        login_url = 'https://cas.hdu.edu.cn/cas/login?state=&service=https%3A%2F%2Fskl.hdu.edu.cn%2Fapi%2Fcas%2Flogin%3Findex%3D'
        while True:
            time.sleep(0.5)
            if self.driver.current_url == login_url:
                student_num_loc = ('id', 'un')
                student_num_input = self.find_element(student_num_loc)
                student_num_input.click()   # 点击学号输入框
                student_num_input.clear()   # 清空
                student_num_input.send_keys(student_num)    # 输入学号
                passwd_loc = ('id', 'pd')
                passwd_input = self.find_element(passwd_loc)
                passwd_input.click()   # 点击密码输入框
                passwd_input.clear()   # 清空
                passwd_input.send_keys(passwd)    # 输入密码
                login_loc = ('id', 'index_login_btn')
                self.find_element(login_loc).click() # 点击登陆
                break

    def get_user_info(self):
        '''获取学生个人信息'''
        user_info_url = 'https://skl.hduhelp.com/#/setting/info?name=%E4%B8%AA%E4%BA%BA%E4%BF%A1%E6%81%AF'
        while True:
            time.sleep(0.5)
            self.driver.get(user_info_url)
            if self.driver.current_url == user_info_url:
                info_loc = ('class name', 'van-cell__value')
                info_elements = self.find_elements(info_loc)
                user_info = [element.text for element in info_elements]
                return user_info
    
    def get_token(self):
        '''获取学生token'''
        token = self.driver.execute_script("return localStorage.getItem('sessionId')")
        return token