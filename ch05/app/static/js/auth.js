/**
 * WeTube – 로그인 상태 적용·로그아웃 (프론트 전용).
 * 로그인: /auth/login 에서 aaa / 123456
 */

(function () {
  const STORAGE_KEY = 'wetube_logged_in';
  const USER_KEY = 'wetube_user';
  const VALID_USER = 'aaa';

  const logoutBtn = document.getElementById('btn-logout');

  function isLoggedIn() {
    return sessionStorage.getItem(STORAGE_KEY) === '1';
  }

  function setLoggedIn(value) {
    if (value) {
      sessionStorage.setItem(STORAGE_KEY, '1');
      sessionStorage.setItem(USER_KEY, VALID_USER);
    } else {
      sessionStorage.removeItem(STORAGE_KEY);
      sessionStorage.removeItem(USER_KEY);
      sessionStorage.removeItem('wetube_admin_logged_in');
    }
  }

  function applyUI() {
    const loggedIn = isLoggedIn();
    const isAdmin = sessionStorage.getItem('wetube_admin_logged_in') === '1';
    document.body.classList.toggle('is-logged-in', loggedIn);
    document.body.classList.toggle('is-admin', isAdmin);
    const userEl = document.getElementById('header-username');
    if (userEl) {
      const u = sessionStorage.getItem(USER_KEY) || VALID_USER;
      userEl.textContent = loggedIn ? (u ? u.charAt(0).toUpperCase() : '') : '';
    }
    document.querySelectorAll('[data-admin-only]').forEach(function (el) {
      el.style.display = isAdmin ? '' : 'none';
    });
  }

  function handleLogout() {
    setLoggedIn(false);
    applyUI();
  }

  if (logoutBtn) logoutBtn.addEventListener('click', handleLogout);

  applyUI();
})();
