import asyncio
from naver_real_estate_crawler import NaverRealEstateCrawler
import time

async def run_with_defaults():
    """기본값으로 크롤러 실행"""
    print("=== 네이버 부동산 크롤러 (기본값 실행) ===")
    
    # 기본값 사용
    center_lat = 37.3642443  # 강남역 근처
    center_lon = 127.1084674
    radius = 0.01  # 더 큰 범위로 설정
    
    print(f"크롤링 시작: 중심좌표 ({center_lat}, {center_lon}), 반경 {radius}")
    
    crawler = NaverRealEstateCrawler()
    
    try:
        # 브라우저 및 세션 초기화
        await crawler.init_browser(headless=True)
        await crawler.init_session()
        
        # 부동산 정보 크롤링
        data = await crawler.crawl_area(center_lat, center_lon, radius)
        
        # 결과 저장
        timestamp = int(time.time())
        json_filename = f'naver_real_estate_data_{timestamp}.json'
        
        crawler.save_to_json(data, json_filename)
        
        try:
            excel_filename = f'naver_real_estate_data_{timestamp}.xlsx'
            crawler.save_to_excel(data, excel_filename)
            print(f"\n결과가 {json_filename}과 {excel_filename}에 저장되었습니다.")
        except Exception as e:
            print(f"\n결과가 {json_filename}에 저장되었습니다. (Excel 저장 실패: {e})")
        
        # 요약 정보 출력
        print("\n=== 크롤링 결과 요약 ===")
        print(f"수집된 단지 수: {len(data['complexes'])}")
        print(f"상세 정보 수집된 단지 수: {len(data['complex_details'])}")
        
        total_articles = sum(len(articles) for articles in data['articles'].values())
        print(f"수집된 매물 수: {total_articles}")
        
        for plan_type, plans in data['development_plans'].items():
            print(f"{plan_type} 개발계획 수: {len(plans)}")
        
        # 단지 정보 미리보기
        if data['complexes']:
            print("\n=== 단지 정보 미리보기 (상위 3개) ===")
            for i, complex_info in enumerate(data['complexes'][:3], 1):
                print(f"{i}. {complex_info.get('complexName', 'N/A')}")
                print(f"   타입: {complex_info.get('realEstateTypeName', 'N/A')}")
                print(f"   완공년월: {complex_info.get('completionYearMonth', 'N/A')}")
                print(f"   세대수: {complex_info.get('totalHouseholdCount', 'N/A')}")
                if 'minDealPrice' in complex_info and 'maxDealPrice' in complex_info:
                    print(f"   매매가격: {complex_info['minDealPrice']:,}만원 ~ {complex_info['maxDealPrice']:,}만원")
                print()
        else:
            print("\n수집된 단지 정보가 없습니다.")
                
    except Exception as e:
        print(f"크롤링 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await crawler.close()

if __name__ == "__main__":
    asyncio.run(run_with_defaults())
