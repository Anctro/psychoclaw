#!/usr/bin/env python3
"""
心理健康测评记录管理脚本
用法：
  python3 record-manager.py list  # 列出所有测评记录
  python3 record-manager.py stat  # 统计测评情况
"""
import sys
from pathlib import Path
from collections import defaultdict

RECORD_PATH = Path("/Users/ange/.openclaw/workspace/mentalhealth.md")

def load_records():
    """加载所有测评记录"""
    if not RECORD_PATH.exists():
        return []
    
    content = RECORD_PATH.read_text(encoding="utf-8")
    records = []
    current_record = {}
    
    for line in content.split("\n"):
        if line.startswith("## "):
            if current_record:
                records.append(current_record)
            time_str, scale_name = line[3:].split(" - ", 1)
            current_record = {
                "time": time_str.strip(),
                "scale_name": scale_name.strip()
            }
        elif line.startswith("- 总分："):
            current_record["total_score"] = line.split("：")[1].strip()
        elif line.startswith("- 等级："):
            current_record["level"] = line.split("：")[1].strip()
        elif line.startswith("- 摘要："):
            current_record["summary"] = line.split("：")[1].strip()
        elif line.startswith("- 建议："):
            current_record["suggestion"] = line.split("：")[1].strip()
    
    if current_record:
        records.append(current_record)
    
    return records

def list_records():
    """列出所有测评记录"""
    records = load_records()
    if not records:
        print("暂无测评记录")
        return
    
    print("="*80)
    print(f"📝 共有 {len(records)} 条测评记录")
    print("="*80)
    for idx, record in enumerate(records, 1):
        print(f"{idx}. [{record['time']}] {record['scale_name']}")
        print(f"   总分：{record['total_score']} | 等级：{record['level']}")
        print(f"   摘要：{record['summary']}")
        print(f"   建议：{record['suggestion']}")
        print("-"*80)

def show_statistics():
    """显示统计信息"""
    records = load_records()
    if not records:
        print("暂无测评记录，无法统计")
        return
    
    # 按量表统计
    scale_count = defaultdict(int)
    level_count = defaultdict(int)
    
    for record in records:
        scale_count[record["scale_name"]] += 1
        level_count[record["level"]] += 1
    
    print("="*60)
    print("📊 测评统计")
    print("="*60)
    print(f"总测评次数：{len(records)}")
    print("\n🔍 各量表使用次数：")
    for scale, count in scale_count.items():
        print(f"  {scale}：{count}次")
    
    print("\n⚠️  风险等级分布：")
    for level, count in level_count.items():
        print(f"  {level}：{count}次")
    
    # 最近一次测评
    latest = records[-1]
    print("\n🕒 最近一次测评：")
    print(f"  时间：{latest['time']}")
    print(f"  量表：{latest['scale_name']}")
    print(f"  等级：{latest['level']}")
    print(f"  摘要：{latest['summary']}")

def main():
    if len(sys.argv) < 2:
        print("用法：")
        print("  python3 record-manager.py list  # 列出所有测评记录")
        print("  python3 record-manager.py stat  # 统计测评情况")
        sys.exit(1)
    
    command = sys.argv[1]
    if command == "list":
        list_records()
    elif command == "stat":
        show_statistics()
    else:
        print("未知命令，支持的命令：list, stat")
        sys.exit(1)

if __name__ == "__main__":
    main()
