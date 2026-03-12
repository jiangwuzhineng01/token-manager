# Token Manager 使用指南

> OpenClaw Token 管理与 API 监控技能

---

## 🚀 快速开始

### 1. 初始化配置

首次使用需要配置 API Key 和模型信息：

```bash
# 创建配置目录
mkdir -p ~/.openclaw/skills/token-manager/config

# 复制示例配置
cp config/config.example.yaml ~/.openclaw/skills/token-manager/config/models.json
```

### 2. 编辑配置

编辑 `~/.openclaw/skills/token-manager/config/models.json`：

```json
{
  "primary_model": {
    "name": "qwen3.5-plus",
    "provider": "bailian",
    "api_key": "sk-your-actual-key",
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

---

## 📖 使用命令

### 查看 Token 用量

```
查看 Token 用量
API 使用统计
本月消耗了多少 Token
```

**输出示例**:
```
📊 Token 使用统计

主模型：qwen3.5-plus
已用：750,000 / 1,000,000 (75.00%)
剩余：250,000

状态：⚠️ 接近阈值 (70%)
```

---

### 切换模型

```
切换到备份模型
手动切换模型
使用 qwen3.5-turbo
```

**输出示例**:
```
✅ 模型切换成功

从：qwen3.5-plus
到：qwen3.5-turbo

原因：Token 用量达到 80%
时间：2026-03-12 20:55:00
```

---

### 配置告警

```
设置 Token 告警阈值为 80%
当用量达到 75% 时提醒我
```

**输出示例**:
```
✅ 告警阈值已更新

当前阈值：80%
告警方式：日志 + 文件
```

---

### 添加备份模型

```
添加备份模型 deepseek-chat
配置备用 API Key
```

**输出示例**:
```
✅ 已添加备份模型

名称：deepseek-chat
提供商：deepseek
优先级：2
状态：已启用
```

---

## 🔍 监控功能

### 自动监控

Token Manager 会在每次 API 调用时自动：

1. **记录用量** - 记录 prompt 和 completion tokens
2. **检查阈值** - 判断是否达到切换阈值
3. **触发告警** - 达到告警阈值时发送通知
4. **自动切换** - 达到切换阈值时自动切换模型

### 手动检查

```
检查 Token 使用情况
查看当前模型状态
```

---

## 📊 统计报告

### 查看使用统计

```
查看最近 30 天的使用情况
生成 Token 使用报告
```

**报告内容**:
- 总 Token 消耗
- 按模型分组统计
- 日均消耗量
- 成本估算
- 趋势分析

---

## ⚙️ 高级配置

### 多模型轮询

配置多个备份模型，自动轮询使用：

```json
{
  "backup_models": [
    {"name": "model-a", "priority": 1},
    {"name": "model-b", "priority": 2},
    {"name": "model-c", "priority": 3}
  ],
  "rotation_enabled": true
}
```

### 成本优化

根据成本自动选择模型：

```json
{
  "optimization_strategy": "cost",
  "max_cost_per_1k_tokens": 0.01
}
```

### 性能优化

根据响应时间自动选择：

```json
{
  "optimization_strategy": "performance",
  "max_response_time_ms": 3000
}
```

---

## 🚨 告警配置

### 告警级别

| 级别 | 阈值 | 说明 |
|-----|------|------|
| 🟢 正常 | < 70% | 正常使用 |
| 🟡 警告 | 70-80% | 接近阈值 |
| 🔴 紧急 | > 80% | 需要切换 |

### 告警渠道

1. **日志告警** - 写入系统日志
2. **文件告警** - 写入告警文件
3. **会话通知** - 在聊天中通知用户

---

## 💡 最佳实践

### 1. 设置合理阈值

```
推荐配置:
- 告警阈值：70%
- 切换阈值：80%
```

### 2. 配置多个备份

```
建议至少配置 2 个备份模型:
1. 同 provider 的低价模型（快速切换）
2. 不同 provider 的模型（防止单点故障）
```

### 3. 定期检查统计

```
每周查看使用统计:
- 检查用量趋势
- 优化模型选择
- 调整阈值配置
```

### 4. 成本监控

```
启用成本估算:
- 跟踪每月支出
- 对比不同模型成本
- 选择性价比最优方案
```

---

## 🔧 故障排查

### 问题 1: 无法切换模型

**原因**: 没有配置备份模型

**解决**:
```bash
# 添加备份模型
添加备份模型 qwen3.5-turbo
```

### 问题 2: 告警不触发

**原因**: 阈值设置过高

**解决**:
```bash
# 降低告警阈值
设置 Token 告警阈值为 60%
```

### 问题 3: 统计数据不准确

**原因**: 使用历史记录丢失

**解决**:
```bash
# 检查历史文件
ls -la ~/.openclaw/skills/token-manager/config/usage_history.json
```

---

## 📝 API 参考

### Python 调用

```python
from token_manager import get_token_manager

# 获取管理器实例
manager = get_token_manager()

# 检查用量
status = manager.check_usage()
print(f"用量：{status['usage_rate']}%")

# 添加使用记录
manager.add_usage(
    model="qwen3.5-plus",
    prompt_tokens=100,
    completion_tokens=50
)

# 获取统计
stats = manager.get_usage_stats(days=30)
print(f"总消耗：{stats['total_tokens']} tokens")
```

---

## 📞 支持

- 文档：`~/.npm-global/lib/node_modules/openclaw/skills/token-manager/README.md`
- 配置示例：`config/config.example.yaml`
- 问题反馈：OpenClaw GitHub Issues

---

*版本：v1.0*  
*更新时间：2026-03-12*
