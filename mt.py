# -*- coding: utf-8 -*-
"""
//更新时间：2023/5/13
//作者：wdvipa
//支持青龙和actions定时执行
//使用方法：创建变量 名字：mt 内容的写法：账号|密码  多个账号用回车键隔开
//例如: 
111|1111
222|2222
//更新内容：加入已签到判断，修复因"补签"无法匹配导致报错行
//如需推送将需要的推送写入变量mt_fs即可多个用&隔开
如:变量内输入push需再添加mt_push变量 内容是push的token即可
"""
import requests
import os
import time
import re
import json

requests.urllib3.disable_warnings()

#------------------设置-------------------
UserAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'

#初始化环境变量开头
cs = 0
ZData = "5"
ttoken = ""
tuserid = ""
push_token = ""
SKey = ""
QKey = ""
ktkey = ""
msgs = ""
datas = ""
message = ""
#检测推送
if cs == 1:
  if "cs_mt" in os.environ:
    datas = os.environ.get("cs_mt")
  else:
    print('您没有输入任何信息')
    exit
elif cs == 2:
    datas =""
else:
  if "mt_fs" in os.environ:
    fs = os.environ.get('mt_fs')
    fss = fs.split("&")
    if("tel" in fss):
        if "mt_telkey" in os.environ:
            telekey = os.environ.get("mt_telkey")
            telekeys = telekey.split('\n')
            ttoken = telekeys[0]
            tuserid = telekeys[1]
    if("qm" in fss):
        if "mt_qkey" in os.environ:
            QKey = os.environ.get("mt_qkey")
    if("stb" in fss):
        if "mt_skey" in os.environ:
            SKey = os.environ.get("mt_skey")
    if("push" in fss):
        if "mt_push" in os.environ:
            push_token = os.environ.get("mt_push")
    if("kt" in fss):
        if "mt_ktkey" in os.environ:
            ktkey = os.environ.get("mt_ktkey")
  if "mt" in os.environ:
    datas = os.environ.get("mt")
  else:
    print('您没有输入任何信息')
    exit
groups = datas.split('\n')
#初始化环境变量结尾

