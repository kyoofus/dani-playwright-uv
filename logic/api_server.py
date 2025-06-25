from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, List, Any
import asyncio
import logging
from naver_real_estate_crawler import NaverRealEstateCrawler

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="네이버 부동산 크롤링 API")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CrawlRequest(BaseModel):
    center_lat: float
    center_lon: float
    radius: Optional[float] = 0.003
    real_estate_type: Optional[str] = "APT:ABYG:JGC:PRE"
    price_type: Optional[str] = "RETAIL"

class CrawlResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

@app.get("/")
async def root():
    return {"message": "네이버 부동산 크롤링 API 서버"}

@app.post("/api/crawl", response_model=CrawlResponse)
async def crawl_real_estate(request: CrawlRequest):
    """부동산 정보를 크롤링합니다."""
    crawler = NaverRealEstateCrawler()
    
    try:
        logger.info(f"크롤링 시작: lat={request.center_lat}, lon={request.center_lon}")
        
        # 브라우저 및 세션 초기화
        await crawler.init_browser(headless=True)
        await crawler.init_session()
        
        # 지역 크롤링 실행
        data = await crawler.crawl_area(
            center_lat=request.center_lat,
            center_lon=request.center_lon,
            radius=request.radius
        )
        
        logger.info("크롤링 완료")
        return CrawlResponse(success=True, data=data)
        
    except Exception as e:
        logger.error(f"크롤링 중 오류: {e}")
        return CrawlResponse(success=False, error=str(e))
        
    finally:
        await crawler.close()

@app.post("/api/complexes", response_model=CrawlResponse)
async def get_complexes(request: CrawlRequest):
    """단지 정보만 가져옵니다."""
    crawler = NaverRealEstateCrawler()
    
    try:
        await crawler.init_browser(headless=True)
        await crawler.init_session()
        
        # 좌표 범위 계산
        left_lon = request.center_lon - request.radius
        right_lon = request.center_lon + request.radius
        top_lat = request.center_lat + request.radius
        bottom_lat = request.center_lat - request.radius
        
        # 단지 정보만 수집
        complexes = await crawler.get_complexes_data(
            left_lon=left_lon,
            right_lon=right_lon,
            top_lat=top_lat,
            bottom_lat=bottom_lat,
            real_estate_type=request.real_estate_type,
            price_type=request.price_type
        )
        
        data = {
            "complexes": complexes,
            "count": len(complexes)
        }
        
        return CrawlResponse(success=True, data=data)
        
    except Exception as e:
        logger.error(f"단지 정보 수집 중 오류: {e}")
        return CrawlResponse(success=False, error=str(e))
        
    finally:
        await crawler.close()

@app.get("/api/complex/{complex_no}", response_model=CrawlResponse)
async def get_complex_detail(complex_no: str):
    """특정 단지의 상세 정보를 가져옵니다."""
    crawler = NaverRealEstateCrawler()
    
    try:
        await crawler.init_browser(headless=True)
        await crawler.init_session()
        
        detail = await crawler.get_complex_detail(complex_no)
        
        if detail:
            return CrawlResponse(success=True, data=detail)
        else:
            return CrawlResponse(success=False, error="단지 정보를 찾을 수 없습니다")
            
    except Exception as e:
        logger.error(f"단지 상세 정보 수집 중 오류: {e}")
        return CrawlResponse(success=False, error=str(e))
        
    finally:
        await crawler.close()

@app.get("/api/complex/{complex_no}/articles", response_model=CrawlResponse)
async def get_complex_articles(complex_no: str, trade_type: str = "A1"):
    """특정 단지의 매물 정보를 가져옵니다."""
    crawler = NaverRealEstateCrawler()
    
    try:
        await crawler.init_browser(headless=True)
        await crawler.init_session()
        
        articles = await crawler.get_complex_articles(complex_no, trade_type)
        
        data = {
            "articles": articles,
            "count": len(articles),
            "complex_no": complex_no,
            "trade_type": trade_type
        }
        
        return CrawlResponse(success=True, data=data)
        
    except Exception as e:
        logger.error(f"매물 정보 수집 중 오류: {e}")
        return CrawlResponse(success=False, error=str(e))
        
    finally:
        await crawler.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
