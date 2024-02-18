function processAudio() {
  var audioInput = document.getElementById('audioUpload');
  var resultDiv = document.getElementById('result_font1');

  if (audioInput.files.length > 0) {
      var audioFile = audioInput.files[0];

      // Process the audio file
      // For example, read the file name and size
      var fileInfo = `File Name: ${audioFile.name}, File Size: ${audioFile.size} bytes`;

      // Display results
      resultDiv.innerHTML = fileInfo;

      // You can add more complex processing here,
      // like analyzing the audio file, playing it,
      // or sending it to a server for further processing.
  } else {
      resultDiv.innerHTML = 'No file selected';
  }
}

let oldOnclick;
async function uploadFile() {
      const fileInput = document.getElementById('audioFile');
      const file = fileInput.files[0];

      // Provide feedback that a file has been selected
      const upload_btn = document.querySelector('.custom_upload_btn');
      document.getElementById('result_font1').style.display = 'none';
      document.getElementById('result_font2').style.display = 'none';  
      document.getElementById("mask0_39_984").style.display = 'none';
      document.querySelector('.svg1').style.display = 'none';
      oldOnclick = upload_btn.onclick;
      upload_btn.onclick = null;
      upload_btn.style.border='2px solid #DFDFDF';
      upload_btn.style.background = '#FFF';

      const svgElement = createSvgElement('svg', {
        'width': '29px',
        'height': '37px',
        'flex-shrink': '0',
        'viewBox': '0 0 30 38',
        'fill': 'none',
        'id': 'mov_svg'}
      );
      
      const paths = [ 
        {'d': "M19.9189 0L24.5667 4.64773L29.2144 9.29545H19.9189V0Z", 'fill':'#92DBFF' },
        {'d' : "M2 0C0.895431 0 0 0.895433 0 2V35.1818C0 36.2864 0.89543 37.1818 2 37.1818H27.2143C28.3189 37.1818 29.2143 36.2864 29.2143 35.1818V9.29545H19.9189V0H2Z"
        , 'fill': '#00A8F4', 'fill-rule': 'evenodd', 'clip-rule': 'evenodd' },
        { 'd': "M21.6737 23.3921L23.3788 18.1973H24.6934L22.5183 24.7466H20.8372L18.6541 18.1973H19.9687L21.6737 23.3921Z", 'fill' : 'white' },
        { 'd' : "M15.7252 24.8665C15.2099 24.8665 14.7345 24.7523 14.299 24.5239C13.8634 24.3008 13.5155 23.9768 13.2552 23.5518C13.0003 23.1216 12.8728 22.6143 12.8728 22.03V20.9146C12.8728 20.3356 13.0003 19.831 13.2552 19.4007C13.5155 18.9705 13.8634 18.6438 14.299 18.4207C14.7345 18.1923 15.2099 18.0781 15.7252 18.0781C16.2404 18.0781 16.7158 18.1923 17.1514 18.4207C17.5869 18.6438 17.9322 18.9705 18.1871 19.4007C18.4474 19.831 18.5776 20.3356 18.5776 20.9146V22.03C18.5776 22.6143 18.4474 23.1216 18.1871 23.5518C17.9322 23.9768 17.5869 24.3008 17.1514 24.5239C16.7158 24.7523 16.2404 24.8665 15.7252 24.8665ZM15.7252 23.7032C16.0173 23.7032 16.2856 23.6395 16.5299 23.512C16.7742 23.3792 16.9681 23.1827 17.1115 22.9224C17.2549 22.6621 17.3267 22.3487 17.3267 21.9822V20.9624C17.3267 20.5959 17.2523 20.2851 17.1036 20.0302C16.9601 19.7699 16.7663 19.5734 16.5219 19.4406C16.2829 19.3078 16.0173 19.2414 15.7252 19.2414C15.433 19.2414 15.1648 19.3078 14.9205 19.4406C14.6814 19.5734 14.4876 19.7699 14.3388 20.0302C14.1954 20.2851 14.1237 20.5959 14.1237 20.9624V21.9822C14.1237 22.3487 14.1954 22.6621 14.3388 22.9224C14.4876 23.1827 14.6814 23.3792 14.9205 23.512C15.1648 23.6395 15.433 23.7032 15.7252 23.7032Z", 'fill' : 'white'},
        { 'd' : "M6.18525 24.7466H4.95825V18.1973H6.62347L8.49584 23.1929L10.3682 18.1973H12.0334V24.7466H10.8064V20.2529L9.1173 24.7466H7.87437L6.18525 20.2529V24.7466Z", 'fill' : 'white' }
        ]
      paths.forEach(path => {
        svgElement.appendChild(createSvgElement('path',path))
      });
      svgElement.id = 'mov_svg';

      const newBox = document.createElement('div');
      newBox.id = 'newBox';
      
      const newBox2 = document.createElement('div');
      newBox2.className = 'newBox2';
      newBox2.onclick = anal;
      newBox2.style.display = 'block';


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

      newBox.appendChild(fileNameElement);
      newBox.appendChild(svgElement);
      newBox.appendChild(fileNameElement3);
      newBox2.appendChild(fileNameElement2);
      upload_btn.appendChild(newBox);
      upload_btn.appendChild(newBox2);
      
      document.getElementsByClassName('delete_svg')[0].style.display = 'block';

      const formData = new FormData();
      formData.append('file', file);

      function result() {
        document.getElementById('spinner').style.display = 'none';
        document.getElementById('result_font3').style.display = 'none'
        document.querySelector('.svg4').style.display = 'block';
        document.getElementById('resultBox').style.display = 'block';
        const analBox = document.querySelector('.custom_upload_btn');
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
        document.getElementById('spinner').style.display = 'block';
        const analBox = document.querySelector('.custom_upload_btn');
        analBox.style.cursor = 'default';
        const analtext = document.createElement('div');
        analtext.id = 'result_font3';
        analtext.innerText = '분석 중...';
        analBox.appendChild(analtext);
        document.getElementsByClassName('delete_svg')[0].style.display = 'none';
        analBox.style.border='2px solid #DFDFDF';
        analBox.style.background = '#FCFCFC';
        analBox.style.position = 'absolute';
        analBox.removeChild(newBox);
        analBox.removeChild(newBox2);

        try {
          const response = await fetch('http://127.0.0.1:8000/detect/', {
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


async function removeFile() {
  const fileInput = document.getElementById('audioFile');
  fileInput.value = '';
  document.getElementsByClassName('delete_svg')[0].style.display = 'none';
  const uploadButton = document.querySelector('.custom_upload_btn');
  const newBox2 = document.querySelector('.newBox2');
  uploadButton.style.backgroundColor = '';
  uploadButton.style.border = '';
  uploadButton.style.width = '';
  uploadButton.style.height = '';
  uploadButton.onclick = oldOnclick;
  uploadButton.style.cursor = 'pointer';

  
  // SVG 아이콘과 텍스트를 다시 보이게 합니다.
  document.querySelector('.svg1').style.display = '';
  document.getElementById('result_font1').style.display = '';
  document.getElementById('result_font2').style.display = '';
  document.getElementById("mask0_39_984").style.display = '';
  document.getElementById('result_font1').innerText = '분석할 발표 영상을 업로드 해주세요';
  
  // 새롭게 추가한 박스를 제거합니다.
  
  uploadButton.removeChild(newBox);
  uploadButton.removeChild(newBox2);
}


function displayResult(result, sessionId) {
    let resultsDiv = document.getElementById('analysisResults');
    if (!resultsDiv) {
        // Create the results div if it does not exist
        resultsDiv = document.createElement('div');
        resultsDiv.id = 'analysisResults';
        document.body.appendChild(resultsDiv); // Append somewhere suitable in your actual layout
    }

    // Update speed result
    const speedResult = document.getElementById('result-speed');
    if (speedResult && result.speech && result.speech.speed) {
        speedResult.textContent = `결과: 속도 ${result.speech.speed}`;
    }

    // Update pause result
    const pauseResult = document.getElementById('result-pause');
    if (pauseResult && result.speech && result.speech.num_pauses !== undefined) {
        pauseResult.textContent = `결과: 일시정지 횟수 ${result.speech.num_pauses}`;
    }

    // Update filler words result
    const fillerWordsResult = document.getElementById('result-filler-words');
    if (fillerWordsResult && result.speech && result.speech.filler_words) {
        const fillerWordsText = Object.entries(result.speech.filler_words)
            .map(([word, count]) => `${word}: ${count}회`)
            .join(', ');
        fillerWordsResult.textContent = `결과: 보충어 ${fillerWordsText}`;
    }

    const emotionResult = document.getElementById('result-emotion');
    if (speedResult && result.emotion && result.emotion.emtion) {
        speedResult.textContent = `결과: 표정 ${result.emotion.emotion}`;
    }
}


function truncateText(text, maxLength) {
  var truncated = text;
  if (truncated.length > maxLength) {
      truncated = truncated.substr(0,maxLength-5) + ' · · · ' + truncated.substr(-5);
  }
  return truncated;
}

