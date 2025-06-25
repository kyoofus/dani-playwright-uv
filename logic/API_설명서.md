# 네이버 부동산 API 분석 및 설명

## 개요
네이버 부동산 사이트는 여러 API를 통해 부동산 정보를 제공합니다. 이 문서는 각 API의 역할과 데이터 구조를 설명합니다.

## 주요 API 엔드포인트

### 1. 단지 마커 정보 API
**URL**: `/api/complexes/single-markers/2.0`

**용도**: 지도에서 보이는 부동산 단지들의 기본 정보를 가져옵니다.

**주요 파라미터**:
- `leftLon`, `rightLon`, `topLat`, `bottomLat`: 지도 영역의 좌표 범위
- `realEstateType`: 부동산 타입 (APT:아파트, ABYG:아파트분양권, JGC:재건축, PRE:분양권)
- `priceType`: 가격 타입 (RETAIL:매매, RENT:전세, MONTHLY:월세)
- `zoom`: 지도 줌 레벨
- `cortarNo`: 지역코드

**응답 데이터**:
```json
{
  "markerId": "2813",
  "markerType": "COMPLEX", 
  "latitude": 37.366916,
  "longitude": 127.120509,
  "complexName": "한솔3단지한일",
  "realEstateTypeCode": "APT",
  "realEstateTypeName": "아파트",
  "completionYearMonth": "199310",
  "totalDongCount": 7,
  "totalHouseholdCount": 416,
  "floorAreaRatio": 154,
  "minDealUnitPrice": 5238,
  "maxDealUnitPrice": 5796,
  "minLeaseUnitPrice": 1684,
  "maxLeaseUnitPrice": 2361,
  "minArea": "77.84",
  "maxArea": "157.35",
  "minDealPrice": 122000,
  "maxDealPrice": 135000,
  "minLeasePrice": 55000,
  "maxLeasePrice": 80000,
  "dealCount": 4,
  "leaseCount": 5,
  "representativePhoto": "/20170919_34/apt_realimage_1505813843003WbUeE_JPEG/8447a4aef2e5a644b9c59508bdcc2feb.jpg",
  "photoCount": 0
}
```

### 2. 단지 상세 정보 API
**URL**: `/api/complexes/detail/{complexNo}`

**용도**: 특정 단지의 상세한 정보를 가져옵니다.

**응답 데이터**:
- 단지의 상세 정보 (주소, 건설사, 시설 정보 등)
- 주변 시설 정보
- 교통 정보

### 3. 매물 정보 API
**URL**: `/api/articles/complex/{complexNo}`

**용도**: 특정 단지의 실제 매물 정보를 가져옵니다.

**주요 파라미터**:
- `complexNo`: 단지 번호
- `tradeType`: 거래 타입 (A1:매매, B1:전세, B2:월세)
- `order`: 정렬 기준 (date:날짜순, price:가격순)

**응답 데이터**:
```json
{
  "articleList": [
    {
      "articleNo": "12345",
      "articleName": "강남구 개포동 매매",
      "realEstateTypeName": "아파트",
      "tradeTypeName": "매매",
      "dealOrWarrantPrc": "13억2000",
      "area1": "85.00",
      "area2": "77.84", 
      "direction": "남향",
      "floorInfo": "5/15",
      "articleConfirmYmd": "2024.01.15",
      "tagList": ["융자금승계", "즉시입주"]
    }
  ]
}
```

### 4. 개발계획 정보 API

#### 4.1 도로 개발계획
**URL**: `/api/developmentplan/road/list`

**용도**: 해당 지역의 도로 개발계획 정보를 가져옵니다.

#### 4.2 철도 개발계획  
**URL**: `/api/developmentplan/rail/list`

**용도**: 해당 지역의 철도 개발계획 정보를 가져옵니다.

#### 4.3 지구 개발계획
**URL**: `/api/developmentplan/jigu/list`

**용도**: 해당 지역의 지구단위 개발계획 정보를 가져옵니다.

**공통 파라미터**:
- `zoom`: 지도 줌 레벨
- `leftLon`, `rightLon`, `topLat`, `bottomLat`: 지도 영역의 좌표 범위

### 5. 행정구역 정보 API
**URL**: `/api/cortars`

**용도**: 특정 지역의 행정구역 정보를 가져옵니다.

**파라미터**:
- `zoom`: 지도 줌 레벨
- `centerLat`, `centerLon`: 중심 좌표

## 데이터 활용 방법

### 1. 지역별 부동산 현황 분석
- 단지 마커 API로 전체 단지 목록 수집
- 각 단지의 평균 가격, 거래량 분석
- 부동산 타입별 분포 현황 파악

### 2. 개별 단지 심층 분석  
- 단지 상세 정보로 시설, 교통 등 분석
- 매물 정보로 실제 거래 가격 추이 분석
- 면적별, 층별 가격 차이 분석

### 3. 지역 개발 계획 분석
- 도로/철도/지구 개발계획으로 미래 가치 예측
- 교통 인프라 개선 계획 파악
- 신규 개발 지역 발굴

## 주의사항

1. **요청 제한**: 과도한 요청으로 인한 차단을 방지하기 위해 요청 간 적절한 딜레이 필요
2. **User-Agent**: 정상적인 브라우저 요청처럼 보이도록 적절한 헤더 설정 필요  
3. **좌표 범위**: 너무 넓은 범위로 요청시 데이터가 많아 응답 시간이 길어질 수 있음
4. **데이터 정확성**: API 응답 데이터는 실시간으로 변경될 수 있으므로 수집 시점 고려 필요

## 법적 고지

이 정보는 네이버 부동산 서비스의 공개 API를 분석한 내용입니다. 실제 사용시에는 네이버의 이용약관 및 로봇 배제 표준(robots.txt)을 준수해야 합니다.
