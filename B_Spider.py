

import requests
import json
import time
import csv
import random
import math

class B_Spider:
    def get_video_data(self,bvid):
        headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
        }
        u5='https://api.bilibili.com/x/web-interface/archive/stat?bvid={}'.format(bvid)
        rep=requests.get(u5,headers=headers,timeout=3)
        rj=rep.json()
        data=rj['data']
        rdata ={
            'time':     int(time.time()),   # 时间戳
            'view':     data["view"],       # 播放量
            'like':     data['like'],       # 点赞
            'coin':     data["coin"],       # 硬币数
            'favorite': data["favorite"],   # 收藏数
            'danmaku':  data["danmaku"],    # 弹幕数
            'reply':    data["reply"],      # 评论数
            'share':    data["share"],      # 分享数
        }
        return rdata   
    
    def get_user_st(self,uid):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
            "cookie":"SESSDATA=a21d9944%2C1661079016%2C7a55a%2A21; "
        }
        u6=f'https://api.bilibili.com/x/relation/stat?vmid={uid}&jsonp=jsonp'
        rep=requests.get(u6,headers=headers,timeout=3)
        data=rep.json()['data']
        rdata={
            'time':int(time.time()),
            'follower':data['follower'], #粉丝数
        }
        return rdata
    
    def get_user_video(self,uid):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
        }
        u6=f'https://api.bilibili.com/x/space/arc/search?mid={uid}&ps=30&tid=0&pn=1&keyword=&order=click&jsonp=jsonp'
        rep=requests.get(u6,headers=headers,timeout=3)
        data=rep.json()['data']
        page=math.ceil(data['page']['count']/30)
        rdatas=[]
        for i in range(page):
            u6=f'https://api.bilibili.com/x/space/arc/search?mid={uid}&ps=30&tid=0&pn={i+1}&keyword=&order=click&jsonp=jsonp'
            rep=requests.get(u6,headers=headers,timeout=3)
            data=rep.json()['data']['list']['vlist']
            time.sleep(random.random())
            for _ in data:
                rdata={}
                rdata['bvid']=_['bvid']
                rdata['title']=_['title']
                rdata['play']=_['play']
                rdata['video_review']=_['video_review'] #弹幕数
                rdata['comment']=_['comment']           #评论数
                rdatas.append(rdata)
        datas={
            'time':int(time.time()),
            'datas':rdatas
        }
        print(datas['time'],"抓取成功")
        return datas
    #爬取用户的所有投稿视频
    def run_3(self):
        uid=input("输入uid:")
        fr=int(input("爬取频率 s/次:"))
        datapath=uid+'_allvideo.csv'
        fieldnames=['time','datas']
        try:
            f=open(datapath)
            f.close()
        except FileNotFoundError:
            with open(datapath,'w',newline='') as f:
                writer=csv.DictWriter(f,fieldnames=fieldnames)
                writer.writeheader()
        while True:
            with open(datapath,'a',newline='') as f:
                writer=csv.DictWriter(f,fieldnames=fieldnames)
                time.sleep(fr+random.random()*2-1)
                data=self.get_user_video(uid=uid)
                writer.writerow(data)
    #爬取视频数据
    def run_1(self):
        
        bvid=input("输入BV号:")
        fr=int(input("爬取频率 s/次:"))
        datapath=bvid+'.csv'
        fieldnames=['time', 'view', 'like', 'coin', 'favorite', 'danmaku', 'reply', 'share']
        try:
            f=open(datapath)
            f.close()
        except FileNotFoundError:
            with open(datapath,'w',newline='') as f:
                writer=csv.DictWriter(f,fieldnames=fieldnames)
                writer.writeheader()
        while True:
            with open(datapath,'a',newline='') as f:
                writer=csv.DictWriter(f,fieldnames=fieldnames)
                time.sleep(fr+random.random()*2-1)
                data=self.get_video_data(bvid)
                writer.writerow(data)
                print(data)
    #爬取用户粉丝量
    def run_2(self):
        uid=input("输入uid:")
        fr=int(input("爬取频率 s/次:"))
        datapath=uid+'.csv'
        fieldnames=['time','follower']
        try:
            f=open(datapath)
            f.close()
        except FileNotFoundError:
            with open(datapath,'w',newline='') as f:
                writer=csv.DictWriter(f,fieldnames=fieldnames)
                writer.writeheader()
        while True:
            with open(datapath,'a',newline='') as f:
                writer=csv.DictWriter(f,fieldnames=fieldnames)
                time.sleep(fr+random.random()*2-1)
                data=self.get_user_st(uid=uid)
                writer.writerow(data)
                print(data)
# %%
op=int(input("爬取方式:\n1:爬取用户粉丝量\n2:爬取用户所有视频数据\n3:爬取视频数据\n"))
l=B_Spider()
if op==1:
    l.run_2()
elif op==2:
    l.run_3()
elif op==3:
    l.run_1()

