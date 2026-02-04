/**
 * 회원정보 수정 페이지 – 프론트 전용. DB·백엔드 없음.
 */

(function () {
  const STORAGE_KEY = 'wetube_logged_in';

  // 로그인 상태 확인
  if (sessionStorage.getItem(STORAGE_KEY) !== '1') {
    alert('로그인이 필요합니다.');
    window.location.href = '/auth/login';
    return;
  }

  const form = document.getElementById('profile-form');
  const msgEl = document.getElementById('profile-msg');
  const password = document.getElementById('profile-password');
  const passwordConfirm = document.getElementById('profile-password-confirm');
  const imageInput = document.getElementById('profile-image-input');
  const imagePreview = document.getElementById('profile-image-preview');
  const imagePlaceholder = document.getElementById('profile-image-placeholder');
  const imageRemove = document.getElementById('profile-image-remove');

  if (!form) return;

  // 프로필 이미지 미리보기
  if (imageInput && imagePreview && imagePlaceholder && imageRemove) {
    imageInput.addEventListener('change', function (e) {
      const file = e.target.files[0];
      if (file) {
        // 파일 크기 확인 (5MB 제한)
        if (file.size > 5 * 1024 * 1024) {
          alert('파일 크기는 5MB 이하여야 합니다.');
          imageInput.value = '';
          return;
        }

        // 이미지 파일인지 확인
        if (!file.type.startsWith('image/')) {
          alert('이미지 파일만 선택할 수 있습니다.');
          imageInput.value = '';
          return;
        }

        const reader = new FileReader();
        reader.onload = function (e) {
          imagePreview.src = e.target.result;
          imagePreview.style.display = 'block';
          imagePlaceholder.style.display = 'none';
          imageRemove.style.display = 'block';
        };
        reader.readAsDataURL(file);
      }
    });

    // 프로필 이미지 제거
    imageRemove.addEventListener('click', function () {
      imageInput.value = '';
      imagePreview.src = '';
      imagePreview.style.display = 'none';
      imagePlaceholder.style.display = 'flex';
      imageRemove.style.display = 'none';
    });
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!msgEl) return;

    // 비밀번호 변경 시 확인
    const pass = (password && password.value) || '';
    const passConfirm = (passwordConfirm && passwordConfirm.value) || '';

    if (pass && pass !== passConfirm) {
      msgEl.textContent = '비밀번호가 일치하지 않습니다.';
      msgEl.className = 'auth-msg auth-msg--error is-visible';
      return;
    }

    // 프론트엔드 전용 메시지
    const hasImage = imageInput && imageInput.files && imageInput.files.length > 0;
    let msg = '프론트엔드 전용입니다. 실제 회원정보 수정 기능은 추후 구현됩니다.';
    if (hasImage) {
      msg += '\n선택한 프로필 사진: ' + imageInput.files[0].name;
    }
    msgEl.textContent = msg;
    msgEl.className = 'auth-msg auth-msg--success is-visible';
  });
})();
