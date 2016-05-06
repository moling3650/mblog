# mblog
-------
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
		|	+static/          <--静态文件
		|	|
		|	+templates/       <--模板文件
		|	|
		|	__init__.py       <--app初始化
		|	|
		|	factorys.py       <--工厂函数
		|	|
		|	models.py         <--模型（数据库的表）
		|	|
		|	routes.py         <--路由
		|
		orm_test.py           <--测试orm
		|
		pymonitor.py          <--监视器
		|
		run.py                <--主运行文件
