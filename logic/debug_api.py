import asyncio
from naver_real_estate_crawler import NaverRealEstateCrawler

async def debug_api_call():
    """API 호출 디버깅"""
    
    crawler = NaverRealEstateCrawler()
    
    try:
        # 브라우저 및 세션 초기화
        await crawler.init_browser(headless=True)
        await crawler.init_session()
        
        # 좌표 범위 (조금 더 넓게)
        center_lat = 37.3642443
        center_lon = 127.1084674
        radius = 0.01  # 더 큰 범위
        
        left_lon = center_lon - radius
        right_lon = center_lon + radius
        top_lat = center_lat + radius
        bottom_lat = center_lat - radius
        
        print(f"좌표 범위:")
        print(f"  left_lon: {left_lon}")
        print(f"  right_lon: {right_lon}")
        print(f"  top_lat: {top_lat}")
        print(f"  bottom_lat: {bottom_lat}")
        
        # API 호출
        complexes = await crawler.get_complexes_data(left_lon, right_lon, top_lat, bottom_lat)
        print(f"\n수집된 단지 수: {len(complexes)}")
        
        if complexes:
            print("\n첫 번째 단지 정보:")
            for key, value in complexes[0].items():
                print(f"  {key}: {value}")
        else:
            print("\n단지가 수집되지 않았습니다.")
            
            # 다른 좌표로 시도
            print("\n다른 좌표로 재시도...")
            test_complexes = await crawler.get_complexes_data(
                left_lon=127.0947345,
                right_lon=127.1222003,
                top_lat=37.3697868,
                bottom_lat=37.3587014
            )
            print(f"테스트 좌표 결과: {len(test_complexes)}개")
            
            if test_complexes:
                print("첫 번째 테스트 단지:")
                for key, value in test_complexes[0].items():
                    print(f"  {key}: {value}")
        
    except Exception as e:
        print(f"오류 발생: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await crawler.close()

if __name__ == "__main__":
    asyncio.run(debug_api_call())
