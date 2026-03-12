#!/usr/bin/env python3
"""
Token Manager 功能演示

演示所有核心功能的实际使用
"""
import sys
import json
import time
from pathlib import Path
from datetime import datetime

# 添加技能路径
skill_path = Path(__file__).parent.parent
sys.path.insert(0, str(skill_path))

from token_manager import TokenManager


def print_header(title: str):
    """打印标题"""
    print("\n" + "="*70)
    print(f" " * (35 - len(title)//2) + title)
    print("="*70 + "\n")


def print_section(title: str):
    """打印小标题"""
    print(f"\n📌 {title}")
    print("-" * 70)


def demo_token_manager():
    """完整功能演示"""
    
    # 创建管理器实例
    manager = TokenManager()
    
    print_header("🔑 Token Manager 功能演示")
    
    # ========== 功能 1: 查看当前配置 ==========
    print_section("功能 1: 查看当前配置")
    
    current_model = manager.get_current_model()
    print(f"""
当前主模型配置:
  📝 名称：{current_model.get('name', 'N/A')}
  🔧 提供商：{current_model.get('provider', 'N/A')}
  💰 月度限额：{current_model.get('monthly_limit', 0):,} tokens
  📊 已用量：{current_model.get('current_usage', 0):,} tokens
  📈 使用率：{current_model.get('current_usage', 0) / current_model.get('monthly_limit', 1) * 100:.2f}%
    """)
    
    time.sleep(1)
    
    # ========== 功能 2: 实时用量监控 ==========
    print_section("功能 2: 实时用量监控")
    
    usage = manager.check_usage()
    print(f"""
Token 使用状态:
  📊 已用：{usage['usage']:,} / {usage['limit']:,} tokens
  📈 使用率：{usage['usage_rate']}%
  ✅ 剩余：{usage['remaining']:,} tokens
  
  告警状态：{'⚠️ 已触发' if usage['alert_reached'] else '✅ 正常'}
  切换状态：{'🔄 需要切换' if usage['threshold_reached'] else '✅ 无需切换'}
    """)
    
    time.sleep(1)
    
    # ========== 功能 3: 模拟 API 调用并记录 ==========
    print_section("功能 3: 记录 API 调用")
    
    print("模拟 3 次 API 调用:")
    
    api_calls = [
        {"model": "qwen3.5-plus", "prompt": 500, "completion": 200},
        {"model": "qwen3.5-plus", "prompt": 800, "completion": 350},
        {"model": "qwen3.5-plus", "prompt": 1200, "completion": 600},
    ]
    
    for i, call in enumerate(api_calls, 1):
        manager.add_usage(call["model"], call["prompt"], call["completion"])
        total = call["prompt"] + call["completion"]
        print(f"  {i}. 调用 {call['model']}: prompt={call['prompt']}, completion={call['completion']}, total={total}")
    
    # 更新后检查用量
    new_usage = manager.check_usage()
    print(f"\n✅ 已更新用量：{new_usage['usage']:,} tokens")
    
    time.sleep(1)
    
    # ========== 功能 4: 使用统计报告 ==========
    print_section("功能 4: 使用统计报告")
    
    stats = manager.get_usage_stats(days=30)
    print(f"""
📊 使用统计报告（最近{stats['period'].split()[1]}天）:

  总请求数：{stats['total_requests']} 次
  总 Token: {stats['total_tokens']:,} tokens
  估算成本：¥{stats['total_cost']}
  日均消耗：{stats['daily_average']:,.0f} tokens/天
  
  按模型统计:
    """)
    
    for model, model_stats in stats.get('by_model', {}).items():
        print(f"    - {model}:")
        print(f"        Token: {model_stats['total_tokens']:,}")
        print(f"        请求数：{model_stats['count']}")
    
    time.sleep(1)
    
    # ========== 功能 5: 告警系统 ==========
    print_section("功能 5: 告警系统")
    
    # 设置告警阈值
    result = manager.set_alert_threshold(0.7)
    print(f"设置告警阈值：{result['message']}")
    
    # 检查告警
    alerts = manager.get_alerts()
    if alerts:
        print("\n⚠️ 当前告警:")
        for alert in alerts:
            print(f"  级别：{alert['level']}")
            print(f"  消息：{alert['message']}")
    else:
        print("\n✅ 无告警 - 用量正常")
    
    time.sleep(1)
    
    # ========== 功能 6: 备份模型管理 ==========
    print_section("功能 6: 备份模型管理")
    
    # 查看备份模型
    backups = manager.get_backup_models()
    print("当前备份模型:")
    if backups:
        for i, backup in enumerate(backups, 1):
            print(f"  {i}. {backup.get('name')} (优先级：{backup.get('priority')}, 状态：{'✅' if backup.get('enabled') else '❌'})")
    else:
        print("  暂无备份模型")
    
    # 添加新备份模型
    print("\n添加新的备份模型:")
    new_backup = {
        "name": "deepseek-chat",
        "provider": "deepseek",
        "api_key": "sk-deepseek-key",
        "priority": 2,
        "enabled": True
    }
    result = manager.add_backup_model(new_backup)
    print(f"  {result['message']}")
    
    time.sleep(1)
    
    # ========== 功能 7: 自动切换演示 ==========
    print_section("功能 7: 自动模型切换演示")
    
    print("当前状态:")
    current = manager.get_current_model()
    print(f"  主模型：{current.get('name')}")
    
    # 模拟达到阈值
    print("\n模拟用量达到 80%...")
    manager.config["primary_model"]["current_usage"] = int(
        manager.config["primary_model"]["monthly_limit"] * 0.85
    )
    manager._save_config()
    
    # 检查是否需要切换
    if manager.should_switch_model():
        print("  ✅ 检测到用量达到阈值（85%）")
        print("  🔄 开始切换到备份模型...")
        
        # 执行切换
        switch_result = manager.switch_to_backup()
        
        print(f"\n  {switch_result['message']}")
        print(f"  切换时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        print("  ℹ️  未达到切换阈值")
    
    time.sleep(1)
    
    # ========== 功能 8: 恢复原始配置 ==========
    print_section("功能 8: 恢复演示配置")
    
    # 重置用量
    manager.config["primary_model"]["current_usage"] = 3000
    manager._save_config()
    print("✅ 已恢复演示配置")
    
    time.sleep(1)
    
    # ========== 总结 ==========
    print_header("✨ 演示完成")
    
    print("""
📋 演示功能总结:

  ✅ 1. 查看当前配置
  ✅ 2. 实时用量监控
  ✅ 3. 记录 API 调用
  ✅ 4. 使用统计报告
  ✅ 5. 告警系统
  ✅ 6. 备份模型管理
  ✅ 7. 自动模型切换
  ✅ 8. 配置管理

💡 在 OpenClaw 中使用:

  查看用量：'查看 Token 用量'
  切换模型：'切换到备份模型'
  设置告警：'设置 Token 告警阈值为 80%'
  添加模型：'添加备份模型 deepseek-chat'

📝 配置文件:

  ~/.openclaw/skills/token-manager/config/models.json

📚 更多文档:

  QUICKSTART.md - 快速上手
  README.md - 完整教程
    """)


if __name__ == '__main__':
    demo_token_manager()
