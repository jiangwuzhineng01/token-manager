# Token Manager Skill

> OpenClaw Token 管理与 API 监控技能

## 描述

自动监控 API Token 使用量，当达到阈值时自动切换到备份大模型。支持多模型配置、使用统计和智能切换策略。

## 功能特性

- ✅ **Token 使用监控** - 实时追踪 API 调用量和 Token 消耗
- ✅ **自动模型切换** - 达到阈值时自动切换到备份模型
- ✅ **多模型支持** - 支持配置多个大模型（主模型 + 多个备份）
- ✅ **使用统计** - 生成 Token 使用报告和成本分析
- ✅ **智能切换策略** - 基于用量、成本、响应时间的智能决策
- ✅ **告警通知** - Token 用量达到阈值时发送告警

## 触发条件

当用户提到以下内容时激活：
- "Token 管理"、"API 监控"、"模型切换"
- "查看 Token 用量"、"切换模型"、"配置备份模型"
- "Token 快用完了"、"API 限额"、"切换备用模型"

## 使用方法

### 1. 初始化配置

```
配置 Token 管理
设置主模型和备份模型
查看当前模型配置
```

### 2. 监控用量

```
查看 Token 用量
API 使用统计
本月消耗了多少 Token
```

### 3. 切换模型

```
切换到备份模型
手动切换模型
使用 [模型名]
```

### 4. 配置告警

```
设置 Token 告警阈值
当用量达到 80% 时提醒我
```

## 配置文件

配置保存在：`~/.openclaw/skills/token-manager/config/models.json`

示例配置：
```json
{
  "primary_model": {
    "name": "qwen3.5-plus",
    "provider": "bailian",
    "api_key": "sk-xxx",
    "monthly_limit": 1000000,
    "current_usage": 0
  },
  "backup_models": [
    {
      "name": "qwen3.5-turbo",
      "provider": "bailian",
      "api_key": "sk-xxx",
      "priority": 1
    },
    {
      "name": "deepseek-chat",
      "provider": "deepseek",
      "api_key": "sk-xxx",
      "priority": 2
    }
  ],
  "switch_threshold": 0.8,
  "alert_threshold": 0.7
}
```

## 相关文件

- `SKILL.md` - 技能说明文件
- `config/models.json` - 模型配置
- `scripts/token_monitor.py` - Token 监控脚本
- `scripts/model_switcher.py` - 模型切换脚本

## 依赖

- Python 3.9+
- OpenClaw Gateway API
- 各模型 provider 的 API 访问权限

## 注意事项

1. 首次使用需要配置 API Key
2. 建议设置合理的告警阈值（70-80%）
3. 定期检查 Token 使用统计
4. 备份模型应保持可用状态

## 更新日志

- v1.0 (2026-03-12) - 初始版本
  - Token 使用监控
  - 自动模型切换
  - 使用统计报告
