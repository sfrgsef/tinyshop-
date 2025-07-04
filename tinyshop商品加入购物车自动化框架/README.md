# 商品购物车自动化测试框架

这是一个基于 Selenium + Pytest + Allure 的商品购物车自动化测试框架。

## 功能特性

- 🛒 商品购物车自动化测试
- 📊 Allure HTML 测试报告
- 📝 详细的日志记录
- 🖼️ 失败截图自动保存
- 🔍 页面源码记录
- 🎯 参数化测试

## 环境要求

- Python 3.7+
- Chrome 浏览器
- ChromeDriver

## 安装依赖

```bash
pip install -r requirements.txt
```

## 安装 Allure 命令行工具

### Windows
```bash
# 使用 scoop
scoop install allure

# 或使用 chocolatey
choco install allure
```

### macOS
```bash
brew install allure
```

### Linux
```bash
# 下载并安装
curl -o allure-2.24.0.tgz -Ls https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.24.0/allure-commandline-2.24.0.tgz
sudo tar -zxvf allure-2.24.0.tgz -C /opt/
sudo ln -s /opt/allure-2.24.0/bin/allure /usr/bin/allure
```

## 运行测试

### 方法一：使用运行脚本（推荐）

```bash
# Windows
run_tests.bat

# 或直接运行 Python 脚本
python run_tests.py
```

### 方法二：使用 pytest 命令

```bash
# 运行测试并生成 allure 结果
pytest --allure-dir=./reports/allure-results --clear-alluredir -v

# 生成 HTML 报告
allure generate ./reports/allure-results -o ./reports/allure-report --clean

# 打开报告
allure open ./reports/allure-report
```

## 报告和日志

### 报告位置
- **Allure 结果数据**: `./reports/allure-results/`
- **HTML 报告**: `./reports/allure-report/`
- **测试日志**: `./reports/pytest.log`

### 报告特性
- 📈 测试执行统计
- 📋 详细的测试步骤
- 🖼️ 失败截图
- 🔍 页面源码
- 📊 测试趋势分析
- 🏷️ 测试标签分类

## 项目结构

```
tinyshop商品加入购物车自动化框架/
├── config.py              # 配置文件
├── conftest.py            # Pytest 配置和 fixtures
├── run_tests.py           # 测试运行脚本
├── run_tests.bat          # Windows 批处理文件
├── requirements.txt       # Python 依赖
├── utlis/
│   ├── helper.py          # 辅助函数
│   └── pytest.ini         # Pytest 配置
├── pages/
│   ├── login_page.py      # 登录页面对象
│   └── buy_page.py        # 购买页面对象
├── testcases/
│   └── test_buy.py        # 测试用例
├── data/
│   └── test_data.py       # 测试数据
└── reports/               # 报告和日志目录
    ├── allure-results/    # Allure 结果数据
    ├── allure-report/     # HTML 报告
    └── pytest.log         # 测试日志
```

## 配置说明

### pytest.ini 配置
- `--allure-dir`: Allure 结果保存目录
- `--clear-alluredir`: 清除之前的结果
- `-v`: 详细输出
- `log_file`: 日志文件路径
- `log_cli`: 控制台日志输出

### 测试用例装饰器
- `@allure.epic()`: 史诗级功能分类
- `@allure.feature()`: 功能模块分类
- `@allure.step()`: 测试步骤
- `@pytest.mark.parametrize()`: 参数化测试

## 日志级别

- `INFO`: 一般信息
- `WARNING`: 警告信息
- `ERROR`: 错误信息
- `DEBUG`: 调试信息

## 故障排除

### 1. Allure 命令未找到
确保已正确安装 Allure 命令行工具，并添加到系统 PATH。

### 2. ChromeDriver 版本不匹配
确保 ChromeDriver 版本与 Chrome 浏览器版本匹配。

### 3. 测试失败无截图
检查浏览器是否正常运行，确保有足够的权限保存文件。

## 扩展功能

### 添加新的测试用例
1. 在 `testcases/` 目录下创建新的测试文件
2. 使用 `@allure` 装饰器添加报告信息
3. 添加适当的日志记录

### 自定义报告样式
可以修改 Allure 配置来自定义报告样式和内容。

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个测试框架。 