class mtanelQd(object):
    def __init__(self,username,password):
        # 账号密码
        self.username = username
        self.password = password
        ##############推送渠道配置区###############
        # 酷推qq推送
        #self.ktkey = ktkey
        # Telegram私聊推送
        self.tele_api_url = 'https://api.telegram.org'
        self.tele_bot_token = ttoken
        self.tele_user_id = tuserid
        ##########################################


    def sign(self,msgs):  # 签到
        headers = {'User-Agent': UserAgent}
        # 获取登陆所需loginhash和formhash
        Hashurl = 'https://bbs.binmt.cc/member.php?mod=logging&action=login&infloat=yes&handlekey=login&inajax=1&ajaxtarget=fwin_content_login'
        session.get(headers=headers, url=Hashurl)
        time.sleep(5)
        headers['referer']=Hashurl
        text = session.get(headers=headers, url=Hashurl).text
        loginhash = re.findall('loginhash=(.*?)">', text, re.S)[0]
        formhash = re.findall('formhash" value="(.*?)".*? />', text, re.S)[0]
        # 模拟登陆
        loginurl = 'https://bbs.binmt.cc/member.php?mod=logging&action=login&loginsubmit=yes&handlekey=login&loginhash=' + loginhash + '&inajax=1'
        data = {
            'formhash': formhash,
            'referer': 'https://bbs.binmt.cc/index.php',
            'loginfield': 'username',
            'username': self.username,
            'password': self.password,
            'questionid': '0',
            'answer': '',
        }
        text1 = session.post(headers=headers, url=loginurl, data=data).text
        # print(page_text1)
        # 验证是否登陆成功
        check = re.findall('root', text1, re.S)
        if (len(check) != 0):
            print('登录成功')
            # 获取签到所需的formhash
            getHashurl = 'https://bbs.binmt.cc/k_misign-sign.html'
            page_text = session.get(headers=headers, url=getHashurl).text
            form = re.findall('formhash" value="(.*?)".*? />', page_text, re.S)[0]
            # 模拟签到
            sign_url = 'https://bbs.binmt.cc/plugin.php?id=k_misign:sign&operation=qiandao&format=text&formhash=' + form
            page_text2 = session.get(headers=headers, url=sign_url).text
            # 验证是否签到成功
            check = re.findall('<root><(.*?)</root>', page_text2, re.S)
            if (len(check) != 0):
                print(f'签到详情：{check}')
                if ("今日已签" in str(check)):
                    jg="今天已经签到过了~"
                    print('今天已经签到过了~')
                elif ("已签到" in str(check)):
                    jg="今天已经签到过了~"
                    print('今天已经签到过了~')
                else:
                    jg="签到成功~"
                    print('签到成功')
                xx = session.get(headers=headers, url=getHashurl).text
                jib = re.findall('积分奖励</h4>.*?></span>',xx,re.S)
                lxb = re.findall('<h4>连续签到.*?></span>',xx,re.S)
                djb = re.findall('签到等级</h4>.*?></span>',xx,re.S)
                ztsb = re.findall('签到等级</h4>.*?></span>',xx,re.S)
                name = re.findall('<div id="comiis_key".*?<span>(.*?)</span>.*?</div>', xx, re.S)[0]
                lx = re.findall('value="(.*?)"',str(lxb))[0]
                jb = re.findall('value="(.*?)"',str(jib))[0]
                dj = re.findall('value="(.*?)"',str(djb))[0]
                dj = re.findall('value="(.*?)"',str(djb))[0]
                zts = re.findall('value="(.*?)"',str(ztsb))[0]
                pm = re.findall('签到排名：(.*?)</div>',xx)[0]
                try:
                    #print(f"昵称：{name}\n签到排名：{pm}\n连续签到：{lx}天\n签到等级：LV.{dj}\n获得金币：{jb}\n总天数：{zts}天")
                    message = '''⏰当前时间：{} 
        MT论坛签到
    ####################
    账号昵称：{}
    签到排名：{}
    连续签到：{}天
    签到等级：LV.{}
    获得金币：{}
    总天数：{}天
    签到结果：签到成功
    ####################
    祝您过上美好的一天！'''.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + 28800)),name,pm,lx,dj,jb,zts)
                    print(message)
                    msgs = msgs + '\n' + message
                except:
                    print("获取信息失败")
                    msgs = msgs + '\n' + "获取信息失败"
            else:
                print('签到失败')
                msgs = msgs + '\n' + '签到失败'
        else:
            print('登陆失败')
            msgs = msgs + '\n' + "登录失败"

        return msgs

    
    # Qmsg私聊推送
    def Qmsg_send(msg):
        if QKey == '':
            return
        qmsg_url = 'https://qmsg.zendee.cn/send/' + str(QKey)
        data = {
            'msg': msg,
        }
        requests.post(qmsg_url, data=data)

    # Server酱推送
    def server_send(self, msg):
        if SKey == '':
            return
        server_url = "https://sctapi.ftqq.com/" + str(SKey) + ".send"
        data = {
            'text': self.name + "MT论坛签到通知",
            'desp': msg
        }
        requests.post(server_url, data=data)

    # 酷推QQ推送
    def kt_send(msg):
        if ktkey == '':
            return
        kt_url = 'https://push.xuthus.cc/send/' + str(ktkey)
        data = ('MT论坛签到完成，点击查看详细信息~\n' + str(msg)).encode("utf-8")
        requests.post(kt_url, data=data)

    #Telegram私聊推送
    def tele_send(self, msg: str):
        if self.tele_bot_token == '':
            return
        tele_url = f"{self.tele_api_url}/bot{self.tele_bot_token}/sendMessage"
        data = {
            'chat_id': self.tele_user_id,
            'parse_mode': "Markdown",
            'text': msg
        }
        requests.post(tele_url, data=data)
        
    # Pushplus推送
    def pushplus_send(msg):
        if push_token == '':
            return
        token = push_token
        title= 'MT论坛签到通知'
        content = msg
        url = 'http://www.pushplus.plus/send'
        data = {
            "token":token,
            "title":title,
            "content":content
            }
        body=json.dumps(data).encode(encoding='utf-8')
        headers = {'Content-Type':'application/json'}
        re = requests.post(url,data=body,headers=headers)
        print(re.status_code)


    def main(self):
        global msgs
        msgs = msgs + self.sign(msgs)

if __name__ == '__main__':  # 直接运行和青龙入口
  i = 0
  n = 0
  print("已设置不显示账号密码等信息")
  while i < len(groups):
    n = n + 1
    group = groups[i]
    profile = group.split('|')
    username = profile[0]
    password = profile[1]
    msgs = msgs + "第" + str(n) + "个用户的签到结果"
    print("第" + str(n) + "个用户开始签到")
    session = requests.session()
    session.headers = {
      'User-Agent': UserAgent,
    }
    run = mtanelQd(username,password)
    run.main()
    time.sleep(5)
    i += 1
  else:
    #mtanelQd.server_send( msgs )
    mtanelQd.kt_send( msgs )
    #mtanelQd.Qmsg_send(mtanelQd.name+"\n"+mtanelQd.email+"\n"+ msgs)
    #mtanelQd.tele_send(mtanelQd.name+"\n"+mtanelQd.email+"\n"+ msgs)
    mtanelQd.pushplus_send( msgs )
