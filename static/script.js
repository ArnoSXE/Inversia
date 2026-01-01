document.addEventListener("DOMContentLoaded", function () {
    const toggle = document.getElementById('modeToggle');
    const label = document.getElementById('modeLabel');
    const body = document.body;
    const uploadArea = document.getElementById('uploadArea');
    const input = document.getElementById('imageInput');
    const preview = document.getElementById('preview');
    const cameraBtn = document.getElementById('cameraBtn');
    const cameraStream = document.getElementById('cameraStream');
    const canvas = document.getElementById('cameraCapture');
    const form = document.getElementById('searchForm');

    toggle.addEventListener('change', function () {
        body.classList.toggle('dark-mode');
        label.innerText = body.classList.contains('dark-mode') ? "Dark Mode" : "Light Mode";
    });

    // Initialize label
    label.innerText = body.classList.contains('dark-mode') ? "Dark Mode" : "Light Mode";

    input.addEventListener('change', function (event) {
        handleFiles(event.target.files);
    });

    uploadArea.addEventListener("click", () => input.click());

    uploadArea.addEventListener("dragover", function (event) {
        event.preventDefault();
        uploadArea.classList.add("dragover");
    });

    uploadArea.addEventListener("dragleave", function (event) {
        uploadArea.classList.remove("dragover");
    });

    uploadArea.addEventListener("drop", function (event) {
        event.preventDefault();
        uploadArea.classList.remove("dragover");
        const files = event.dataTransfer.files;
        input.files = files;
        handleFiles(files);
    });

    function handleFiles(files) {
        preview.innerHTML = "";
        const file = files[0];
        if (file) {
            const img = document.createElement("img");
            img.src = URL.createObjectURL(file);
            img.style.maxWidth = "100%";
            preview.appendChild(img);
            
            // Hide the upload icon and text when an image is selected
            const uploadIcon = uploadArea.querySelector('.upload-icon');
            const uploadText = uploadArea.querySelector('p');
            if (uploadIcon) uploadIcon.style.display = 'none';
            if (uploadText) uploadText.style.display = 'none';
        }
    }

    // CAMERA FEATURE
    let stream;
    cameraBtn.addEventListener("click", async () => {
        if (!stream) {
            try {
                stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } });
                cameraStream.srcObject = stream;
                cameraStream.style.display = 'block';
                cameraBtn.innerHTML = '<i class="fas fa-camera"></i> Capture Photo';
            } catch (err) {
                console.error("Camera error:", err);
                alert("Could not access camera. Please ensure you've given permission.");
            }
        } else {
            // capture image
            canvas.width = cameraStream.videoWidth;
            canvas.height = cameraStream.videoHeight;
            canvas.getContext("2d").drawImage(cameraStream, 0, 0);
            
            canvas.toBlob(blob => {
                const file = new File([blob], "camera.jpg", { type: "image/jpeg" });

                // Update the file input
                const dt = new DataTransfer();
                dt.items.add(file);
                input.files = dt.files;

                handleFiles([file]);

                // Stop camera and reset button
                stream.getTracks().forEach(track => track.stop());
                stream = null;
                cameraStream.style.display = 'none';
                cameraBtn.innerHTML = '<i class="fas fa-camera"></i> Use Camera';
            }, "image/jpeg", 0.95);
        }
    });
});
