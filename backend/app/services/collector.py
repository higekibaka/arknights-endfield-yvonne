from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import asyncio
from app.services.search_service import get_search_service
from app.services.scraper import get_scraper

class DataCollector:
    """数据收集器 - 定时任务"""
    
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.search_service = get_search_service()
        self.scraper = get_scraper()
    
    async def collect_daily(self):
        """每日数据收集任务"""
        print(f"[{datetime.now()}] 开始执行每日数据收集...")
        
        try:
            # 1. Tavily搜索
            search_results = await self.search_service.search_yvonne_teams()
            print(f"✅ Tavily搜索完成，获取 {len(search_results)} 组结果")
            
            # 2. B站抓取
            bilibili_results = await self.scraper.fetch_bilibili()
            print(f"✅ B站抓取完成，获取 {len(bilibili_results)} 条视频")
            
            # TODO: 数据清洗与存储
            # 这里需要将结果保存到数据库
            
            print(f"[{datetime.now()}] 数据收集完成！")
            
        except Exception as e:
            print(f"❌ 数据收集失败: {e}")
    
    def start_scheduler(self):
        """启动定时任务"""
        # 每天早上8点执行
        self.scheduler.add_job(
            self._run_collect,
            CronTrigger(hour=8, minute=0),
            id="daily_collect",
            name="每日伊冯配队数据收集",
            replace_existing=True
        )
        
        self.scheduler.start()
        print("✅ 定时任务已启动，每天 08:00 执行")
    
    def _run_collect(self):
        """运行收集任务（同步包装）"""
        asyncio.run(self.collect_daily())
    
    def stop_scheduler(self):
        """停止定时任务"""
        self.scheduler.shutdown()
        print("✅ 定时任务已停止")

# 全局实例
collector = DataCollector()
