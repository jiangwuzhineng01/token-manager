# Token Manager Skill - 开发完成报告

> OpenClaw Token 管理与 API 监控技能  
> 开发时间：2026-03-12

---

## ✅ 完成内容

### 1. 核心功能模块

**文件结构**:
```
token-manager/
├── SKILL.md                      # 技能说明
├── token_manager.py              # 核心管理器
├── README.md                     # 使用指南
├── config/
│   └── config.example.yaml       # 配置示例
└── scripts/
    └── test_token_manager.py     # 测试脚本
```

### 2. 已实现功能

| 功能 | 状态 | 说明 |
|-----|------|------|
| Token 使用监控 | ✅ 完成 | 实时追踪 API 调用和 Token 消耗 |
| 自动模型切换 | ✅ 完成 | 达到阈值自动切换到备份模型 |
| 多模型支持 | ✅ 完成 | 支持 1 个主模型 + N 个备份模型 |
| 使用统计 | ✅ 完成 | 生成 Token 使用报告和成本分析 |
| 告警通知 | ✅ 完成 | 达到阈值时发送告警 |
| 配置管理 | ✅ 完成 | JSON 配置文件，易于修改 |

---

## 🎯 核心功能

### 1. Token 使用监控

```python
manager = TokenManager()
usage = manager.check_usage()

# 输出:
{
  "model": "qwen3.5-plus",
  "usage": 750000,
  "limit": 1000000,
  "usage_rate": 75.0,
  "remaining": 250000,
  "threshold_reached": False,
  "alert_reached": True
}
```

### 2. 自动模型切换

```python
# 当用量达到 80% 时自动切换
if manager.should_switch_model():
    result = manager.switch_to_backup()
    
# 输出:
{
  "success": True,
  "message": "已从 qwen3.5-plus 切换到 qwen3.5-turbo",
  "previous_model": "qwen3.5-plus",
  "current_model": "qwen3.5-turbo"
}
```

### 3. 使用统计

```python
stats = manager.get_usage_stats(days=30)

# 输出:
{
  "period": "Last 30 days",
  "total_tokens": 1500000,
  "total_requests": 1000,
  "total_cost": 15.0,
  "by_model": {
    "qwen3.5-plus": {"total_tokens": 1000000, ...},
    "qwen3.5-turbo": {"total_tokens": 500000, ...}
  },
  "daily_average": 50000
}
```

### 4. 告警系统

```python
alerts = manager.get_alerts()

# 当用量达到 70% 时:
[
  {
    "type": "usage_warning",
    "level": "warning",
    "message": "Token 用量已达到 75.0%",
    "usage": 750000,
    "limit": 1000000
  }
]
```

---

## 📊 测试结果

```bash
$ python3 scripts/test_token_manager.py

======================================================================
                    🔑 Token Manager 测试
======================================================================

✅ 测试 1: 查看当前配置 - 通过
✅ 测试 2: 检查 Token 用量 - 通过
✅ 测试 3: 添加使用记录 - 通过
✅ 测试 4: 获取使用统计 - 通过
✅ 测试 5: 设置告警阈值 - 通过
✅ 测试 6: 获取当前告警 - 通过
✅ 测试 7: 添加备份模型 - 通过
✅ 测试 8: 查看备份模型列表 - 通过
✅ 测试 9: 模拟模型切换 - 通过

======================================================================
✅ 所有测试通过
```

---

## 🚀 使用方法

### 在 OpenClaw 中使用

**查看用量**:
```
查看 Token 用量
API 使用统计
本月消耗了多少 Token
```

**切换模型**:
```
切换到备份模型
手动切换模型
使用 qwen3.5-turbo
```

**配置告警**:
```
设置 Token 告警阈值为 80%
当用量达到 75% 时提醒我
```

**添加备份模型**:
```
添加备份模型 deepseek-chat
配置备用 API Key
```

---

## ⚙️ 配置示例

### 配置文件位置

```
~/.openclaw/skills/token-manager/config/models.json
```

### 配置内容

```json
{
  "primary_model": {
    "name": "qwen3.5-plus",
    "provider": "bailian",
    "api_key": "sk-your-key",
    "monthly_limit": 1000000,
    "current_usage": 0
  },
  "backup_models": [
    {
      "name": "qwen3.5-turbo",
      "provider": "bailian",
      "api_key": "sk-backup-key",
      "priority": 1,
      "enabled": true
    },
    {
      "name": "deepseek-chat",
      "provider": "deepseek",
      "api_key": "sk-deepseek-key",
      "priority": 2,
      "enabled": true
    }
  ],
  "switch_threshold": 0.8,
  "alert_threshold": 0.7,
  "auto_switch": true
}
```

---

## 📈 使用场景

### 场景 1: 防止 API 超限

**问题**: 主模型 Token 快用完了

**解决**:
1. 设置告警阈值 70%
2. 设置切换阈值 80%
3. 配置 2 个备份模型
4. 达到 80% 自动切换

### 场景 2: 成本优化

**问题**: 需要控制 API 成本

**解决**:
1. 配置低价模型作为备份
2. 查看使用统计和成本估算
3. 根据成本调整模型选择

### 场景 3: 多模型轮询

**问题**: 单个模型不稳定

**解决**:
1. 配置多个备份模型
2. 启用自动切换
3. 故障时自动切换到可用模型

---

## 💡 最佳实践

### 1. 阈值设置

```
推荐配置:
- 告警阈值：70% (提前预警)
- 切换阈值：80% (留有余量)
```

### 2. 备份模型

```
建议配置:
1. 同 provider 的低价模型 (快速切换)
2. 不同 provider 的模型 (防止单点故障)
3. 本地模型 (最后备选)
```

### 3. 监控频率

```
建议检查:
- 每天：查看用量
- 每周：查看统计
- 每月：优化配置
```

---

## 🔧 技术实现

### 核心类

```python
class TokenManager:
    - __init__()           # 初始化
    - check_usage()        # 检查用量
    - should_switch_model() # 判断是否切换
    - switch_to_backup()   # 切换到备份
    - add_usage()          # 添加使用记录
    - get_usage_stats()    # 获取统计
    - set_alert_threshold() # 设置告警
    - add_backup_model()   # 添加备份模型
    - get_alerts()         # 获取告警
```

### 数据存储

```
配置文件：
- models.json         # 模型配置
- usage_history.json  # 使用历史

位置:
~/.openclaw/skills/token-manager/config/
```

---

## 📝 相关文档

- `SKILL.md` - 技能说明文件
- `README.md` - 完整使用指南
- `config.example.yaml` - 配置示例
- `scripts/test_token_manager.py` - 测试脚本

---

## 🎉 总结

**开发时间**: 1 小时  
**代码行数**: 600+ 行  
**测试覆盖**: 9 个测试用例  
**功能状态**: ✅ 全部完成

**核心优势**:
- ✅ 自动监控 API 用量
- ✅ 智能切换备份模型
- ✅ 详细使用统计
- ✅ 灵活告警配置
- ✅ 易于集成和使用

**下一步**:
- [ ] 集成到 OpenClaw 主系统
- [ ] 添加更多告警渠道（邮件、短信）
- [ ] 支持更多模型提供商
- [ ] 优化成本估算算法

---

*报告时间：2026-03-12*  
*版本：v1.0*  
*状态：✅ 开发完成*
