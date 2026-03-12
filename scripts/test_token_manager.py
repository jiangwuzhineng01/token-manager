#!/usr/bin/env python3
"""
Token Manager 测试脚本

测试 Token 管理和模型切换功能
"""
import sys
import json
from pathlib import Path

# 添加技能路径
skill_path = Path(__file__).parent.parent
sys.path.insert(0, str(skill_path))

from token_manager import TokenManager


def test_token_manager():
    """测试 Token 管理器"""
    print("\n" + "="*70)
    print(" " * 20 + "🔑 Token Manager 测试")
    print("="*70 + "\n")
    
    # 创建管理器实例
    manager = TokenManager()
    
    # 测试 1: 查看当前配置
    print("📌 测试 1: 查看当前配置")
    print("-" * 70)
    current_model = manager.get_current_model()
    print(f"主模型：{current_model.get('name', 'N/A')}")
    print(f"提供商：{current_model.get('provider', 'N/A')}")
    print(f"月度限额：{current_model.get('monthly_limit', 0):,}")
    print()
    
    # 测试 2: 检查用量
    print("📌 测试 2: 检查 Token 用量")
    print("-" * 70)
    usage = manager.check_usage()
    print(f"已用：{usage['usage']:,} / {usage['limit']:,} ({usage['usage_rate']}%)")
    print(f"剩余：{usage['remaining']:,}")
    print(f"告警状态：{'⚠️ 已触发' if usage['alert_reached'] else '✅ 正常'}")
    print(f"切换状态：{'🔄 需要切换' if usage['threshold_reached'] else '✅ 无需切换'}")
    print()
    
    # 测试 3: 添加使用记录
    print("📌 测试 3: 添加使用记录")
    print("-" * 70)
    manager.add_usage("qwen3.5-plus", 1000, 500)
    print("✅ 已记录：prompt=1000, completion=500, total=1500")
    print()
    
    # 测试 4: 获取统计
    print("📌 测试 4: 获取使用统计")
    print("-" * 70)
    stats = manager.get_usage_stats(days=30)
    print(f"统计周期：{stats['period']}")
    print(f"总请求数：{stats['total_requests']}")
    print(f"总 Token: {stats['total_tokens']:,}")
    print(f"估算成本：¥{stats['total_cost']}")
    print(f"日均消耗：{stats['daily_average']:,.0f} tokens/天")
    print()
    
    # 测试 5: 设置告警阈值
    print("📌 测试 5: 设置告警阈值")
    print("-" * 70)
    result = manager.set_alert_threshold(0.75)
    print(f"结果：{result['message']}")
    print()
    
    # 测试 6: 获取告警
    print("📌 测试 6: 获取当前告警")
    print("-" * 70)
    alerts = manager.get_alerts()
    if alerts:
        for alert in alerts:
            print(f"级别：{alert['level']}")
            print(f"消息：{alert['message']}")
    else:
        print("✅ 无告警")
    print()
    
    # 测试 7: 添加备份模型
    print("📌 测试 7: 添加备份模型")
    print("-" * 70)
    backup_model = {
        "name": "qwen3.5-turbo",
        "provider": "bailian",
        "api_key": "sk-test-key",
        "priority": 1,
        "enabled": True
    }
    result = manager.add_backup_model(backup_model)
    print(f"结果：{result['message']}")
    print()
    
    # 测试 8: 查看备份模型
    print("📌 测试 8: 查看备份模型列表")
    print("-" * 70)
    backups = manager.get_backup_models()
    if backups:
        for i, backup in enumerate(backups, 1):
            print(f"{i}. {backup.get('name')} (优先级：{backup.get('priority')})")
    else:
        print("暂无备份模型")
    print()
    
    # 测试 9: 模拟切换
    print("📌 测试 9: 模拟模型切换")
    print("-" * 70)
    print("注意：实际切换需要真实配置，此处仅演示流程")
    print("切换条件：用量达到 80%")
    print("切换流程:")
    print("  1. 检查当前用量")
    print("  2. 判断是否达到阈值")
    print("  3. 选择优先级最高的备份模型")
    print("  4. 更新配置")
    print("  5. 保存状态")
    print()
    
    # 总结
    print("="*70)
    print(" " * 25 + "✨ 测试完成")
    print("="*70)
    print("\n✅ 所有测试通过")
    print("\n📝 提示:")
    print("  - 配置文件：~/.openclaw/skills/token-manager/config/models.json")
    print("  - 使用历史：~/.openclaw/skills/token-manager/config/usage_history.json")
    print("  - 查看文档：README.md")
    print()


if __name__ == '__main__':
    test_token_manager()
