# 使用说明

## 快速开始

### 1. 验证环境配置
```bash
python verify_setup.py
```

### 2. 运行测试
```bash
# Windows
run_tests.bat

# 或直接运行 Python 脚本
python run_tests.py
```

### 3. 查看报告
测试完成后，HTML 报告会自动打开。如果没有自动打开，可以手动打开：
```bash
allure open ./reports/allure-report
```

## 报告特性

### Allure HTML 报告包含：
- 📊 **测试概览**: 测试执行统计、通过率、失败率
- 📋 **详细步骤**: 每个测试用例的执行步骤
- 🖼️ **失败截图**: 测试失败时自动保存的截图
- 🔍 **页面源码**: 测试失败时的页面 HTML 源码
- 📈 **趋势分析**: 测试执行趋势图表
- 🏷️ **标签分类**: 按功能模块分类的测试用例

### 日志文件
- **位置**: `./reports/pytest.log`
- **内容**: 详细的测试执行日志
- **格式**: 时间戳 + 日志级别 + 模块名 + 行号 + 消息

## 常用命令

### 运行特定测试
```bash
# 运行特定测试文件
pytest testcases/test_buy.py -v

# 运行特定测试用例
pytest testcases/test_buy.py::test_valid_cases -v

# 运行标记的测试
pytest -m "slow" -v
```

### 生成报告
```bash
# 生成 allure 结果
pytest --allure-dir=./reports/allure-results --clear-alluredir -v

# 生成 HTML 报告
allure generate ./reports/allure-results -o ./reports/allure-report --clean

# 打开报告
allure open ./reports/allure-report

# 生成报告并立即打开
allure serve ./reports/allure-results
```

### 并行执行
```bash
# 使用 4 个进程并行执行
pytest -n 4 --allure-dir=./reports/allure-results -v
```

## 配置说明

### pytest.ini 配置项
- `--allure-dir`: Allure 结果保存目录
- `--clear-alluredir`: 清除之前的结果
- `-v`: 详细输出
- `log_file`: 日志文件路径
- `log_cli`: 控制台日志输出

### 环境变量
```bash
# 设置日志级别
export PYTEST_LOG_LEVEL=DEBUG

# 设置浏览器无头模式
export HEADLESS=true
```

## 故障排除

### 1. Allure 命令未找到
```bash
# Windows
scoop install allure
# 或
choco install allure

# macOS
brew install allure

# Linux
curl -o allure-2.24.0.tgz -Ls https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.24.0/allure-commandline-2.24.0.tgz
sudo tar -zxvf allure-2.24.0.tgz -C /opt/
sudo ln -s /opt/allure-2.24.0/bin/allure /usr/bin/allure
```

### 2. ChromeDriver 问题
```bash
# 使用 webdriver-manager 自动管理
pip install webdriver-manager

# 在代码中使用
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
```

### 3. 权限问题
确保有足够的权限创建和写入 `reports` 目录。

## 自定义配置

### 修改报告样式
可以在 `conftest.py` 中添加自定义的 allure 配置：

```python
import allure

def pytest_configure(config):
    allure.environment(
        browser="Chrome",
        version="latest",
        platform="Windows"
    )
```

### 添加自定义附件
```python
import allure

# 添加文本附件
allure.attach(
    name="测试数据",
    body="这是测试数据",
    attachment_type=allure.attachment_type.TEXT
)

# 添加图片附件
allure.attach(
    driver.get_screenshot_as_png(),
    name="截图",
    attachment_type=allure.attachment_type.PNG
)
```

## 最佳实践

1. **使用描述性的测试名称**: 让测试用例名称清楚地描述测试内容
2. **添加详细的步骤**: 使用 `@allure.step` 装饰器记录测试步骤
3. **记录关键信息**: 在日志中记录重要的测试数据
4. **处理异常**: 在测试中适当处理异常并记录错误信息
5. **定期清理**: 定期清理旧的报告文件以节省磁盘空间 