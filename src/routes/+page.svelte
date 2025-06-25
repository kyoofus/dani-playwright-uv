<script lang="ts">
	import { onMount } from 'svelte';

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
		complexes: Array<Record<string, any>>;
		complex_details: Record<string, any>;
		articles: Record<string, any>;
		development_plans: {
			road: Array<Record<string, any>>;
			rail: Array<Record<string, any>>;
			jigu: Array<Record<string, any>>;
		};
	}

	// 상태 변수들
	let centerLat = $state(37.3642443); // 강남역 기본값
	let centerLon = $state(127.1084674);
	let radius = $state(0.003);
	let realEstateType = $state('APT:ABYG:JGC:PRE');
	let priceType = $state('RETAIL');
	
	let isLoading = $state(false);
	let crawlData: RealEstateData | null = $state(null);
	let error = $state('');

	// 미리 정의된 지역들
	const presetLocations = [
		{ name: '강남역', lat: 37.3642443, lon: 127.1084674 },
		{ name: '홍대입구역', lat: 37.5563073, lon: 126.9227004 },
		{ name: '잠실역', lat: 37.5132665, lon: 127.1002370 },
		{ name: '신촌역', lat: 37.5559711, lon: 126.9371711 }
	];

	// 부동산 타입 옵션
	const realEstateTypes = [
		{ value: 'APT:ABYG:JGC:PRE', label: '전체 (아파트, 분양권, 재건축)' },
		{ value: 'APT', label: '아파트' },
		{ value: 'ABYG', label: '아파트 분양권' },
		{ value: 'JGC', label: '재건축' },
		{ value: 'PRE', label: '분양권' }
	];

	// 가격 타입 옵션
	const priceTypes = [
		{ value: 'RETAIL', label: '매매' },
		{ value: 'RENT', label: '전세' },
		{ value: 'MONTHLY', label: '월세' }
	];

	// 크롤링 실행
	async function startCrawling() {
		if (isLoading) return;

		isLoading = true;
		error = '';
		crawlData = null;

		try {
			const requestData: CrawlRequest = {
				center_lat: centerLat,
				center_lon: centerLon,
				radius: radius,
				real_estate_type: realEstateType,
				price_type: priceType
			};

			const response = await fetch('/api/real-estate', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(requestData)
			});

			const result = await response.json();

			if (result.success) {
				crawlData = result.data;
			} else {
				error = result.error || '크롤링 중 오류가 발생했습니다.';
			}
		} catch (err) {
			error = '서버 연결 오류가 발생했습니다.';
			console.error('크롤링 오류:', err);
		} finally {
			isLoading = false;
		}
	}

	// 미리 정의된 위치 선택
	function selectLocation(location: typeof presetLocations[0]) {
		centerLat = location.lat;
		centerLon = location.lon;
	}

	// 가격 포맷팅
	function formatPrice(price: number): string {
		if (price >= 100000) {
			return `${(price / 10000).toFixed(1)}억`;
		} else if (price >= 10000) {
			return `${(price / 10000).toFixed(1)}억`;
		} else {
			return `${price.toLocaleString()}만원`;
		}
	}
</script>

