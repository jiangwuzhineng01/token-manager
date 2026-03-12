#!/bin/bash
# Token Manager 快速配置脚本

echo "======================================================================"
echo "                    🔑 Token Manager 快速配置"
echo "======================================================================"

# 创建配置目录
echo ""
echo "📁 创建配置目录..."
mkdir -p ~/.openclaw/skills/token-manager/config

# 检查是否已有配置
if [ -f ~/.openclaw/skills/token-manager/config/models.json ]; then
    echo "✅ 配置文件已存在"
    echo ""
    echo "查看当前配置:"
    cat ~/.openclaw/skills/token-manager/config/models.json
else
    echo "⚠️  创建新配置文件..."
    
    # 创建默认配置
    cat > ~/.openclaw/skills/token-manager/config/models.json << 'EOF'
{
  "primary_model": {
    "name": "qwen3.5-plus",
    "provider": "bailian",
    "api_key": "sk-your-api-key-here",
    "monthly_limit": 1000000,
    "current_usage": 0
  },
  "backup_models": [
    {
      "name": "qwen3.5-turbo",
      "provider": "bailian",
      "api_key": "sk-backup-key-here",
      "priority": 1,
      "enabled": true
    }
  ],
  "switch_threshold": 0.8,
  "alert_threshold": 0.7,
  "auto_switch": true
}
EOF
    
    echo "✅ 配置文件已创建"
    echo ""
    echo "📝 请编辑配置文件:"
    echo "   nano ~/.openclaw/skills/token-manager/config/models.json"
    echo ""
    echo "需要修改:"
    echo "   1. api_key - 替换为你的真实 API Key"
    echo "   2. monthly_limit - 设置你的月度限额"
    echo "   3. backup_models - 添加备份模型"
fi

# 运行测试
echo ""
echo "======================================================================"
echo "                         🧪 运行测试"
echo "======================================================================"
echo ""

cd /home/jiangwu24/.npm-global/lib/node_modules/openclaw/skills/token-manager
python3 scripts/test_token_manager.py

echo ""
echo "======================================================================"
echo "                         ✅ 配置完成"
echo "======================================================================"
echo ""
echo "📖 使用指南:"
echo "   在 OpenClaw 中说:"
echo "   - '查看 Token 用量'"
echo "   - '切换到备份模型'"
echo "   - '设置 Token 告警阈值'"
echo ""
echo "📝 配置文件:"
echo "   ~/.openclaw/skills/token-manager/config/models.json"
echo ""
echo "📚 文档:"
echo "   README.md"
echo ""
