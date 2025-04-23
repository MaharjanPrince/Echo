function triggerUpload() {
    document.getElementById('realFileInput').click();
  }
  
  function displayFileName() {
    const input = document.getElementById('realFileInput');
    const label = document.getElementById('fileLabel');
    const file = input.files[0];
  
    if (file) {
      label.textContent = file.name;
    } else {
      label.textContent = "Upload a PDF…";
    }
  }
  
  function uploadBook() {
    const fileInput = document.getElementById('realFileInput');
    const file = fileInput.files[0];
  
    if (!file) {
      alert("Please choose a file first.");
      return;
    }
  
    alert(`Echo is reading: ${file.name}`);
    // Proceed with backend upload via fetch
  }
  
let bookId = "";

        // Upload Book
        function uploadBook() {
            const fileInput = document.getElementById('fileInput');
            const formData = new FormData();
            formData.append('file', fileInput.files[0]);

            fetch('http://127.0.0.1:8000/upload-book/', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                bookId = data.book_id;
                document.getElementById('book-id-section').style.display = 'block';  // Show question section
                alert("Book uploaded successfully. Now you can ask questions!");
            })
            .catch(error => alert("Error uploading book: " + error));
        }

        // Ask Echo a question
        function askEcho() {
            const userPrompt = document.getElementById('userPrompt').value;
            fetch('http://127.0.0.1:8000/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    book_id: bookId,
                    user_prompt: userPrompt
                })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('response').textContent = data.response;
            })
            .catch(error => alert("Error asking question: " + error));
        }
