# 동아리연합회 회원 인정 여부 확인

## 가동법

### 0. 개발 환경 준비
- vscode 설치
- python 설치

### 1. repository clone
- cd webapp
- git clone https://github.com/CAU-Club/ClubMembershp-Check.git

### 2. 회원명단 원본 파일 저장
- 재등록이 끝나고 최종 '회원명단.xlsx'를 준비, 같은 경로에 올리기

### 3. HASH_PEPPER 값 전달받기
- local의 `webapp/.env` 로 저장

### 4. Vercel
- Settings → Environment Variables에서 `HASH_PEPPER` = `.env`이어야 함

### 5. environment setting
- cd webapp
- pip install -r requirements.txt

### 6. HASH_PEPPER 잃어버린 경우
- `회원명단.xlsx`로 `build_data.py` 재실행

## 구조

```
webapp/
  index.html               프론트엔드 (확인 폼)
  api/check.js             서버리스 함수 (해시 대조만 수행)
  data/members.hashes.json 회원 정보를 해시로 변환한 결과물
  scripts/build_data.py    회원명단.xlsx -> members.hashes.json 생성 script
  .env                     HASH_PEPPER 값
```
## 회원명단이 바뀔 때 (재배포)

1. 새 `회원명단.xlsx`로 교체
2. cd webapp
3. $env:HASH_PEPPER="(.env에 있는 값)"
4. python scripts/build_data.py ../회원명단.xlsx
5. `git add .
6. git commit -m "회원명단 갱신"
7. git push


