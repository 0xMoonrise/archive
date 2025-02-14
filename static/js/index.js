function uploadFile() {
    const fileInput = document.getElementById('file-input');
    const file = fileInput.files[0];

    if (file) {
        const formData = new FormData();
        formData.append('file', file);

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.reload();
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
}

const form = document.querySelector(".form-input");

async function sendData() {
  const formData = new FormData(form);
  try {
    const response = await fetch(`${window.location.origin}/`, {
      method: "POST",
      body: formData,
    });
    data = await response.json();
    console.log(data.message);
  } catch (e) {
    console.error(e);
  }
  
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  sendData();
});
