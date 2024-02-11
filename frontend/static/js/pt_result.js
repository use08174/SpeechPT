const fileNameDisplay = document.querySelector('.file-name-display');
const fileNameElement = document.querySelector('.file-name');

// 전 페이지에서 받아온 파일 이름을 저장할 변수
let receivedFileName;

// 페이지 로드 시점에 실행
window.addEventListener('load', () => {
  // URL 파라미터에서 파일 이름 추출
const urlParams = new URLSearchParams(window.location.search);
receivedFileName = urlParams.get('fileName');

  // 파일 이름이 존재하면 표시
if (receivedFileName) {
    fileNameElement.textContent = receivedFileName;
    fileNameDisplay.classList.remove('hidden');
} else {
    // 파일 이름이 없으면 '파일 이름을 찾을 수 없습니다' 메시지 표시
    fileNameElement.textContent = '파일 이름을 찾을 수 없습니다.';
}
});

// 파일 이름 표시 영역 숨기기 함수
function hideFileNameDisplay() {
fileNameDisplay.classList.add('hidden');
}


