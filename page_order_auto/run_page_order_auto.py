import os
import shutil

import pytest

if __name__ == "__main__":
    if os.path.exists("./temp"):
        shutil.rmtree("./temp")  # 删除目录及其内容
    # 执行pytest测试并生成结果到temp目录
    pytest.main(["-vs", "--alluredir=./temp"])

    # 生成Allure报告（添加--clean参数在这里）
    os.system("allure generate ./temp -o ./allure-report --clean")
