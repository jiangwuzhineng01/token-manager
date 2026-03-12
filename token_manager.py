"""
OpenClaw Token 管理与 API 监控

功能:
- 监控 API Token 使用量
- 自动切换到备份模型
- 生成使用统计报告
"""
import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import asyncio


@dataclass
class ModelConfig:
    """模型配置"""
    name: str
    provider: str
    api_key: str
    monthly_limit: int = 1000000
    current_usage: int = 0
    priority: int = 0
    enabled: bool = True
    last_switch_time: Optional[str] = None


@dataclass
class TokenUsage:
    """Token 使用记录"""
    model: str
    timestamp: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cost: float = 0.0


class TokenManager:
    """Token 管理器"""
    
    def __init__(self, config_path: str = None):
        """
        初始化 Token 管理器
        
        Args:
            config_path: 配置文件路径
        """
        if config_path is None:
            config_path = Path.home() / ".openclaw" / "skills" / "token-manager" / "config" / "models.json"
        
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.usage_history = self._load_usage_history()
    
    def _load_config(self) -> Dict:
        """加载配置"""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # 返回默认配置
        return {
            "primary_model": {
                "name": "qwen3.5-plus",
                "provider": "bailian",
                "api_key": "",
                "monthly_limit": 1000000,
                "current_usage": 0
            },
            "backup_models": [],
            "switch_threshold": 0.8,
            "alert_threshold": 0.7,
            "auto_switch": True
        }
    
    def _save_config(self):
        """保存配置"""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def _load_usage_history(self) -> List[Dict]:
        """加载使用历史"""
        history_path = self.config_path.parent / "usage_history.json"
        if history_path.exists():
            with open(history_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def _save_usage_history(self):
        """保存使用历史"""
        history_path = self.config_path.parent / "usage_history.json"
        with open(history_path, 'w', encoding='utf-8') as f:
            json.dump(self.usage_history, f, ensure_ascii=False, indent=2)
    
    def get_current_model(self) -> Dict:
        """获取当前使用的模型"""
        return self.config.get("primary_model", {})
    
    def get_backup_models(self) -> List[Dict]:
        """获取备份模型列表"""
        return self.config.get("backup_models", [])
    
    def check_usage(self) -> Dict:
        """
        检查 Token 使用情况
        
        Returns:
            使用状态字典
        """
        primary = self.config.get("primary_model", {})
        limit = primary.get("monthly_limit", 1000000)
        usage = primary.get("current_usage", 0)
        
        usage_rate = usage / limit if limit > 0 else 0
        
        return {
            "model": primary.get("name", "unknown"),
            "usage": usage,
            "limit": limit,
            "usage_rate": round(usage_rate * 100, 2),
            "remaining": limit - usage,
            "threshold_reached": usage_rate >= self.config.get("switch_threshold", 0.8),
            "alert_reached": usage_rate >= self.config.get("alert_threshold", 0.7)
        }
    
    def should_switch_model(self) -> bool:
        """
        判断是否应该切换模型
        
        Returns:
            是否应该切换
        """
        usage_status = self.check_usage()
        return usage_status["threshold_reached"] and self.config.get("auto_switch", True)
    
    def switch_to_backup(self) -> Dict:
        """
        切换到备份模型
        
        Returns:
            切换结果
        """
        backup_models = self.get_backup_models()
        
        if not backup_models:
            return {
                "success": False,
                "message": "没有配置备份模型"
            }
        
        # 获取当前主模型
        current_primary = self.config.get("primary_model", {})
        
        # 找到优先级最高的可用备份模型
        available_backup = None
        for backup in sorted(backup_models, key=lambda x: x.get("priority", 999)):
            if backup.get("enabled", True):
                available_backup = backup
                break
        
        if not available_backup:
            return {
                "success": False,
                "message": "没有可用的备份模型"
            }
        
        # 保存当前主模型到历史
        current_primary["last_switch_time"] = datetime.now().isoformat()
        
        # 将当前主模型设为备份
        if "backup_models" not in self.config:
            self.config["backup_models"] = []
        self.config["backup_models"].append(current_primary)
        
        # 将备份模型设为主模型
        self.config["primary_model"] = available_backup
        
        # 从备份列表移除
        self.config["backup_models"] = [
            m for m in self.config["backup_models"]
            if m.get("name") != available_backup.get("name")
        ]
        
        # 保存配置
        self._save_config()
        
        return {
            "success": True,
            "message": f"已从 {current_primary.get('name')} 切换到 {available_backup.get('name')}",
            "previous_model": current_primary.get("name"),
            "current_model": available_backup.get("name")
        }
    
    def add_usage(self, model: str, prompt_tokens: int, completion_tokens: int):
        """
        添加使用记录
        
        Args:
            model: 模型名称
            prompt_tokens: 输入 Token 数
            completion_tokens: 输出 Token 数
        """
        total_tokens = prompt_tokens + completion_tokens
        
        # 更新当前使用量
        if model == self.config.get("primary_model", {}).get("name"):
            self.config["primary_model"]["current_usage"] += total_tokens
            self._save_config()
        
        # 记录使用历史
        usage_record = {
            "model": model,
            "timestamp": datetime.now().isoformat(),
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens
        }
        
        self.usage_history.append(usage_record)
        self._save_usage_history()
    
    def get_usage_stats(self, days: int = 30) -> Dict:
        """
        获取使用统计
        
        Args:
            days: 统计天数
            
        Returns:
            统计信息
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # 过滤指定时间范围内的记录
        recent_usage = [
            record for record in self.usage_history
            if datetime.fromisoformat(record["timestamp"]) >= cutoff_date
        ]
        
        # 按模型分组统计
        stats_by_model = {}
        for record in recent_usage:
            model = record["model"]
            if model not in stats_by_model:
                stats_by_model[model] = {
                    "total_tokens": 0,
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "count": 0
                }
            
            stats_by_model[model]["total_tokens"] += record["total_tokens"]
            stats_by_model[model]["prompt_tokens"] += record["prompt_tokens"]
            stats_by_model[model]["completion_tokens"] += record["completion_tokens"]
            stats_by_model[model]["count"] += 1
        
        # 计算总统计
        total_tokens = sum(s["total_tokens"] for s in stats_by_model.values())
        total_cost = self._estimate_cost(stats_by_model)
        
        return {
            "period": f"Last {days} days",
            "total_tokens": total_tokens,
            "total_requests": len(recent_usage),
            "total_cost": total_cost,
            "by_model": stats_by_model,
            "daily_average": total_tokens / days if days > 0 else 0
        }
    
    def _estimate_cost(self, stats: Dict) -> float:
        """
        估算成本
        
        Args:
            stats: 使用统计
            
        Returns:
            估算成本（元）
        """
        # 简化成本估算（实际应根据不同模型定价）
        cost_per_1k_tokens = 0.01  # 假设每 1k tokens 0.01 元
        
        total_cost = 0.0
        for model, model_stats in stats.items():
            tokens = model_stats["total_tokens"]
            total_cost += (tokens / 1000) * cost_per_1k_tokens
        
        return round(total_cost, 2)
    
    def set_alert_threshold(self, threshold: float):
        """
        设置告警阈值
        
        Args:
            threshold: 阈值（0-1 之间）
        """
        if 0 < threshold < 1:
            self.config["alert_threshold"] = threshold
            self._save_config()
            return {"success": True, "message": f"告警阈值已设置为 {threshold*100}%"}
        return {"success": False, "message": "阈值必须在 0-1 之间"}
    
    def add_backup_model(self, model_config: Dict) -> Dict:
        """
        添加备份模型
        
        Args:
            model_config: 模型配置
            
        Returns:
            添加结果
        """
        if "backup_models" not in self.config:
            self.config["backup_models"] = []
        
        # 检查是否已存在
        existing = [
            m for m in self.config["backup_models"]
            if m.get("name") == model_config.get("name")
        ]
        
        if existing:
            return {"success": False, "message": "该模型已存在"}
        
        self.config["backup_models"].append(model_config)
        self._save_config()
        
        return {"success": True, "message": f"已添加备份模型 {model_config.get('name')}"}
    
    def get_alerts(self) -> List[Dict]:
        """
        获取当前告警
        
        Returns:
            告警列表
        """
        alerts = []
        usage_status = self.check_usage()
        
        if usage_status["alert_reached"]:
            alerts.append({
                "type": "usage_warning",
                "level": "warning" if not usage_status["threshold_reached"] else "critical",
                "message": f"Token 用量已达到 {usage_status['usage_rate']}%",
                "usage": usage_status["usage"],
                "limit": usage_status["limit"]
            })
        
        return alerts


# 全局实例
_token_manager = None

def get_token_manager() -> TokenManager:
    """获取 Token 管理器实例"""
    global _token_manager
    if _token_manager is None:
        _token_manager = TokenManager()
    return _token_manager
