# scrapy框架

+ 安装 pip install scrapy

+ 常用命令
>创建项目：scrapy startproject xxx  
进入项目：cd xxx #进入某个文件夹下  
创建爬虫：scrapy genspider xxx（爬虫名） xxx.com （爬取域）  
生成文件：scrapy crawl xxx -o xxx.json (生成某种类型的文件)  
运行爬虫：scrapy crawl XXX  
列出所有爬虫：scrapy list  
获得配置信息：scrapy settings [options]  

>1.scrapy startproject vehicle_model
>> 创建的文件
scrapy.cfg: 项目的配置文件  
vehicle_model/: 该项目的python模块。在此放入代码（核心）  
vehicle_model/items.py: 项目中的item文件.（这是创建容器的地方，爬取的信息分别放到不同容器里）  
vehicle_model/middlewares.py: 项目中的中间件文件. 
vehicle_model/pipelines.py: 项目中的pipelines文件.  
vehicle_model/settings.py: 项目的设置文件.（我用到的设置一下基础参数，比如加个文件头，设置一个编码）  
vehicle_model/spiders/: 放置spider代码的目录. （放爬虫的地方）  


>2 启动爬虫
>> cd 爬虫路径  
scrapy crawl vehicleModel