#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
네이버 부동산 크롤링 결과
URL: https://new.land.naver.com/complexes?ms=37.3642443,127.1084674,16&a=APT:ABYG:JGC:PRE&e=RETAIL
크롤링 일시: 2025-06-25
지역: 경기도 성남시 분당구 정자동
"""

import json
from datetime import datetime

# 크롤링한 부동산 데이터
real_estate_data = [
    {
        "name": "피더하우스(실버주택)",
        "price_per_pyeong": "2,320만",
        "prices": {
            "sale": "4억",
            "jeonse": "5.5억",
            "monthly": "55만"
        },
        "area": "57㎡"
    },
    {
        "name": "한솔3단지한일",
        "price_per_pyeong": "5,581만",
        "prices": {
            "sale": "13억",
            "jeonse": "5.5억",
            "monthly": "55만"
        },
        "area": "77㎡"
    },
    {
        "name": "아이파크분당(주상복합)",
        "price_per_pyeong": "3,783만",
        "prices": {
            "sale": "23억",
            "jeonse": "14.5억",
            "monthly": "2백"
        },
        "area": "201㎡"
    },
    {
        "name": "느티마을공무원4단지",
        "price_per_pyeong": "6,288만",
        "prices": {
            "sale": "17.5억",
            "jeonse": "2.8억",
            "monthly": "55만"
        },
        "area": "92㎡"
    },
    {
        "name": "한솔4단지주공",
        "price_per_pyeong": "4,165만",
        "prices": {
            "sale": "6.3억",
            "jeonse": "2.8억",
            "monthly": "55만"
        },
        "area": "50㎡"
    },
    {
        "name": "상록라이프",
        "price_per_pyeong": "4,458만",
        "prices": {
            "sale": "20.5억",
            "jeonse": "8.5억"
        },
        "area": "152㎡"
    },
    {
        "name": "느티마을공무원3단지",
        "price_per_pyeong": "7,007만",
        "prices": {
            "sale": "19.5억"
        },
        "area": "92㎡"
    },
    {
        "name": "한솔1단지청구",
        "price_per_pyeong": "4,649만",
        "prices": {
            "sale": "9억",
            "jeonse": "3.9억"
        },
        "area": "64㎡"
    },
    {
        "name": "아데나팰리스(주상복합)",
        "price_per_pyeong": "3,019만",
        "prices": {
            "sale": "20억"
        },
        "area": "219㎡"
    },
    {
        "name": "성원상떼뷰(주상복합)",
        "price_per_pyeong": "3,761만",
        "prices": {
            "sale": "19억",
            "jeonse": "13억"
        },
        "area": "167㎡"
    },
    {
        "name": "정든신화",
        "price_per_pyeong": "4,541만",
        "prices": {
            "sale": "12.5억"
        },
        "area": "91㎡"
    },
    {
        "name": "푸른벽산,신성,쌍용",
        "price_per_pyeong": "5,456만",
        "prices": {
            "sale": "17억",
            "jeonse": "7.5억"
        },
        "area": "103㎡"
    },
    {
        "name": "정든한진6차",
        "price_per_pyeong": "3,391만",
        "prices": {
            "sale": "16억"
        },
        "area": "156㎡"
    },
    {
        "name": "분당더샵스타파크(주상복합)",
        "price_per_pyeong": "3,806만",
        "prices": {
            "sale": "17.5억",
            "monthly": "2.5백"
        },
        "area": "152㎡"
    },
    {
        "name": "더헤리티지",
        "price_per_pyeong": "2,105만",
        "prices": {
            "sale": "13.5억",
            "jeonse": "7.5억",
            "monthly": "2.4백"
        },
        "area": "212㎡"
    },
    {
        "name": "정든우성4단지",
        "price_per_pyeong": "3,369만",
        "prices": {
            "sale": "15.9억",
            "jeonse": "7.5억"
        },
        "area": "156㎡"
    },
    {
        "name": "정든한진7차",
        "price_per_pyeong": "4,545만",
        "prices": {
            "sale": "12.1억"
        },
        "area": "88㎡"
    },
    {
        "name": "정든한진8차",
        "price_per_pyeong": "3,620만",
        "prices": {
            "sale": "17.3억"
        },
        "area": "158㎡"
    },
    {
        "name": "하이츠빌리지I",
        "price_per_pyeong": "2,602만",
        "prices": {
            "sale": "17억",
            "jeonse": "8억"
        },
        "area": "216㎡"
    },
    {
        "name": "하이츠빌리지",
        "price_per_pyeong": "2,296만",
        "prices": {
            "sale": "12.5억"
        },
        "area": "180㎡"
    },
    {
        "name": "한솔2단지LG",
        "price_per_pyeong": "3,357만",
        "prices": {
            "sale": "16.25억",
            "jeonse": "8.5억",
            "monthly": "70만"
        },
        "area": "160㎡"
    },
    {
        "name": "정든우성6단지",
        "price_per_pyeong": "4,287만",
        "prices": {
            "sale": "8.3억",
            "jeonse": "3.67억"
        },
        "area": "64㎡"
    },
    {
        "name": "한솔5단지주공",
        "price_per_pyeong": "4,525만",
        "prices": {
            "sale": "8.35억",
            "jeonse": "1.8억",
            "monthly": "70만"
        },
        "area": "61㎡"
    },
    {
        "name": "파크타운",
        "price_per_pyeong": "5,078만",
        "prices": {
            "sale": "25.5억",
            "jeonse": "9억",
            "monthly": "2.8백"
        },
        "area": "166㎡"
    },
    {
        "name": "위브제니스(주상복합)",
        "price_per_pyeong": "3,959만",
        "prices": {
            "sale": "20억"
        },
        "area": "167㎡"
    },
    {
        "name": "삼성아데나루체(주상복합)",
        "price_per_pyeong": "3,661만",
        "prices": {
            "sale": "17.5억"
        },
        "area": "158㎡"
    },
    {
        "name": "정든동아2단지",
        "price_per_pyeong": "4,390만",
        "prices": {
            "sale": "8.5억",
            "jeonse": "3.9억"
        },
        "area": "64㎡"
    },
    {
        "name": "상록임광보성",
        "price_per_pyeong": "5,614만",
        "prices": {
            "sale": "18억",
            "jeonse": "6.7억",
            "monthly": "2백"
        },
        "area": "106㎡"
    },
    {
        "name": "동양정자파라곤(주상복합)",
        "price_per_pyeong": "4,031만",
        "prices": {
            "sale": "20억",
            "jeonse": "15억"
        },
        "area": "164㎡"
    },
    {
        "name": "한솔6단지주공",
        "price_per_pyeong": "4,179만",
        "prices": {
            "sale": "6.7억",
            "jeonse": "3억"
        },
        "area": "53㎡"
    },
    {
        "name": "정든동아1단지",
        "price_per_pyeong": "3,510만",
        "prices": {
            "sale": "15.5억",
            "jeonse": "8억"
        },
        "area": "146㎡"
    },
    {
        "name": "상록우성",
        "price_per_pyeong": "5,186만",
        "prices": {
            "sale": "24억",
            "jeonse": "9억",
            "monthly": "80만"
        },
        "area": "153㎡"
    },
    {
        "name": "미켈란쉐르빌(주상복합)",
        "price_per_pyeong": "3,682만",
        "prices": {
            "sale": "22.5억",
            "jeonse": "15억",
            "monthly": "6백"
        },
        "area": "202㎡"
    }
]

def get_summary_stats():
    """부동산 데이터 요약 통계"""
    print(f"총 단지 수: {len(real_estate_data)}개")
    print(f"크롤링 일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # 가격대별 분포
    price_ranges = {
        "10억 미만": 0,
        "10억-20억": 0,
        "20억 이상": 0
    }
    
    for complex_data in real_estate_data:
        sale_price = complex_data["prices"].get("sale", "")
        if sale_price:
            # 간단한 가격 파싱 (억 단위)
            if "억" in sale_price:
                price_num = float(sale_price.replace("억", ""))
                if price_num < 10:
                    price_ranges["10억 미만"] += 1
                elif price_num < 20:
                    price_ranges["10억-20억"] += 1
                else:
                    price_ranges["20억 이상"] += 1
    
    print("매매가격 분포:")
    for range_name, count in price_ranges.items():
        print(f"  {range_name}: {count}개 단지")

def save_to_json(filename="real_estate_data.json"):
    """JSON 파일로 저장"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump({
            "crawled_at": datetime.now().isoformat(),
            "source_url": "https://new.land.naver.com/complexes?ms=37.3642443,127.1084674,16&a=APT:ABYG:JGC:PRE&e=RETAIL",
            "location": "경기도 성남시 분당구 정자동",
            "total_count": len(real_estate_data),
            "data": real_estate_data
        }, f, ensure_ascii=False, indent=2)
    print(f"데이터가 {filename}에 저장되었습니다.")

if __name__ == "__main__":
    get_summary_stats()
    save_to_json()
    
    print("\n상위 5개 단지 (평당가 기준):")
    # 평당가를 숫자로 변환해서 정렬
    sorted_complexes = sorted(
        real_estate_data, 
        key=lambda x: int(x["price_per_pyeong"].replace(",", "").replace("만", "")), 
        reverse=True
    )
    
    for i, complex_data in enumerate(sorted_complexes[:5], 1):
        print(f"{i}. {complex_data['name']}")
        print(f"   평당가: {complex_data['price_per_pyeong']}")
        print(f"   매매가: {complex_data['prices'].get('sale', 'N/A')}")
        print(f"   면적: {complex_data['area']}")
        print()
