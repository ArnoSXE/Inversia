document.addEventListener("DOMContentLoaded", function() {
    const toggle = document.getElementById('modeToggle');
    const label = document.getElementById('modeLabel');
    const body = document.body;
    const uploadArea = document.getElementById('uploadArea');
    const input = document.getElementById('imageInput');
    const preview = document.getElementById('preview');

    toggle.addEventListener('change', function() {
        body.classList.toggle('dark-mode');
        label.innerText = body.classList.contains('dark-mode') ? "Dark Mode" : "Light Mode";
    });

    input.addEventListener('change', function(event) {
        handleFiles(event.target.files);
    });

    uploadArea.addEventListener("click", () => input.click());

    uploadArea.addEventListener("dragover", function(event) {
        event.preventDefault();
        uploadArea.classList.add("dragover");
    });

    uploadArea.addEventListener("dragleave", function(event) {
        uploadArea.classList.remove("dragover");
    });

    uploadArea.addEventListener("drop", function(event) {
        event.preventDefault();
        uploadArea.classList.remove("dragover");
        const files = event.dataTransfer.files;
        input.files = files; // Sync with hidden input
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
        }
    }
});
