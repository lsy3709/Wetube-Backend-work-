/**
 * 검색 페이지 – 프론트 전용. DB·백엔드 없음.
 */

(function () {
  const STORAGE_KEY = 'wetube_logged_in';

  // 로그인 상태 확인
  if (sessionStorage.getItem(STORAGE_KEY) !== '1') {
    return;
  }

  // 필터 탭
  const filterTabs = document.querySelectorAll('.filter-tab');
  const resultsList = document.getElementById('results-list');
  const resultsChannels = document.getElementById('results-channels');

  filterTabs.forEach(function (tab) {
    tab.addEventListener('click', function () {
      const filter = this.dataset.filter;

      // 탭 활성화
      filterTabs.forEach(function (t) { t.classList.remove('active'); });
      this.classList.add('active');

      // 결과 표시/숨김
      if (filter === 'channels') {
        if (resultsList) resultsList.style.display = 'none';
        if (resultsChannels) resultsChannels.style.display = 'block';
      } else {
        if (resultsList) resultsList.style.display = 'block';
        if (resultsChannels) resultsChannels.style.display = 'none';
      }

      // 결과 수 업데이트
      const countEl = document.getElementById('results-count');
      if (countEl) {
        if (filter === 'channels') {
          countEl.textContent = '5';
        } else {
          countEl.textContent = '10';
        }
      }
    });
  });

  // 정렬 메뉴
  const sortBtn = document.getElementById('sort-btn');
  const sortMenu = document.getElementById('sort-menu');
  const sortOptions = document.querySelectorAll('.sort-option');

  if (sortBtn && sortMenu) {
    sortBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      sortMenu.style.display = sortMenu.style.display === 'none' ? 'block' : 'none';
    });

    // 외부 클릭 시 메뉴 닫기
    document.addEventListener('click', function (e) {
      if (!sortBtn.contains(e.target) && !sortMenu.contains(e.target)) {
        sortMenu.style.display = 'none';
      }
    });
  }

  // 정렬 옵션 선택
  sortOptions.forEach(function (option) {
    option.addEventListener('click', function () {
      const sort = this.dataset.sort;

      // 옵션 활성화
      sortOptions.forEach(function (o) { o.classList.remove('active'); });
      this.classList.add('active');

      // 정렬 텍스트 업데이트
      const sortText = sortBtn.querySelector('.sort-text');
      if (sortText) {
        const sortLabels = {
          relevance: '관련성',
          date: '업로드 날짜',
          views: '조회수',
          rating: '평점'
        };
        sortText.textContent = sortLabels[sort] || '정렬 기준';
      }

      // 메뉴 닫기
      if (sortMenu) sortMenu.style.display = 'none';

      // 프론트엔드 전용: 실제 정렬은 백엔드에서 처리
      console.log('정렬 기준:', sort);
    });
  });

  // 구독 버튼 (채널 결과)
  const subscribeBtns = document.querySelectorAll('[data-subscribe]');
  subscribeBtns.forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();

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
  });
})();
