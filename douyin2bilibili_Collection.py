# -*- coding:utf-8 -*-
from contextlib import closing
import requests, json, re, os, sys, random, cv2, random, qrcode, pygame, shutil, time, urllib, math
from ipaddress import ip_address
from subprocess import Popen, PIPE
import urllib
from PIL import Image,ImageDraw,ImageFont,ImageFilter
from io import BytesIO
import http.cookiejar
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

backMode = {
            #背景图属性，我的背景图上需要添加一个二维码和多个文本框
            "back_url":"timg.jpg",
            "size":(550,363),
            "QR":{#二维码属性
                "frame":(130,130),#大小
                "position":(380,750),#位置
            },

            "nicklogo":{#头像属性
                "frame":(130,130),#大小
                "position":(120,750),#位置
            },
            
            
            "nickname":[{#昵称属性
                "size":45,#字号
                "ttf":"GBK.ttf",#字体
                "color":"",#颜色
                "position":(120,950),
                "frame":(500,20),
            },],
            "text":[{#文本框属性
                "size":40,#字号
                "ttf":"GBK.ttf",#字体
                "color":"",#颜色
                "position":(120,400),
                "frame":(400,20),
            },{
                "size":40,
                "ttf":"GBK.ttf",
                "color":"",
                "position":(120,460),
                "frame":(400,20),
            },{
                "size":40,
                "ttf":"GBK.ttf",
                "color":"",
                "position":(120,520),
                "frame":(400,20),
            },{
                "size":40,
                "ttf":"GBK.ttf",
                "color":"",
                "position":(120,580),
                "frame":(400,20),
            },{
                "size":40,
                "ttf":"GBK.ttf",
                "color":"",
                "position":(120,640),
                "frame":(400,20),
            },],
        }







