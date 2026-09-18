const crypto = require('crypto');
const data = require('../data/members.hashes.json');
const MEMBERS = data.members;
const PEPPER = process.env.HASH_PEPPER;
const MAX_ATTEMPTS = 5;
const LOCK_MS = 10 * 60 * 1000;
const attempts = new Map();

function digitsOnly(value) {
  return String(value || '').replace(/[^0-9]/g, '');
}

module.exports = (req, res) => {
  if (req.method !== 'POST') {
    res.status(405).json({ status: 'error', message: 'POST 요청만 허용됩니다.' });
    return;
  }

  if (!PEPPER) {
    res.status(500).json({ status: 'error', message: '서버 설정 오류입니다. 관리자에게 문의해주세요.' });
    return;
  }

  const body = req.body || {};
  const studentId = digitsOnly(body.studentId);
  const name = String(body.name || '').trim().normalize('NFC');
  const phoneLast4 = digitsOnly(body.phoneLast4);

  if (!studentId || !name || phoneLast4.length !== 4) {
    res.status(400).json({ status: 'error', message: '학번, 이름, 전화번호 뒷자리 4자리를 모두 정확히 입력해주세요.' });
    return;
  }

  const now = Date.now();
  const record = attempts.get(studentId);
  if (record && record.count >= MAX_ATTEMPTS && now - record.first < LOCK_MS) {
    res.status(429).json({ status: 'locked', message: '시도 횟수를 초과했습니다. 10분 후 다시 시도해주세요.' });
    return;
  }

  const key = `${studentId}:${name}:${phoneLast4}:${PEPPER}`;
  const hash = crypto.createHash('sha256').update(key, 'utf8').digest('hex');
  const clubs = MEMBERS[hash];

  if (clubs) {
    attempts.delete(studentId);
    const clubText = clubs.length ? clubs.join(', ') : '정보 없음';
    res.status(200).json({
      status: 'found',
      recognized: true,
      message: `정회원으로 인정되었습니다.\n${name}님 가입 동아리: ${clubText}`
    });
    return;
  }

  if (!record || now - record.first > LOCK_MS) {
    attempts.set(studentId, { count: 1, first: now });
  } else {
    record.count += 1;
  }

  res.status(200).json({
    status: 'not_found',
    recognized: false,
    message: '입력하신 정보와 일치하는 회원 명단을 찾을 수 없습니다. \n개인정보를 다시 확인해주세요. \n 문의사항은 [동아리연합회 사무회계국]으로 문의해주세요.'
  });
};
