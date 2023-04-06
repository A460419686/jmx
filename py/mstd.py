#coding=utf-8
#!/usr/bin/python
import sys
sys.path.append('..') 
from base.spider import Spider
import json
import time
import base64
import requests

class Spider(Spider):  # 元类 默认的元类 type
	def getName(self):
		return "美食天地"
	def init(self,extend=""):
		print("============{0}============".format(extend))
		pass
	def isVideoFormat(self,url):
		pass
	def manualVideoCheck(self):
		pass
	def homeContent(self,filter):
		result = {}
		cateManual = {
			"美食": "美食",
"披萨": "披萨",
"火锅": "火锅",
"烧烤": "烧烤",
"烤鱼": "烤鱼",
"海鲜": "海鲜",
"津菜": "津菜",
"川菜": "川菜",
"湘菜": "湘菜",
"鲁菜": "鲁菜",
"苏菜": "苏菜",
"闽菜": "闽菜",
"粤菜": "粤菜",
"东北菜": "东北菜",
"冀菜": "冀菜",
"豫菜": "豫菜",
"鄂菜": "鄂菜",
"本帮菜": "本帮菜",
"客家菜": "客家菜",
"赣菜": "赣菜",
"京菜": "京菜",
"浙菜": "浙菜",
"徽菜": "徽菜",
"湘菜": "湘菜",
"凉菜": "凉菜",
"蒸菜": "蒸菜",
"日料": "日料",
"点心": "点心",
"面食": "面食",
"汉堡": "汉堡",
"小吃": "小吃",
"素食": "素食",
"韩国菜": "韩国菜",
"泰国菜": "泰国菜",
"穆斯林菜": "穆斯林菜",
"土耳其菜系": "土耳其菜系",
"法国菜": "法国菜",
"意大利菜": "意大利菜",
"希腊菜": "希腊菜",
"德国菜": "德国菜",
"西班牙菜": "西班牙菜",
"阿拉伯菜": "阿拉伯菜",
"伊朗菜": "伊朗菜",
"中亚菜": "中亚菜",
"糖尿病菜": "糖尿病菜",
"早餐": "早餐"
		}
		classes = []
		for k in cateManual:
			classes.append({
				'type_name':k,
				'type_id':cateManual[k]
			})
		result['class'] = classes
		if(filter):
			result['filters'] = self.config['filter']
		return result
	def homeVideoContent(self):
		result = {
			'list':[]
		}
		return result
	cookies = ''
	def getCookie(self):
		cookies_str = self.fetch("https://agit.ai/138001380000/MHQTV/raw/branch/master/bbcookie.txt").text
		cookies_dic = dict([co.strip().split('=') for co in cookies_str.split(';')])
		rsp = requests.session()
		cookies_jar = requests.utils.cookiejar_from_dict(cookies_dic)
		rsp.cookies = cookies_jar
		content = self.fetch("http://api.bilibili.com/x/web-interface/nav", cookies=rsp.cookies)
		res = json.loads(content.text)
		if res["code"] == 0:
			self.cookies = rsp.cookies
		else:
			rsp = self.fetch("https://www.bilibili.com/")
			self.cookies = rsp.cookies
		return rsp.cookies
		
	def categoryContent(self,tid,pg,filter,extend):		
		result = {}
		url = 'https://api.bilibili.com/x/web-interface/search/type?search_type=video&keyword={0}&duration=4&page={1}'.format(tid,pg)
		if len(self.cookies) <= 0:
			self.getCookie()
		rsp = self.fetch(url,cookies=self.cookies)
		content = rsp.text
		jo = json.loads(content)
		if jo['code'] != 0:			
			rspRetry = self.fetch(url,cookies=self.getCookie())
			content = rspRetry.text		
		jo = json.loads(content)
		videos = []
		vodList = jo['data']['result']
		for vod in vodList:
			aid = str(vod['aid']).strip()
			title = vod['title'].strip().replace("<em class=\"keyword\">","").replace("</em>","")
			img = 'https:' + vod['pic'].strip()
			remark = str(vod['duration']).strip()
			videos.append({
				"vod_id":aid,
				"vod_name":title,
				"vod_pic":img,
				"vod_remarks":remark
			})
		result['list'] = videos
		result['page'] = pg
		result['pagecount'] = 9999
		result['limit'] = 90
		result['total'] = 999999
		return result
	def cleanSpace(self,str):
		return str.replace('\n','').replace('\t','').replace('\r','').replace(' ','')
	def detailContent(self,array):
		aid = array[0]
		url = "https://api.bilibili.com/x/web-interface/view?aid={0}".format(aid)

		rsp = self.fetch(url,headers=self.header)
		jRoot = json.loads(rsp.text)
		jo = jRoot['data']
		title = jo['title'].replace("<em class=\"keyword\">","").replace("</em>","")
		pic = jo['pic']
		desc = jo['desc']
		typeName = jo['tname']
		vod = {
			"vod_id":aid,
			"vod_name":title,
			"vod_pic":pic,
			"type_name":typeName,
			"vod_year":"",
			"vod_area":"",
			"vod_remarks":"",
			"vod_actor":"",
			"vod_director":"",
			"vod_content":desc
		}
		ja = jo['pages']
		playUrl = ''
		for tmpJo in ja:
			cid = tmpJo['cid']
			part = tmpJo['part']
			playUrl = playUrl + '{0}${1}_{2}#'.format(part,aid,cid)

		vod['vod_play_from'] = 'B站'
		vod['vod_play_url'] = playUrl

		result = {
			'list':[
				vod
			]
		}
		return result
	def searchContent(self,key,quick):
		result = {
			'list':[]
		}
		return result
	def playerContent(self,flag,id,vipFlags):
		# https://www.555dianying.cc/vodplay/static/js/playerconfig.js
		result = {}

		ids = id.split("_")
		url = 'https://api.bilibili.com:443/x/player/playurl?avid={0}&cid=%20%20{1}&qn=112'.format(ids[0],ids[1])
		rsp = self.fetch(url, cookies=self.cookies)
		jRoot = json.loads(rsp.text)
		jo = jRoot['data']
		ja = jo['durl']
		
		maxSize = -1
		position = -1
		for i in range(len(ja)):
			tmpJo = ja[i]
			if maxSize < int(tmpJo['size']):
				maxSize = int(tmpJo['size'])
				position = i

		url = ''
		if len(ja) > 0:
			if position == -1:
				position = 0
			url = ja[position]['url']

		result["parse"] = 0
		result["playUrl"] = ''
		result["url"] = url
		result["header"] = {
			"Referer":"https://www.bilibili.com",
			"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
		}
		result["contentType"] = 'video/x-flv'
		return result

	config = {
		"player": {},
		"filter": {}
	}
	header = {}

	def localProxy(self,param):
		return [200, "video/MP2T", action, ""]
