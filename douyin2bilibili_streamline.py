# -*- coding:utf-8 -*-
from contextlib import closing
import requests, json, re, os, sys, random, pygame, shutil, cv2
from ipaddress import ip_address
from subprocess import Popen, PIPE
from moviepy.editor import VideoFileClip
import urllib, math
import time
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

            "nicklogo":{#头像属性
                "frame":160,#大小
                "position":(106,727),#位置
            },
            
            
            "nickname":[{#昵称属性
                "size":45,#字号
                "ttf":"GBK.ttf",#字体
                "color":"",#颜色
                "position":(120,940),
                "frame":(500,20),
            },],
            "text":[{#文本框属性
                "size":40,#字号
                "ttf":"GBK.ttf",#字体
                "color":"",#颜色
                "position":(113,400),
                "frame":(400,20),
            },{
                "size":40,
                "ttf":"GBK.ttf",
                "color":"",
                "position":(113,460),
                "frame":(400,20),
            },{
                "size":40,
                "ttf":"GBK.ttf",
                "color":"",
                "position":(113,520),
                "frame":(400,20),
            },{
                "size":40,
                "ttf":"GBK.ttf",
                "color":"",
                "position":(113,580),
                "frame":(400,20),
            },{
                "size":40,
                "ttf":"GBK.ttf",
                "color":"",
                "position":(113,640),
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



        def parse_douyin(self, url):
                flag = 0
                headers = {
                        'User-Agent': 'Aweme/2.7.0 (iPhone; iOS 11.0; Scale/2.00)'
                }
                r = requests.get(url, allow_redirects=True)
                redirecturl = r.url
                rct = requests.get(redirecturl, headers=headers)


                playurl = re.findall('playAddr:(.*?)\,', str(rct.text))[0]

                if(playurl == ' ""'):
                        flag = 1
                        return 'www', 'www', 'www', 'www', flag
                              
                playurl = playurl.replace('playwm', 'play')
                playurl = playurl.replace("\"", "")
                try:
                        share_desc = re.findall('<p class="desc">(.*?)\</p>', str(rct.text))[0]
                except:
                        share_desc ="这个人懒死了，什么也没写！"
                        
                        
                nickname = re.findall('<p class="name nowrap">(.*?)\</p>', str(rct.text))[0]
                nicklogo = re.findall('fl"><img src="(.*?)\" a', str(rct.text))[0]
                nicklogo = nicklogo.replace('100x100','200x200')
                if os.name == 'nt':
                                for c in r'\/:*?"<>|':
                                        nickname = nickname.replace(c, '').strip().strip('\.')
                                        share_desc = share_desc.replace(c, '').strip()
                                for c in r' ':
                                        nickname = nickname.replace(c, '_').strip().strip('\.')
                                        share_desc = share_desc.replace(c, '_').strip()
                #title_bg_url2 = re.findall('"og:image" content="(.*?)">', str(rct.text))[0]
                print('\n')
                
                return share_desc, playurl, nickname, nicklogo, flag

        
                
                

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
                        download_url = video_url
                # 无水印视频
                else:
                        download_url = video_url.replace('playwm', 'play')

                return download_url

        def video_downloader(self, video_url, video_name):
                size = 0
                with closing(requests.get(video_url, headers=self.headers, stream=True)) as response:
                        chunk_size = 1024
                        
                        content_size = int(response.headers['content-length'])
                        
                        if response.status_code == 200:
                                sys.stdout.write('  [文件大小]:%0.2f MB\n' % (content_size / chunk_size / 1024))

                                with open(video_name+'.mp4', 'wb') as file:
                                        for data in response.iter_content(chunk_size = chunk_size):
                                                file.write(data)
                                                size += len(data)
                                                file.flush()

                                                #sys.stdout.write('  [下载进度]:%.2f%%\n' % float(size / content_size * 100) + '\r')
                                                sys.stdout.flush()
                                                
        def tran_single(self, timemark2, timemark3, timemark):
                input = os.path.join(timemark,timemark3)
                background = os.path.join(timemark,timemark2)
                output = os.path.join(timemark,"Fragment_"+timemark2)#w宽 h高
                cap=cv2.VideoCapture(input+'.mp4')
                w = cap.get(3)
                h = cap.get(4)

                height = math.ceil(608*h/w)
                if(height>1080):
                        height = 1080
                        
                str_height = str(height)
                finishcode = "ffmpeg -i "+input+".mp4"+" -i "+background+".jpg"+" -filter_complex [0:v]scale=608:"+str_height+"[video1];[1:v][video1]overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/2 -s 1920*1080 -y "+output+".mp4"#209，记得补充判断信息
                os.system(finishcode)
                #os.remove(input+".mp4")
                os.remove(background+".jpg")


        def tran_all(self, timemark):
                list_txt = os.path.join(timemark,"list")
                finishcode2 = "ffmpeg -f concat -i "+list_txt+".txt"+" -c copy "+"output.mp4"
                os.system(finishcode2)
                

        def run(self):
                
                self.hello()
                timemark = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
                os.mkdir(timemark)

                
                f = open("视频列表.txt")
                fl = open(os.path.join(timemark,'list.txt'),'w+')

                
                file_text = f.read()
                digi_str = re.findall(r'http://v.douyin.com/.*?\/',file_text)         
                i=0
                j=0
                k=0
                for j in range(len(digi_str)):
                        #print (digi_str+'\n')
                        share_url = digi_str[i]
                        i=i+1
                        print('自动填写短链接ing:\n')
                        print(share_url+'\n')
                        video_name, video_url, nickname, nicklogo, flag = self.parse_douyin(share_url)
                        if(flag == 0):
                                print('视频下载中!\n')
                                print('  解析视频链接中，请稍后!\n')
                                if '\\' in video_name:
                                        video_name = video_name.replace('\\', '')
                                elif '/' in video_name:
                                        video_name = video_name.replace('/', '')
                                else:
                                        video_name = video_name
                                if os.path.isfile(os.path.join(timemark,video_name+'.mp4')):
                                        print('视频已存在')
                                else:
                                        timemark3 = str(round(time.time() * 1000))
                                        self.video_downloader(video_url, os.path.join(timemark,timemark3))
                                        print('\n')
                                print('下载完成!\n')
                                timemark2 = self.make_pic(backMode, nickname, video_name, share_url, nicklogo, timemark)
                                self.tran_single(timemark2, timemark3, timemark)
                                var = 'file '+timemark+'/Fragment_'+timemark2+'.mp4'
                                fl.writelines(var)
                                fl.write('\n')
                                k=k+1
                                if(k == 1):
                                        title_num = os.path.join('./'+timemark,'01.jpg')
                                        self.title_single(timemark, timemark3, title_num)

                                if(k == 2):
                                        title_num = os.path.join('./'+timemark,'02.jpg')
                                        self.title_single(timemark, timemark3, title_num)
                                        
                                if(k == 3):
                                        title_num = os.path.join('./'+timemark,'03.jpg')
                                        self.title_single(timemark, timemark3, title_num)


                                  
                self.get_title_bg(timemark)

                f.close()
                fl.close()
                self.tran_all(timemark)
                filepath_0 = os.path.join(timemark)#确定TEMP目录
                shutil.rmtree(filepath_0)#执行删除目录操作
                self.web_upload()
                shutil.move(os.path.join('output.mp4'),os.path.join('video_temp',timemark+'.mp4'))#执行将视频移动到video_temp的操作
                



        def com_pic(self, topimg, backimg, position):#合并图片1
                nodeA = position
                w, h = topimg.size 
                nodeB = (position[0]+w, position[1]+h)
                backimg.paste(topimg, (nodeA[0], nodeA[1], nodeB[0], nodeB[1]))
                return backimg
        def com_pic2(self, topimg, backimg, position, frame):#合并图片2
                nodeA = position
                
                topimg = topimg.resize((frame,frame),Image.ANTIALIAS)
                w, h = topimg.size
                nodeB = (position[0]+w, position[1]+h)
                backimg.paste(topimg, (nodeA[0], nodeA[1], nodeB[0], nodeB[1]))
                return backimg

        def com_pic3(self, img, img_b, img_left, img_right):#合并图片3，这个是处理封面的，待优化


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
                if(re_fg_w<=800):
                        flag = True
                        img = self.com_pic4(img_left, img, flag, fg_pointx)
                        flag = False
                        img = self.com_pic4(img_right, img, flag, fg_pointx)
                
                img.paste(img2, (fg_pointx,fg_pointy,fg_pointx+re_fg_w,fg_pointy+re_fg_h))#拼合
                r,g,b,a = img_b.split()
                img.paste(img_b, (698,725,1204,1050),mask = a)
                img.save(os.path.join('bak_img'+'.jpg'), quality=100)

        def com_pic4(self, img_side, img, flag, pointx):
                w, h = img_side.size
                if(w>=h*pointx/1080):
                        bg_w=math.ceil(1080*w/h)
                        bg_h=1080
                else:
                        bg_w=pointx
                        bg_h=math.ceil(pointx*h/w)
                        
                img_side = img_side.resize((bg_w,bg_h),Image.ANTIALIAS)#把原图处理成填充图

                bg_pointx = int((bg_w-pointx)/2)
                bg_pointy = int((bg_h-1080)/2)
                img_side = img_side.crop([bg_pointx,bg_pointy,bg_pointx+pointx,bg_pointy+1080])#裁切填充图
                
                if(flag == True):
                        img.paste(img_side, (0,0,pointx,1080))#拼合
                else:
                        img.paste(img_side, (1920-pointx,0,1920,1080))#拼合

                return img

        def title_single(self, timemark, timemark3, title_num):
                
                pathIn = os.path.join(timemark,timemark3)+'.mp4'
                clip = VideoFileClip(pathIn)
                sec = int(clip.duration/2)
                clip.close()
                fin = 'ffmpeg -i '+pathIn+' -y -f image2 -ss '+str(sec)+' -vframes 1 '+title_num
                os.system(fin)
        

        def get_title_bg(self, timemark):
                #输入三图，输出title_bg.jpg到目录，执行完毕后记得删除，视频移动到tmp文件夹，但封面图还是删了吧。
                #这个是用来合成的，但三图的话，单个图片还是需要另行处理的，我把它放到了title_single。
                self.change_size(os.path.join(timemark,'01.jpg'))
                
                title_bg_res1 = Image.open(os.path.join(timemark,'01.jpg'))

                title_bg_res2 = Image.open('background_logo.png')

                self.change_size(os.path.join(timemark,'02.jpg'))

                title_bg_left = Image.open(os.path.join(timemark,'02.jpg'))

                self.change_size(os.path.join(timemark,'03.jpg'))

                title_bg_right = Image.open(os.path.join(timemark,'03.jpg'))

                self.com_pic3(title_bg_res1, title_bg_res2, title_bg_left, title_bg_right)#合成3，输入原始图片，输出处理好的封面图


        def change_size(self, read_file):
                image=cv2.imread(read_file,1)
                b=cv2.threshold(image,25,255,cv2.THRESH_BINARY)          #调整裁剪效果
                binary_image=b[1]               #二值图--具有三通道
                binary_image=cv2.cvtColor(binary_image,cv2.COLOR_BGR2GRAY)
                print(binary_image.shape)       #改为单通道

                x=binary_image.shape[0]
                print("高度x=",x)
                y=binary_image.shape[1]
                print("宽度y=",y)
                edges_x=[]
                edges_y=[]

                for i in range(x):
                        for j in range(y):
                                if binary_image[i][j]==255:
                                # print("横坐标",i)
                                # print("纵坐标",j)
                                        edges_x.append(i)
                                        edges_y.append(j)

                left=min(edges_x)               #左边界
                right=max(edges_x)              #右边界
                width=right-left                #宽度

                bottom=min(edges_y)             #底部
                top=max(edges_y)                #顶部
                height=top-bottom               #高度

                pre1_picture=image[left:left+width,bottom:bottom+height]        #图片截取

                cv2.imwrite(read_file, pre1_picture)


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
         
         
        def make_pic(self, mode, nickname, text, url, nicklogo, timemark):
                img = Image.open(mode["back_url"])#读取背景图片
                
                response_img = requests.get(nicklogo)
                try:
                        nicklogo_res = Image.open(BytesIO(response_img.content))
                except:
                        nicklogo_res = Image.open('noface.jpg')
                img = self.com_pic2(nicklogo_res, img, mode["nicklogo"]["position"], mode["nicklogo"]["frame"])#合成2
                img = self.write_text(img, text, mode["text"], nickname, mode["nickname"])#写文本
                timemark2 = str(round(time.time() * 1000))
                img.save(os.path.join(timemark,timemark2+'.jpg'), quality=100)
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
                
                """
                print('*' * 100)
                print('\t\t\t\t抖音视频下载合成小助手')
                print('\t\t原作者:Jack Cui、steven7851')
                print('\t\t移植:同和君Hocassian')
                print('*' * 100)


if __name__ == '__main__':
        douyin = DouYin()
        douyin.run()
