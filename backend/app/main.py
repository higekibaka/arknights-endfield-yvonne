from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from typing import List, Optional

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.database import EquipmentBuild, SearchLog, SessionLocal, TeamComposition, get_db, init_db
from app.services.seed_data import seed_demo_data_if_empty


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()

    db = SessionLocal()
    try:
        seeded = seed_demo_data_if_empty(db)
    finally:
        db.close()

    if seeded:
        print("✅ 数据库初始化完成，已注入演示数据")
    else:
        print("✅ 数据库初始化完成")

    yield


app = FastAPI(
    title="明日方舟终末地 - 伊冯配队数据API",
    description="提供伊冯角色配队、装备、输出手法等数据的查询接口",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3131"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TeamCompositionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    characters: list
    equipment: Optional[dict]
    rotation: Optional[str]
    source_platform: str
    author: Optional[str]
    rating: float
    views: int
    created_at: datetime
    version: Optional[str]


class EquipmentBuildResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    character_name: str
    weapon_name: Optional[str]
    weapon_stats: Optional[dict]
    artifact_set: Optional[str]
    recommendation_reason: Optional[str]
    created_at: datetime


@app.get("/")
def root():
    return {
        "message": "明日方舟终末地 - 伊冯配队数据API",
        "version": "0.1.0",
        "endpoints": ["/api/teams", "/api/equipment", "/api/search-logs", "/api/stats"],
    }


@app.get("/api/teams", response_model=List[TeamCompositionResponse])
def get_teams(
    platform: Optional[str] = Query(None, description="来源平台过滤"),
    version: Optional[str] = Query(None, description="游戏版本过滤"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    query = db.query(TeamComposition)

    if platform:
        query = query.filter(TeamComposition.source_platform == platform)
    if version:
        query = query.filter(TeamComposition.version == version)

    return query.order_by(TeamComposition.created_at.desc()).offset(offset).limit(limit).all()


@app.get("/api/teams/{team_id}", response_model=TeamCompositionResponse)
def get_team(team_id: int, db: Session = Depends(get_db)):
    team = db.query(TeamComposition).filter(TeamComposition.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="配队未找到")
    return team


@app.get("/api/equipment", response_model=List[EquipmentBuildResponse])
def get_equipment(
    character: Optional[str] = Query(None, description="角色名过滤"),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(EquipmentBuild)

    if character:
        query = query.filter(EquipmentBuild.character_name == character)

    return query.order_by(EquipmentBuild.created_at.desc()).limit(limit).all()


@app.get("/api/search-logs")
def get_search_logs(days: int = Query(7, ge=1, le=30), db: Session = Depends(get_db)):
    since = datetime.utcnow() - timedelta(days=days)
    return db.query(SearchLog).filter(SearchLog.executed_at >= since).all()


@app.get("/api/stats")
def get_stats(db: Session = Depends(get_db)):
    total_teams = db.query(TeamComposition).count()
    total_equipment = db.query(EquipmentBuild).count()

    platform_stats = (
        db.query(TeamComposition.source_platform, func.count(TeamComposition.id).label("count"))
        .group_by(TeamComposition.source_platform)
        .all()
    )

    week_ago = datetime.utcnow() - timedelta(days=7)
    recent_teams = db.query(TeamComposition).filter(TeamComposition.created_at >= week_ago).count()

    return {
        "total_teams": total_teams,
        "total_equipment": total_equipment,
        "recent_teams_7d": recent_teams,
        "platform_distribution": {platform: count for platform, count in platform_stats},
        "last_updated": datetime.utcnow().isoformat(),
    }


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8181, reload=False)
