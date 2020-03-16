# crawler
爬虫集合

# carModel 
使用线程池抓取车型， 通过车辆型号查询车辆信息  
 https://www.cn357.com

# vehicleEmissions
爬取车辆的工况、排量、型号、通用名称等信息爬取  
http://www.miit.gov.cn/asopCmsSearch/n2282/index.html?searchId=qcppcx

# vehicleModel
使用scrapy小试牛刀，爬取易车网车型对应的价格等  
http://car.bitauto.com/charlist.html

# 汽车vin判断是否正确以及可能对应的品牌车型
- brand.py      vin对应的品牌、车辆型号等 (使用selenium爬取)  http://www.chinacar.com.cn/vin_index.html
- verify.py     检验vin是否正确