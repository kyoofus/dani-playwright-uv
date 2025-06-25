import asyncio
import json
from playwright.async_api import async_playwright

async def test_api_with_browser():
    """브라우저를 사용해서 실제 API 호출 테스트"""
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            # 먼저 네이버 부동산 사이트 방문
            print("네이버 부동산 사이트 방문 중...")
            await page.goto("https://new.land.naver.com/complexes?ms=37.3642443,127.1084674,16&a=APT:ABYG:JGC:PRE&e=RETAIL")
            await page.wait_for_load_state("networkidle")
            
            # 쿠키 및 헤더 정보 가져오기
            cookies = await context.cookies()
            print(f"쿠키 개수: {len(cookies)}")
            
            # API 직접 호출
            api_url = "https://new.land.naver.com/api/complexes/single-markers/2.0"
            params = {
                'cortarNo': '4113510300',
                'zoom': '16',
                'priceType': 'RETAIL',
                'realEstateType': 'APT:ABYG:JGC:PRE',
                'leftLon': '127.0947345',
                'rightLon': '127.1222003',
                'topLat': '37.3697868',
                'bottomLat': '37.3587014',
                'isPresale': 'true'
            }
            
            # URL 구성
            query_string = "&".join([f"{k}={v}" for k, v in params.items()])
            full_url = f"{api_url}?{query_string}"
            
            print(f"API 호출: {full_url}")
            
            # API 페이지로 이동
            response = await page.goto(full_url)
            content = await page.content()
            
            print(f"응답 상태: {response.status}")
            print(f"응답 내용 길이: {len(content)}")
            
            # JSON 파싱 시도
            try:
                if '<pre>' in content:
                    # JSON이 <pre> 태그 안에 있는 경우
                    json_start = content.find('<pre>') + 5
                    json_end = content.find('</pre>')
                    json_content = content[json_start:json_end]
                else:
                    json_content = content
                    
                data = json.loads(json_content)
                print(f"파싱된 데이터 개수: {len(data)}")
                
                if data:
                    print("\n=== 첫 번째 단지 정보 ===")
                    first_complex = data[0]
                    print(f"단지명: {first_complex.get('complexName', 'N/A')}")
                    print(f"타입: {first_complex.get('realEstateTypeName', 'N/A')}")
                    print(f"위치: ({first_complex.get('latitude', 'N/A')}, {first_complex.get('longitude', 'N/A')})")
                    
                # 결과 저장
                with open('browser_test_result.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print("\n결과가 'browser_test_result.json'에 저장되었습니다.")
                
            except json.JSONDecodeError as e:
                print(f"JSON 파싱 실패: {e}")
                print(f"응답 내용 (처음 500자): {content[:500]}")
                
        except Exception as e:
            print(f"오류 발생: {e}")
        
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(test_api_with_browser())
