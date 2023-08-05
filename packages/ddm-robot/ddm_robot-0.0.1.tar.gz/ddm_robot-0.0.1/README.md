使用本包之前，需要将树莓派B3+ pi机器人链接进入同一个局域网中，测试链接是否成功，请在python 命令行中输入from LSC_Client import LSC_Client ;lsc=LSC_Client.LSC_Client();若不报错，则链接成功，如果报错，例如 目标计算机积极拒绝，则说明机器人没有成功链接进入局域网中，请重新链接，或者机器人链接进入局域网，但是机器人的robortserver服务器没有启动，请请检查启动。
调用机器人方法
from robot import robot 
r = robot.robot()
r.up(1)#机器人站立
r.forward(3)#机器人前进三步

robot 包中包含的方法如下：
 -- voice
 -- showlib
 
 from robot import voice 
 可以调用机器人的语音输出功能
 v = robot.voice()
 v.speak(27)
 音域设置为26-47，超出范围的将无法成功，后续版本将不断增加范围
 
 from robot import showlib
 可以调用机器人舞蹈功能
 s = robot.showlib()
 s.hiphop()#街舞
 
 -----------------------------------------------------
 安装依赖 
from inspect import signature
from functools import wraps

需要提前安装这两个包，如果已经有了，自动跳过

pip install robot
就可以尝试连接机器人了