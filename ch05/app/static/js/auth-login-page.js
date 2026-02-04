/**
 * 로그인 페이지 – 프론트 전용.
 * 일반: aaa / 123456 → /
 * 관리자: admin / 1234qwer → /admin/
 */

(function () {
  const STORAGE_KEY = 'wetube_logged_in';
  const USER_KEY = 'wetube_user';
  const ADMIN_KEY = 'wetube_admin_logged_in';

  const form = document.getElementById('login-form');
  const username = document.getElementById('login-username');
  const password = document.getElementById('login-password');
  const errorEl = document.getElementById('login-error');

  if (!form) return;

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var user = (username && username.value) || '';
    var pass = (password && password.value) || '';

    if (errorEl) {
      errorEl.textContent = '';
      errorEl.classList.remove('is-visible', 'auth-msg--error');
    }

    // 관리자 로그인
    if (user === 'admin' && pass === '1234qwer') {
      sessionStorage.setItem(STORAGE_KEY, '1');
      sessionStorage.setItem(USER_KEY, 'admin');
      sessionStorage.setItem(ADMIN_KEY, '1');
      window.location.href = '/admin/';
      return;
    }

    // 일반 사용자 로그인
    if (user === 'aaa' && pass === '123456') {
      sessionStorage.setItem(STORAGE_KEY, '1');
      sessionStorage.setItem(USER_KEY, 'aaa');
      sessionStorage.removeItem(ADMIN_KEY);
      window.location.href = '/';
      return;
    }

    if (errorEl) {
      errorEl.textContent = '사용자명 또는 비밀번호가 올바르지 않습니다.';
      errorEl.classList.add('is-visible', 'auth-msg--error');
    }
  });
})();
