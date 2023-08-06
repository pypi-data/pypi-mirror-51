这是做什么的？
=======================
这是一个任务调度工具，可以根据设定的时间运行指定的任务（函数），时间设置丰富，欢迎使用

怎么安装？
=========
pip install sxclzy

怎么使用
=========
```
from sxclzy.sxclzy import Sxclzy

def your_function(func_arc):
    # your missions with func_arc
    pass

SL = Sxclzy()
SL.add_schedule(
            name='your function name',          # （必须）任务名称，是唯一的，任务的标示
            func=your_function,                 # （必须）任务函数，注意不要加上括号()
            schedule={'second': '*/10'},        # （必须）任务安排，传入字典，或全日期字符串，具体解释见下面
            run_times=3,                        # 任务运行的次数，默认为无数次，到达任务次数后需要重新add一次任务
            args={'func_arc': args},             # 传入任务函数的关键字字典，
            status=1,                           # 任务的启用状态，默认为1为启用，0 则不启用
            overwrite_if_exist=True             # 若任务列表已有任务，是否覆盖，默认为True
        )
SL.start()  # 开始任务
```

使用add_schedule 方法后，将在数据库中储存传入的任务函数源码，所以不必担心下次运行时代码丢失的问题。
但是必须要注意的是，暂时不支持传入类内方法，例如：
```
class A:
    def test_a(self, name):
        print('Hi {}! test is running'.format(name))
        self.test_b(name)

    def test_b(self, name):
        print('call from test_a: ', 'hi {}'.format(name))


a = A()
test = a.test_a     # 类内方法

SL = Sxclzy()
SL.add_schedule(
            name='func1',
            func=test,      # 这样将报错
            ...
          )
```

上面的 class 内方法不会被正确调度运行。
暂时只支持传入完整的单独方法。

正确调度输出如下：
![Image text](https://github.com/GuardianGH/sxclzy/blob/master/images/2019-08-14%2017-59-16.png?raw=true)

查看已导入的任务列表：
```
get_res = SL.get_schedules(print_pretty=False)
```
返回的 get_res 为一个列表字典：
```
[{'schedule': {'second': '*/10'}, 'create_time': '2019-08-17 15:49:26', 'args': {'name': 'Lilei'}, 'func_name': 'test', 'func': "def test(name):\n    print('Hi {}! '.format(name))\n", 'status': 1, 'name': 'func1', 'id': 1}]
```
若您只是临时查看，建议将 get_schedules 的参数 print_pretty 设置为 True，程序将调用 prettytable 打印出一个好看的表格：
![Image text](https://github.com/GuardianGH/sxclzy/blob/master/images/2019-08-17%2015-39-33.png?raw=true)

删除已有的调度任务：
```
SL.clear_schedules(names=None)
```
参数 names 可以传入需要删除的任务名称，可以是单个名称，也可以是名称的列表。

删除成功将输出日志：
```
2019-08-17 16:07:03,832 >>> schedules clear up: ['func1']
```


关于时间设置
============
“schedule” 的值需要一个字典，或全日期字符串，字典的值类似：
```
{"second": "*/30"}
```
意思是每30秒运行一次，也可以设置为具体的某个时间点，例如：
```
...
{
    'year': 2019,
    'month': 6,
    'day': 4,
    'hour': 10,
    'minute': 50,
    'second': 50
  }
```
或者：
```
{
    "y": 2019,
    "m": 9,
    "d": 13,
    "w": 3,         # 星期设定不可与日设置同时存在
    "H": 13,
    "M": 30,
    "S": 00,
}
```

这样的设置是单次任务模式，任务只在设定的时间点（2019-06-04 10:50:50）运行一次。

也可以是只有分钟，或者只有秒，或者只有小时、天、月、年，程序将自动计算下次到达设定的时间的时间间隔，

例如当设置为：
```
{"hour": 10}
```
而此时系统时间为 17:37:12，则爬虫将在明天，以及接下来的每一天的上午的 10:37:12 自动运行任务。

若只设置为：
```
{'day': 4}
```
则意思是从下个月开始的每个月的4号的当前时分秒启动，以此类推

需要注意的是，设定的月为1~12， 日小于等于月最大天数，小时为0-23， 分钟数0-59，秒数0-59

至此，我想你应该已经完全了解在参数中加 “ * / ” 或 不加 “ * / ”的作用了，若仍觉得不清楚，

直接使用它你会发现其中的含义。
----------------------------

此外还可以设定星期数，例如：
```
{'week': '*/2'}
```
意思是每周的周三执行，对的，星期的范围为0~6。

星期可以配合年、月、时、分、秒同时设定，但是不可同时设定星期数和天，否则将只按照天来计算，并忽略星期的设定。

若 schedule 的值为字符串，则需要这样的格式：
```
'2019,9,13,16,30,0'     # 2019年9月13日16点30分00秒
```
