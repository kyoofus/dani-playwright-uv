import asyncio
import json
from naver_real_estate_crawler import NaverRealEstateCrawler

async def simple_example():
    """간단한 사용 예제"""
    
    crawler = NaverRealEstateCrawler()
    await crawler.init_session()
    
    try:
        print("=== 강남역 주변 부동산 정보 수집 예제 ===")
        
        # 강남역 주변 좌표
        center_lat = 37.3642443
        center_lon = 127.1084674
        
        # 1. 단지 정보만 빠르게 수집
        complexes = await crawler.get_complexes_data(
            left_lon=center_lon - 0.003,
            right_lon=center_lon + 0.003, 
            top_lat=center_lat + 0.003,
            bottom_lat=center_lat - 0.003
        )
        
        print(f"발견된 단지 수: {len(complexes)}")
        
        # 2. 첫 번째 단지의 상세 정보 가져오기
        if complexes:
            first_complex = complexes[0]
            complex_no = first_complex['markerId']
            
            print(f"\n첫 번째 단지: {first_complex['complexName']}")
            
            # 상세 정보
            detail = await crawler.get_complex_detail(complex_no)
            if detail:
                print("상세 정보 수집 완료")
                
            # 매물 정보
            articles = await crawler.get_complex_articles(complex_no)
            print(f"매물 수: {len(articles)}")
            
        # 3. 개발계획 정보 수집
        road_plans = await crawler.get_development_plans(
            left_lon=center_lon - 0.003,
            right_lon=center_lon + 0.003,
            top_lat=center_lat + 0.003, 
            bottom_lat=center_lat - 0.003,
            plan_type="road"
        )
        
        print(f"도로 개발계획: {len(road_plans)}개")
        
        # 결과를 파일로 저장
        result = {
            'complexes': complexes[:5],  # 상위 5개만 저장
            'road_plans': road_plans
        }
        
        with open('simple_example_result.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
            
        print("\n결과가 'simple_example_result.json'에 저장되었습니다.")
        
    finally:
        await crawler.close()

if __name__ == "__main__":
    asyncio.run(simple_example())
