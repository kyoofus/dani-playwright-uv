# 네이버 부동산 크롤러 Svelte 애플리케이션

이 프로젝트는 네이버 부동산 사이트에서 부동산 정보를 크롤링하는 Svelte 5 기반 웹 애플리케이션입니다.

## 🚀 기능

- **실시간 부동산 데이터 크롤링**: 네이버 부동산에서 실시간으로 매물 정보 수집
- **지역별 검색**: 좌표 기반으로 특정 지역의 부동산 정보 검색
- **다양한 필터링**: 아파트, 분양권, 재건축 등 부동산 타입별 필터링
- **거래 타입 선택**: 매매, 전세, 월세 선택 가능
- **미리 정의된 위치**: 강남역, 홍대입구역, 잠실역, 신촌역 등 빠른 위치 선택
- **실시간 결과 표시**: 수집된 데이터를 실시간으로 시각화

## 🏗️ 아키텍처

### 프론트엔드 (Svelte 5)
- `src/routes/+page.svelte`: 메인 UI 컴포넌트
- `src/routes/api/real-estate/+server.ts`: SvelteKit API 엔드포인트
- 반응형 디자인으로 모바일과 데스크톱 모두 지원

### 백엔드 (Python FastAPI)
- `logic/api_server.py`: FastAPI 서버
- `logic/naver_real_estate_crawler.py`: 크롤링 로직
- Playwright를 사용한 브라우저 자동화

## 📋 사전 요구사항

### Python 환경
- Python 3.8 이상
- pip 또는 uv 패키지 매니저

### Node.js 환경
- Node.js 18 이상
- npm 또는 pnpm

## 🛠️ 설치 및 실행

### 1. Python 의존성 설치

```bash
# uv 사용 (권장)
uv add fastapi uvicorn pydantic aiohttp pandas playwright openpyxl

# 또는 pip 사용
pip install -r requirements.txt
```

### 2. Playwright 브라우저 설치

```bash
playwright install chromium
```

### 3. Node.js 의존성 설치

```bash
npm install
# 또는
pnpm install
```

### 4. 백엔드 서버 실행

```bash
# logic 디렉토리에서 실행
cd logic
python api_server.py
```

백엔드 서버가 `http://localhost:8000`에서 실행됩니다.

### 5. 프론트엔드 개발 서버 실행

```bash
# 프로젝트 루트에서 실행
npm run dev
# 또는
pnpm dev
```

프론트엔드가 `http://localhost:5173`에서 실행됩니다.

## 📱 사용법

1. **지역 선택**: 미리 정의된 위치를 클릭하거나 직접 좌표를 입력합니다.
2. **검색 옵션 설정**: 
   - 검색 반경 조정 (기본값: 0.003도 ≈ 약 300m)
   - 부동산 타입 선택 (아파트, 분양권, 재건축 등)
   - 거래 타입 선택 (매매, 전세, 월세)
3. **크롤링 시작**: "🚀 크롤링 시작" 버튼을 클릭합니다.
4. **결과 확인**: 수집된 부동산 정보를 실시간으로 확인합니다.

## 🔧 개발 가이드

### 프로젝트 구조

```
├── src/
│   ├── routes/
│   │   ├── +page.svelte          # 메인 페이지
│   │   └── api/
│   │       └── real-estate/
│   │           └── +server.ts     # API 엔드포인트
│   ├── lib/                       # 재사용 가능한 컴포넌트/유틸리티
│   └── app.html                   # HTML 템플릿
├── logic/
│   ├── api_server.py              # FastAPI 백엔드 서버
│   ├── naver_real_estate_crawler.py  # 크롤링 로직
│   └── requirements.txt           # Python 의존성
├── static/                        # 정적 파일
└── package.json                   # Node.js 의존성
```

### API 엔드포인트

#### `/api/real-estate` (POST)
전체 지역 크롤링을 수행합니다.

**요청 형식:**
```json
{
  "center_lat": 37.3642443,
  "center_lon": 127.1084674,
  "radius": 0.003,
  "real_estate_type": "APT:ABYG:JGC:PRE",
  "price_type": "RETAIL"
}
```

**응답 형식:**
```json
{
  "success": true,
  "data": {
    "area_info": { ... },
    "complexes": [ ... ],
    "complex_details": { ... },
    "articles": { ... },
    "development_plans": { ... }
  }
}
```

### Python FastAPI 엔드포인트

#### `POST /api/crawl`
전체 크롤링 실행

#### `POST /api/complexes`
단지 정보만 수집

#### `GET /api/complex/{complex_no}`
특정 단지 상세 정보

#### `GET /api/complex/{complex_no}/articles`
특정 단지의 매물 정보

## ⚠️ 주의사항

1. **법적 고지**: 이 도구는 교육 및 연구 목적으로만 사용해야 합니다. 상업적 목적으로 사용할 경우 네이버의 이용약관을 확인하세요.

2. **API 제한**: 네이버 부동산 API에는 요청 제한이 있을 수 있습니다. 과도한 요청을 피하고 적절한 간격을 두고 사용하세요.

3. **데이터 정확성**: 크롤링된 데이터의 정확성을 보장하지 않습니다. 중요한 결정은 공식 데이터를 바탕으로 하세요.

4. **의존성**: Playwright가 Chromium 브라우저를 다운로드하므로 충분한 저장 공간이 필요합니다.

## 🔒 보안 고려사항

- 프로덕션 환경에서는 CORS 설정을 적절히 제한하세요.
- API 키나 민감한 정보는 환경 변수로 관리하세요.
- 속도 제한(Rate Limiting)을 구현하여 남용을 방지하세요.

## 🚀 배포

### Vercel 배포 (프론트엔드)

```bash
npm run build
npx vercel --prod
```

### Docker 배포 (백엔드)

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN playwright install chromium

COPY logic/ .
CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🐛 문제 해결

### 일반적인 문제들

1. **Python 서버 연결 실패**
   - `logic/api_server.py`가 실행 중인지 확인
   - 포트 8000이 사용 가능한지 확인

2. **Playwright 오류**
   - `playwright install chromium` 실행
   - 충분한 시스템 메모리 확인

3. **크롤링 실패**
   - 네트워크 연결 상태 확인
   - 네이버 부동산 사이트 접근 가능 여부 확인

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 LICENSE 파일을 참조하세요.

## 🤝 기여

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 지원

문제가 발생하거나 질문이 있으시면 [Issues](https://github.com/your-repo/issues) 페이지에서 문의해 주세요.
