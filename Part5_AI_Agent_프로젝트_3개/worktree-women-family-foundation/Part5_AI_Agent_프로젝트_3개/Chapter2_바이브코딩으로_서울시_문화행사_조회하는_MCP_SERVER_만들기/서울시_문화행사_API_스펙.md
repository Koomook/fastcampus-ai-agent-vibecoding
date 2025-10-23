# 서울시 문화행사 API 스펙

## 메타정보

| 항목 | 내용 |
|------|------|
| **공공정보명** | 문화/관광 |
| **서비스명** | 서울시 문화행사 정보 |
| **서비스설명** | 서울문화포털에서 제공하는 문화행사 정보입니다.<br>공연, 행사에 대한 장소, 날짜, 기관명, 이용대상, 이용요금, 출연자, 프로그램 등의 정보를 제공합니다. |
| **분류체계** | 문화관광>문화 |
| **원본시스템** | 서울문화포털 홈페이지 |
| **태그** | 행사, 문화, 문화포털 |
| **저작권자명** | 서울특별시 |
| **제공기관** | 서울특별시 |
| **저작권자연락처** | 02-2133-2548 |
| **제공부서** | 문화본부 문화정책과 |
| **제3저작권자** | 없음 |
| **담당자명** | 김희경 |
| **원본형태** | DB |
| **담당자연락처** | 02-2133-2548 |
| **적재주기** | 매일1회 |
| **생성기준일** | 2018.11.29 |
| **최종수정일** | 2025.10.20 |
| **데이터 공개일자** | 2018.11.29 |
| **이용허락조건** | 공공누리 1유형<br>출처표시 (상업적 이용 및 변경 가능) |

## 개요
서울문화포털에서 제공하는 문화행사 정보를 조회할 수 있는 Open API입니다.

## API 엔드포인트

### Base URL
```
http://openapi.seoul.go.kr:8088
```

### URL 구조
```
http://openapi.seoul.go.kr:8088/{KEY}/{TYPE}/culturalEventInfo/{START_INDEX}/{END_INDEX}/
```

### 샘플 URL
```
http://openapi.seoul.go.kr:8088/sample/xml/culturalEventInfo/1/5/
```

## 요청 인자

| 변수 | 타입 | 변수명 | 값 설명 |
|------|------|--------|---------|
| `KEY` | STRING(필수) | 인증키 | OPENAPI에서 발급된 인증키 |
| `TYPE` | STRING(필수) | 요청파일 타입 | xml : xml<br>xml파일 : xmlf<br>엑셀파일 : xls<br>json파일 : json |
| `SERVICE` | STRING(필수) | 서비스명 | culturalEventInfo |
| `START_INDEX` | INTEGER(필수) | 요청시작위치 | 정수 입력 (1부터 시작) |
| `END_INDEX` | INTEGER(필수) | 요청종료위치 | 정수 입력 (최대 1000건) |
| `CODENAME` | STRING(선택) | 분류 | 행사 분류 필터 |
| `TITLE` | STRING(선택) | 공연/행사명 | 행사명 검색 |
| `DATE` | STRING(선택) | 날짜/시간 | YYYY-MM-DD 형식 |

### 요청 예시

#### JSON 형식으로 1-5번 데이터 조회
```
http://openapi.seoul.go.kr:8088/{YOUR_KEY}/json/culturalEventInfo/1/5/
```

#### 특정 날짜 행사 조회
```
http://openapi.seoul.go.kr:8088/{YOUR_KEY}/json/culturalEventInfo/1/100/콘서트//2025-12-13
```

## 응답 구조

### Response Format (JSON)
```json
{
  "culturalEventInfo": {
    "list_total_count": 4,
    "RESULT": {
      "CODE": "INFO-000",
      "MESSAGE": "정상 처리되었습니다"
    },
    "row": [...]
  }
}
```

## 출력 필드

