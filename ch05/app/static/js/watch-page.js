/**
 * Watch 페이지 – 프론트 전용. DB·백엔드 없음.
 */

(function () {
  const STORAGE_KEY = 'wetube_logged_in';

  // 로그인 상태 확인
  if (sessionStorage.getItem(STORAGE_KEY) !== '1') {
    return;
  }

  // 좋아요/싫어요 버튼
  const likeBtn = document.getElementById('btn-like');
  const dislikeBtn = document.getElementById('btn-dislike');

  if (likeBtn) {
    likeBtn.addEventListener('click', function () {
      this.classList.toggle('active');
      if (dislikeBtn) dislikeBtn.classList.remove('active');
      
      const countEl = this.querySelector('.action-count');
      if (countEl) {
        const current = parseInt(countEl.textContent) || 0;
        countEl.textContent = this.classList.contains('active') ? current + 1 : Math.max(0, current - 1);
      }
    });
  }

  if (dislikeBtn) {
    dislikeBtn.addEventListener('click', function () {
      this.classList.toggle('active');
      if (likeBtn) likeBtn.classList.remove('active');
    });
  }

  // 공유 버튼
  const shareBtn = document.getElementById('btn-share');
  if (shareBtn) {
    shareBtn.addEventListener('click', function () {
      const url = window.location.href;
      if (navigator.clipboard) {
        navigator.clipboard.writeText(url).then(function () {
          alert('링크가 클립보드에 복사되었습니다.');
        });
      } else {
        prompt('링크를 복사하세요:', url);
      }
    });
  }

  // 저장 버튼
  const saveBtn = document.getElementById('btn-save');
  if (saveBtn) {
    saveBtn.addEventListener('click', function () {
      this.classList.toggle('active');
      const text = this.querySelector('.action-text');
      if (text) {
        text.textContent = this.classList.contains('active') ? '저장됨' : '저장';
      }
    });
  }

  // 구독 버튼
  const subscribeBtn = document.getElementById('btn-subscribe');
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

  // 설명 더보기/접기
  const descriptionContent = document.getElementById('description-content');
  const descriptionToggle = document.getElementById('description-toggle');

  if (descriptionContent && descriptionToggle) {
    descriptionToggle.addEventListener('click', function () {
      descriptionContent.classList.toggle('expanded');
      this.textContent = descriptionContent.classList.contains('expanded') ? '간략히' : '더보기';
    });
  }

  // 댓글 입력
  const commentInput = document.getElementById('comment-input');
  const commentActions = document.getElementById('comment-actions');
  const commentCancel = document.getElementById('comment-cancel');
  const commentSubmit = document.getElementById('comment-submit');
  const commentsList = document.getElementById('comments-list');
  const commentsCount = document.getElementById('comments-count');

  if (commentInput && commentActions) {
    commentInput.addEventListener('focus', function () {
      commentActions.style.display = 'flex';
    });
  }

  if (commentCancel) {
    commentCancel.addEventListener('click', function () {
      commentInput.value = '';
      commentActions.style.display = 'none';
      commentInput.blur();
    });
  }

  if (commentSubmit) {
    commentSubmit.addEventListener('click', function () {
      const text = commentInput.value.trim();
      if (!text) {
        alert('댓글 내용을 입력해주세요.');
        return;
      }

      // 새 댓글 추가 (프론트엔드 전용)
      const commentItem = document.createElement('div');
      commentItem.className = 'comment-item';
      commentItem.innerHTML = `
        <div class="comment-avatar"><span>A</span></div>
        <div class="comment-body">
          <div class="comment-header">
            <span class="comment-author">aaa</span>
            <span class="comment-time">방금 전</span>
          </div>
          <p class="comment-text">${escapeHtml(text)}</p>
          <div class="comment-footer">
            <button type="button" class="comment-action">👍 0</button>
            <button type="button" class="comment-action">👎</button>
            <button type="button" class="comment-action">답글</button>
          </div>
        </div>
      `;

      if (commentsList) {
        commentsList.insertBefore(commentItem, commentsList.firstChild);
      }

      // 댓글 수 업데이트
      if (commentsCount) {
        commentsCount.textContent = parseInt(commentsCount.textContent) + 1;
      }

      // 입력 초기화
      commentInput.value = '';
      commentActions.style.display = 'none';
    });
  }

  // HTML 이스케이프
  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  // 정렬 버튼
  const sortBtns = document.querySelectorAll('.sort-btn');
  sortBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      sortBtns.forEach(function (b) { b.classList.remove('active'); });
      this.classList.add('active');
    });
  });
})();