<div class="container">
	<header class="header">
		<h1>🏠 네이버 부동산 크롤러</h1>
		<p>원하는 지역의 부동산 정보를 실시간으로 수집합니다</p>
	</header>

	<div class="main-content">
		<!-- 설정 패널 -->
		<div class="settings-panel">
			<h2>크롤링 설정</h2>
			
			<!-- 미리 정의된 위치 -->
			<div class="form-group">
				<label>빠른 위치 선택:</label>
				<div class="preset-buttons">
					{#each presetLocations as location}
						<button 
							type="button"
							class="preset-btn"
							onclick={() => selectLocation(location)}
						>
							{location.name}
						</button>
					{/each}
				</div>
			</div>

			<!-- 좌표 입력 -->
			<div class="form-row">
				<div class="form-group">
					<label for="lat">위도:</label>
					<input 
						id="lat"
						type="number" 
						bind:value={centerLat} 
						step="0.0001"
						placeholder="37.3642443"
					/>
				</div>
				<div class="form-group">
					<label for="lon">경도:</label>
					<input 
						id="lon"
						type="number" 
						bind:value={centerLon} 
						step="0.0001"
						placeholder="127.1084674"
					/>
				</div>
			</div>

			<!-- 반경 설정 -->
			<div class="form-group">
				<label for="radius">검색 반경:</label>
				<input 
					id="radius"
					type="number" 
					bind:value={radius} 
					step="0.001"
					min="0.001"
					max="0.01"
				/>
				<small>단위: 도 (0.001 ≈ 약 100m)</small>
			</div>

			<!-- 부동산 타입 선택 -->
			<div class="form-group">
				<label for="estate-type">부동산 타입:</label>
				<select id="estate-type" bind:value={realEstateType}>
					{#each realEstateTypes as type}
						<option value={type.value}>{type.label}</option>
					{/each}
				</select>
			</div>

			<!-- 가격 타입 선택 -->
			<div class="form-group">
				<label for="price-type">거래 타입:</label>
				<select id="price-type" bind:value={priceType}>
					{#each priceTypes as type}
						<option value={type.value}>{type.label}</option>
					{/each}
				</select>
			</div>

			<!-- 크롤링 시작 버튼 -->
			<button 
				class="crawl-btn"
				onclick={startCrawling}
				disabled={isLoading}
			>
				{#if isLoading}
					<span class="spinner"></span>
					크롤링 중...
				{:else}
					🚀 크롤링 시작
				{/if}
			</button>
		</div>

		<!-- 결과 패널 -->
		<div class="results-panel">
			<h2>크롤링 결과</h2>
			
			{#if error}
				<div class="error-message">
					❌ {error}
				</div>
			{/if}

			{#if isLoading}
				<div class="loading-message">
					<div class="spinner large"></div>
					<p>부동산 정보를 수집하고 있습니다...</p>
					<small>이 작업은 몇 분 정도 소요될 수 있습니다.</small>
				</div>
			{/if}

			{#if crawlData && !isLoading}
				<div class="results-content">
					<!-- 요약 정보 -->
					<div class="summary-card">
						<h3>📊 수집 요약</h3>
						<div class="summary-grid">
							<div class="summary-item">
								<span class="label">수집된 단지 수:</span>
								<span class="value">{crawlData.complexes.length}개</span>
							</div>
							<div class="summary-item">
								<span class="label">상세 정보:</span>
								<span class="value">{Object.keys(crawlData.complex_details).length}개</span>
							</div>
							<div class="summary-item">
								<span class="label">매물 정보:</span>
								<span class="value">{Object.keys(crawlData.articles).length}개</span>
							</div>
						</div>
					</div>

					<!-- 지역 정보 -->
					<div class="area-info-card">
						<h3>🗺️ 검색 지역</h3>
						<p>중심 좌표: {crawlData.area_info.center_lat.toFixed(6)}, {crawlData.area_info.center_lon.toFixed(6)}</p>
						<p>검색 범위: 
							위도 {crawlData.area_info.bounds.bottom_lat.toFixed(6)} ~ {crawlData.area_info.bounds.top_lat.toFixed(6)}, 
							경도 {crawlData.area_info.bounds.left_lon.toFixed(6)} ~ {crawlData.area_info.bounds.right_lon.toFixed(6)}
						</p>
					</div>

					<!-- 단지 목록 -->
					{#if crawlData.complexes.length > 0}
						<div class="complexes-card">
							<h3>🏢 단지 목록</h3>
							<div class="complexes-grid">
								{#each crawlData.complexes as complex}
									<div class="complex-item">
										<h4>{complex.complexName || '단지명 없음'}</h4>
										<div class="complex-details">
											{#if complex.tradePriceMin && complex.tradePriceMax}
												<p><strong>매매가:</strong> {formatPrice(complex.tradePriceMin)} ~ {formatPrice(complex.tradePriceMax)}</p>
											{/if}
											{#if complex.rentPriceMin && complex.rentPriceMax}
												<p><strong>전세가:</strong> {formatPrice(complex.rentPriceMin)} ~ {formatPrice(complex.rentPriceMax)}</p>
											{/if}
											<p><small>위치: {complex.lat?.toFixed(6)}, {complex.lon?.toFixed(6)}</small></p>
										</div>
									</div>
								{/each}
							</div>
						</div>
					{/if}

					<!-- 개발계획 정보 -->
					{#if crawlData.development_plans.road.length > 0 || crawlData.development_plans.rail.length > 0 || crawlData.development_plans.jigu.length > 0}
						<div class="development-card">
							<h3>🚧 개발계획</h3>
							{#if crawlData.development_plans.road.length > 0}
								<p><strong>도로:</strong> {crawlData.development_plans.road.length}개</p>
							{/if}
							{#if crawlData.development_plans.rail.length > 0}
								<p><strong>철도:</strong> {crawlData.development_plans.rail.length}개</p>
							{/if}
							{#if crawlData.development_plans.jigu.length > 0}
								<p><strong>지구:</strong> {crawlData.development_plans.jigu.length}개</p>
							{/if}
						</div>
					{/if}
				</div>
			{/if}
		</div>
	</div>
</div>

<style>
	.container {
		max-width: 1400px;
		margin: 0 auto;
		padding: 20px;
		font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
	}

	.header {
		text-align: center;
		margin-bottom: 40px;
	}

	.header h1 {
		font-size: 2.5rem;
		color: #2c3e50;
		margin-bottom: 10px;
	}

	.header p {
		color: #7f8c8d;
		font-size: 1.1rem;
	}

	.main-content {
		display: grid;
		grid-template-columns: 400px 1fr;
		gap: 30px;
		align-items: start;
	}

	.settings-panel {
		background: white;
		border-radius: 12px;
		padding: 25px;
		box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
		border: 1px solid #e1e8ed;
	}

	.settings-panel h2 {
		color: #2c3e50;
		margin-bottom: 20px;
		font-size: 1.4rem;
	}

	.form-group {
		margin-bottom: 20px;
	}

	.form-row {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 15px;
	}

	.form-group label {
		display: block;
		margin-bottom: 8px;
		font-weight: 600;
		color: #34495e;
	}

	.form-group input,
	.form-group select {
		width: 100%;
		padding: 10px 12px;
		border: 2px solid #e1e8ed;
		border-radius: 8px;
		font-size: 14px;
		transition: border-color 0.2s;
	}

	.form-group input:focus,
	.form-group select:focus {
		outline: none;
		border-color: #3498db;
	}

	.form-group small {
		display: block;
		margin-top: 5px;
		color: #7f8c8d;
		font-size: 12px;
	}

	.preset-buttons {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 8px;
		margin-top: 8px;
	}

	.preset-btn {
		padding: 8px 12px;
		border: 1px solid #bdc3c7;
		border-radius: 6px;
		background: white;
		cursor: pointer;
		font-size: 13px;
		transition: all 0.2s;
	}

	.preset-btn:hover {
		background: #ecf0f1;
		border-color: #95a5a6;
	}

	.crawl-btn {
		width: 100%;
		padding: 15px;
		background: linear-gradient(135deg, #3498db, #2980b9);
		color: white;
		border: none;
		border-radius: 8px;
		font-size: 16px;
		font-weight: 600;
		cursor: pointer;
		transition: all 0.3s;
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 8px;
	}

	.crawl-btn:hover:not(:disabled) {
		background: linear-gradient(135deg, #2980b9, #21618c);
		transform: translateY(-2px);
	}

	.crawl-btn:disabled {
		opacity: 0.7;
		cursor: not-allowed;
		transform: none;
	}

	.results-panel {
		background: white;
		border-radius: 12px;
		padding: 25px;
		box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
		border: 1px solid #e1e8ed;
		min-height: 600px;
	}

	.results-panel h2 {
		color: #2c3e50;
		margin-bottom: 20px;
		font-size: 1.4rem;
	}

	.error-message {
		background: #fee;
		color: #e74c3c;
		padding: 15px;
		border-radius: 8px;
		border: 1px solid #fadbd8;
		margin-bottom: 20px;
	}

	.loading-message {
		text-align: center;
		padding: 60px 20px;
		color: #7f8c8d;
	}

	.loading-message p {
		margin: 15px 0 5px 0;
		font-size: 1.1rem;
	}

	.spinner {
		width: 20px;
		height: 20px;
		border: 2px solid #f3f3f3;
		border-top: 2px solid #3498db;
		border-radius: 50%;
		animation: spin 1s linear infinite;
		display: inline-block;
	}

	.spinner.large {
		width: 40px;
		height: 40px;
		border-width: 3px;
	}

	@keyframes spin {
		0% { transform: rotate(0deg); }
		100% { transform: rotate(360deg); }
	}

	.results-content {
		display: flex;
		flex-direction: column;
		gap: 20px;
	}

	.summary-card,
	.area-info-card,
	.complexes-card,
	.development-card {
		background: #f8f9fa;
		border-radius: 8px;
		padding: 20px;
		border: 1px solid #e9ecef;
	}

	.summary-card h3,
	.area-info-card h3,
	.complexes-card h3,
	.development-card h3 {
		color: #2c3e50;
		margin-bottom: 15px;
		font-size: 1.2rem;
	}

	.summary-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
		gap: 15px;
	}

	.summary-item {
		display: flex;
		flex-direction: column;
		align-items: center;
		text-align: center;
	}

	.summary-item .label {
		font-size: 13px;
		color: #7f8c8d;
		margin-bottom: 5px;
	}

	.summary-item .value {
		font-size: 1.4rem;
		font-weight: 700;
		color: #2c3e50;
	}

	.complexes-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
		gap: 15px;
	}

	.complex-item {
		background: white;
		border-radius: 6px;
		padding: 15px;
		border: 1px solid #dee2e6;
	}

	.complex-item h4 {
		color: #2c3e50;
		margin-bottom: 10px;
		font-size: 1rem;
	}

	.complex-details p {
		margin: 5px 0;
		font-size: 14px;
		color: #495057;
	}

	.complex-details strong {
		color: #2c3e50;
	}

	@media (max-width: 1024px) {
		.main-content {
			grid-template-columns: 1fr;
			gap: 20px;
		}
		
		.settings-panel {
			order: 1;
		}
		
		.results-panel {
			order: 2;
		}
	}

	@media (max-width: 768px) {
		.container {
			padding: 15px;
		}
		
		.header h1 {
			font-size: 2rem;
		}
		
		.form-row {
			grid-template-columns: 1fr;
		}
		
		.preset-buttons {
			grid-template-columns: 1fr;
		}
		
		.complexes-grid {
			grid-template-columns: 1fr;
		}
	}
</style>
