/**
 * 사용자 프로필 페이지 – 프론트 전용.
 */

(function () {
  const subscribeBtn = document.getElementById('btn-subscribe');
  const profileTabs = document.querySelectorAll('.profile-tab');
  const tabContents = document.querySelectorAll('.user-profile-content');

  if (subscribeBtn) {
    subscribeBtn.addEventListener('click', function () {
      if (this.classList.contains('subscribed')) {
        this.classList.remove('subscribed', 'btn--outline');
        this.classList.add('btn--primary');
        this.textContent = '구독';
      } else {
        this.classList.add('subscribed', 'btn--outline');
        this.classList.remove('btn--primary');
        this.textContent = '구독중';
      }
    });
  }

  profileTabs.forEach(function (tab) {
    tab.addEventListener('click', function () {
      const tabName = this.dataset.tab;

      profileTabs.forEach(function (t) { t.classList.remove('active'); });
      this.classList.add('active');

      tabContents.forEach(function (content) {
        const id = content.id;
        if (id === 'tab-' + tabName) {
          content.style.display = 'block';
        } else {
          content.style.display = 'none';
        }
      });
    });
  });
})();
