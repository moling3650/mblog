# mblog
[演示站点](http://119.29.191.109/)

一个用python3.5.1实现的个人博客网站，内含自己实现的简易版ORM框架和Web框架，欢迎查看学习。如果喜欢的话，可以点击右上角的Star按钮支持下我的工作^_^

基本按照[廖雪峰的python3教程](http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/001432170876125c96f6cc10717484baea0c6da9bee2be4000)实战部分来编写，经过不少简化或重构而成（基本上看不懂的地方最后弄明白再改写了），欢迎发起pull request来完善注释和功能。

##准备工作
请确保你已经安装以下的库

1. python3.5 及以上版本

1. aiohttp: 支持异步http服务器

1. jinja2: python的模板引擎

1. aiomysql: aiomysql针对asyncio框架用于访问mysql的库

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
		|	+-routes.py         <--路由
		|
		orm_test.py           <--测试orm
		|
		pymonitor.py          <--监视器
		|
		run.py                <--主运行文件
## 难点讲解  
* ORM  
我相信大多数新手遇到的第一道坎就是ORM（Object Relational Mapping），虽然不太了解ORM，但python的`dict`还是知道的吧，`dict`本身就是一种对象关系映射。
还有这里面涉及数据库的操作，而大多数初次写web程序的人都是都是不太了解SQL(Structured Query Language)。所以大多数人就卡在这里了。
	1.  ORM，说白了就是一个名字=>列对象的字典，想通过某一个名字就能找相对的值，所在ModelMetaclass中第一任务就是生成一个关系对应映射，以便在以后每个创建的类中都会自动生成一张关系对应表，代码里的`attrs['__mappings__']`就是这样的一个东西。
	2.  SQL，除`attrs['__mappings__']`以外的新建属性都是为SQL操作存在的。
		- `attrs['__table__']`： 在某一数据库中的表名
		- `attrs['__primary_key__']`： 在某张表中的主键（主键都是唯一的，通常作为查询的依据
		- `attrs['__select__']`： SQL的查询语句，例如 `SELECT * FROM (%table) WHERE (%s) ORDERBY (%s) LIMIT (%s)` (WHERE:条件限定，ORDERBY：排序方法，LIMIT：查询位置与个数，这三个都是可选的参数而已）
		- `attrs['__insert__']`： SQL的插入语句，例如 `INSERT INTO (%table) (%keys) VALUES (%values)`，刚才创建的`attrs['__mappings__']`就可以发挥它作用了，`keys`和`values`都是`attrs['__mappings__']`这个字典的属性
		- `attrs['__update__']`： SQL的更改语句，例如`UPDATE (%table) SET (% keys = new values) WHERE (% condition)`，WHERE并不是必须的，但没有条件限制的话，一个表所有内容都会被更改了，所以一般情况下是只改某一处，条件当然就是独一无二的主键匹配了
		- `attrs['__delete__']`： SQL的删除语句，如果`DELETE FROM (%table) WHERE (%condition)`，`condition`可以是多变的，但这里只考虑删除某一特定的对象，所以通常是用`(%primary_key) = ?`来限定唯一的删除对象