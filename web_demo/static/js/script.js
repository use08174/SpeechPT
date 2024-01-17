function processAudio() {
    var audioInput = document.getElementById('audioUpload');
    var resultDiv = document.getElementById('result');

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
