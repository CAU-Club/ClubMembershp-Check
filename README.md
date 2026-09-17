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

### 4. Vercel 회원가입 + project 확인
- [ ] Vercel 대시보드에서 이 프로젝트의 **팀원으로 초대**받거나, 프로젝트/계정 자체를 이전받기
- [ ] Settings → Environment Variables에서 `HASH_PEPPER`가 로컬 `.env`와 동일한 값으로 등록되어 있는지 확인
- [ ] 배포된 URL(`https://....vercel.app`, 또는 연결된 커스텀 도메인)이 정상 작동하는지 직접 확인/테스트

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

## 배포 방법

1. **GitHub 비공개 저장소 생성**
   - `webapp` 폴더만 올릴 새 저장소를 만드세요 (반드시 **Private**).
   - `회원명단.xlsx` 원본 파일은 이 저장소에 절대 올리지 마세요 (`.gitignore`에 이미 `*.xlsx`, `.env` 제외 처리됨).
   - `git init` -> `git add .` -> `git commit` -> GitHub에 push.
   - `data/members.hashes.json`은 해시값만 있어서 커밋해도 안전합니다.

2. **Vercel 프로젝트 생성**
   - [vercel.com](https://vercel.com) 가입 (GitHub 계정으로 로그인 가능) 후 `New Project` -> 방금 만든 저장소 선택.
   - Framework Preset: `Other` (자동 감지됨, 별도 빌드 설정 불필요).

3. **환경변수 등록 (가장 중요)**
   - Vercel 프로젝트 -> Settings -> Environment Variables
   - `HASH_PEPPER` = (로컬 `webapp/.env` 파일에 있는 값과 **똑같이** 입력, Production/Preview 둘 다 체크)
   - 이 값이 다르면 모든 조회가 "일치하는 회원이 없습니다"로 나옵니다.

4. **Deploy** 클릭 -> 완료되면 `https://프로젝트이름.vercel.app` 형태 URL이 생성됩니다. 이 링크를 회원들에게 공유하면 됩니다.

## 회원명단이 바뀔 때 (재배포)

1. 새 `회원명단.xlsx`로 교체
2. cd webapp
3. $env:HASH_PEPPER="(.env에 있는 값)"
4. python scripts/build_data.py ../회원명단.xlsx
5. `git add .
6. git commit -m "회원명단 갱신"
7. git push


