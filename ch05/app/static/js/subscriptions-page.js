/**
 * 구독 페이지 – 프론트 전용. DB·백엔드 없음.
 */

(function () {
  const STORAGE_KEY = 'wetube_logged_in';

  // 로그인 상태 확인
  if (sessionStorage.getItem(STORAGE_KEY) !== '1') {
    return;
  }

  // 필터 버튼
  const filterBtns = document.querySelectorAll('.filter-btn');
  const subscriptionSections = document.querySelectorAll('.subscription-section');
  const subscriptionsEmpty = document.getElementById('subscriptions-empty');

  filterBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      const filter = this.dataset.filter;

      // 버튼 활성화
      filterBtns.forEach(function (b) { b.classList.remove('active'); });
      this.classList.add('active');

      // 필터 적용 (프론트엔드 전용 - 실제 필터링은 백엔드에서 처리)
      console.log('필터 적용:', filter);

      // 예시: 오늘 필터는 빈 상태 표시
      if (filter === 'today' && subscriptionsEmpty) {
        subscriptionSections.forEach(function (section) {
          section.style.display = 'none';
        });
        subscriptionsEmpty.style.display = 'block';
      } else {
        subscriptionSections.forEach(function (section) {
          section.style.display = 'block';
        });
        if (subscriptionsEmpty) subscriptionsEmpty.style.display = 'none';
      }
    });
  });

  // 구독 취소 버튼
  const unsubscribeBtns = document.querySelectorAll('[data-unsubscribe]');

  unsubscribeBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      const channelId = this.dataset.channel;
      const section = this.closest('.subscription-section');

      if (confirm('정말로 이 채널의 구독을 취소하시겠습니까?')) {
        // 프론트엔드 전용: 섹션 숨김
        if (section) {
          section.style.transition = 'opacity 0.3s';
          section.style.opacity = '0';
          setTimeout(function () {
            section.style.display = 'none';

            // 모든 섹션이 숨겨졌는지 확인
            const visibleSections = Array.from(subscriptionSections).filter(function (s) {
              return s.style.display !== 'none';
            });

            if (visibleSections.length === 0 && subscriptionsEmpty) {
              subscriptionsEmpty.style.display = 'block';
            }
          }, 300);
        }

        console.log('구독 취소:', channelId);
      }
    });
  });
})();
