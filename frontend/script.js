const imageInput = document.getElementById("imageInput");
const originalImage = document.getElementById("originalImage");
const maskImage = document.getElementById("maskImage");
const statusText = document.getElementById("status");

function predict() {
    const file = imageInput.files[0];

    if (!file) {
        alert("Please select an image first");
        return;
    }

    // Show original image
    originalImage.src = URL.createObjectURL(file);
    statusText.innerText = "⏳ Predicting...";

    const formData = new FormData();
    formData.append("file", file);

    fetch("/predict", {
        method: "POST",
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Prediction failed");
        }
        return response.blob();
    })
    .then(blob => {
        maskImage.src = URL.createObjectURL(blob);
        statusText.innerText = " Prediction completed";
    })
    .catch(error => {
        console.error(error);
        statusText.innerText = "❌ Error during prediction";
    });
}
