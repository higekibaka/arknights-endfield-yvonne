from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import asyncio
import re

class WebScraper:
    """网页抓取服务 - 使用Playwright"""
    
    def __init__(self):
        self.playwright = None
        self.browser = None
    
    async def init(self):
        """初始化浏览器"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)
    
    async def close(self):
        """关闭浏览器"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
    
    async def fetch_bilibili(self, keyword: str = "明日方舟终末地 伊冯") -> List[Dict]:
        """抓取B站搜索结果"""
        if not self.browser:
            await self.init()
        
        page = await self.browser.new_page()
        try:
            search_url = f"https://search.bilibili.com/all?keyword={keyword.replace(' ', '+')}"
            await page.goto(search_url, wait_until="networkidle")
            
            # 等待内容加载
            await page.wait_for_selector(".video-list-item, .bili-video-card", timeout=10000)
            
            content = await page.content()
            soup = BeautifulSoup(content, 'html.parser')
            
            results = []
            # B站搜索结果解析
            items = soup.select('.video-list-item, .bili-video-card')
            for item in items[:10]:  # 只取前10条
                try:
                    title_elem = item.select_one('.bili-video-card__info--tit a, .title')
                    author_elem = item.select_one('.bili-video-card__info--author, .up-name')
                    
                    if title_elem:
                        results.append({
                            "platform": "B站",
                            "title": title_elem.get_text(strip=True),
                            "url": "https:" + title_elem.get('href', '') if title_elem.get('href', '').startswith('//') else title_elem.get('href', ''),
                            "author": author_elem.get_text(strip=True) if author_elem else "未知",
                            "type": "video"
                        })
                except Exception as e:
                    print(f"解析B站条目失败: {e}")
                    continue
            
            return results
        finally:
            await page.close()
    
    async def fetch_nga(self, keyword: str = "终末地 伊冯") -> List[Dict]:
        """抓取NGA论坛搜索结果"""
        # NGA需要特殊处理，可能需要登录
        # 这里使用搜索API或简化版本
        return []
    
    async def fetch_senkonjima(self) -> List[Dict]:
        """抓取森空岛数据"""
        # 森空岛可能需要API token
        return []
    
    def parse_team_composition(self, content: str) -> Optional[Dict]:
        """从内容中解析配队信息"""
        # 使用正则提取角色、装备等信息
        patterns = {
            "characters": r"([\u4e00-\u9fa5]{2,4})\s*[+/＋]\s*([\u4e00-\u9fa5]{2,4})",
            "weapons": r"武器[:：]\s*([\u4e00-\u9fa5]+)",
            "rotation": r"输出手法[:：]([\s\S]+?)(?=\n\n|\Z)"
        }
        
        result = {}
        for key, pattern in patterns.items():
            matches = re.findall(pattern, content)
            if matches:
                result[key] = matches
        
        return result if result else None

# 单例
_scraper: Optional[WebScraper] = None

def get_scraper() -> WebScraper:
    global _scraper
    if _scraper is None:
        _scraper = WebScraper()
    return _scraper