| 순번 | 필드명 | 출력명 | 설명 |
|------|--------|--------|------|
| 1 | `CODENAME` | 분류 | 행사/공연의 카테고리 (예: 전시/미술, 콘서트, 클래식, 연극) |
| 2 | `GUNAME` | 자치구 | 서울시 자치구명 (예: 강남구, 용산구, 마포구, 구로구) |
| 3 | `TITLE` | 공연/행사명 | 문화행사의 제목 |
| 4 | `DATE` | 날짜/시간 | 행사 기간 (YYYY-MM-DD~YYYY-MM-DD 형식) |
| 5 | `PLACE` | 장소 | 행사 장소명 |
| 6 | `ORG_NAME` | 기관명 | 주최 기관명 |
| 7 | `USE_TRGT` | 이용대상 | 대상 연령층 (예: 누구나, 성인, 청소년, 8세이상 관람가능) |
| 8 | `USE_FEE` | 이용요금 | 입장료/티켓 가격 정보 |
| 10 | `PLAYER` | 출연자정보 | 공연 출연자 정보 |
| 11 | `PROGRAM` | 프로그램소개 | 프로그램 상세 설명 |
| 12 | `ETC_DESC` | 기타내용 | 기타 추가 설명 |
| 13 | `ORG_LINK` | 홈페이지 주소 | 주최 기관 또는 예매 페이지 URL |
| 14 | `MAIN_IMG` | 대표이미지 | 행사 대표 이미지 URL |
| 15 | `RGSTDATE` | 신청일 | 등록일자 (YYYY-MM-DD 형식) |
| 16 | `TICKET` | 시민/기관 | 티켓 판매 주체 구분 |
| 17 | `STRTDATE` | 시작일 | 시작일 (Unix timestamp, milliseconds) |
| 18 | `END_DATE` | 종료일 | 종료일 (Unix timestamp, milliseconds) |
| 19 | `THEMECODE` | 테마분류 | 테마 분류 코드 |
| 20 | `LOT` | 위도(Y좌표) | 장소의 위도 좌표 |
| 21 | `LAT` | 경도(X좌표) | 장소의 경도 좌표 |
| 22 | `IS_FREE` | 유무료 | 유료/무료 구분 |
| 23 | `HMPG_ADDR` | 문화포털상세URL | 서울문화포털 상세 페이지 URL |

## 데이터 예시 (DATA)

### 예시 1: 전시/미술
```json
{
  "codename": "전시/미술",
  "title": "K-핸드메이드페어 2025",
  "date": "2025-12-18~2025-12-21",
  "strtdate": 1765983600000,
  "end_date": 1766242800000,
  "place": "서울 삼성동 코엑스 1층 B홀",
  "org_name": "기타",
  "use_trgt": "누구나",
  "use_fee": "사전 예매가: 8,000원, 현장 구매가: 10,000원",
  "is_free": "유료",
  "ticket": "기관",
  "player": null,
  "program": null,
  "guname": "강남구",
  "lat": "37.5118239121138",
  "lot": "127.059159043842",
  "main_img": "https://culture.seoul.go.kr/cmmn/file/getImage.do?atchFileId=42afe00583eb4b0983dba37a04a41222&thumb=Y",
  "hmpg_addr": "https://culture.seoul.go.kr/culture/culture/cultureEvent/view.do?cultcode=152033&menuNo=200009",
  "org_link": "https://k-handmade.com/",
  "themecode": "기타",
  "rgstdate": "2025-01-10",
  "etc_desc": null
}
```

### 예시 2: 콘서트
```json
{
  "codename": "콘서트",
  "title": "2025 카즈미 타테이시 트리오 내한공연 [지브리, 재즈를 만나다-서울]",
  "date": "2025-12-13~2025-12-13",
  "strtdate": 1765551600000,
  "end_date": 1765551600000,
  "place": "용산아트홀 대극장 미르",
  "org_name": "기타",
  "use_trgt": "성인, 청소년",
  "use_fee": "VIP석 77,000원 R석 66,000원 A석 55,000원",
  "is_free": "유료",
  "ticket": "시민",
  "guname": "용산구",
  "lat": "37.5324522944579",
  "lot": "126.990478820837",
  "main_img": "https://culture.seoul.go.kr/cmmn/file/getImage.do?atchFileId=311fd9815943420c808f1a00933ae9fb&thumb=Y",
  "hmpg_addr": "https://culture.seoul.go.kr/culture/culture/cultureEvent/view.do?cultcode=154341&menuNo=200008",
  "org_link": "https://tickets.interpark.com/goods/25009778",
  "themecode": "기타",
  "rgstdate": "2025-07-11"
}
```

### 예시 3: 클래식
```json
{
  "codename": "클래식",
  "title": "[마포문화재단] M 아티스트 2025 바리톤 박주성 리사이틀 Ⅱ",
  "date": "2025-12-06~2025-12-06",
  "place": "마포아트센터 아트홀맥",
  "org_name": "마포문화재단",
  "use_trgt": "8세이상 관람가능(미취학아동입장불가)",
  "use_fee": "R석 40,000원, S석 25,000원",
  "is_free": "유료",
  "ticket": "기관",
  "program": "대한민국 성악가 최초 오스트리아 빈 국립 오페라 극장 전속 솔리스트로 활동 중인 사계 성악계의 떠오르는 별 '바리톤 박주성'",
  "guname": "마포구",
  "lat": "37.5499060881738",
  "lot": "126.945533810385",
  "main_img": "https://culture.seoul.go.kr/cmmn/file/getImage.do?atchFileId=4561e62e2eca40e49c603db1855b06a4&thumb=Y",
  "hmpg_addr": "https://culture.seoul.go.kr/culture/culture/cultureEvent/view.do?cultcode=153461&menuNo=200008",
  "org_link": "https://www.mfac.or.kr/performance/whole_view.jsp?sc_b_category=17&sc_b_code=BOARD_1207683401&pk_seq=2474&page=1",
  "rgstdate": "2025-05-07"
}
```

## 분류 카테고리 (CODENAME)