class DouYin(object):
        def __init__(self, width = 500, height = 300):
                """
                抖音App视频下载
                """
                rip = ip_address('0.0.0.0')
                while rip.is_private:
                        rip = ip_address('.'.join(map(str, (random.randint(0, 255) for _ in range(4)))))
                self.headers = {
                        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                        'accept-encoding': 'gzip, deflate, br',
                        'accept-language': 'zh-CN,zh;q=0.9',
                        'pragma': 'no-cache',
                        'cache-control': 'no-cache',
                        'upgrade-insecure-requests': '1',
                        'user-agent': 'Mozilla/5.0 (Linux; U; Android 5.1.1; zh-cn; MI 4S Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.146 Mobile Safari/537.36 XiaoMi/MiuiBrowser/9.1.3',
                        'X-Real-IP': str(rip),
                        'X-Forwarded-For': str(rip),
                }

        def getToken(self):
                req = requests.get('https://api.appsign.vip:2688/token/douyin/version/2.9.1').json()
                return self.save_json(req)

        def getDevice(self):
                req = requests.get('https://api.appsign.vip:2688/douyin/device/new/version/2.7.0').json()
                device_info = req['data']
                return device_info

        def getSign(self, token, query):
                req = requests.post('https://api.appsign.vip:2688/sign', json={'token': token, 'query': query}).json()
                if req['success']:
                        sign = req['data']
                else:
                        sign = req['success']

                
                return sign

        def params2str(self, params):
                query = ''
                for k, v in params.items():
                        query += '%s=%s&' % (k, v)
                query = query.strip('&')
                return query

        def save_json(self, data):
                with open('douyin.txt', 'w') as f:
                        json.dump(data, f, ensure_ascii=False)

        def load_json(self):
                with open('douyin.txt', 'r') as f:
                        data = json.load(f)
                        return data

        def get_video_urls(self, user_link, type_flag):
                """
                获得视频播放地址
                Parameters:
                        user_id：查询的用户ID
                Returns:
                        video_names: 视频名字列表
                        video_urls: 视频链接列表
                        nickname: 用户昵称
                """


                headers = {
                        'User-Agent': 'Aweme/2.7.0 (iPhone; iOS 11.0; Scale/2.00)'
                }
                r = requests.get(user_link, allow_redirects=True)
                redirecturl = r.url

                uid = re.findall('user/(.*?)\?u_code=', redirecturl)
                rct = requests.get(redirecturl, headers=headers)

                nickname = re.findall('<p class="nickname">(.*?)\</p>', str(rct.text))[0]
                nicklogo = re.findall('<img class="avatar" src="(.*?)">', str(rct.text))[0]
                                
                video_names = []
                video_urls = []
                share_urls = []
                unique_id = ''
                max_cursor = 0
                has_more = 1
                device_info = self.getDevice()
                APPINFO = {
                        'version_code': '2.7.0',
                        'app_version': '2.7.0',
                        'channel': 'App%20Stroe',
                        'app_name': 'aweme',
                        'build_number': '27014',
                        'aid': '1128'
                }
                params = {
                        'iid': device_info['iid'],
                        'idfa': device_info['idfa'],
                        'vid': device_info['vid'],
                        'device_id': device_info['device_id'],
                        'openudid': device_info['openudid'],
                        'device_type': device_info['device_type'],
                        'os_version': device_info['os_version'],
                        'os_api': device_info['os_api'],
                        'screen_width': device_info['screen_width'],
                        'device_platform': device_info['device_platform'],
                        'version_code': APPINFO['version_code'],
                        'channel': APPINFO['channel'],
                        'app_name': APPINFO['app_name'],
                        'build_number': APPINFO['build_number'],
                        'app_version': APPINFO['app_version'],
                        'aid': APPINFO['aid'],
                        'ac': 'WIFI',
                        'count': '12',
                        'offset': '0'
                }


                
                print('解析视频链接中……')
                query = self.params2str(params)
                if not os.path.isfile('douyin.txt'):
                        self.getToken()
                token = self.load_json()['token']
                sign = self.getSign(token, query)
                while not sign:
                        self.getToken()
                        token = self.load_json()['token']
                        sign = self.getSign(token, query)
                params['mas'] = sign['mas']
                params['as'] = sign['as']
                params['ts'] = sign['ts']
                
                urllib.request.urlretrieve('https://raw.githubusercontent.com/Jack-Cherish/python-spider/master/douyin/fuck-byted-acrawler.js', 'fuck-byted-acrawler.js')
                try:
                        process = Popen(['node', 'fuck-byted-acrawler.js', str(uid)], stdout=PIPE, stderr=PIPE)
                except (OSError, IOError) as err:
                        print('请先安装 node.js: https://nodejs.org/')
                        sys.exit()
                _sign = process.communicate()[0].decode().strip('\n').strip('\r')
                
                del params['offset']
                params['count'] = '21'
                params['user_id'] = uid
                user_url_prefix = 'https://www.amemv.com/aweme/v1/aweme/favorite' if type_flag == 'f' else 'https://aweme.snssdk.com/aweme/v1/aweme/post/'


                while has_more != 0:
                        if type_flag == 'f':
                                user_url = user_url_prefix + '/?user_id=%s&max_cursor=%s&count=21&aid=1128&_signature=%s&dytk=%s' % (uid, max_cursor, _sign, dytk)
                                req = requests.get(user_url, headers=self.headers)
                                while req.status_code != 200:
                                        req = requests.get(user_url, headers=self.headers)
                                html = json.loads(req.text)
                        else:
                                params['max_cursor'] = max_cursor
                                req = requests.get(user_url_prefix, params=params, headers=headers)
                                while req.status_code != 200:
                                        req = requests.get(user_url_prefix, params=params, headers=headers)
                                html = json.loads(req.text)
                                while html['status_code'] != 0:
                                        req = requests.get(user_url_prefix, params=params, headers=headers)
                                        while req.status_code != 200:
                                                req = requests.get(user_url_prefix, params=params, headers=headers)
                                        html = json.loads(req.text)
                        for each in html['aweme_list']:
                                try:
                                        if type_flag == 'f':
                                                video_url = each['video']['play_addr']['url_list'][0]
                                                share_desc = each['share_info']['share_title']
                                        else:
                                                video_url = each['video']['bit_rate'][0]['play_addr']['url_list'][2]
                                                share_desc = each['desc']
                                except:
                                        continue
                                if os.name == 'nt':
                                        for c in r'\/:*?"<>|':
                                                nickname = nickname.replace(c, '').strip().strip('\.')
                                                share_desc = share_desc.replace(c, '').strip()
                                share_id = each['aweme_id']
                                
                                video_names.append(share_desc)
                                share_urls.append(each['share_url'])
                                video_urls.append(video_url)
                        max_cursor = html['max_cursor']
                        has_more = html['has_more']

                return video_names, video_urls, share_urls, nickname, nicklogo

        def get_download_url(self, video_url, watermark_flag):
                """
                获得带水印的视频播放地址
                Parameters:
                        video_url：带水印的视频播放地址
                Returns:
                        download_url: 带水印的视频下载地址
                """
                # 带水印视频
                if watermark_flag == True:
                        download_url = video_url.replace('/play/', '/playwm/')
                # 无水印视频
                else:
                        download_url = video_url.replace('/playwm/', '/play/')

                return download_url

        def video_downloader(self, video_url, video_name, watermark_flag=False):
                """
                视频下载
                Parameters:
                        video_url: 带水印的视频地址
                        video_name: 视频名
                        watermark_flag: 是否下载带水印的视频
                Returns:
                        无
                """
                size = 0
                video_url = self.get_download_url(video_url, watermark_flag=watermark_flag)
                with closing(requests.get(video_url, headers=self.headers, stream=True)) as response:
                        chunk_size = 1024
                        content_size = int(response.headers['content-length'])
                        if response.status_code == 200:
                                sys.stdout.write('  [文件大小]:%0.2f MB\n' % (content_size / chunk_size / 1024))

                                with open(video_name, 'wb') as file:
                                        for data in response.iter_content(chunk_size = chunk_size):
                                                file.write(data)
                                                size += len(data)
                                                file.flush()

                                                sys.stdout.write('  [下载进度]:%.2f%%' % float(size / content_size * 100) + '\r')
                                                sys.stdout.flush()


        def tran_single(self, timemark2, timemark5, timemark4):
                input = os.path.join(timemark4,timemark5)
                background = os.path.join(timemark4,timemark2)
                output = os.path.join(timemark4,"Fragment_"+timemark2)#w宽 h高

                cap=cv2.VideoCapture(input+'.mp4')
                w = cap.get(3)
                h = cap.get(4)

                #print(w,h)
                
                height = math.ceil(608*h/w)
                if(height>1080):
                        height = 1080
                        
                str_height = str(height)
                finishcode = "ffmpeg -i "+input+".mp4"+" -i "+background+".jpg"+" -filter_complex [0:v]scale=608:"+str_height+"[video1];[1:v][video1]overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/2 -s 1920*1080 -y "+output+".mp4"#209，记得补充判断信息
                os.system(finishcode)
                
                os.remove(background+".jpg")


        def tran_all(self, timemark4):
                list_txt = os.path.join(timemark4,"list")
                finishcode2 = "ffmpeg -f concat -i "+list_txt+".txt"+" -c copy "+"output.mp4"
                os.system(finishcode2)


        def run(self):
                """
                运行函数
                Parameters:
                        None
                Returns:
                        None
                """
                self.hello()
                user_id = input('请输入作者短链接 (例如http://v.douyin.com/RbxoM4/):')
                user_id = user_id if user_id else 'http://v.douyin.com/RbxoM4/'
                watermark_flag = False
                type_flag = 'p'
                timemark4 = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))#timemark4为文件夹名
                video_names, video_urls, share_urls, nickname, nicklogo = self.get_video_urls(user_id, type_flag)
                nickname_dir = os.path.join(timemark4)
                if not os.path.exists(timemark4):
                        os.makedirs(timemark4)

                fl = open(os.path.join(timemark4,'list.txt'),'w+')
                flp = open("视频标封.txt")

                title_text = flp.read()
                title_str = re.findall(r'标题1(.*?)\s',title_text)[0]
                title_pic_url = share_urls[0]
                self.get_title_bg(title_pic_url)

                if type_flag == 'f':
                        if 'favorite' not in os.listdir(nickname_dir):
                                os.mkdir(os.path.join(nickname_dir, 'favorite'))
                print('视频下载中:共有%d个作品!\n' % len(video_urls))
                for num in range(len(video_urls)):
                        print('  解析第%d个视频链接 [%s] 中，请稍后!\n' % (num + 1, share_urls[num]))
                        if '\\' in video_names[num]:
                                video_name = video_names[num].replace('\\', '')
                        elif '/' in video_names[num]:
                                video_name = video_names[num].replace('/', '')
                        else:
                                video_name = video_names[num]

                        timemark5 = str(round(time.time() * 1000))#timemark5为下载的视频第一次改的名字
                        video_path = os.path.join(nickname_dir, timemark5+'.mp4') if type_flag!='f' else os.path.join(nickname_dir, 'favorite', timemark5)
                        if os.path.isfile(video_path):
                                print('视频已存在')
                        else:
                                self.video_downloader(video_urls[num], video_path, watermark_flag)
                        print('\n')
                        timemark2 = self.make_pic(backMode, nickname, video_name, share_urls[num], nicklogo, timemark4)#timemark2为片段视频对应图片的名字
                        self.tran_single(timemark2, timemark5, timemark4)
                        var = 'file '+timemark4+'/Fragment_'+timemark2+'.mp4'
                        fl.writelines(var)
                        fl.write('\n')


                fl.close()
                flp.close()
                self.tran_all(timemark4)
                filepath_0 = os.path.join(timemark4)#确定TEMP目录
                shutil.rmtree(filepath_0)#执行删除目录操作
                print('下载完成!')
                #self.web_upload()
                shutil.move(os.path.join('output.mp4'),os.path.join('video_temp',nickname+'.mp4'))#执行将视频移动到video_temp的操作
                


        def make_QR(self, content, sizeW = 0, sizeH = 0):#创建二维码
                qr = qrcode.QRCode(version=3, box_size=3, border=1, error_correction=qrcode.constants.ERROR_CORRECT_H)
                qr.add_data(content)  
                qr.make(fit=True)  
                img = qr.make_image()
                if sizeW == 0 and sizeH == 0:
                        return img
                w, h = img.size 
                img = img.resize((sizeW,sizeH),Image.ANTIALIAS)
                
                return img
        def com_pic(self, topimg, backimg, position):#合并图片1
                nodeA = position
                w, h = topimg.size
                nodeB = (position[0]+w, position[1]+h)
                backimg.paste(topimg, (nodeA[0], nodeA[1], nodeB[0], nodeB[1]))
                return backimg
        def com_pic2(self, topimg, backimg, position):#合并图片2
                nodeA = position

                topimg = topimg.resize((130,130),Image.ANTIALIAS)
                w, h = topimg.size
                nodeB = (position[0]+w, position[1]+h)
                backimg.paste(topimg, (nodeA[0], nodeA[1], nodeB[0], nodeB[1]))
                return backimg

        def com_pic3(self, img):#合并图片3，这个是处理封面的，待优化

                w, h = img.size
                if(w>=h*16/9):
                        re_bg_w=math.ceil(1080*w/h)
                        re_bg_h=1080
                        re_fg_w=1920
                        re_fg_h=math.ceil(1920*h/w)
                else:
                        re_bg_w=1920
                        re_bg_h=math.ceil(1920*h/w)
                        re_fg_h=1080
                        re_fg_w=math.ceil(1080*w/h)

                
                back_img_tmp = img.resize((re_bg_w,re_bg_h),Image.ANTIALIAS)#把原图放大为背景图
                img2 = img.resize((re_fg_w,re_fg_h),Image.ANTIALIAS)#把原图处理成前景图
                bg_pointx = int((re_bg_w-1920)/2)
                bg_pointy = int((re_bg_h-1080)/2)
                back_img_tmp2 = back_img_tmp.crop([bg_pointx,bg_pointy,bg_pointx+1920,bg_pointy+1080])#裁切背景图
                img = back_img_tmp2.filter(ImageFilter.GaussianBlur(radius=18))#模糊背景图
                fg_pointx = int((1920-re_fg_w)/2)
                fg_pointy = int((1080-re_fg_h)/2)
                img.paste(img2, (fg_pointx,fg_pointy,fg_pointx+re_fg_w,fg_pointy+re_fg_h))#拼合
                img.save(os.path.join('bak_img'+'.jpg'), quality=100)



        def get_title_bg(self, url):
                #输入短链接，输出title_bg.jpg到目录，执行完毕后记得删除，视频移动到tmp文件夹，但封面图还是删了吧。
                headers = {
                        'User-Agent': 'Aweme/2.7.0 (iPhone; iOS 11.0; Scale/2.00)'
                }
                r = requests.get(url, allow_redirects=True)
                redirecturl = r.url
                rct = requests.get(redirecturl, headers=headers)
                title_bg_url = re.findall('"og:image" content="(.*?)">', str(rct.text))[0]
                #print(title_bg_url)
                response_img = requests.get(title_bg_url)
                title_bg_res1 = Image.open(BytesIO(response_img.content))
                #title_bg_res2 = Image.open('background_logo.png')
                self.com_pic3(title_bg_res1)#合成3，输入原始图片，输出处理好的封面图


        def write_line(self, backimg ,text, tmode):#给单个文本框填充数据
                myfont = ImageFont.truetype(tmode["ttf"],size=tmode["size"])
                draw = ImageDraw.Draw(backimg)
                tend = len(text)
                while True:
                        text_size = draw.textsize(text[:tend], font=myfont) #文本图层的尺寸
                        #print(text_size)
                        if text_size[0] <= tmode["frame"][0]:
                                break
                        else:
                                tend -= 1#文本太长，调整文本长度
                draw.text((tmode["position"][0], tmode["position"][1]), text[:tend], font=myfont)
                return backimg, tend
         
        def write_text(self, img , text, tmodeList, nickname, nickmode):#写文本
                tlist = text.split("\n")
                mnum = 0
                draw = ImageDraw.Draw(img)
                for t in tlist:
                        tbegin = 0
                        tend = len(t)
                        while True:
                                img, tend = self.write_line(img, t[tbegin:tend], tmodeList[mnum])
                                mnum += 1
                                if tbegin + tend == len(t) or mnum == len(tmodeList):
                                        break
                                else:
                                        tbegin = tbegin + tend
                                        tend = len(t)
                        if mnum == len(tmodeList):
                                break

                img, tend = self.write_line(img, nickname, nickmode[0])
                return img


        def make_pic(self, mode, nickname, text, url, nicklogo, timemark4):
                img = Image.open(mode["back_url"])#读取背景图片
                
                url = re.findall('(.*?)&u_code', url)
                #print(url)
                QR_res = self.make_QR(url, mode["QR"]["frame"][0], mode["QR"]["frame"][1])#创建二维码
                img = self.com_pic(QR_res, img, mode["QR"]["position"])#合成1
                response_img = requests.get(nicklogo)
                try:
                        nicklogo_res = Image.open(BytesIO(response_img.content))
                except:
                        nicklogo_res = Image.open('noface.jpg')
                img = self.com_pic2(nicklogo_res, img, mode["nicklogo"]["position"])#合成2
                img = self.write_text(img, text, mode["text"], nickname, mode["nickname"])#写文本
                timemark2 = str(round(time.time() * 1000))
                img.save(os.path.join(timemark4,timemark2+'.jpg'), quality=100)
                del img
                return timemark2



        def web_upload(self):
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
                sel.find_element_by_id("accounts180").click()#有的时候一些元素会灰掉，无法选择，记得注释掉，比如这个百度号
                sel.find_element_by_id("accounts58").click()
                sel.find_element_by_id("accounts51").click()
                sel.find_element_by_id("accounts76").click()
                sel.find_element_by_id("accounts77").click()
                sel.find_element_by_id("accounts178").click()
                flp = open("视频标封.txt")
                title_text = flp.read()
                title_str = re.findall(r'标题1(.*?)\s',title_text)[0]
                elem_input_microvideotitle = sel.find_element_by_xpath('//input[@placeholder="请输入节目名称（注：在美拍、秒拍等UGC平台中，该名称不显示）"]')
                elem_input_microvideotitle.send_keys(title_str)
                flpv = open("视频基本信息.txt")#有标签和简介，到时候还要自动填充时间上去，不过时间就不写入这个文本了
                video_tag = flpv.readline()
                video_intro = flpv.readline()
                print(video_tag,video_intro)
                elem_input_microvideotag = sel.find_element_by_id('input_center')
                elem_input_microvideotag.send_keys(video_tag)
                timemark = time.strftime('[%Y.%m.%d]\n',time.localtime(time.time()))
                elem_input_microvideoinform = sel.find_element_by_xpath('//textarea[@placeholder="请输入简介"]')
                elem_input_microvideoinform.send_keys(timemark+video_intro)
                time.sleep(1)
                sel.find_element_by_id("uploadBtn").click()
                os.system(r'C:\\python-spider-master\douyin\upload.exe')
                time.sleep(1)
                target = sel.find_element_by_class_name("unifine_label")
                sel.execute_script("arguments[0].scrollIntoView();", target)
                time.sleep(1)
                sel.find_element_by_xpath('//div[@class="demo-upload-list-icon"]').click()
                os.system(r'C:\\python-spider-master\douyin\upload_bg.exe')
                time.sleep(2)
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




        def hello(self):
                """
                打印欢迎界面
                Parameters:
                        None
                Returns:
                        None
                """
                print('*' * 100)
                print('\t\t\t\t抖音App视频下载小助手')
                print('\t\t作者:Jack Cui、steven7851')
                print('*' * 100)


if __name__ == '__main__':
        douyin = DouYin()
        douyin.run()
