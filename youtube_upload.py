
import requests, shutil, time, os, re

import http.cookiejar
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


url_str = input("input url:")
tran_title = input("input title:")
print('1.抖音快手短视频\n2.动漫_原创\n3.电影_影视\n4.游戏\n5.学校相关\n6.生活娱乐\n7.音乐\n8.动漫_GAL\n9.科技')
choice = input("input choice:")
if(choice == '1'):
    choice_one = '抖音快手短视频'
elif(choice == '2'):
    choice_one = '动漫_原创'
elif(choice == '3'):
    choice_one = '电影_影视'
elif(choice == '4'):
    choice_one = '游戏'
elif(choice == '5'):
    choice_one = '学校相关'
elif(choice == '6'):
    choice_one = '生活娱乐'
elif(choice == '7'):
    choice_one = '音乐'
elif(choice == '8'):
    choice_one = '动漫_GAL相关'
else:
    choice_one = '科技'

#print(choice)
#print(choice_one)

you_get = 'you-get '+ url_str
os.system(you_get)
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',  # noqa
    'Accept-Charset': 'UTF-8,*;q=0.5',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0',  # noqa
}
#测试：https://www.youtube.com/watch?v=jNQXAC9IVRw
#print(url_str)
Thumbnail = re.findall('watch\?v=(.*)', url_str)[0]
Thumbnail  = 'http://i3.ytimg.com/vi/'+Thumbnail+'/maxresdefault.jpg'
img = requests.get(Thumbnail, headers = headers)
flag = 0
#print(img.headers['content-length'])
if(int(img.headers['content-length']) > 1098):
    flag = 1
    with open('bak_img.jpg', 'wb') as f:
        f.write(img.content)
        f.close()

for file in os.listdir("./"):
    st_name = os.path.splitext(file)[1]
    if st_name == '.webm' or st_name == '.mp4' or st_name == '.flv':
        
        title = re.findall('(.*?)'+st_name, file)[0]
        os.rename(file, 'output.mp4')
        _st_name = st_name

#print(title, flag)



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
elem_select_account_microvideo = sel.find_element_by_xpath("//li[text()=\'"+choice_one+"\']")
elem_select_account_microvideo.click()
time.sleep(1)

sel.find_element_by_id("accounts190").click()

title_str = tran_title
elem_input_microvideotitle = sel.find_element_by_xpath('//input[@placeholder="请输入节目名称（注：在美拍、秒拍等UGC平台中，该名称不显示）"]')
elem_input_microvideotitle.send_keys(title_str)

video_intro = '更多精彩内容，请关注「同和系视频矩阵」~'
video_title = '原标题：'+title+'\n'
#print(video_tag,video_intro)
#elem_input_microvideotag = sel.find_element_by_id('input_center')
#elem_input_microvideotag.send_keys(video_tag)
timemark = time.strftime('[%Y.%m.%d]\n',time.localtime(time.time()))
elem_input_microvideoinform = sel.find_element_by_xpath('//textarea[@placeholder="请输入简介"]')
elem_input_microvideoinform.send_keys(timemark+video_title+video_intro)
time.sleep(1)
sel.find_element_by_id("uploadBtn").click()
os.system(r'C:\\python-spider-master\douyin\upload.exe')
time.sleep(1)
shutil.move(os.path.join('output.mp4'),os.path.join('video_temp',title+_st_name))#执行将视频移动到video_temp的操作
sel.find_element_by_id("accounts77").click()
sel.find_element_by_id("accounts51").click()
sel.find_element_by_id("accounts94").click()
sel.find_element_by_id("accounts49").click()
sel.find_element_by_id("accounts188").click()
#sel.find_element_by_id("accounts185").click()
sel.find_element_by_id("accounts76").click()
sel.find_element_by_id("accounts58").click()
time.sleep(1)
target = sel.find_element_by_class_name("unifine_label")
sel.execute_script("arguments[0].scrollIntoView();", target)
time.sleep(1)
if(flag == 1):
    sel.find_element_by_xpath('//label[@class="unifine_label"]').click()
    os.system(r'C:\\python-spider-master\douyin\upload_bg.exe')
    time.sleep(1)
    sel.find_element_by_xpath('//span[@id="postfiles"]').click()
    time.sleep(2)

sel.find_element_by_xpath('//label[@class="mar_left ivu-radio-wrapper ivu-radio-group-item"][1]').click()
time.sleep(1)
elem_tran = sel.find_element_by_xpath('//div[@class="unified_catalogue catalogue_form_config"]/div/form/div/div/div/input[@placeholder="转载视频请注明来源（例：转自http://www.xxxx.com/yyyy）"]')
elem_tran.send_keys(url_str)


time.sleep(100)
while True:
    try:
            time.sleep(5)
            sel.find_element_by_xpath('//div[@class="unified_catalogue catalogue_form_config"]/div/div[@class="issue_box"]/button[@class="issue_btn"]').click()
    except:
            break









