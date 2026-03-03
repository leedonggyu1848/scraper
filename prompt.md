# 일정 간격으로 githubaction을 이용하여 특정 사이트를 크롤링하고 유용한 데이터를 Telegram으로 보내는 서비스
# 참고: api에 대한 자세한 설명은 @apiexample.md 파일에 잘 정리했음
## 1. 자소설 닷컴
url: https://jasoseol.com/employment/calendar_list.json

1. post요청으로 위 사이트에서 정보를 가져옴
   - 오늘부터 한달간의 데이터를 가져오면 됨
2. employment리스트를 아래를 모두 만족하는 기준으로 필터링
   - employments의 데이터에서
   - duty_groups에 group_id가 [160, 173] 범위에 있는게 포함된 회사 (닫힌 구간)
   - division이 1 또는 3인 회사
3. 위에서 필터링한 employment 각각을 https://jasoseol.com/employment/get.json
3. 위에서 필터링한 employments를 각각 https://jasoseol.com/employment/employment_question.json 통해 자소서 질문을 가져옴
4. employment_company_id를 통해 어떤 직무가 있는지 확인하고 직무가 [160, 173]에 속하고 devision이 1또는 3인 공고를 필터링
5. 위에서 필터링한 데이터를 아래 정보를 추가하여 Telegram으로 보냄 (Telegram에 대한 정보는 시크릿으로 관리)
// 가져왔으면 하는 정보들
1. 시작일과 끝: start_time, end_time
2. 직무와 직무별 자소서 질문리스트: question
3. 공고 내용 (사진링크):  content에 src의 url
4. 공고 이름: field

# [프로젝트 개요]
GitHub Actions의 Cron 스케줄러를 이용하여 주기적으로 '자소설닷컴'의 API를 크롤링하고, 특정 조건에 맞는 개발자 채용 공고와 자소서 문항을 파싱하여 Telegram 채널로 전송하는 자동화 봇을 파이썬(Python)으로 개발하려고 합니다. 

참고: API에 대한 상세 응답 구조는 `@apiexample.md` 파일에 정의되어 있으니 이를 기반으로 코드를 작성해 주세요.

# [데이터 파이프라인 및 요구사항]

## Step 1: 전체 채용 달력 데이터 조회
- **Endpoint:** `POST https://jasoseol.com/employment/calendar_list.json`
- **Payload:** `start_time` (오늘 날짜), `end_time` (오늘부터 1달 뒤 날짜)를 ISO 8601 형식으로 요청합니다.
- **Action:** 위 API를 호출하여 한 달간의 전체 `employment` 리스트 데이터를 가져옵니다.

## Step 2: 1차 필터링 (타겟 공고 추출)
- 가져온 `employment` 리스트를 순회하며 아래 조건을 **모두** 만족하는 공고만 남깁니다.
  - 조건 1: `employments` 배열 내 요소의 `division` 값이 `1` 또는 `3` 이어야 함.
  - 조건 2: 해당 요소의 `duty_groups` 배열 내 `group_id` 값이 `160 <= group_id <= 173` (닫힌 구간)에 포함되어야 함.

## Step 3: 공고 상세 내용 및 자소서 문항 조회
- 1차 필터링을 통과한 각 공고(employment)의 ID를 사용하여 다음 두 API를 호출합니다.
  1. **상세 정보 조회:** `https://jasoseol.com/employment/get.json` (이 API 응답의 `content` HTML 내에서 `src` 속성의 이미지 URL을 추출)
  2. **자소서 문항 조회:** `https://jasoseol.com/employment/employment_question.json`

## Step 4: 2차 필터링 및 데이터 결합
- 자소서 문항 API의 응답 데이터에서 `employment_company_id` 등을 확인하여 여러 직무 중 타겟 직무만 골라냅니다.
- 앞서 정의한 필터링 조건 (`division`이 1 또는 3 이고, `group_id`가 160~173 사이)에 해당하는 직무의 자소서 문항(`question`)만 최종 데이터로 결합합니다.

## Step 5: Telegram 메시지 포맷팅 및 전송
- 추출된 데이터를 읽기 좋게 포맷팅하여 Telegram API로 전송합니다. 봇 토큰과 채널 ID는 GitHub Actions의 `Secrets` 환경변수(`TELEGRAM_TOKEN`, `TELEGRAM_CHAT_ID`)를 사용해 안전하게 로드합니다.
- **메시지에 반드시 포함되어야 할 정보:**
  1. **공고 이름:** `field` (또는 `name`)
  2. **접수 기간:** `start_time` ~ `end_time` (보기 편한 날짜 형식으로 변환)
  3. **공고 본문 이미지:** 추출한 `content` 내부의 `src` 이미지 링크
  4. **모집 직무 및 자소서 문항:** 필터링된 직무 이름과 해당 직무의 `question` 리스트 내용

# [지시사항]
위 요구사항을 바탕으로 `requests` 라이브러리를 활용한 파이썬 스크립트 코드와, 이 스크립트를 주기적으로 실행할 GitHub Actions `workflow.yml` 파일을 함께 작성해 주세요. 중복 전송 방지에 대한 간단한 로직(예: 발송된 공고 ID를 파일로 임시 저장)도 포함되면 좋습니다.