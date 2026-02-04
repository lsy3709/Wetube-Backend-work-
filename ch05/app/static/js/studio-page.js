/**
 * Studio 페이지 – 프론트 전용. DB·백엔드 없음.
 */

(function () {
  const STORAGE_KEY = 'wetube_logged_in';
  const uploadBtn = document.getElementById('btn-upload');
  const uploadBtnEmpty = document.getElementById('btn-upload-empty');
  const emptyState = document.getElementById('studio-empty');
  const videoList = document.getElementById('studio-video-list');

  // 로그인 상태 확인
  if (sessionStorage.getItem(STORAGE_KEY) !== '1') {
    // 로그인하지 않은 경우는 base.html의 data-logged-out-only가 처리
    return;
  }

  // 업로드 버튼은 링크로 처리 (studio/upload.html로 이동)

  // 동영상 목록 표시/숨김 (샘플 데이터가 있으면 목록 표시)
  if (emptyState && videoList) {
    const hasVideos = document.querySelectorAll('.video-row').length > 0;
    if (hasVideos) {
      emptyState.style.display = 'none';
      videoList.style.display = 'block';
    } else {
      emptyState.style.display = 'block';
      videoList.style.display = 'none';
    }
  }
})();
