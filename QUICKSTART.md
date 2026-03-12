# Token Manager - 快速上手指南

> 5 分钟开始使用 Token 管理功能

---

## ✅ 安装状态

```
✅ Skill 已安装：~/.npm-global/lib/node_modules/openclaw/skills/token-manager/
✅ 配置文件：~/.openclaw/skills/token-manager/config/models.json
✅ 测试通过：9/9 测试用例
✅ 当前用量：3,000 / 1,000,000 (0.3%)
```

---

## 🚀 立即开始

### 方式 1：在 OpenClaw 中直接使用（推荐）

**打开 OpenClaw，然后说**:

```
查看 Token 用量
```

**系统会回复**:
```
📊 Token 使用统计

主模型：qwen3.5-plus
已用：3,000 / 1,000,000 (0.30%)
剩余：997,000

状态：✅ 正常
```

---

### 方式 2：命令行测试

```bash
cd /home/jiangwu24/.npm-global/lib/node_modules/openclaw/skills/token-manager
python3 scripts/test_token_manager.py
```

---

## 📝 配置 API Key（重要）

**编辑配置文件**:
```bash
nano ~/.openclaw/skills/token-manager/config/models.json
```

**修改内容**:
```json
{
  "primary_model": {
    "name": "qwen3.5-plus",
    "provider": "bailian",
    "api_key": "sk-你的真实 API Key",  // ← 修改这里
    "monthly_limit": 1000000
  },
  "backup_models": [
    {
      "name": "qwen3.5-turbo",
      "provider": "bailian",
      "api_key": "sk-备份 API Key",  // ← 修改这里
      "priority": 1
    }
  ]
}
```

**保存并退出**:
- Ctrl+O 保存
- Enter 确认
- Ctrl+X 退出

---

## 💬 常用命令

### 查看用量

```
查看 Token 用量
API 使用统计
本月用了多少 Token
```

### 切换模型

```
切换到备份模型
手动切换模型
现在使用 qwen3.5-turbo
```

### 配置告警

```
设置 Token 告警阈值为 80%
用量达到 70% 时提醒我
```

### 添加备份模型

```
添加备份模型 deepseek-chat
配置备用 API Key
```

### 查看统计

```
查看最近 30 天使用情况
生成 Token 使用报告
```

---

## 🎯 实际使用场景

### 场景 1：日常监控

**每天早上**:
```
查看 Token 用量
```

**系统回复**:
```
📊 Token 使用统计
主模型：qwen3.5-plus
已用：50,000 / 1,000,000 (5.00%)
剩余：950,000
状态：✅ 正常
```

---

### 场景 2：接近限额

**当用量达到 80%**:
```
系统自动切换到备份模型

✅ 模型切换成功
从：qwen3.5-plus
到：qwen3.5-turbo
原因：Token 用量达到 80%
```

---

### 场景 3：查看成本

```
查看本月 Token 成本

📊 成本统计
周期：最近 30 天
总 Token: 500,000
估算成本：¥5.00
日均消耗：16,667 tokens/天
```

---

## 📊 配置文件说明

```json
{
  "primary_model": {           // 主模型
    "name": "qwen3.5-plus",    // 模型名称
    "provider": "bailian",     // 提供商
    "api_key": "sk-xxx",       // API Key
    "monthly_limit": 1000000,  // 月度限额
    "current_usage": 3000      // 当前用量（自动更新）
  },
  "backup_models": [           // 备份模型列表
    {
      "name": "qwen3.5-turbo",
      "priority": 1,           // 优先级（数字越小越优先）
      "enabled": true          // 是否启用
    }
  ],
  "switch_threshold": 0.8,     // 切换阈值（80%）
  "alert_threshold": 0.75,     // 告警阈值（75%）
  "auto_switch": true          // 是否自动切换
}
```

---

## 🔍 验证安装

**运行测试**:
```bash
cd /home/jiangwu24/.npm-global/lib/node_modules/openclaw/skills/token-manager
python3 scripts/test_token_manager.py
```

**预期输出**:
```
✅ 所有测试通过
```

**检查配置**:
```bash
cat ~/.openclaw/skills/token-manager/config/models.json
```

**预期输出**:
```json
{
  "primary_model": {...},
  "backup_models": [...]
}
```

---

## 💡 最佳实践

### 1. 设置合理限额

```
建议：
- 查看 API 提供商的限额
- 设置为实际限额的 80-90%
- 留有余量防止超限
```

### 2. 配置多个备份

```
推荐配置:
1. qwen3.5-turbo（同 provider，低价）
2. deepseek-chat（不同 provider）
3. glm-4（不同 provider）
```

### 3. 定期检查

```
建议频率:
- 每天：快速查看用量
- 每周：详细统计
- 每月：优化配置
```

---

## 🚨 常见问题

### Q1: 看不到 Token 用量？
**A**: 需要先在 OpenClaw 中启用 Token Manager skill

### Q2: 如何修改限额？
**A**: 编辑 `~/.openclaw/skills/token-manager/config/models.json`

### Q3: 自动切换不工作？
**A**: 检查 `auto_switch` 是否为 `true`

### Q4: 如何关闭自动切换？
**A**: 设置 `auto_switch: false`

---

## 📞 获取帮助

**查看文档**:
```bash
cat /home/jiangwu24/.npm-global/lib/node_modules/openclaw/skills/token-manager/README.md
```

**查看技能说明**:
```bash
cat /home/jiangwu24/.npm-global/lib/node_modules/openclaw/skills/token-manager/SKILL.md
```

**运行测试**:
```bash
python3 /home/jiangwu24/.npm-global/lib/node_modules/openclaw/skills/token-manager/scripts/test_token_manager.py
```

---

## ✅ 检查清单

- [x] Skill 已安装
- [x] 配置文件已创建
- [x] 测试通过
- [ ] 配置 API Key（需要手动）
- [ ] 设置合理的限额
- [ ] 添加备份模型

---

*版本：v1.0*  
*更新时间：2026-03-12 20:59*  
*状态：✅ 已安装，可以使用*
