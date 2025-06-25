# 네이버 부동산 크롤러

네이버 부동산 사이트에서 부동산 정보를 수집하는 Python 크롤러입니다.

## 기능

- 지역별 부동산 단지 정보 수집
- 단지별 상세 정보 및 매물 정보 수집  
- 개발계획 정보 수집 (도로, 철도, 지구개발)
- JSON 및 Excel 형태로 데이터 저장

## 설치

```bash
# uv를 사용하는 경우
uv add aiohttp playwright pandas openpyxl

# pip를 사용하는 경우  
pip install aiohttp playwright pandas openpyxl

# Playwright 브라우저 설치
playwright install
```

## 사용법

### 기본 사용법

```bash
python main.py
```

실행 후 중심 좌표와 반경을 입력하면 해당 지역의 부동산 정보를 수집합니다.

### 프로그래밍 방식 사용

```python
import asyncio
from naver_real_estate_crawler import NaverRealEstateCrawler

async def example():
    crawler = NaverRealEstateCrawler()
    await crawler.init_session()
    
    try:
        # 강남역 주변 정보 수집
        data = await crawler.crawl_area(37.3642443, 127.1084674, radius=0.005)
        crawler.save_to_json(data, 'result.json')
    finally:
        await crawler.close()

asyncio.run(example())
```

### 간단한 예제 실행

```bash
python example.py
```

## API 정보

네이버 부동산에서 사용하는 주요 API들:

1. **단지 마커 정보**: `/api/complexes/single-markers/2.0`
   - 지도에 표시되는 부동산 단지들의 기본 정보

2. **단지 상세 정보**: `/api/complexes/detail/{complexNo}`
   - 특정 단지의 상세한 정보

3. **매물 정보**: `/api/articles/complex/{complexNo}`
   - 실제 매물 리스트와 가격 정보

4. **개발계획 정보**: `/api/developmentplan/{type}/list`
   - 도로, 철도, 지구개발 계획 정보

자세한 API 정보는 `API_설명서.md`를 참고하세요.

## 출력 데이터

수집된 데이터는 다음과 같은 구조로 저장됩니다:

```json
{
  "area_info": {
    "center_lat": 37.3642443,
    "center_lon": 127.1084674,
    "bounds": { ... }
  },
  "complexes": [ ... ],
  "complex_details": { ... },
  "articles": { ... },
  "development_plans": {
    "road": [ ... ],
    "rail": [ ... ],
    "jigu": [ ... ]
  }
}
```

## 주의사항

1. **과도한 요청 금지**: 네이버 서버에 부하를 주지 않도록 적절한 딜레이를 두고 사용하세요.
2. **이용약관 준수**: 네이버의 이용약관 및 robots.txt를 확인하고 준수하세요.
3. **개인정보 보호**: 수집된 데이터에 개인정보가 포함될 수 있으니 주의하여 처리하세요.

## 라이선스

이 프로젝트는 교육 및 연구 목적으로만 사용해야 합니다.