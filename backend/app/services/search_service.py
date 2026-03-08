import httpx
import os
from typing import List, Dict, Optional
from datetime import datetime

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
TAVILY_BASE_URL = "https://api.tavily.com"

class SearchService:
    """搜索服务 - 使用Tavily API"""
    
    def __init__(self):
        self.api_key = TAVILY_API_KEY
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def search(self, query: str, max_results: int = 10, topic: str = "general") -> Dict:
        """
        执行搜索
        
        Args:
            query: 搜索关键词
            max_results: 最大结果数
            topic: general 或 news
        """
        if not self.api_key:
            raise ValueError("TAVILY_API_KEY 未设置")
        
        url = f"{TAVILY_BASE_URL}/search"
        payload = {
            "api_key": self.api_key,
            "query": query,
            "max_results": max_results,
            "topic": topic,
            "include_answer": True,
            "include_raw_content": False,
            "search_depth": "advanced"  # basic 或 advanced
        }
        
        response = await self.client.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    
    async def search_yvonne_teams(self) -> List[Dict]:
        """搜索伊冯配队相关数据"""
        queries = [
            "明日方舟终末地 伊冯 配队",
            "Arknights Endfield Yvonne team composition",
            "终末地 伊冯 阵容搭配",
            "伊冯 输出手法 终末地"
        ]
        
        all_results = []
        for query in queries:
            try:
                result = await self.search(query, max_results=5)
                all_results.append({
                    "query": query,
                    "results": result.get("results", []),
                    "answer": result.get("answer", "")
                })
            except Exception as e:
                print(f"搜索失败 [{query}]: {e}")
        
        return all_results
    
    async def extract_content(self, url: str) -> Dict:
        """从URL提取内容"""
        extract_url = f"{TAVILY_BASE_URL}/extract"
        payload = {
            "api_key": self.api_key,
            "urls": [url]
        }
        
        response = await self.client.post(extract_url, json=payload)
        response.raise_for_status()
        return response.json()
    
    async def close(self):
        await self.client.aclose()

# 单例实例
_search_service: Optional[SearchService] = None

def get_search_service() -> SearchService:
    global _search_service
    if _search_service is None:
        _search_service = SearchService()
    return _search_service
