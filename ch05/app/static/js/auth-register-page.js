/**
 * 회원가입 페이지 – 프론트 전용. DB·백엔드 없음.
 */

(function () {
  const form = document.getElementById('register-form');
  const msgEl = document.getElementById('register-msg');

  if (!form) return;

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!msgEl) return;

    msgEl.textContent = '프론트엔드 전용입니다. 실제 회원가입 기능은 추후 구현됩니다.';
    msgEl.className = 'auth-msg auth-msg--error is-visible';
  });
})();
