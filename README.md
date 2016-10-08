# mblog
经过漫长的备案，网线总算是上线了，接下来应该是各种小修小补，力求完善功能和增强体验。
我的个人技术博客：<http://www.qiangtaoli.com/>

一个用python3.5.1实现的个人博客网站，内含自己实现的简易版ORM框架和Web框架，欢迎查看学习。如果喜欢的话，可以点击右上角的Star按钮支持下我^_^

用Flask重建过后端，只花了一周的时间，感叹Flask这个轻框架的结构真的是太优雅了！基本上是无痛切换，如果你想深入学习MVC框架，那你最好也看一下我用Flask框架实现的[mblog-Flask](https://github.com/moling3650/mblog-Flask)，你会对整个框架的架构有更深的体会的。

此博客基本按照[廖雪峰的python3教程](http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/001432170876125c96f6cc10717484baea0c6da9bee2be4000)实战部分来编写，经过不少简化或重构而成（基本上看不懂的地方最后弄明白再改写了），欢迎发起pull request来完善注释和功能。

## HTTP请求的生命周期
![项目流程图](https://github.com/moling3650/mblog/blob/master/www/app/static/img/Process.png)

1. 客户端（浏览器）发起请求  
2. 路由分发请求（这个框架自动帮处理），add_routes函数就是注册路由。  
3. 中间件预处理  
   - 打印日志
   - 验证用户登陆
   - 收集Request（请求）的数据
4. RequestHandler清理参数并调用控制器（Django和Flask把这些处理请求的控制器称为view functions）
5. 控制器做相关的逻辑判断，有必要时通过ORM框架处理Model的事务。
6. 模型层的主要事务是数据库的查增改删。
7. 控制器再次接管控制权，返回相应的数据。
8. Response_factory根据控制器传过来的数据产生不同的响应。
9. 客户端（浏览器）接收到来自服务器的响应。

## 添加更新日志  
直到现在才发现有需要写一个更新日志...orz  
最近在学习前端，更新应该还是很频繁的。
[点我查看更新](https://github.com/moling3650/mblog/blob/master/CHANGELOG.md)

##准备工作
请确保你已经安装以下的库

1. python3.5 及以上版本

1. aiohttp: 支持异步http服务器

1. jinja2: python的模板引擎

1. aiomysql: aiomysql针对asyncio框架用于访问mysql的库

1. Pygments：用于实现网页代码高亮的库

1. mistune: 将文本markdown化，结合Pygments可以精确高亮绝大多数编程语言

所有的库都可以通过pip安装，或者更方便地使用`pip install -r requirements.txt`命令来安装。



###项目结构

    mblog/                    <--根目录
    |
    +-conf/                   <--服务器配置目录
    |
    +-db_init/                <--数据库初始化文件目录
    |
    +-log/                    <--服务器日志目录
    |
    +-www/                    <--web项目目录
    	|
		+-config/             <--项目配置目录
		|
		+-app/                <--app目录
		|	|
		|	+-frame/          <--web和orm框架
		|	|
		|	+-static/          <--静态文件
		|	|
		|	+-templates/       <--模板文件
		|	|
		|	+__init__.py       <--app初始化
		|	|
		|	+factorys.py       <--工厂函数
		|	|
		|	+models.py         <--模型（数据库的表）
		|	|
		|	+-route.py         <--路由
		|   |
		|   +-api.py       　　<-- api接口
		|
		orm_test.py           <--测试orm
		|
		pymonitor.py          <--监视器
		|
		run.py                <--主运行文件
		

### 项目近况（Todo list）  
- 把前端迁移到Bootstrap框架，全面支持响应式布局  （达成）
- 因为js的数据处理和前端绑定，js代码估计也需要修改，然而我还未学过javaScript  （达成）
- 将来肯定要支持代码高亮的  （达成）
- 数据库可迁移也是要弄的  （0%）
- 编写更安全更可扩展的Restful api v2 （75%）
- 添加Aboat me页面 （0%）
- 添加测试功能  （0%）


### 支持代码高亮
- <s>只支持python代码的高亮。</s>  
- <s>现在好像还没有支持python3.5的新语法，我也不知道为什么，明明在pygments官网示范是支持的。</s>   
- <s>只支持区块代码的高亮，markdown默认区块代码是前面四个空格。</s> 
- 支持html语法高亮，代码需要以`<`开头  
- 支持javascript语法高亮，代码需要以`var`或`function`或`$`开头  
- 支持python3语法高亮，默认就是python3的解析器
- 支持php语法高亮，代码需要以`<?php`开头
- 支持大部分语言的代码高亮，需要用<kbd>\`\`\`(lang)\n(code)\n\`\`\`</kbd>包裹
