# mblog
经过漫长的备案，网线总算是上线了，接下来应该是各种小修小补，力求完善功能和增强体验。
我的个人技术博客：<http://www.qiangtaoli.com/>

一个用python3.5.1实现的个人博客网站，内含自己实现的简易版ORM框架和Web框架，欢迎查看学习。如果喜欢的话，可以点击右上角的Star按钮支持下我的工作^_^

基本按照[廖雪峰的python3教程](http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/001432170876125c96f6cc10717484baea0c6da9bee2be4000)实战部分来编写，经过不少简化或重构而成（基本上看不懂的地方最后弄明白再改写了），欢迎发起pull request来完善注释和功能。

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
- 把前端迁移到Bootstrap框架，全面支持响应式布局  
- 因为js的数据处理和前端绑定，js代码估计也需要修改，然而我还未学过javaScript  
- <s>将来肯定要支持代码高亮的</s>  
- 数据库可迁移也是要弄的  

### 支持代码高亮
- <s>只支持python代码的高亮。</s>  
- <s>现在好像还没有支持python3.5的新语法，我也不知道为什么，明明在pygments官网示范是支持的。</s>   
- <s>只支持区块代码的高亮，markdown默认区块代码是前面四个空格。</s> 
- 支持html语法高亮，代码需要以`<`开头  
- 支持javascript语法高亮，代码需要以`var`或`function`或`$`开头  
- 支持python3语法高亮，默认就是python3的解析器
- 支持php语法高亮，代码需要以`<?php`开头
- 支持大部分语言的代码高亮，需要用<kbd>\`\`\`(lang)\n(code)\n\`\`\`</kbd>包裹
