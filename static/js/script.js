const upscaleButton = document.getElementById("upscaleButton");
const uploadFileButton = document.getElementById("uploadFile");
const imagePreviewBox = document.getElementById("imagePreview");
const noImageBox = document.getElementById("noImage");
const noImageText = document.getElementById("noImageText");

window.addEventListener("pageshow", function (event) {
    if (event.persisted ||
        (typeof window.performance !== "undefined" &&
            window.performance.getEntriesByType("navigation")[0].type === "back_forward")) {
        window.location.reload();
    }
});

uploadFileButton.addEventListener('change', function () {
    CheckUploadFile();
});

function CheckUploadFile() {
    if (uploadFileButton.files.length > 0) {
        upscaleButton.disabled = false;

        const file = uploadFileButton.files[0];
        const reader = new FileReader();

        reader.onload = function (e) {
            imagePreviewBox.src = e.target.result;

            imagePreviewBox.style.display = 'block';
            noImageBox.style.display = 'none';
            noImageText.style.display = 'none';
            upscaleButton.textContent = 'UPSCALE IMAGE';
        }
        reader.readAsDataURL(file);
    }
    else {
        upscaleButton.disabled = true;

        imagePreviewBox.src = " ";

        imagePreviewBox.style.display = 'none';
        noImageBox.style.display = 'block';
        noImageText.style.display = 'block';

        upscaleButton.textContent = 'UPSCALE IMAGE';
    }
}
CheckUploadFile()