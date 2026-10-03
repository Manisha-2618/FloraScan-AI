/**
 * script.js - Plant Disease Detection Frontend Logic
 * Manages drag-and-drop file upload, real-time image preview,
 * asynchronous Fetch API requests to Flask backend, dynamic UI updates,
 * and error handling.
 */

document.addEventListener("DOMContentLoaded", () => {
  // Elements
  const dropzone = document.getElementById("dropzone");
  const fileInput = document.getElementById("fileInput");
  const browseBtn = document.getElementById("browseBtn");
  const previewContainer = document.getElementById("previewContainer");
  const previewImage = document.getElementById("previewImage");
  const previewName = document.getElementById("previewName");
  const previewSize = document.getElementById("previewSize");
  const removeImageBtn = document.getElementById("removeImageBtn");
  const analyzeBtn = document.getElementById("analyzeBtn");

  // State Containers
  const loadingOverlay = document.getElementById("loadingOverlay");
  const loadingStatusText = document.getElementById("loadingStatusText");
  const resultCard = document.getElementById("resultCard");
  const emptyState = document.getElementById("emptyState");
  const errorAlert = document.getElementById("errorAlert");
  const errorMessage = document.getElementById("errorMessage");

  // Result Elements
  const resultPlantBadge = document.getElementById("resultPlantBadge");
  const resultDiseaseName = document.getElementById("resultDiseaseName");
  const resultConfidence = document.getElementById("resultConfidence");
  const confidenceBarFill = document.getElementById("confidenceBarFill");
  const resultDescription = document.getElementById("resultDescription");
  const symptomsList = document.getElementById("symptomsList");
  const treatmentList = document.getElementById("treatmentList");
  const resultDisclaimer = document.getElementById("resultDisclaimer");
  const topPredictionsContainer = document.getElementById("topPredictionsContainer");
  const topPredictionsList = document.getElementById("topPredictionsList");

  // Sample Chips
  const sampleChips = document.querySelectorAll(".sample-chip");

  let currentFile = null;
  const ALLOWED_TYPES = ["image/jpeg", "image/jpg", "image/png", "image/webp"];
  const MAX_FILE_SIZE_BYTES = 16 * 1024 * 1024; // 16MB

  // ---------------------------------------------------------------------------
  // Dropzone & File Selection Event Listeners
  // ---------------------------------------------------------------------------

  if (browseBtn && fileInput) {
    browseBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      fileInput.click();
    });
  }

  if (dropzone && fileInput) {
    dropzone.addEventListener("click", () => {
      fileInput.click();
    });

    // Drag-over styling
    ["dragenter", "dragover"].forEach((eventName) => {
      dropzone.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropzone.classList.add("dragover");
      });
    });

    ["dragleave", "drop"].forEach((eventName) => {
      dropzone.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropzone.classList.remove("dragover");
      });
    });

    // Handle dropped files
    dropzone.addEventListener("drop", (e) => {
      const dt = e.dataTransfer;
      const files = dt.files;
      if (files && files.length > 0) {
        handleFileSelection(files[0]);
      }
    });

    // Handle input change
    fileInput.addEventListener("change", (e) => {
      if (e.target.files && e.target.files.length > 0) {
        handleFileSelection(e.target.files[0]);
      }
    });
  }

  // Remove image
  if (removeImageBtn) {
    removeImageBtn.addEventListener("click", resetUploadState);
  }

  // Analyze button click
  if (analyzeBtn) {
    analyzeBtn.addEventListener("click", submitImageForAnalysis);
  }

  // Sample Leaf buttons
  sampleChips.forEach((chip) => {
    chip.addEventListener("click", () => {
      const samplePath = chip.getAttribute("data-sample");
      if (samplePath) {
        loadSampleImage(samplePath, chip.textContent.trim());
      }
    });
  });

  // ---------------------------------------------------------------------------
  // File Validation & Preview Handling
  // ---------------------------------------------------------------------------

  function handleFileSelection(file) {
    hideError();

    // Validate type
    if (!ALLOWED_TYPES.includes(file.type.toLowerCase()) && !file.name.match(/\.(jpg|jpeg|png|webp)$/i)) {
      showError("Unsupported file type. Please upload a PNG, JPG, JPEG, or WEBP leaf image.");
      return;
    }

    // Validate size
    if (file.size > MAX_FILE_SIZE_BYTES) {
      showError("File is too large. Maximum allowable size is 16MB.");
      return;
    }

    currentFile = file;

    // Display metadata
    if (previewName) previewName.textContent = file.name;
    if (previewSize) previewSize.textContent = formatBytes(file.size);

    // Read and render preview
    const reader = new FileReader();
    reader.onload = (e) => {
      previewImage.src = e.target.result;
      dropzone.style.display = "none";
      previewContainer.style.display = "block";
    };
    reader.readAsDataURL(file);
  }

  function resetUploadState() {
    currentFile = null;
    if (fileInput) fileInput.value = "";
    previewImage.src = "";
    previewContainer.style.display = "none";
    dropzone.style.display = "block";
    hideError();
  }

  function formatBytes(bytes) {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
  }

  // ---------------------------------------------------------------------------
  // Load Sample Leaves Directly
  // ---------------------------------------------------------------------------

  async function loadSampleImage(url, label) {
    try {
      showLoading("Loading sample leaf image...");
      const response = await fetch(url);
      if (!response.ok) throw new Error("Could not fetch sample leaf image.");
      const blob = await response.blob();
      const filename = `${label.toLowerCase().replace(/\s+/g, "_")}.jpg`;
      const file = new File([blob], filename, { type: "image/jpeg" });
      hideLoading();
      handleFileSelection(file);
    } catch (err) {
      hideLoading();
      showError(`Failed to load sample image: ${err.message}`);
    }
  }

  // ---------------------------------------------------------------------------
  // API Fetch Submission
  // ---------------------------------------------------------------------------

  async function submitImageForAnalysis() {
    if (!currentFile) {
      showError("Please select or drop a plant leaf image first.");
      return;
    }

    hideError();
    showLoading("Extracting deep botanical features...");

    // Simulated status updates for engaging UX during inference
    const statusMessages = [
      "Preprocessing leaf geometry...",
      "Executing MobileNetV2 convolutional layers...",
      "Analyzing pathology patterns & chlorophyll indices...",
      "Cross-referencing agricultural database..."
    ];
    let msgIndex = 0;
    const statusInterval = setInterval(() => {
      if (loadingOverlay && loadingOverlay.style.display !== "none") {
        msgIndex = (msgIndex + 1) % statusMessages.length;
        if (loadingStatusText) {
          loadingStatusText.textContent = statusMessages[msgIndex];
        }
      }
    }, 600);

    const formData = new FormData();
    formData.append("image", currentFile);

    try {
      const response = await fetch("/api/predict", {
        method: "POST",
        body: formData
      });

      clearInterval(statusInterval);
      const data = await response.json();

      hideLoading();

      if (!response.ok || !data.success) {
        const errorMsg = data.error || `Server responded with status ${response.status}`;
        showError(errorMsg);
        return;
      }

      // Render prediction result dynamically
      renderPrediction(data);

    } catch (networkError) {
      clearInterval(statusInterval);
      hideLoading();
      showError(`Network communication error: ${networkError.message}. Ensure Flask app is running.`);
    }
  }

  // ---------------------------------------------------------------------------
  // Dynamic UI Renderers
  // ---------------------------------------------------------------------------

  function renderPrediction(data) {
    if (emptyState) emptyState.style.display = "none";
    if (resultCard) resultCard.style.display = "block";

    // Plant Name & Disease
    if (resultPlantBadge) resultPlantBadge.textContent = `Plant: ${data.plant}`;
    if (resultDiseaseName) {
      resultDiseaseName.textContent = data.disease;
      if (data.disease.toLowerCase().includes("healthy")) {
        resultDiseaseName.classList.add("healthy");
      } else {
        resultDiseaseName.classList.remove("healthy");
      }
    }

    // Confidence Percentage
    const confValue = Math.min(100, Math.max(0, data.confidence));
    if (resultConfidence) {
      resultConfidence.textContent = `${confValue.toFixed(2)}%`;
    }

    // Confidence Progress Bar
    if (confidenceBarFill) {
      confidenceBarFill.style.width = "0%";
      setTimeout(() => {
        confidenceBarFill.style.width = `${confValue}%`;
        if (confValue > 85) {
          confidenceBarFill.style.background = "linear-gradient(90deg, #10b981 0%, #34d399 100%)";
        } else if (confValue > 60) {
          confidenceBarFill.style.background = "linear-gradient(90deg, #f59e0b 0%, #fbbf24 100%)";
        } else {
          confidenceBarFill.style.background = "linear-gradient(90deg, #f43f5e 0%, #fb7185 100%)";
        }
      }, 50);
    }

    // Description
    if (resultDescription) {
      resultDescription.textContent = data.description || "No specific pathological description provided.";
    }

    // Symptoms List
    if (symptomsList) {
      symptomsList.innerHTML = "";
      if (Array.isArray(data.symptoms) && data.symptoms.length > 0) {
        data.symptoms.forEach((symptom) => {
          const li = document.createElement("li");
          li.textContent = symptom;
          symptomsList.appendChild(li);
        });
      } else {
        const li = document.createElement("li");
        li.textContent = "No visible pathological symptoms cataloged.";
        symptomsList.appendChild(li);
      }
    }

    // Treatment & Prevention List
    if (treatmentList) {
      treatmentList.innerHTML = "";
      if (Array.isArray(data.treatment) && data.treatment.length > 0) {
        data.treatment.forEach((step) => {
          const li = document.createElement("li");
          li.textContent = step;
          treatmentList.appendChild(li);
        });
      } else {
        const li = document.createElement("li");
        li.textContent = "Maintain optimal cultural practices and standard nutrition.";
        treatmentList.appendChild(li);
      }
    }

    // Educational Disclaimer
    if (resultDisclaimer) {
      resultDisclaimer.textContent = data.disclaimer || (
        "Educational guidance only. Always consult a regional agricultural specialist or certified plant pathologist before applying treatments."
      );
    }

    // Top Predictions breakdown (if present)
    if (topPredictionsContainer && topPredictionsList) {
      if (Array.isArray(data.top_predictions) && data.top_predictions.length > 1) {
        topPredictionsContainer.style.display = "block";
        topPredictionsList.innerHTML = "";
        data.top_predictions.forEach((item) => {
          const formatted = item.class_name.replace(/___/g, " - ").replace(/_/g, " ");
          const div = document.createElement("div");
          div.className = "top-pred-item";
          div.style.cssText = "display: flex; justify-content: space-between; font-size: 0.82rem; padding: 0.35rem 0; border-bottom: 1px solid rgba(255,255,255,0.05);";
          div.innerHTML = `<span>${formatted}</span><strong style="color: var(--primary-light); font-family: var(--font-mono);">${item.confidence}%</strong>`;
          topPredictionsList.appendChild(div);
        });
      } else {
        topPredictionsContainer.style.display = "none";
      }
    }

    // Scroll smoothly to result if on mobile
    if (window.innerWidth < 960 && resultCard) {
      resultCard.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }

  // ---------------------------------------------------------------------------
  // Helper UI States
  // ---------------------------------------------------------------------------

  function showLoading(msg = "Analyzing leaf...") {
    if (loadingOverlay) loadingOverlay.style.display = "block";
    if (loadingStatusText) loadingStatusText.textContent = msg;
    if (emptyState) emptyState.style.display = "none";
    if (resultCard) resultCard.style.display = "none";
    if (analyzeBtn) analyzeBtn.disabled = true;
  }

  function hideLoading() {
    if (loadingOverlay) loadingOverlay.style.display = "none";
    if (analyzeBtn) analyzeBtn.disabled = false;
  }

  function showError(msg) {
    if (errorMessage) errorMessage.textContent = msg;
    if (errorAlert) {
      errorAlert.style.display = "flex";
      errorAlert.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }
  }

  function hideError() {
    if (errorAlert) errorAlert.style.display = "none";
  }
});
