# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['httptesting',
 'httptesting.case',
 'httptesting.globalVar',
 'httptesting.library']

package_data = \
{'': ['*'], 'httptesting': ['config/*', 'template/*']}

install_requires = \
['colorama==0.4.1',
 'pytest-html==1.21.1',
 'pytest-repeat==0.8.0',
 'pytest-rerunfailures==7.0',
 'pytest-xdist==1.29.0',
 'pytest==5.0.1',
 'pyyaml==5.1.1',
 'requests-toolbelt==0.9.1',
 'requests==2.22.0']

entry_points = \
{'console_scripts': ['AM = HttpTesting.main:run_min',
                     'AMT = HttpTesting.main:run_min',
                     'am = HttpTesting.main:run_min',
                     'amt = HttpTesting.main:run_min']}

setup_kwargs = {
    'name': 'httptesting',
    'version': '1.1.71',
    'description': 'Httptesting HTTP(s) interface testing framework.',
    'long_description': '\ufeff# HttpTesting\n\n![PyPI](https://img.shields.io/pypi/v/Httptesting)\n![PyPI - License](https://img.shields.io/pypi/l/HttpTesting)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/HttpTesting)\n![PyPI - Wheel](https://img.shields.io/pypi/wheel/HttpTesting)\n\n\nHttpTesting 是HTTP(S)协议接口测试框架，通过YAML来编写测试用例，通过命令行运行代码，不固定目录结构，支持通过命令行生成脚手架。\n\n\n\n\n## 功能描述\nhttptesting通过YAML编写测试用例，安装httptesting后通过amt命令执行测试用例，支持指定YAML中CASE名称进行单用例执行，支持指定请求头默认值来共享请求头，支持自定义扩展功能(在case执行根目录下创建extfunc.py文件来自定义代码)。\n支持多进程执行用例，支持用例执行出错重试功能，支持设定执行用例次数；支持设置控制台输出和报告输出；支持参数化功能与用户自定义用户变量。\n\n\n### 安装包下载: \n[https://pypi.org/project/httptesting/#files](https://pypi.org/project/httptesting/#files)\n\n### 源码：\n[https://github.com/HttpTesting/pyhttp](https://github.com/HttpTesting/pyhttp)\n\n\n\n\n## 版本信息\n\n|序号|版本号|描述|\n|:---|:---|:---| \n|1|v1.0|使用unittest框架|\n|2|v1.1|使用pytest框架|\n\n\n\n\n## 快速开始\n\n### 环境准备\n\n#### python虚拟环境virtualenv使用\n\n- 安装虚拟环境: pip install virtualenv\n\n- 创建虚拟环境: virtualenv  demo_env\n\n- 命令行模式切换到虚拟环境Script目录: /../scripts/\n\n- 激活虚拟环境: activate.bat \n\n#### HttpTesting安装\n以下三种方式选择其一即可。\n\n##### pip在线安装\n\n- pip install HttpTesting==1.1.69\n\n##### 下载whl文件进行安装\n\n- pip install HttpTesting-1.1.69-py3-none-any.whl \n\n\n##### 更新httptesting包\n\n已安装httptesting包,通过pip命令进行更新\n\n- pip list  查看HttpTesting安装包版本信息\n\n- pip install --upgrade HttpTesting\n\n- pip install --upgrade HttpTesting==1.0.26\n\n\n\n### 使用命令运行\n\n以下四个命令作用相同\n\n- am \n- AM\n- amt\n- AMT\n\n|序号|命令参数|描述|\n|:---|:---|:---|  \n|1|am -conf set 或--config set|此命令用来设置config.yaml基本配置|\n|2|am -f template.yaml或--file template.yaml|执行YAML用例，支持绝对或相对路径|\n|3|am -d testcase或--dir testcase|批量执行testcase目录下的YAML用例，支持绝对路径或相对路径|\n|4|am -sp demo或--startproject demo|生成脚手架demo目录,以及用例模版|\n|5|am -har httphar.har|根据抓包工具导出的http har文件，生成测试用例YAML|\n|6|am -c demo.yaml或--convert demo.yaml|转换数据为HttpTesting测试用例|\n\n\n\n\n#### 基本配置\n\n- [通过开关启用功能：并发执行, 失败重新执行, 用例执行次数, Debug模式，输出模式(html与控制台)，URL基本路径]\n\n- URL设置\n\n- 钉钉机器人设置\n\n- 测试报告设置\n\n- EMAIL邮箱设置\n\n- 用例执行配置\n\n\n\n\n#### 用例执行\n\n- YAML执行: \n\n- [整个YAML文件执行，指定CASE名称执行，批定多个CASE名称执行并且按指定顺序执行]\n\n- am -f template.yaml\n\n- am -f template.yaml Case1\n\n- am -f template.yaml Case2 Case1\n\n\n- YAML批量执行: \n\n- [批量执行testcase目录下所有YAML测试用例文件]\n\n- am -dir testcase\n\n\n\n####  脚手架生成\n\n- am -sp demo 此命令生成一个demo文件夹结构。\n\n- 脚手架功能,是生成一个测试用例结构与Case模版.\n\n\n\n#### HAR\n\n- 执行命令: am -har httphar.har  自动生成httptesting用例 har_testcase.yaml。\n\n- har命令来解析, Charles抓包工具导出的http .har请求文件, 自动生成HttpTesting用例格式.\n\n\n\n\n\n### 用例编写\n\n\n#### 用例模型\n\n>TESTCASE{\n\n>>\'case1\':[\'description\',{},{}],  #场景模式每个{}一个接口\n\n>>\'case2\':[\'description\',{}],     #单接口模式\n\n>}\n\n\n### YAML用例格式  \n\n### 场景模式\n\tTESTCASE:\n\t\t#Case1由两个请求组成的场景\n\t\tCase1:\n\t\t\t-\n\t\t\t\tDesc: xxxx业务场景(登录->编辑)\n\t\t\t-\n\t\t\t\tDesc: 登录接口\n\t\t\t\tUrl: /login/login\n\t\t\t\tMethod: GET\n\t\t\t\tHeaders:\n\t\t\t\t\tcontent-type: "application/json"\n\t\t\t\t\tcache-control: "no-cache"\n\t\t\t\tData:\n\t\t\t\t\tname: "test"\n\t\t\t\t\tpass: "test123"\n\t\t\t\tOutPara: \n\t\t\t\t\t"H_token": result.data\n\t\t\t\t\t"content_type": header.content-type\n\t\t\t\t\t"name": Data.name \n\t\t\t\t\t"pass": Data.pass\n\t\t\t\tAssert:\n\t\t\t\t\t- eq: [result.status, \'success\']\n\t\t\t-\n\t\t\t\tDesc: 编辑接口\n\t\t\t\tUrl: /user/edit\n\t\t\t\tMethod: GET\n\t\t\t\tHeaders:\n\t\t\t\t\tcontent-type: "${content_type}$"   \n\t\t\t\t\tcache-control: "no-cache"\n\t\t\t\t\ttoken: "$H_token$"\n\t\t\t\tData:\n\t\t\t\t\tname: "${name}$"\n\t\t\t\t\tpass: "${pass}$"\n\t\t\t\tOutPara: \n\t\t\t\t\t"$H_token$": result.data\n\t\t\t\tAssert:\n\t\t\t\t\t- ai: [\'success\', result.status]\n\t\t\t\t\t- eq: [\'result.status\', \'修改成功\']\n\n### 多CASE模式\n\n\tTESTCASE:\n\t\t#同一接口,不同参数,扩充为多个CASE\n\t\tCase1:\n\t\t\t-\n\t\t\t\tDesc: 登录接口-正常登录功能\n\t\t\t-\n\t\t\t\tDesc: 登录接口\n\t\t\t\tUrl: /login/login\n\t\t\t\tMethod: GET\n\t\t\t\tHeaders:\n\t\t\t\t\tcontent-type: "application/json"\n\t\t\t\t\tcache-control: "no-cache"\n\t\t\t\tData:\n\t\t\t\t\tname: "test"\n\t\t\t\t\tpass: "test123"\n\t\t\t\tOutPara: \n\t\t\t\t\t"H_cookie": cookie.SESSION\n\t\t\t\tAssert:\n\t\t\t\t\t- eq: [result.status, \'success\']\n\t\tCase2:\n\t\t\t-\n\t\t\t\tDesc: 登录接口-错误密码\n\t\t\t-\n\t\t\t\tDesc: 登录接口\n\t\t\t\tUrl: /login/login\n\t\t\t\tMethod: GET\n\t\t\t\tHeaders:\n\t\t\t\t\tcontent-type: "application/json"\n\t\t\t\t\tcache-control: "no-cache"\n\t\t\t\tData:\n\t\t\t\t\tname: "test"\n\t\t\t\t\tpass: "test123"\n\t\t\t\tOutPara:\n\t\t\t\t\t"H_cookie": cookie.SESSION \n\t\t\t\tAssert:\n\t\t\t\t\t- eq: [result.status, \'error\']\n\n\n### 参数说明\n\n- "${H_cookie}$": 为参数变量,可以头信息里与Data数据里进行使用\n- "%{md5(\'aaaa\')}%": 为函数原型,具体支持函数下方表格可见.\n\n### 自定义变量\n\n变量作用域为当前CASE.\n\n- 通过在Case下定义USER_VAR字段，来自定义变量\n- USER_VAR字段下定义的字段为用户变量，作用于当前Case\n\n### 示例1(自定义变量)\n\n\tTESTCASE: \n\t\tCase1:\n\t\t\t- \n\t\t\t\tDesc: 接口详细描述\n\t\t\t\tUSER_VAR:\n\t\t\t\t\ttoken:  xxxxxxxx\n\t\t\t-\n\t\t\t\tUrl: /xxxx/xxxx\n\t\t\t\tMethod: POST\n\t\t\t\tHeaders: \n\t\t\t\t\ttoken: ${token}$\n\t\t\t\tData:\n\t\t\t\tOutPara:\n\t\t\t\tAssert: []\n\n### 示例2(自定义变量)\n\n\tTEST_CASE:\n\t\tCase1:\n\t\t-   \n\t\t\tDesc: 扫码校验券(支持检测微信券二维码码、微信会员h5券二维码、条码)\n\t\t\tUSER_VAR:\n\t\t\t\tversion: 1.0\n\t\t\t\tdata: \n\t\t\t\t\treq:\n\t\t\t\t\t\tsid: \'1380598237\'\n\t\t\t\t\t\twxcode: "164073966187485312752286" #209736174428\n\t\t\t\t\tappid: dp0Rm4wNl6A7q6w1QzcZQstr\n\t\t\t\t\tsig: 9c8c96b38d759abe6633c124a5d37225\n\t\t\t\t\tv: "${version}$"\n\t\t\t\t\tts: 1564643536\n\t\t\t\n\t\t-   Desc: 扫码校验券\n\t\t\tUrl: /pos/checkcoupon\n\t\t\tMethod: POST\n\t\t\tHeaders:\n\t\t\t\tcontent-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW\n\t\t\t\tcache-control: no-cache\n\t\t\tData: ${data}$\n\t\t\tOutPara: \n\t\t\tAssert:\n\t\t\t-   eq: [result.errcode, 0]\n\n\n- 以上通过USER_VAR字典对象来定义变量, key为变量名, value为变量值; 使用方法: ${token}$\n\n- 无需定义变量, USER_VAR字段在用例中,可以省略.\n\n#### OutPara字段变量使用\n\nOutPara字段用来做公共变量,供其它接口使用,默认为""; \n\n-  示例: "H_token": result.data 是请求结果，返回的嵌套级别,使用方法: ${H_token}$\n-  OutPara为dict类型,可以做多个公共变量.\n\n\n#### Assert断言\n\nAssert字段默认为[].\n\n|序号|断言方法|断言描述|\n|:---|:---|:---|\n|1|eq: [a, b]|判断 a与b相等,否则fail|\n|2|nq: [a, b]|判断 a与b不相等,否则fail|\n|3|al: [a, b]|判断 a is b 相当于id(a) == id(b),否则fail|\n|4|at: [a, b]|判断 a is not b 相当于id(a) != id(b)|\n|5|ai: [a, b]|判断 a in b ,否则fail|\n|6|ani: [a, b]|判断 a in not b,否则fail|\n|7|ais: [a, b]|判断 isinstance(a, b) True|\n|8|anis: [a, b]|判断 isinstance(a, b) False|\n|9|ln: [a]|判断 a is None,否则fail|\n|10|lnn: [a]|判断 a is not none|\n|11|bt: [a]|判断 a 为True|\n|12|bf: [a]|判断 a 为False|\n\n\n#### 内置函数及扩展\n\n使用原型(带参数与不带参数)\n\n- "%{md5(\'aaaa\')}%" 或 "%{timestamp()}%"\n\n\n\n|函数名|参数|说明|\n|:---|:---|:---|\n|md5|txt字符串|生成md5字符串示例: cbfbf4ea6d7c8032584dcf0defa10276|\n|timestamp|-|秒级时间戳示例: 1563183829|\n|uuid1|-|生成唯一id,uuid1示例:ebcd6df8a77611e99bb588b111064583|\n|datetimestr|-|生成日期时间串,示例:2019-07-16 10:50:16|\n|mstimestamp|-|毫秒级时间戳,20位|\n|sleep_time|-|线程睡眠,0.5为500毫秒，1为1秒|\n|rnd_list|[]|随机从列表中选择值|\n\n- 其它后续添加\n\n### 自定义函数扩展功能说明\n- 在执行用例root目录，新建extfunc.py文件\n- 按模型自定义函数\n- 类名 Extend不可更改\n- @staticmethod函数必须定义为静态\n- 函数各数不做限制\n\n### 自定义函数扩展功能模型\n\tclass Extend:\n\t\t@staticmethod\n\t\tdef func1():\n\t\t\treturn \'ext func\'\n\t\t\n\t\t@staticmethod\n\t\tdef func2(args):\n\t\t\treturn args\n\n- 使用示例1："%{func1()}%" \n- 使用示例2: "%{func1(\'aaaa\')}%" \n\n\n### 参数化功能\n定义参数化参数后，同一用例会按照参数个数决定用例执行次数。\n- 通过在用例Case下定义PARAM_VAR字段\n- PARAM_VAR字段下定义参数化变量，供之后引用\n- 如果在PARAM_VAR下定义多个，参数化变量，参数个数要匹配。\n- 现在如果定义了多个参数化变量，执行用例的次数是排列组合数。\n- 之后如有必要会改成，按参数化变量内参数的各数决定执行用例次数。\n\n### 参数化功能模型\n\tTEST_CASE:\n\t\tCase2:\n\t\t-   Desc: 给指定用户发送验证码\n\t\t\tUSER_VAR:\n\t\t\t\tcno_list:\n\t\t\t\t- \'1674921314241197\'\n\t\t\t\t- \'1581199496593872\'\n\t\t\t\t- \'1623770534820512\'\n\t\t\t\t- \'1674921701066628\'\n\t\t\t\t- \'1581199096195979\'\n\t\t\t\t- \'1623770606653991\'\n\t\t\tPARAM_VAR: \n\t\t\t\tsig: [1,2,3,4,5]\n\n\t\t-   Desc: 给指定用户发送验证码\n\t\t\tUrl: /user/sendcode\n\t\t\tMethod: POST\n\t\t\tHeaders:\n\t\t\t\tcontent-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW\n\t\t\t\tcache-control: no-cache\n\t\t\tData:\n\t\t\t\treq:\n\t\t\t\t\tcno: \'%{rnd_list("${cno_list}$")}%\'\n\t\t\t\tappid: dp1svA1gkNt8cQMkoIv7HmD1\n\t\t\t\tsig: "${sig}$"\n\t\t\t\tv: 2.0\n\t\t\t\tts: 123\n\t\t\tOutPara: null\n\t\t\tAssert:\n\t\t\t-   eq:\n\t\t\t\t- result.errcode\n\t\t\t\t- 0\n\t\t\t-   eq:\n\t\t\t\t- result.res.result\n\t\t\t\t- SUCCESS\n\n\n## 常用对象(通常做参数变量时使用)\n- res: 请求Response对象\n- result: res.json 或 res.text\n- cookie: res.cookie 响应cookie字典对象;  当做为参数时如果cookie.SESSION这样的写法代表取cookie中的SESSION对象. 如果只写cookie,会解析成"SESSION=xxxxxxx; NAME=xxxxxx"\n- headers: res.headers 响应头字典对象\n- header: header.content-type 请求头对象\n\n\n## 用例执行\n- 1、生成脚手架\n- 2、编写脚手架中testcase下YAML模版用例\n- 3、切换到testcase目录\n- 4、amt -dir testcase 自动运行testcase下YAML用例\n- 5、自动生成测试报告Html\n\n\n##  框架基本配置\n- 1、通过命令打开框架config.yaml\n- 2、amt -config set\n- 3、修改基本配置，并保存\n\n\n## 新增功能\n\n### 指定case编号执行\n\n- 指定单个Case执行 amt -f xxxx.yaml Case1\n- 指定多个Case执行 amt -f xxxx.yaml Case1 Case2 Case3\n\n\n### 请求头默认值\n\tTEST_CASE:\n\t\tCase1:\n\t\t-   Desc: 给用户发送验证码业务场景(发送1->发送2)\n\t\t\tUSER_VAR:\n\t\t\t\tcno_list:\n\t\t\t\t- \'1674921314241197\'\n\t\t\t\t- \'1581199496593872\'\n\t\t\t\t- \'1623770534820512\'\n\t\t\t\t- \'1674921701066628\'\n\t\t\t\t- \'1581199096195979\'\n\t\t\t\t- \'1623770606653991\'\n\n\t\t\tREQ_HEADER:\n\t\t\t\tcontent-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW\n\t\t\t\tcache-control: no-cache            \n\n\t\t-   Desc: 给指定用户发送验证码1\n\t\t\tUrl: /user/sendcode\n\t\t\tMethod: POST\n\t\t\tData:\n\t\t\t\treq:\n\t\t\t\t\tcno: \'%{rnd_list("${cno_list}$")}%\'\n\t\t\t\tappid: dp1svA1gkNt8cQMkoIv7HmD1\n\t\t\t\tsig: "123"\n\t\t\t\tv: 2.0\n\t\t\t\tts: 123\n\t\t\tOutPara: null\n\t\t\tAssert:\n\t\t\t-   eq:\n\t\t\t\t- result.errcode\n\t\t\t\t- 0\n\t\t\t-   eq:\n\t\t\t\t- result.res.result\n\t\t\t\t- SUCCESS\n\t\t-   Desc: 给指定用户发送验证码2\n\t\t\tUrl: /user/sendcode\n\t\t\tMethod: POST\n\t\t\tData:\n\t\t\t\treq:\n\t\t\t\t\tcno: \'%{rnd_list("${cno_list}$")}%\'\n\t\t\t\tappid: dp1svA1gkNt8cQMkoIv7HmD1\n\t\t\t\tsig: "123"\n\t\t\t\tv: 2.0\n\t\t\t\tts: 123\n\t\t\tHeaders:\n\t\t\t\tcontent-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW\n\t\t\t\tcache-control: no-cache    \t\t\t\n\t\t\tOutPara: null\n\t\t\tAssert:\n\t\t\t-   eq:\n\t\t\t\t- result.errcode\n\t\t\t\t- 0\n\t\t\t-   eq:\n\t\t\t\t- result.res.result\n\t\t\t\t- SUCCESS\n- 在Case中增加REQ_HEADER字段来做为公共的请求头。\n- 之后Case中执行共享此请求头\n- 如果在用例中设置了REQ_HEADER字段与请求中也单独设置了请求头，那么第一顺序为请求中的为主。\n- 上边的例子为场景用例，由两个请求组成，请求1，使用的是请求头默认值，请求2，使用自身请求头。\n\n### 功能对比\n|序号|功能|V1.0|V1.1|配置参数|\n|--|--|--|--|--|\n|1|并发执行|-|√|ENABLE_EXECUTION:False EXECUTION_NUM: 4|\n|2|失败重新执行|√|√|ENABLE_RERUN: False  RERUN_NUM:  2|\n|3|重复执行|-|√|ENABLE_REPEAT: False REPEAT_NUM: 2\n|4|钉钉消息|√|√|ENABLE_DDING:  False |\n|5|发送报告邮件|√|√|EMAIL_ENABLE: False|\n|6|控制台输出|-|√|ENABLE_EXEC_MODE: False|\n|7|自定义函数扩展|√|√|用例执行root目录增加extfunc.py|\n|8|自定义变量|√|√|在用例中用USER_VAR字段定义变量，作用于当前Case|\n|9|用例参数化|√|√|在用例中用PARAM_VAR字段定义参数化变量,作用于当前Case|\n|10|请求头默认值|√|√|设置用例请求头默认值,整个case共享请求头。|\n|11|指定case执行|-|√|单个yaml文件指定case执行|\n\n## 代码打包与上传PyPi\n\n  \n\n### 通过setuptools工具进行框架打包,需要编写setup.py\n\n\n\n- 打包：python3 setup.py bdist_wheel\n\n  \n\n- 上传PyP: twine upload dist/*\n\n  \n### 通过poetry工具打包\n\n- poetry build\n\n- poetry config repositories.testpypi https://pypi.org/project/HttpTesting\n\n- poetry pushlish  输入pypi用户名和密码',
    'author': 'lengyaohui',
    'author_email': 'lengyaohui@163.com',
    'url': 'https://github.com/HttpTesting/pyhttp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
