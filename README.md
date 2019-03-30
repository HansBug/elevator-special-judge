### 电梯系列作业Special Judge

------

#### 第一次作业：多线程傻瓜调度单电梯

指导书链接[见此](https://gitlab.buaaoo.top/oo_course_2019/homework-guide-books/blob/master/Unit2%20-%20Elevator/%E9%9D%A2%E5%90%91%E5%AF%B9%E8%B1%A1%E7%94%B5%E6%A2%AF%E7%B3%BB%E5%88%97%E7%AC%AC%E4%B8%80%E6%AC%A1%E6%8C%87%E5%AF%BC%E4%B9%A6.md)


#### 打包工具
 - requirements: pyinstaller >= 3.3 (mac仅有此依赖)
 - usage: ./pack.sh check_interface.py    将会在`./dist`目录下生成可执行文件datacheck

#### 可执行文件
 - usage: ./datacheck -i <input_path> -o <output_path> 
   
   input_path中是需要检查的样例文件，若程序正常运行将会在`output_path`输出检查的信息，否则会在`stderr`输出隐藏了部分信息的报错
