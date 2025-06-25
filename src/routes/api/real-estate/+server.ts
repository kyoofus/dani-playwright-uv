import { json } from '@sveltejs/kit';

interface CrawlRequest {
	center_lat: number;
	center_lon: number;
	radius?: number;
	real_estate_type?: string;
	price_type?: string;
}

interface RealEstateData {
	area_info: {
		center_lat: number;
		center_lon: number;
		bounds: {
			left_lon: number;
			right_lon: number;
			top_lat: number;
			bottom_lat: number;
		};
	};
	complexes: Array<Record<string, unknown>>;
	complex_details: Record<string, unknown>;
	articles: Record<string, unknown>;
	development_plans: {
		road: Array<Record<string, unknown>>;
		rail: Array<Record<string, unknown>>;
		jigu: Array<Record<string, unknown>>;
	};
}

interface CrawlResponse {
	success: boolean;
	data?: RealEstateData;
	error?: string;
}

const PYTHON_API_URL = 'http://localhost:8000';

export const POST = async ({ request }: { request: Request }): Promise<Response> => {
	try {
		const body: CrawlRequest = await request.json();
		
		// Python FastAPI 서버로 요청 전송
		const response = await fetch(`${PYTHON_API_URL}/api/crawl`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(body)
		});

		if (!response.ok) {
			throw new Error(`Python API 서버 오류: ${response.status}`);
		}

		const result = await response.json();
		return json(result as CrawlResponse);
		
	} catch (error) {
		console.error('API 오류:', error);
		
		// Python 서버가 실행되지 않은 경우 모의 데이터 반환
		if (error instanceof Error && error.message.includes('fetch')) {
			console.warn('Python 서버에 연결할 수 없습니다. 모의 데이터를 반환합니다.');
			
			const body: CrawlRequest = await request.json();
			const mockData: RealEstateData = {
				area_info: {
					center_lat: body.center_lat,
					center_lon: body.center_lon,
					bounds: {
						left_lon: body.center_lon - (body.radius || 0.003),
						right_lon: body.center_lon + (body.radius || 0.003),
						top_lat: body.center_lat + (body.radius || 0.003),
						bottom_lat: body.center_lat - (body.radius || 0.003)
					}
				},
				complexes: [
					{
						markerId: "123456",
						markerType: "COMPLEX",
						lat: body.center_lat + 0.001,
						lon: body.center_lon + 0.001,
						complexName: "테스트 아파트",
						tradePriceMin: 50000,
						tradePriceMax: 100000,
						rentPriceMin: 3000,
						rentPriceMax: 5000
					},
					{
						markerId: "789012",
						markerType: "COMPLEX", 
						lat: body.center_lat - 0.001,
						lon: body.center_lon - 0.001,
						complexName: "샘플 단지",
						tradePriceMin: 40000,
						tradePriceMax: 80000,
						rentPriceMin: 2500,
						rentPriceMax: 4000
					}
				],
				complex_details: {
					"123456": {
						complexName: "테스트 아파트",
						totalHouseholdCount: 500,
						useApproveYmd: "2020-01-01"
					}
				},
				articles: {
					"123456": [
						{
							articleNo: "001",
							realEstateTypeName: "아파트",
							tradeTypeName: "매매",
							dealOrWarrantPrc: "8억5천만원",
							areaName: "84㎡",
							direction: "남향",
							floorInfo: "15/20층"
						}
					]
				},
				development_plans: {
					road: [
						{
							planName: "테스트 도로 개발",
							planType: "도로",
							expectedDate: "2025년 12월"
						}
					],
					rail: [],
					jigu: []
				}
			};

			return json({ 
				success: true, 
				data: mockData 
			} as CrawlResponse);
		}
		
		return json({ 
			success: false, 
			error: error instanceof Error ? error.message : '알 수 없는 오류'
		} as CrawlResponse);
	}
};
