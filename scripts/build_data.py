import sys
import os
import json
import hashlib
import unicodedata
import openpyxl

def norm_name(value):
    return unicodedata.normalize('NFC', str(value).strip())

def digits_only(value):
    return ''.join(ch for ch in str(value) if ch.isdigit())

def main():
    if len(sys.argv) < 2:
        sys.exit('사용법: python build_data.py <회원명단.xlsx 경로>')

    xlsx_path = sys.argv[1]
    pepper = os.environ.get('HASH_PEPPER')
    if not pepper:
        sys.exit(
            'HASH_PEPPER 환경변수가 설정되지 않았습니다.\n'
            '먼저 임의의 긴 랜덤 문자열을 정하고 아래처럼 실행하세요.\n'
            '  PowerShell:  $env:HASH_PEPPER="긴랜덤문자열"\n'
            '같은 값을 Vercel 프로젝트의 환경변수 HASH_PEPPER 에도 반드시 동일하게 등록해야 합니다.'
        )

    wb = openpyxl.load_workbook(xlsx_path, read_only=True, data_only=True)
    ws = wb.worksheets[0]
    rows = ws.iter_rows(values_only=True)
    header = list(next(rows))
    idx = {h: i for i, h in enumerate(header) if h}

    for required in ('학번', '이름', '전화번호'):
        if required not in idx:
            sys.exit(f'헤더에서 "{required}" 컬럼을 찾을 수 없습니다. 실제 헤더: {header}')

    club_col = idx.get('동아리명')

    members = {}
    skipped = 0
    for row in rows:
        student_id = digits_only(row[idx['학번']])
        name = norm_name(row[idx['이름']])
        phone_digits = digits_only(row[idx['전화번호']])
        club = str(row[club_col]).strip() if club_col is not None and row[club_col] else ''

        if not student_id or not name or len(phone_digits) < 4:
            skipped += 1
            continue

        last4 = phone_digits[-4:]
        key = f'{student_id}:{name}:{last4}:{pepper}'
        h = hashlib.sha256(key.encode('utf-8')).hexdigest()

        clubs = members.setdefault(h, [])
        if club and club not in clubs:
            clubs.append(club)

    out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'members.hashes.json')

    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump({'members': members}, f, ensure_ascii=False)

    print(f'생성 완료: 고유 {len(members)}건 -> {out_path} (스킵된 행: {skipped}건)')

if __name__ == '__main__':
    main()
