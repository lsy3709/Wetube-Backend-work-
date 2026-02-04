/**
 * Studio 영상 수정 페이지 – 프론트 전용. DB·백엔드 없음.
 */

(function () {
  const MAX_THUMBNAIL_SIZE = 5 * 1024 * 1024; // 5MB

  // 로그인 미연동: 편집 시 서버에서 config.DEFAULT_USER_ID 사용
  const form = document.getElementById('edit-form');
  const thumbnailInput = document.getElementById('edit-thumbnail');
  const thumbnailPlaceholder = document.getElementById('edit-thumbnail-placeholder');
  const thumbnailImg = document.getElementById('edit-thumbnail-img');
  const thumbnailRemove = document.getElementById('edit-thumbnail-remove');
  const titleInput = document.getElementById('edit-title');
  const descriptionInput = document.getElementById('edit-description');
  const msgEl = document.getElementById('edit-msg');
  const submitBtn = document.getElementById('edit-submit-btn');
  const deleteBtn = document.getElementById('edit-delete-btn');

  // 썸네일 선택
  if (thumbnailInput) {
    thumbnailInput.addEventListener('change', function (e) {
      const file = e.target.files[0];
      if (file) {
        if (file.size > MAX_THUMBNAIL_SIZE) {
          if (msgEl) {
            msgEl.textContent = '썸네일 파일 크기는 5MB 이하여야 합니다.';
            msgEl.className = 'auth-msg auth-msg--error is-visible';
          }
          thumbnailInput.value = '';
          return;
        }

        if (!file.type.startsWith('image/')) {
          if (msgEl) {
            msgEl.textContent = '이미지 파일만 선택할 수 있습니다.';
            msgEl.className = 'auth-msg auth-msg--error is-visible';
          }
          thumbnailInput.value = '';
          return;
        }

        const reader = new FileReader();
        reader.onload = function (e) {
          if (thumbnailImg) {
            thumbnailImg.src = e.target.result;
            thumbnailImg.style.display = 'block';
          }
          if (thumbnailPlaceholder) thumbnailPlaceholder.style.display = 'none';
          if (thumbnailRemove) thumbnailRemove.style.display = 'block';
        };
        reader.readAsDataURL(file);
      }
    });

    // 썸네일 제거
    if (thumbnailRemove) {
      thumbnailRemove.addEventListener('click', function () {
        thumbnailInput.value = '';
        if (thumbnailImg) {
          thumbnailImg.src = '';
          thumbnailImg.style.display = 'none';
        }
        if (thumbnailPlaceholder) thumbnailPlaceholder.style.display = 'flex';
        thumbnailRemove.style.display = 'none';
      });
    }
  }

  // 폼 제출 (저장)
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!msgEl) return;

      const title = titleInput && titleInput.value.trim();

      if (!title) {
        msgEl.textContent = '제목을 입력해주세요.';
        msgEl.className = 'auth-msg auth-msg--error is-visible';
        titleInput && titleInput.focus();
        return;
      }

      // 프론트엔드 전용 메시지
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.textContent = '저장 중...';
      }

      setTimeout(function () {
        msgEl.textContent = '프론트엔드 전용입니다. 실제 저장 기능은 추후 구현됩니다.';
        msgEl.className = 'auth-msg auth-msg--success is-visible';

        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.textContent = '저장';
        }
      }, 1000);
    });
  }

  // 삭제 버튼
  if (deleteBtn) {
    deleteBtn.addEventListener('click', function () {
      if (confirm('정말로 이 동영상을 삭제하시겠습니까?\n이 작업은 되돌릴 수 없습니다.')) {
        if (msgEl) {
          msgEl.textContent = '프론트엔드 전용입니다. 실제 삭제 기능은 추후 구현됩니다.';
          msgEl.className = 'auth-msg auth-msg--success is-visible';
        }
      }
    });
  }

  // 문자 수 카운터
  if (titleInput) {
    titleInput.addEventListener('input', function () {
      const len = this.value.length;
      const hint = this.nextElementSibling;
      if (hint && hint.classList.contains('form-hint')) {
        hint.textContent = len + '/100자';
      }
    });
  }

  if (descriptionInput) {
    descriptionInput.addEventListener('input', function () {
      const len = this.value.length;
      const hint = this.nextElementSibling;
      if (hint && hint.classList.contains('form-hint')) {
        hint.textContent = len + '/5000자';
      }
    });
  }
})();