API에서 제공하는 주요 분류:
- 전시/미술
- 콘서트
- 클래식
- 연극
- 기타

## 자치구 목록 (GUNAME)

서울시 25개 자치구:
- 강남구, 강동구, 강북구, 강서구
- 관악구, 광진구, 구로구, 금천구
- 노원구, 도봉구, 동대문구, 동작구
- 마포구, 서대문구, 서초구, 성동구
- 성북구, 송파구, 양천구, 영등포구
- 용산구, 은평구, 종로구, 중구, 중랑구

## 데이터 타입

- **문자열**: `codename`, `title`, `date`, `place`, `org_name`, `use_trgt`, `use_fee`, `is_free`, `ticket`, `player`, `program`, `guname`, `lat`, `lot`, `main_img`, `hmpg_addr`, `org_link`, `themecode`, `rgstdate`, `etc_desc`
- **숫자 (Unix timestamp)**: `strtdate`, `end_date`
- **Nullable**: `player`, `program`, `etc_desc` 필드는 null 값을 가질 수 있음

## 좌표 시스템

- `LAT` (경도): X좌표, WGS84 좌표계
- `LOT` (위도): Y좌표, WGS84 좌표계
- 예시: 강남구 코엑스 - 위도 37.5118239121138, 경도 127.059159043842

## 이미지 URL

대표 이미지는 서울문화포털의 이미지 서버에서 제공:
```
https://culture.seoul.go.kr/cmmn/file/getImage.do?atchFileId={파일ID}&thumb=Y
```

## 상세 정보 URL

각 문화행사의 상세 정보는 서울문화포털에서 확인 가능:
```
https://culture.seoul.go.kr/culture/culture/cultureEvent/view.do?cultcode={코드}&menuNo=200008
```

## 에러 및 정보 메시지

| 코드 | 메시지 | 설명 |
|------|--------|------|
| INFO-000 | 정상 처리되었습니다 | API 요청이 성공적으로 처리됨 |
| INFO-100 | 인증키가 유효하지 않습니다 | 인증키가 없는 경우, 열린 데이터 광장 홈페이지에서 인증키를 신청하십시오 |
| INFO-200 | 해당하는 데이터가 없습니다 | 검색 결과가 없음 |
| ERROR-300 | 필수 값이 누락되어 있습니다 | 요청인자를 참고하십시오 |
| ERROR-301 | 파일타입 값이 누락 혹은 유효하지 않습니다 | 요청인자 중 TYPE을 확인하십시오 |
| ERROR-310 | 해당하는 서비스를 찾을 수 없습니다 | 요청인자 중 SERVICE를 확인하십시오 |
| ERROR-331 | 요청시작위치 값을 확인하십시오 | 요청인자 중 START_INDEX를 확인하십시오 |
| ERROR-332 | 요청종료위치 값을 확인하십시오 | 요청인자 중 END_INDEX를 확인하십시오 |
| ERROR-333 | 요청위치 값의 타입이 유효하지 않습니다 | 요청위치 값은 정수를 입력하세요 |
| ERROR-334 | 요청종료위치 보다 요청시작위치가 더 큽니다 | 요청시작조회건수는 정수를 입력하세요 |
| ERROR-335 | 샘플데이터(샘플키:sample) 는 한번에 최대 5건을 넘을 수 없습니다 | 요청시작위치와 요청종료위치 값은 1 ~ 5 사이만 가능합니다 |
| ERROR-336 | 데이터요청은 한번에 최대 1000건을 넘을 수 없습니다 | 요청종료위치에서 요청시작위치를 뺀 값이 1000을 넘지 않도록 수정하세요 |
| ERROR-500 | 서버 오류입니다 | 지속적으로 발생시 열린 데이터 광장으로 문의(Q&A) 바랍니다 |
| ERROR-600 | 데이터베이스 연결 오류입니다 | 지속적으로 발생시 열린 데이터 광장으로 문의(Q&A) 바랍니다 |
| ERROR-601 | SQL 문장 오류 입니다 | 지속적으로 발생시 열린 데이터 광장으로 문의(Q&A) 바랍니다 |

## 주의사항 및 제약사항

1. **인증키 발급**: 서울 열린데이터광장에서 인증키를 발급받아야 합니다
2. **데이터 요청 제한**: 한 번에 최대 1000건까지만 조회 가능합니다
3. **샘플키 제한**: 샘플키(sample)로는 최대 5건까지만 조회 가능합니다
4. **날짜 형식**:
   - `DATE`: YYYY-MM-DD~YYYY-MM-DD 형식의 문자열
   - `STRTDATE`, `END_DATE`: 밀리초 단위의 Unix timestamp
5. **좌표값**: `LAT`, `LOT`는 문자열 형태로 제공됩니다
6. **Nullable 필드**: `PLAYER`, `PROGRAM`, `ETC_DESC` 등은 null 값을 가질 수 있습니다
7. **적재주기**: 매일 1회 데이터가 업데이트됩니다
