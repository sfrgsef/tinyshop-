import pytest

# 运行所有用例并生成 allure 测试报告，带详细进度
def main():
    pytest.main(["-v", "--alluredir=reports"])
if __name__ == "__main__":
    main()
