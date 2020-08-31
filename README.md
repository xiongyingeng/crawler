# crawler
爬虫集合

## carModel 
使用线程池抓取车型， 通过车辆型号查询车辆信息  
 https://www.cn357.com

## vehicleEmissions
爬取车辆的工况、排量、型号、通用名称等信息爬取  
http://www.miit.gov.cn/asopCmsSearch/n2282/index.html?searchId=qcppcx

## vehicleModel
使用scrapy小试牛刀，爬取易车网车型对应的价格等  
http://car.bitauto.com/charlist.html

## vinMatch 
汽车vin判断是否正确以及可能对应的品牌车型
- brand.py      vin对应的品牌、车辆型号等 (使用selenium爬取)  http://www.chinacar.com.cn/vin_index.html
- verify.py     检验vin是否正确、以及对应的VIN年份

## vin2Model
汽车vin对应的品牌、车型、年份、底盘等（网站有限制)
- vinToModel.py   爬取http://www.fenco.cn/Index/search.html?

## cn357_notice
商车网汽车公众型号 https://www.cn357.com/notice_list/
notcie_list_multithreading.py -- 多线程处理
notice_list.py -- 单线程处理

