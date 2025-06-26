# 百度搜索自动化测试项目

这是一个使用Selenium和Pytest对百度搜索功能进行自动化测试的项目。

## 项目特性

- 🔍 全面的百度搜索功能测试
- 🚀 自动化的浏览器管理
- 📊 详细的HTML测试报告
- 🛠️ 易于使用的测试运行脚本
- ⚡ 快速的测试执行

## 测试覆盖范围

- 百度首页加载测试
- 搜索功能测试
- 回车键搜索测试
- 空搜索测试
- 搜索建议功能测试
- 特殊字符搜索测试

## 环境要求

- Python 3.7+
- Chrome浏览器
- Windows/Linux/macOS

## 安装步骤

1. **克隆或下载项目**
   ```bash
   git clone <项目地址>
   cd 百度搜索自动化测试
   ```

2. **安装依赖包**
   ```bash
   pip install -r requirements.txt
   ```

3. **验证安装**
   ```bash
   python -c "import selenium; import pytest; print('安装成功！')"
   ```

## 使用方法

### 方法一：使用运行脚本（推荐）

```bash
python run_tests.py
```

这个脚本会：
- 自动运行所有测试
- 生成带时间戳的HTML测试报告
- 在浏览器中自动打开报告

### 方法二：直接使用pytest

```bash
# 运行所有测试
pytest test_baidu_search.py -v

# 生成HTML报告
pytest test_baidu_search.py --html=test_report.html --self-contained-html

# 运行特定测试
pytest test_baidu_search.py::TestBaiduSearch::test_search_functionality -v
```

### 方法三：运行特定测试类或方法

```bash
# 运行特定测试类
pytest test_baidu_search.py::TestBaiduSearch -v

# 运行特定测试方法
pytest test_baidu_search.py::TestBaiduSearch::test_baidu_homepage_load -v
```

## 项目结构

```
ai自动化测试/
├── conftest.py              # Pytest配置文件，浏览器设置
├── test_baidu_search.py     # 百度搜索测试用例
├── run_tests.py             # 测试运行脚本
├── requirements.txt         # 项目依赖
├── README.md               # 项目说明文档
└── test_reports/           # 测试报告目录（自动生成）
    └── baidu_test_report_YYYYMMDD_HHMMSS.html
```

## 测试报告

测试完成后，会在 `test_reports/` 目录下生成HTML格式的测试报告，包含：

- 测试执行时间
- 测试结果统计
- 详细的测试步骤
- 错误信息和截图（如果有）
- 测试环境信息

## 故障排除

### 常见问题

1. **ChromeDriver版本不匹配**
   - 解决方案：项目使用webdriver-manager自动管理ChromeDriver版本

2. **浏览器启动失败**
   - 确保Chrome浏览器已安装
   - 检查防火墙设置
   - 尝试以管理员权限运行

3. **网络连接问题**
   - 确保网络连接正常
   - 检查是否能访问百度网站

4. **元素定位失败**
   - 百度网站可能更新了页面结构
   - 检查测试代码中的元素选择器

### 调试模式

如果需要调试，可以修改 `conftest.py` 中的浏览器选项：

```python
# 添加无头模式（不显示浏览器窗口）
options.add_argument('--headless')

# 添加详细日志
options.add_argument('--enable-logging')
options.add_argument('--v=1')
```

## 扩展测试

要添加新的测试用例，只需在 `test_baidu_search.py` 文件中添加新的测试方法：

```python
def test_new_feature(self, browser):
    """测试新功能"""
    # 测试代码
    pass
```

## 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 许可证

MIT License 