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

let oldOnclick;
async function uploadFile() {
  const fileInput = document.getElementById('textfile');
  const file = fileInput.files[0];
  const upload_btn = document.querySelector('.analysis-box');
  document.getElementById('analysis-exp-text').style.display = 'none';
  document.getElementById('analysis-exp-text2').style.display = 'none';  
  document.getElementById("mask0_39_984").style.display = 'none';
  document.querySelector('.upload_svg').style.display = 'none';
  oldOnclick = upload_btn.onclick;
  upload_btn.onclick = null;
  upload_btn.style.border='2px solid #DFDFDF';
  upload_btn.style.background = '#FFF';
  upload_btn.style.cursor = 'default';

  const svgElement = createSvgElement('svg', {
    'width': '29px',
    'height': '37px',
    'flex-shrink': '0',
    'viewBox': '0 0 30 38',
    'fill': 'none',
    'id': 'pdf_svg'}
  );
  
  const paths = [ 
    {'d': "M19.8213 0L24.4463 4.625L29.0713 9.25H19.8213V0Z", 'fill':'#92DBFF' },
    {'d' : "M2 0C0.895431 0 0 0.895432 0 2V35C0 36.1046 0.895431 37 2 37H27.0714C28.176 37 29.0714 36.1046 29.0714 35V9.25H19.8215V0H2Z",'fill-rule':'evenodd'
    , 'fill': '#00A8F4', 'clip-rule': 'evenodd' },
    { 'd': "M23.3811 18.1084V19.2025H20.4396V20.8041H23.0719V21.8983H20.4396V24.6257H19.1948V18.1084H23.3811Z", 'fill' : 'white' },
    { 'd' : "M15.3969 18.1084C15.9624 18.1084 16.4699 18.222 16.9192 18.4493C17.3684 18.6713 17.7199 18.999 17.9737 19.4325C18.2327 19.8659 18.3622 20.3813 18.3622 20.9785V21.7555C18.3622 22.3528 18.2327 22.8682 17.9737 23.3016C17.7199 23.735 17.3684 24.0628 16.9192 24.2848C16.4699 24.512 15.9624 24.6257 15.3969 24.6257H13.0024V18.1084H15.3969ZM17.1174 21.0182C17.1174 20.4315 16.9588 19.9901 16.6417 19.6941C16.3298 19.3928 15.9149 19.2422 15.3969 19.2422H14.2472V23.4919H15.3969C15.9202 23.4919 16.3377 23.3439 16.6496 23.0479C16.9614 22.7519 17.1174 22.3079 17.1174 21.7159V21.0182Z", 'fill' : 'white'},
    { 'd' : "M10.0872 18.1084C10.7585 18.1084 11.3002 18.2828 11.7125 18.6317C12.1248 18.9753 12.331 19.48 12.331 20.146C12.331 20.8173 12.1248 21.3248 11.7125 21.6683C11.3002 22.0119 10.7585 22.1837 10.0872 22.1837H8.61246V24.6257H7.36768V18.1084H10.0872ZM10.0237 21.0895C10.3673 21.0895 10.629 21.0076 10.8087 20.8438C10.9937 20.6799 11.0862 20.4473 11.0862 20.146C11.0862 19.8448 10.9937 19.6122 10.8087 19.4483C10.629 19.2845 10.3673 19.2025 10.0237 19.2025H8.61246V21.0895H10.0237Z", 'fill' : 'white' }
    ]
  paths.forEach(path => {
    svgElement.appendChild(createSvgElement('path',path))
  });
  svgElement.id = 'pdf_svg';

  const waitingBox = document.createElement('div');
  waitingBox.className = 'uploadBox';
  waitingBox.style.cursor = 'default';

  // document.querySelector('.analButton').style.display = 'block';
  const analbutton = document.createElement('div');
  analbutton.className = 'analButton';
  analbutton.onclick = anal;
  analbutton.style.display = 'block';
  
  const fileSizeInMB = file.size/1024/1024;

  const fileNameElement = document.createElement('div');
  fileNameElement.id = 'fileNameElementId';
  var file_name = truncateText(file.name,18);
  fileNameElement.innerText = file_name;

  const fileNameElement2 = document.createElement('div');
  fileNameElement2.id = 'fileNameElementId2';
  fileNameElement2.innerText = '분석하기'

  const fileNameElement3 = document.createElement('div');
  fileNameElement3.id = 'fileNameElementId3';
  fileNameElement3.innerText = fileSizeInMB.toFixed(2)+'MB';

  waitingBox.appendChild(fileNameElement);
  waitingBox.appendChild(svgElement);
  waitingBox.appendChild(fileNameElement3);
  analbutton.appendChild(fileNameElement2);
  upload_btn.appendChild(waitingBox);
  upload_btn.appendChild(analbutton);
  document.getElementsByClassName('delete_svg')[0].style.display = 'block';

  const formData = new FormData();
  formData.append('file', file);

  function result() {
    document.getElementById('anal_spinner').style.display = 'none';
    document.getElementById('analysis-exp-text3').style.display = 'none'
    document.querySelector('.circle-checkmark').style.display = 'block';
    document.querySelector('.file-name-display').style.display = 'block';
    const analBox = document.querySelector('.analysis-box');
    const resulttext = document.createElement('div');
    resulttext.id = 'result_font3';
    resulttext.innerText = '분석 완료';
    analBox.appendChild(resulttext);
    analBox.style.border='2px solid #DFDFDF';
    analBox.style.background = '#FCFCFC';
    const fileNameElement = document.createElement('div');
    fileNameElement.id = 'fileNameElementId';
    var file_name = truncateText(file.name,18)
    fileNameElement.innerText = file_name;
    
    const fileNameElement3 = document.createElement('div');
    fileNameElement3.id = 'fileNameElementId3';
    
    const fileSizeInMB = file.size/1024/1024;
    fileNameElement3.innerText = fileSizeInMB.toFixed(2)+'MB';
    resultBox.appendChild(fileNameElement);
    resultBox.appendChild(fileNameElement3);
     
    svgElement.id = 'result_svg';
    resultBox.appendChild(svgElement);
  }
  async function anal() {
    document.getElementById('anal_spinner').style.display = 'block';
    const analBox = document.querySelector('.analysis-box');
    analBox.style.cursor = 'default';
    const analtext = document.createElement('div');
    analtext.id = 'analysis-exp-text3';
    analtext.innerText = '분석 중...';
    analBox.appendChild(analtext);
    document.getElementsByClassName('delete_svg')[0].style.display = 'none';
    analBox.style.border='2px solid #DFDFDF';
    analBox.style.background = '#FCFCFC';
    analBox.style.position = 'absolute';
    analBox.removeChild(waitingBox);
    analBox.removeChild(analbutton);
    try {
      const response = await fetch('http://127.0.0.1:8000/detect_sum/', {
          method: 'POST',
          body: formData
      });
      if (response.ok){
        const data = await response.json();
        result()
        // Assuming the result is now in `data.result` and session_id in `data.session_id`
        console.log('Analysis complete:', data);
        displayResult(data.result, data.session_id); // Display results to the user
      }
      } catch (error) {
        console.error('Error:', error);
        alert(error)
      } 
  
  }
}


