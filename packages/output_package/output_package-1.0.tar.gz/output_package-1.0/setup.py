from distutils.core import setup
setup(
name='output_package', # 对外我们模块的名字
version='1.0', # 版本号
description='这是第一个对外发布的模块，测试哦', #描述
author='汤健', # 作者
author_email='2492391400@qq.com',
py_modules=['output_package.output1', 'output_package.output2'] # 要发布的模块
)