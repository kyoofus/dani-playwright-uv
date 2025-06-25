import asyncio
import json
import time
from typing import List, Dict, Optional
from urllib.parse import urlencode
import aiohttp
import pandas as pd
from playwright.async_api import async_playwright, Page, Browser
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NaverRealEstateCrawler:
    """네이버 부동산 크롤러"""
    
    def __init__(self):
        self.base_url = "https://new.land.naver.com"
        self.session = None
        self.browser = None
        self.page = None
        
    async def init_browser(self, headless: bool = True):
        """브라우저 초기화"""
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=headless)
        context = await self.browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        self.page = await context.new_page()
        
    async def init_session(self):
        """HTTP 세션 초기화 - 브라우저를 통해 쿠키와 헤더 설정"""
        # 먼저 브라우저로 사이트 방문하여 쿠키 설정
        if not self.browser:
            await self.init_browser(headless=True)
            
        # 네이버 부동산 사이트 방문
        await self.page.goto("https://new.land.naver.com/complexes?ms=37.3642443,127.1084674,16&a=APT:ABYG:JGC:PRE&e=RETAIL")
        await self.page.wait_for_load_state("networkidle")
        await asyncio.sleep(2)  # 페이지 완전 로드 대기
        
        # 쿠키 및 User-Agent 가져오기
        context = self.page.context
        cookies = await context.cookies()
        cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}
        user_agent = await self.page.evaluate("navigator.userAgent")
        
        # HTTP 세션 생성
        headers = {
            'User-Agent': user_agent,
            'Referer': 'https://new.land.naver.com/',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'ko-KR,ko;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin'
        }
        
        connector = aiohttp.TCPConnector(ssl=False)
        timeout = aiohttp.ClientTimeout(total=30)
        
        self.session = aiohttp.ClientSession(
            headers=headers,
            cookies=cookie_dict,
            connector=connector,
            timeout=timeout
        )
        
        logger.info(f"세션 초기화 완료 (쿠키: {len(cookies)}개)")
        
        
    async def get_complexes_data(self, 
                               left_lon: float, 
                               right_lon: float, 
                               top_lat: float, 
                               bottom_lat: float,
                               real_estate_type: str = "APT:ABYG:JGC:PRE",
                               price_type: str = "RETAIL") -> List[Dict]:
        """
        부동산 단지 정보를 가져옵니다.
        
        Args:
            left_lon: 왼쪽 경도
            right_lon: 오른쪽 경도  
            top_lat: 위쪽 위도
            bottom_lat: 아래쪽 위도
            real_estate_type: 부동산 타입 (APT:아파트, ABYG:아파트분양권, JGC:재건축, PRE:분양권)
            price_type: 가격 타입 (RETAIL:매매, RENT:전세, MONTHLY:월세)
        """
        
        params = {
            'cortarNo': '4113510300',  # 지역코드 (강남구)
            'zoom': '16',
            'priceType': price_type,
            'markerId': '',
            'markerType': '',
            'selectedComplexNo': '',
            'selectedComplexBuildingNo': '',
            'fakeComplexMarker': '',
            'realEstateType': real_estate_type,
            'tradeType': '',
            'tag': ':::::::',
            'rentPriceMin': '0',
            'rentPriceMax': '900000000',
            'priceMin': '0',
            'priceMax': '900000000',
            'areaMin': '0',
            'areaMax': '900000000',
            'oldBuildYears': '',
            'recentlyBuildYears': '',
            'minHouseHoldCount': '',
            'maxHouseHoldCount': '',
            'showArticle': 'false',
            'sameAddressGroup': 'false',
            'minMaintenanceCost': '',
            'maxMaintenanceCost': '',
            'directions': '',
            'leftLon': str(left_lon),
            'rightLon': str(right_lon),
            'topLat': str(top_lat),
            'bottomLat': str(bottom_lat),
            'isPresale': 'true'
        }
        
        url = f"{self.base_url}/api/complexes/single-markers/2.0"
        
        try:
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"단지 정보 {len(data)}개 수집 완료")
                    return data
                else:
                    logger.error(f"API 요청 실패: {response.status}")
                    return []
        except Exception as e:
            logger.error(f"단지 정보 수집 중 오류: {e}")
            return []
            
    async def get_complex_detail(self, complex_no: str) -> Optional[Dict]:
        """
        특정 단지의 상세 정보를 가져옵니다.
        
        Args:
            complex_no: 단지 번호
        """
        url = f"{self.base_url}/api/complexes/detail/{complex_no}"
        
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"단지 {complex_no} 상세 정보 수집 완료")
                    return data
                else:
                    logger.error(f"단지 상세 정보 요청 실패: {response.status}")
                    return None
        except Exception as e:
            logger.error(f"단지 상세 정보 수집 중 오류: {e}")
            return None
            
    async def get_complex_articles(self, complex_no: str, trade_type: str = "A1") -> List[Dict]:
        """
        단지의 매물 정보를 가져옵니다.
        
        Args:
            complex_no: 단지 번호
            trade_type: 거래 타입 (A1:매매, B1:전세, B2:월세)
        """
        params = {
            'complexNo': complex_no,
            'tradeType': trade_type,
            'order': 'date',
            'showArticle': 'true'
        }
        
        url = f"{self.base_url}/api/articles/complex/{complex_no}"
        
        try:
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    articles = data.get('articleList', [])
                    logger.info(f"단지 {complex_no} 매물 정보 {len(articles)}개 수집 완료")
                    return articles
                else:
                    logger.error(f"매물 정보 요청 실패: {response.status}")
                    return []
        except Exception as e:
            logger.error(f"매물 정보 수집 중 오류: {e}")
            return []
            
    async def get_development_plans(self, 
                                  left_lon: float, 
                                  right_lon: float, 
                                  top_lat: float, 
                                  bottom_lat: float,
                                  plan_type: str = "road") -> List[Dict]:
        """
        개발계획 정보를 가져옵니다.
        
        Args:
            left_lon: 왼쪽 경도
            right_lon: 오른쪽 경도
            top_lat: 위쪽 위도
            bottom_lat: 아래쪽 위도
            plan_type: 계획 타입 (road:도로, rail:철도, jigu:지구)
        """
        params = {
            'zoom': '16',
            'leftLon': str(left_lon),
            'rightLon': str(right_lon), 
            'topLat': str(top_lat),
            'bottomLat': str(bottom_lat)
        }
        
        url = f"{self.base_url}/api/developmentplan/{plan_type}/list"
        
        try:
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"{plan_type} 개발계획 정보 {len(data)}개 수집 완료")
                    return data
                else:
                    logger.error(f"개발계획 정보 요청 실패: {response.status}")
                    return []
        except Exception as e:
            logger.error(f"개발계획 정보 수집 중 오류: {e}")
            return []
            
    async def crawl_area(self, 
                        center_lat: float, 
                        center_lon: float, 
                        radius: float = 0.01) -> Dict:
        """
        특정 지역의 부동산 정보를 종합적으로 크롤링합니다.
        
        Args:
            center_lat: 중심 위도
            center_lon: 중심 경도
            radius: 반경 (도 단위)
        """
        logger.info(f"지역 크롤링 시작: ({center_lat}, {center_lon})")
        
        # 좌표 범위 계산
        left_lon = center_lon - radius
        right_lon = center_lon + radius
        top_lat = center_lat + radius
        bottom_lat = center_lat - radius
        
        result = {
            'area_info': {
                'center_lat': center_lat,
                'center_lon': center_lon,
                'bounds': {
                    'left_lon': left_lon,
                    'right_lon': right_lon,
                    'top_lat': top_lat,
                    'bottom_lat': bottom_lat
                }
            },
            'complexes': [],
            'complex_details': {},
            'articles': {},
            'development_plans': {
                'road': [],
                'rail': [],
                'jigu': []
            }
        }
        
        # 1. 단지 정보 수집
        complexes = await self.get_complexes_data(left_lon, right_lon, top_lat, bottom_lat)
        result['complexes'] = complexes
        
        # 2. 각 단지의 상세 정보 및 매물 정보 수집 (최대 5개)
        for i, complex_data in enumerate(complexes[:5]):  # 처리량 제한
            if 'markerId' in complex_data:
                complex_no = complex_data['markerId']
                
                # 단지 상세 정보
                detail = await self.get_complex_detail(complex_no)
                if detail:
                    result['complex_details'][complex_no] = detail
                
                # 매물 정보 (매매)
                articles = await self.get_complex_articles(complex_no, "A1")
                if articles:
                    result['articles'][complex_no] = articles
                    
                # 요청 간격 조절
                await asyncio.sleep(1)  # 더 긴 대기 시간
                
        # 3. 개발계획 정보 수집
        for plan_type in ['road', 'rail', 'jigu']:
            plans = await self.get_development_plans(left_lon, right_lon, top_lat, bottom_lat, plan_type)
            result['development_plans'][plan_type] = plans
            await asyncio.sleep(0.5)
            
        logger.info("지역 크롤링 완료")
        return result
        
    def save_to_json(self, data: Dict, filename: str):
        """데이터를 JSON 파일로 저장"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"데이터를 {filename}에 저장 완료")
        
    def save_to_excel(self, data: Dict, filename: str):
        """데이터를 Excel 파일로 저장"""
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # 단지 정보
            if data['complexes']:
                df_complexes = pd.DataFrame(data['complexes'])
                df_complexes.to_excel(writer, sheet_name='단지정보', index=False)
                
            # 매물 정보
            all_articles = []
            for complex_no, articles in data['articles'].items():
                for article in articles:
                    article['complex_no'] = complex_no
                    all_articles.append(article)
                    
            if all_articles:
                df_articles = pd.DataFrame(all_articles)
                df_articles.to_excel(writer, sheet_name='매물정보', index=False)
                
            # 개발계획 정보
            for plan_type, plans in data['development_plans'].items():
                if plans:
                    df_plans = pd.DataFrame(plans)
                    df_plans.to_excel(writer, sheet_name=f'{plan_type}_개발계획', index=False)
                    
        logger.info(f"데이터를 {filename}에 저장 완료")
        
    async def close(self):
        """리소스 정리"""
        if self.session:
            await self.session.close()
        if self.browser:
            await self.browser.close()

async def main():
    """메인 실행 함수"""
    crawler = NaverRealEstateCrawler()
    
    try:
        # 브라우저 및 세션 초기화
        await crawler.init_browser(headless=True)
        await crawler.init_session()
        
        # 강남역 주변 부동산 정보 크롤링 (예시 좌표)
        center_lat = 37.3642443
        center_lon = 127.1084674
        
        logger.info("네이버 부동산 크롤링 시작")
        data = await crawler.crawl_area(center_lat, center_lon, radius=0.003)  # 더 작은 반경
        
        # 결과 저장
        timestamp = int(time.time())
        crawler.save_to_json(data, f'naver_real_estate_data_{timestamp}.json')
        
        try:
            crawler.save_to_excel(data, f'naver_real_estate_data_{timestamp}.xlsx')
        except Exception as e:
            logger.warning(f"Excel 저장 실패: {e}")
        
        # 요약 정보 출력
        print("\n=== 크롤링 결과 요약 ===")
        print(f"수집된 단지 수: {len(data['complexes'])}")
        print(f"상세 정보 수집된 단지 수: {len(data['complex_details'])}")
        
        total_articles = sum(len(articles) for articles in data['articles'].values())
        print(f"수집된 매물 수: {total_articles}")
        
        for plan_type, plans in data['development_plans'].items():
            print(f"{plan_type} 개발계획 수: {len(plans)}")
            
    except Exception as e:
        logger.error(f"크롤링 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await crawler.close()

if __name__ == "__main__":
    asyncio.run(main())
