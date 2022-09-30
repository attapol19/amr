# loginscraping.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import datetime 
from flask import Flask, request, abort
from linebot import LineBotApi
from linebot import WebhookHandler
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,)


ser = Service(r'C:\Python310\chromedriver.exe')
op = webdriver.ChromeOptions()
op.add_argument("disable-popup-blocking")
op.add_argument("disable-notifications")
driver = webdriver.Chrome(service=ser, options=op)

url = 'https://www.amr.pea.co.th/'
#url = 'http://www.google.com'
driver.get(url)
time.sleep(2)

# ปิด popup
try:
	x_path = r'/html/body/div[2]/div[1]/button/span[1]'
	button = driver.find_element("xpath",x_path)
	button.click()
	time.sleep(2)
except Exception:
	pass

#login

txtuser = driver.find_element(By.ID,'txtUserName')
txtpass = driver.find_element(By.ID, 'txtPassword')
txtuser.send_keys('020002437075')
txtpass.send_keys(r'Gcb5/5')
btnok = driver.find_element(By.ID,'btnOK')
btnok.click()
#txtpass.send_keys(Keys.RETURN)


# Set time
dt = datetime.datetime.now()
date = dt.strftime("%d/%m/%Y")
time.sleep(10)

#Goto Data
#url เช็คข้อมูลพลังไฟฟ้าสูงสุด
url_data = r'https://www.amr.pea.co.th/AMRWEB/showDailyProfile.aspx?Custid=0&CustCode=020002437075&MeterPoint=47438&SumMeter=0&RepDate={}&GrphType=Col&DataType=0&kWh=1&kVarh=0&kW=0&kVar=0&kWh1=0&kVarh1=0&kW1=0&kVar1=0&Cur=0&Vol=0&PF=0&PD=0'.format(date)
driver.get(url_data)
time.sleep(2)

x_path1 = '//*[@id="tabs-0"]/table/tbody/tr[98]/td[2]'
x_path2 ='//*[@id="tabs-0"]/table/tbody/tr[98]/td[3]'
x_path3 ='//*[@id="tabs-0"]/table/tbody/tr[98]/td[4]'
powerpeak1 = driver.find_element(By.XPATH,x_path1)
powerpeak2 = driver.find_element(By.XPATH,x_path2)
powerpeak3 = driver.find_element(By.XPATH,x_path3)
print ('รายงานข้อมูลกิโลวัตต์รายวัน \n','RATE A:  '+powerpeak1.text+'\n','RATE B:  '+powerpeak2.text+'\n','RATE C:  '+powerpeak3.text)
text_out = 'รายงานข้อมูลกิโลวัตต์รายวัน \n','RATE A:  '+powerpeak1.text+'\n','RATE B:  '+powerpeak2.text+'\n','RATE C:  '+powerpeak3.text

#logout
logout =r'https://www.amr.pea.co.th/AMRWEB/Logout.aspx'
time.sleep(1)
driver.close()

# ส่งไลน์แชตบอท
#ห้องโกลเด้นคลิฟบีช
channel_secret = "c4e0d4d39cbe8cd829ce53ef0ebfd478"
channel_access_token = "VDYXwfhKyNw5+NmKn7g9pQK4dB5YCiBnuyj/gS6U9tZQfw/n2kyaKXEI8m/cRQQXdExTndELZSJJ3NOka27ukucKDrTY/rxJrvR+wDlnwjmVt/i1NDwmMNO7vsFTGrrg4FhIXBwLXuRxZo2zwG4UbgdB04t89/1O/w1cDnyilFU="


line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():
	try:
		signature = request.headers["X-Line-Signature"]
		body = request.get_data(as_text=True)
		handler.handle(body, signature)
	except:
		pass
	return "Hello Line Chatbot"
group_id = 'C277517c597499be569b68d279602f505'
line_bot_api.push_message(group_id,TextSendMessage(text=text_out))
#txtpass.send_keys(Keys.RETURN)

# เข้าหน้า monthly profile
# url = 'https://www.amr.pea.co.th/AMRWEB/selMonthlyProfile.aspx?CustCode=020002437075&Custid=41677%22'
# url ='https://www.amr.pea.co.th/AMRWEB/showMonthlyProfile.aspx?Custid=41677%22&CustCode=020002437075&PeaNo=23075862&MeterPoint=47438&SumMeter=0&RepDate=01/09/2565&GrphType=Line&DataType=2&RepType=kW&RateType=&SumType=0&SubSys=0&RoundType=0'