from datetime import datetime
from pathlib import Path

from sqlalchemy import JSON, Column, DateTime, Float, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class TeamComposition(Base):
    """配队组合表"""

    __tablename__ = "team_compositions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    characters = Column(JSON, nullable=False)  # [{"name": "伊冯", "role": "主C"}, ...]
    equipment = Column(JSON)  # {"weapon": "...", "artifacts": "..."}
    rotation = Column(Text)  # 输出手法/连招
    source_url = Column(String(500))
    source_platform = Column(String(50))  # B站, NGA, 森空岛
    author = Column(String(100))
    rating = Column(Float, default=0)  # 评分 0-5
    views = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    version = Column(String(20))  # 游戏版本


class EquipmentBuild(Base):
    """装备配置表"""

    __tablename__ = "equipment_builds"

    id = Column(Integer, primary_key=True, index=True)
    character_name = Column(String(50), nullable=False)
    weapon_name = Column(String(100))
    weapon_stats = Column(JSON)
    artifact_set = Column(String(100))
    artifact_main_stats = Column(JSON)
    artifact_sub_stats = Column(JSON)
    recommendation_reason = Column(Text)
    source_url = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)


class SearchLog(Base):
    """搜索日志表"""

    __tablename__ = "search_logs"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String(50), nullable=False)
    keyword = Column(String(200), nullable=False)
    results_count = Column(Integer, default=0)
    new_items_count = Column(Integer, default=0)
    executed_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default="pending")  # pending, success, failed
    error_message = Column(Text)


BASE_DIR = Path(__file__).resolve().parents[3]
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "arknights_endfield.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

DATA_DIR.mkdir(parents=True, exist_ok=True)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
