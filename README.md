
# 💡 codex-usage

> 一个轻量级命令行工具，用于实时查看 **ChatGPT Codex** 的使用额度（包括 5 小时与 7 天窗口），支持彩色进度条、自动刷新与命令行参数。

---

## 📦 安装 Installation

### 方式一（推荐开发者使用）

克隆仓库后本地安装：

```bash
git clone https://github.com/<yourname>/codex-usage.git
cd codex-usage
pip install .
````

或开发模式（无需重复安装）：

```bash
pip install -e .
```

---

## 🧩 使用 Usage

### 基本用法

```bash
codex-usage
```

使用默认的配置文件或 `configs.py` 中的 `AUTH_TOKEN`。

---

### 指定 Token

```bash
codex-usage --token "Bearer eyJh..."
```

---

### 持续监控模式（每隔 5 分钟刷新）

```bash
codex-usage --watch 300
```

或带 Token：

```bash
codex-usage --watch 300 --token "Bearer eyJh..."
```

---

### 查看帮助

```bash
codex-usage --help
```

输出：

```
usage: codex-usage [-h] [--token TOKEN] [--watch WATCH]

查看 ChatGPT Codex 使用额度

optional arguments:
  -h, --help        显示帮助
  --token TOKEN     手动传入 Bearer Token（会覆盖 configs.py 中的）
  --watch WATCH     每隔 N 秒自动刷新显示额度
```

---

## ⚙️ 配置 Config

在 `codex_usage/configs.py` 中添加你的 Codex 授权 Token：

```python
AUTH_TOKEN = "Bearer ..."
```

未来版本将支持自动读取：

```
~/.codex_usage/config.json
```

---

## 🧠 输出示例

```bash
💡 ChatGPT Codex 使用情况
账户类型: plus

🔹 短期窗口（5小时）
[█████░░░░░░░░░░░░░░░░░░░░] 22.0%
已用: 22.0%  剩余: 78.0%
额度将在 3小时 47分钟 后重置。

🔹 长期窗口（7天）
[██░░░░░░░░░░░░░░░░░░░░░░░░] 6.0%
已用: 6.0%  剩余: 94.0%
额度将在 6天 4小时 后重置。
```

---

## 📁 项目结构 Project Layout

```
codex_usage/
├── setup.py
├── README.md
└── codex_usage/
    ├── __init__.py
    ├── main.py
    └── configs.py
```

---

## 🧰 开发 Development

### 重新安装

```bash
pip uninstall codex-usage -y
pip install .
```

### 调试模式（自动加载改动）

```bash
pip install -e .
```

---

## 🛠️ 依赖 Dependencies

* [requests](https://pypi.org/project/requests/)
* [rich](https://pypi.org/project/rich/)

---

## 🧾 许可证 License

This module is licensed under the MIT License.
---