function createSvgElement(elementType, attributes) {
  const element = document.createElementNS('http://www.w3.org/2000/svg', elementType);
  for (let key in attributes) {
      element.setAttribute(key, attributes[key]);
  }
  return element;
  }
  
function truncateText(text, maxLength) {
  var truncated = text;
  if (truncated.length > maxLength) {
      truncated = truncated.substr(0,maxLength-5) + ' · · · ' + truncated.substr(-5);
  }
  return truncated;
}

async function removeFile() {
  const fileInput = document.getElementById('textfile');
  fileInput.value = '';
  document.getElementsByClassName('delete_svg')[0].style.display = 'none';
  const uploadButton = document.querySelector('.analysis-box');
  const waitingBox = document.querySelector('.uploadBox')
  const analbutton = document.querySelector('.analButton');
  uploadButton.style.backgroundColor = '#FCFCFC';
  uploadButton.style.border = '';
  uploadButton.style.width = '';
  uploadButton.style.height = '';
  uploadButton.onclick = oldOnclick;
  uploadButton.style.cursor = 'pointer';

  document.querySelector('.upload_svg').style.display = '';
  document.getElementById('analysis-exp-text').style.display = '';
  document.getElementById('analysis-exp-text2').style.display = '';
  document.getElementById("mask0_39_984").style.display = '';
  document.getElementById('analysis-exp-text').innerText = '요약할 자료를 업로드 해주세요';

  uploadButton.removeChild(waitingBox);
  uploadButton.removeChild(analbutton);
}
