/**
 * Watch 페이지 – 프론트 전용. DB·백엔드 없음.
 */

(function () {
  // 로그인 미연동: 시청은 로그인 없이 사용 가능 (업로드와 동일)

  // 좋아요/싫어요 버튼
  const likeBtn = document.getElementById('btn-like');
  const dislikeBtn = document.getElementById('btn-dislike');

  if (likeBtn) {
    likeBtn.addEventListener('click', function () {
      this.classList.toggle('active');
      if (dislikeBtn) dislikeBtn.classList.remove('active');
      // 좋아요 수 갱신 (백엔드 연동 전: 로컬 UI만. 추후 POST /api/videos/<id>/like 구현 시 연동)
      const countEl = this.querySelector('.action-count');
      if (countEl) {
        const initial = parseInt(this.dataset.initialLikes || '0', 10) || 0;
        const delta = this.classList.contains('active') ? 1 : -1;
        const current = parseInt(countEl.textContent, 10) || initial;
        countEl.textContent = Math.max(0, current + delta);
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

  // 구독 버튼 (DB 반영)
  const subscribeBtn = document.getElementById('btn-subscribe');
  if (subscribeBtn) {
    subscribeBtn.addEventListener('click', function () {
      const username = this.dataset.channelUsername;
      if (!username) return;

      const btn = this;
      btn.disabled = true;

      var csrfMeta = document.querySelector('meta[name="csrf-token"]');
      var headers = { 'Content-Type': 'application/json', 'X-Requested-With': 'XMLHttpRequest' };
      if (csrfMeta) headers['X-CSRFToken'] = csrfMeta.getAttribute('content');

      fetch('/user/' + encodeURIComponent(username) + '/subscribe', {
        method: 'POST',
        headers: headers,
      })
        .then(function (r) { return r.json(); })
        .then(function (data) {
          if (data.ok) {
            if (data.is_subscribed) {
              btn.classList.add('subscribed', 'btn--outline');
              btn.classList.remove('btn--primary');
              btn.textContent = '구독중';
            } else {
              btn.classList.remove('subscribed', 'btn--outline');
              btn.classList.add('btn--primary');
              btn.textContent = '구독';
            }
            // 구독자 수 화면 갱신
            const subsEl = document.getElementById('channel-subs');
            if (subsEl && typeof data.subscriber_count === 'number') {
              subsEl.textContent = '구독자 ' + data.subscriber_count + '명';
            }
          } else {
            alert(data.error || '오류가 발생했습니다.');
          }
        })
        .catch(function () { alert('요청 실패'); })
        .finally(function () { btn.disabled = false; });
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

  // 댓글 입력 – 포커스 시 액션 버튼 표시 (폼 제출은 POST로 처리)
  const commentInput = document.getElementById('comment-input');
  const commentActions = document.getElementById('comment-actions');
  const commentCancel = document.getElementById('comment-cancel');

  if (commentInput && commentActions) {
    commentInput.addEventListener('focus', function () {
      commentActions.style.display = 'flex';
    });
  }

  if (commentCancel && commentInput) {
    commentCancel.addEventListener('click', function () {
      commentInput.value = '';
      commentActions.style.display = 'none';
      commentInput.blur();
    });
  }

  // 답글 버튼 – 클릭 시 답글 폼 표시
  document.querySelectorAll('.comment-reply-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      const parentId = this.dataset.parentId;
      const wrap = document.getElementById('reply-form-wrap-' + parentId);
      if (!wrap) return;
      wrap.style.display = wrap.style.display === 'none' ? 'block' : 'none';
    });
  });

  // 답글 취소
  document.querySelectorAll('.reply-cancel').forEach(function (btn) {
    btn.addEventListener('click', function () {
      const parentId = this.dataset.parentId;
      const wrap = document.getElementById('reply-form-wrap-' + parentId);
      if (wrap) wrap.style.display = 'none';
    });
  });

  // 수정 버튼 – 클릭 시 편집 폼 표시
  document.querySelectorAll('.comment-edit-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      const commentId = this.dataset.commentId;
      const textEl = document.querySelector('.comment-text[data-comment-id="' + commentId + '"]');
      const formWrap = document.getElementById('edit-form-' + commentId);
      if (!textEl || !formWrap) return;
      textEl.style.display = 'none';
      formWrap.style.display = 'block';
    });
  });

  // 수정 취소
  document.querySelectorAll('.comment-edit-cancel').forEach(function (btn) {
    btn.addEventListener('click', function () {
      const commentId = this.dataset.commentId;
      const textEl = document.querySelector('.comment-text[data-comment-id="' + commentId + '"]');
      const formWrap = document.getElementById('edit-form-' + commentId);
      if (textEl) textEl.style.display = '';
      if (formWrap) formWrap.style.display = 'none';
    });
  });

  // 정렬 버튼
  const sortBtns = document.querySelectorAll('.sort-btn');
  sortBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      sortBtns.forEach(function (b) { b.classList.remove('active'); });
      this.classList.add('active');
    });
  });
})();
