
import requests, shutil, time, os, re

import http.cookiejar
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

profile_dir=r"C:\Users\Administrator\AppData\Local\Google\Chrome\User Data"    # 对应你的chrome的用户数据存放路径  
chrome_options=webdriver.ChromeOptions()  
chrome_options.add_argument("user-data-dir="+os.path.abspath(profile_dir))  
sel=webdriver.Chrome(chrome_options=chrome_options)
time.sleep(1)
sel.get("https://publish.caasdata.com/homeIndex/program_upload_index")
time.sleep(1)
elem_select_account = sel.find_element_by_class_name("account_sel")
elem_select_account.click()
time.sleep(1)
elem_select_account_microvideo = sel.find_element_by_xpath("//li[text()='抖音快手短视频']")
elem_select_account_microvideo.click()
time.sleep(1)
sel.find_element_by_id("accounts49").click()
sel.find_element_by_id("accounts189").click()
sel.find_element_by_id("accounts188").click()
sel.find_element_by_id("accounts185").click()
sel.find_element_by_id("accounts190").click()
sel.find_element_by_id("accounts94").click()
#sel.find_element_by_id("accounts180").click()#有的时候一些元素会灰掉，无法选择，记得注释掉，比如这个百度号
sel.find_element_by_id("accounts58").click()
sel.find_element_by_id("accounts51").click()
sel.find_element_by_id("accounts76").click()
sel.find_element_by_id("accounts77").click()
sel.find_element_by_id("accounts178").click()
flp = open("视频标题.txt")
title_text = flp.read()
title_str = re.findall(r'标题1(.*)',title_text)[0]
elem_input_microvideotitle = sel.find_element_by_xpath('//input[@placeholder="请输入节目名称（注：在美拍、秒拍等UGC平台中，该名称不显示）"]')
elem_input_microvideotitle.send_keys(title_str)
flpv = open("视频基本信息.txt")#有标签和简介，到时候还要自动填充时间上去，不过时间就不写入这个文本了
video_tag = flpv.readline()
video_intro = flpv.readline()
#print(video_tag,video_intro)
elem_input_microvideotag = sel.find_element_by_id('input_center')
elem_input_microvideotag.send_keys(video_tag)
timemark = time.strftime('[%Y.%m.%d]\n',time.localtime(time.time()))
elem_input_microvideoinform = sel.find_element_by_xpath('//textarea[@placeholder="请输入简介"]')
elem_input_microvideoinform.send_keys(timemark+video_intro)
time.sleep(1)
sel.find_element_by_id("uploadBtn").click()
os.system(r'C:\\python-spider-master\douyin\upload.exe')
time.sleep(1)
timemark2 = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
shutil.move(os.path.join('output.mp4'),os.path.join('video_temp',timemark2+'.mp4'))#执行将视频移动到video_temp的操作
target = sel.find_element_by_class_name("unifine_label")
sel.execute_script("arguments[0].scrollIntoView();", target)
time.sleep(1)
sel.find_element_by_xpath('//label[@class="unifine_label"]').click()
os.system(r'C:\\python-spider-master\douyin\upload_bg.exe')
time.sleep(1)
sel.find_element_by_xpath('//span[@id="postfiles"]').click()

time.sleep(50)
while True:
    try:
            time.sleep(5)
            sel.find_element_by_xpath('//div[@class="unified_catalogue catalogue_form_config"]/div/div[@class="issue_box"]/button[@class="issue_btn"]').click()
    except:
            break

flp.close()
flpv.close()

