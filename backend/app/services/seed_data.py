from __future__ import annotations

from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.database import EquipmentBuild, SearchLog, TeamComposition


DEMO_TEAMS = [
    {
        "name": "伊冯·高压速切队（通用开荒）",
        "characters": [
            {"name": "伊冯", "role": "主C"},
            {"name": "赫德利", "role": "副C"},
            {"name": "铃兰", "role": "增伤辅助"},
            {"name": "可露希尔", "role": "生存/护盾"},
        ],
        "equipment": {
            "weapon": "霓光短弧",
            "artifacts": "双暴优先 + 攻速模块",
            "notes": "适合主线与资源本，循环稳定",
        },
        "rotation": "开局可露希尔护盾 → 铃兰挂易伤 → 伊冯E爆发 → 赫德利补刀收尾。",
        "source_url": "https://www.bilibili.com/video/BV1yvDemo",
        "source_platform": "B站",
        "author": "终末地攻略组",
        "rating": 4.7,
        "views": 3250,
        "version": "CBT-0.3",
        "created_at": datetime.utcnow() - timedelta(days=2),
    },
    {
        "name": "伊冯·持续输出队（Boss向）",
        "characters": [
            {"name": "伊冯", "role": "主C"},
            {"name": "芙蓉", "role": "治疗"},
            {"name": "风丸", "role": "减抗辅助"},
            {"name": "塞希尔", "role": "破甲"},
        ],
        "equipment": {
            "weapon": "湮灭电磁枪",
            "artifacts": "攻击力套 + 技能增幅",
            "notes": "对单高压，适合周常Boss",
        },
        "rotation": "风丸先手减抗 → 塞希尔破甲 → 伊冯长轴输出，芙蓉穿插保命抬血。",
        "source_url": "https://ngabbs.com/read.php?tid=demo_yvonne_1",
        "source_platform": "NGA",
        "author": "NGA-夜航星",
        "rating": 4.5,
        "views": 1980,
        "version": "CBT-0.3",
        "created_at": datetime.utcnow() - timedelta(days=5),
    },
    {
        "name": "伊冯·低配平民队（材料本）",
        "characters": [
            {"name": "伊冯", "role": "主C"},
            {"name": "米娅", "role": "聚怪"},
            {"name": "安洁", "role": "增益"},
            {"name": "罗伊", "role": "副坦"},
        ],
        "equipment": {
            "weapon": "标准突击刃",
            "artifacts": "命中/能量回复混搭",
            "notes": "成型快，容错高",
        },
        "rotation": "米娅聚怪起手 → 安洁上攻速 → 伊冯AOE清场 → 罗伊补位抗伤。",
        "source_url": "https://www.senkongdao.com/topic/demo-yvonne",
        "source_platform": "森空岛",
        "author": "岛民-灰烬",
        "rating": 4.3,
        "views": 1420,
        "version": "CBT-0.2",
        "created_at": datetime.utcnow() - timedelta(days=1),
    },
]

DEMO_EQUIPMENT = [
    {
        "character_name": "伊冯",
        "weapon_name": "霓光短弧",
        "weapon_stats": {"attack": 612, "crit_rate": "18%", "energy_regen": "12%"},
        "artifact_set": "疾速猎手 4件",
        "artifact_main_stats": {"head": "暴击率", "body": "攻击力%", "legs": "攻速%"},
        "artifact_sub_stats": ["暴击伤害", "攻击力", "技能急速"],
        "recommendation_reason": "覆盖最常见开荒与速刷场景，手感与伤害平衡。",
        "source_url": "https://www.bilibili.com/video/BV1equipDemo",
        "created_at": datetime.utcnow() - timedelta(days=2),
    },
    {
        "character_name": "伊冯",
        "weapon_name": "湮灭电磁枪",
        "weapon_stats": {"attack": 655, "crit_damage": "34%", "skill_amp": "10%"},
        "artifact_set": "崩解协同 2+2",
        "artifact_main_stats": {"head": "暴击伤害", "body": "攻击力%", "legs": "技能增幅"},
        "artifact_sub_stats": ["暴击率", "攻击力", "穿透"],
        "recommendation_reason": "对单Boss上限更高，配合破甲辅助表现稳定。",
        "source_url": "https://ngabbs.com/read.php?tid=demo_equip_2",
        "created_at": datetime.utcnow() - timedelta(days=4),
    },
]

DEMO_SEARCH_LOGS = [
    {
        "platform": "B站",
        "keyword": "明日方舟终末地 伊冯 配队",
        "results_count": 18,
        "new_items_count": 3,
        "status": "success",
        "executed_at": datetime.utcnow() - timedelta(hours=18),
    },
    {
        "platform": "NGA",
        "keyword": "终末地 伊冯 阵容",
        "results_count": 9,
        "new_items_count": 2,
        "status": "success",
        "executed_at": datetime.utcnow() - timedelta(hours=7),
    },
]


def seed_demo_data_if_empty(db: Session) -> bool:
    """数据库为空时写入最小演示数据。

    Returns:
        bool: 是否执行了写入
    """
    has_team_data = db.query(TeamComposition.id).first() is not None
    has_equipment_data = db.query(EquipmentBuild.id).first() is not None
    has_log_data = db.query(SearchLog.id).first() is not None

    if has_team_data and has_equipment_data and has_log_data:
        return False

    if not has_team_data:
        db.add_all([TeamComposition(**item) for item in DEMO_TEAMS])

    if not has_equipment_data:
        db.add_all([EquipmentBuild(**item) for item in DEMO_EQUIPMENT])

    if not has_log_data:
        db.add_all([SearchLog(**item) for item in DEMO_SEARCH_LOGS])

    db.commit()
    return True
