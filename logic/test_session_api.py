import asyncio
import json
import aiohttp
from playwright.async_api import async_playwright

async def test_api_with_session():
    """세션을 사용해서 실제 API 호출 테스트"""
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            # 먼저 네이버 부동산 사이트 방문하여 쿠키 및 세션 설정
            print("네이버 부동산 사이트 방문 중...")
            await page.goto("https://new.land.naver.com/complexes?ms=37.3642443,127.1084674,16&a=APT:ABYG:JGC:PRE&e=RETAIL")
            await page.wait_for_load_state("networkidle")
            
            # 페이지가 완전히 로드될 때까지 대기
            await asyncio.sleep(3)
            
            # 쿠키 가져오기
            cookies = await context.cookies()
            cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}
            
            # User-Agent 가져오기
            user_agent = await page.evaluate("navigator.userAgent")
            
            print(f"쿠키 개수: {len(cookies)}")
            print(f"User-Agent: {user_agent}")
            
            # HTTP 세션 생성
            headers = {
                'User-Agent': user_agent,
                'Referer': 'https://new.land.naver.com/complexes?ms=37.3642443,127.1084674,16&a=APT:ABYG:JGC:PRE&e=RETAIL',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'ko-KR,ko;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin'
            }
            
            # aiohttp 세션으로 API 호출
            connector = aiohttp.TCPConnector(ssl=False)
            timeout = aiohttp.ClientTimeout(total=30)
            
            async with aiohttp.ClientSession(
                headers=headers,
                cookies=cookie_dict,
                connector=connector,
                timeout=timeout
            ) as session:
                
                # API 파라미터
                params = {
                    'cortarNo': '4113510300',
                    'zoom': '16',
                    'priceType': 'RETAIL',
                    'markerId': '',
                    'markerType': '',
                    'selectedComplexNo': '',
                    'selectedComplexBuildingNo': '',
                    'fakeComplexMarker': '',
                    'realEstateType': 'APT:ABYG:JGC:PRE',
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
                    'leftLon': '127.0947345',
                    'rightLon': '127.1222003',
                    'topLat': '37.3697868',
                    'bottomLat': '37.3587014',
                    'isPresale': 'true'
                }
                
                api_url = "https://new.land.naver.com/api/complexes/single-markers/2.0"
                
                print(f"API 호출: {api_url}")
                
                async with session.get(api_url, params=params) as response:
                    print(f"응답 상태: {response.status}")
                    print(f"응답 헤더: {dict(response.headers)}")
                    
                    if response.status == 200:
                        try:
                            data = await response.json()
                            print(f"파싱된 데이터 개수: {len(data)}")
                            
                            if data:
                                print("\n=== 첫 번째 단지 정보 ===")
                                first_complex = data[0]
                                for key, value in first_complex.items():
                                    print(f"{key}: {value}")
                                
                                # 결과 저장
                                with open('session_test_result.json', 'w', encoding='utf-8') as f:
                                    json.dump(data, f, ensure_ascii=False, indent=2)
                                print("\n결과가 'session_test_result.json'에 저장되었습니다.")
                            else:
                                print("빈 데이터 응답")
                                
                        except json.JSONDecodeError as e:
                            text = await response.text()
                            print(f"JSON 파싱 실패: {e}")
                            print(f"응답 내용 (처음 500자): {text[:500]}")
                    else:
                        text = await response.text()
                        print(f"API 호출 실패. 응답: {text[:500]}")
                        
        except Exception as e:
            print(f"오류 발생: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(test_api_with_session())
