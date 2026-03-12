# Token Manager - OpenClaw Token 管理与 API 监控

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-green.svg)](https://github.com/openclaw/openclaw)

> 🔑 OpenClaw 的 Token 管理与 API 监控技能 - 自动监控 API 用量，智能切换备份模型

---

## ✨ 功能特性

- 📊 **Token 使用监控** - 实时追踪 API 调用量和 Token 消耗
- 🔄 **自动模型切换** - 达到阈值时自动切换到备份模型
- 🎯 **多模型支持** - 支持配置多个大模型（主模型 + 多个备份）
- 📈 **使用统计** - 生成 Token 使用报告和成本分析
- 🚨 **智能告警** - Token 用量达到阈值时发送告警
- ⚙️ **配置管理** - JSON 配置文件，易于修改

---

## 🚀 快速开始

### 安装

```bash
# 克隆到 OpenClaw skills 目录
cd ~/.npm-global/lib/node_modules/openclaw/skills/
git clone https://github.com/YOUR_USERNAME/token-manager.git
cd token-manager

# 运行配置脚本
./setup.sh
```

### 配置

编辑配置文件 `~/.openclaw/skills/token-manager/config/models.json`:

```json
{
  "primary_model": {
    "name": "qwen3.5-plus",
    "provider": "bailian",
    "api_key": "sk-your-api-key",
    "monthly_limit": 1000000
  },
  "backup_models": [
    {
      "name": "qwen3.5-turbo",
      "provider": "bailian",
      "api_key": "sk-backup-key",
      "priority": 1
    }
  ],
  "switch_threshold": 0.8,
  "alert_threshold": 0.7
}
```

### 使用

在 OpenClaw 中直接使用：

```
查看 Token 用量
切换到备份模型
设置 Token 告警阈值
添加备份模型
```

---

## 📖 功能说明

### 1. Token 使用监控

实时监控 API 调用和 Token 消耗：

```python
from token_manager import TokenManager

manager = TokenManager()
usage = manager.check_usage()

print(f"已用：{usage['usage']} / {usage['limit']} ({usage['usage_rate']}%)")
```

### 2. 自动模型切换

当用量达到阈值时自动切换到备份模型：

```python
if manager.should_switch_model():
    result = manager.switch_to_backup()
    print(f"已切换到 {result['current_model']}")
```

### 3. 使用统计

生成详细的使用报告：

```python
stats = manager.get_usage_stats(days=30)
print(f"总 Token: {stats['total_tokens']}")
print(f"估算成本：¥{stats['total_cost']}")
```

### 4. 告警系统

设置用量告警阈值：

```python
manager.set_alert_threshold(0.8)  # 80% 时告警
alerts = manager.get_alerts()
```

---

## 📁 项目结构

```
token-manager/
├── SKILL.md                      # 技能说明
├── token_manager.py              # 核心管理器
├── README.md                     # 使用指南
├── QUICKSTART.md                 # 快速开始
├── DEVELOPMENT_REPORT.md         # 开发报告
├── DEMO_REPORT.md                # 演示报告
├── setup.sh                      # 配置脚本
├── config/
│   ├── config.example.yaml       # 配置示例
│   └── models.json               # 模型配置（运行时生成）
└── scripts/
    ├── test_token_manager.py     # 测试脚本
    └── demo.py                   # 功能演示
```

---

## 🧪 测试

```bash
# 运行测试
python3 scripts/test_token_manager.py

# 运行完整演示
python3 scripts/demo.py
```

---

## 💡 使用场景

### 场景 1: 防止 API 超限

```
问题：主模型 Token 快用完了
解决：
  1. 设置告警阈值 70%
  2. 设置切换阈值 80%
  3. 配置 2 个备份模型
  4. 达到 80% 自动切换
```

### 场景 2: 成本优化

```
问题：需要控制 API 成本
解决：
  1. 配置低价模型作为备份
  2. 查看使用统计和成本估算
  3. 根据成本调整模型选择
```

### 场景 3: 多模型轮询

```
问题：单个模型不稳定
解决：
  1. 配置多个备份模型
  2. 启用自动切换
  3. 故障时自动切换到可用模型
```

---

## ⚙️ 配置说明

### 主模型配置

| 参数 | 说明 | 示例 |
|-----|------|------|
| name | 模型名称 | qwen3.5-plus |
| provider | 提供商 | bailian |
| api_key | API Key | sk-xxx |
| monthly_limit | 月度限额 | 1000000 |
| current_usage | 当前用量 | 0 (自动更新) |

### 备份模型配置

| 参数 | 说明 | 示例 |
|-----|------|------|
| name | 模型名称 | qwen3.5-turbo |
| provider | 提供商 | bailian |
| api_key | API Key | sk-xxx |
| priority | 优先级 | 1 (数字越小越优先) |
| enabled | 是否启用 | true |

### 全局配置

| 参数 | 说明 | 默认值 |
|-----|------|--------|
| switch_threshold | 切换阈值 | 0.8 (80%) |
| alert_threshold | 告警阈值 | 0.7 (70%) |
| auto_switch | 自动切换 | true |

---

## 📊 命令行工具

### 查看用量

```bash
python3 -c "
from token_manager import TokenManager
m = TokenManager()
u = m.check_usage()
print(f'用量：{u[\"usage_rate\"]}%')
"
```

### 切换模型

```bash
python3 -c "
from token_manager import TokenManager
m = TokenManager()
r = m.switch_to_backup()
print(r['message'])
"
```

---

## 🔧 开发

### 添加新的模型提供商

```python
# 在 token_manager.py 中添加
def add_provider(self, name: str, config: dict):
    self.config['providers'][name] = config
    self._save_config()
```

### 自定义告警渠道

```python
def send_alert(self, message: str, channel: str = 'log'):
    if channel == 'log':
        logging.warning(message)
    elif channel == 'file':
        with open('alerts.log', 'a') as f:
            f.write(message + '\n')
```

---

## 📝 更新日志

### v1.0 (2026-03-12)

- ✅ 初始版本
- ✅ Token 使用监控
- ✅ 自动模型切换
- ✅ 使用统计报告
- ✅ 告警系统
- ✅ 配置管理

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

## 📞 联系方式

- 作者：jiangwu24
- 项目：OpenClaw Token Manager
- 文档：README.md

---

## 🙏 致谢

- [OpenClaw](https://github.com/openclaw/openclaw) - OpenClaw 框架
- [通义千问](https://help.aliyun.com/zh/dashscope/) - API 支持

---

<p align="center">Made with ❤️ by jiangwu24</p>
