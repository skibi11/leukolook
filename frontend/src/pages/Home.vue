<template>
  <div class="home-container">
    <div v-if="isLoading" class="spinner-container">
      <div class="spinner"></div>
    </div>

    <div v-else class="home-content">
      <section class="hero-section">
        <div class="hero-main-group">
          <div class="hero-visual">
            <img :src="eyeIcon" alt="Eye Icon" class="hero-icon" />
          </div>
          <div class="hero-text">
            <h1>
              Flash.<br />
              Scan.<br />
              Detect.
            </h1>
          </div>
        </div>
        <p class="hero-subtext">Check for Leukocoria Early</p>
      </section>

      <section class="action-card">
        <div class="action-grid">
          <div class="action-option">
            <img :src="folderIcon" alt="Folder Icon" class="action-icon" />
            <h3>Upload a Photo</h3>
            <p>Choose a photo from your gallery</p>
            <button class="btn btn-secondary" @click="openFilePicker">
              Browse Files
            </button>
            <input
              type="file"
              accept="image/*"
              ref="fileInput"
              @change="onFileSelected"
              style="display: none"
            />
          </div>

          <div class="action-option">
            <img :src="cameraIcon" alt="Camera Icon" class="action-icon" />
            <h3>Use Camera</h3>
            <p>Use your device's camera now</p>
            <button class="btn btn-primary" @click="goToCamera">
              Take Photo
            </button>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import eyeIcon from '../assets/eye.svg' // Make sure this path is correct
import folderIcon from '../assets/folder.svg' // Make sure this path is correct
import cameraIcon from '../assets/camera.svg' // Make sure this path is correct

const router = useRouter()
const fileInput = ref<HTMLInputElement>()
const isLoading = ref(false)

function openFilePicker() {
  fileInput.value?.click()
}

function onFileSelected(e: Event) {
  const files = (e.target as HTMLInputElement).files
  if (!files || !files[0]) return

  const imageFile = files[0]
  isLoading.value = true

  const formData = new FormData()
  formData.append('image', imageFile)

  console.log("Sending image to backend...");

  fetch(`${import.meta.env.VITE_API_BASE_URL}/api/eye-detect/`, {
    method: 'POST',
    body: formData,
  })
    .then(async (res) => {
      console.log("Received API Response:", res);
      console.log("Response Status:", res.status, res.statusText);

      const data = await res.json();
      console.log("Parsed JSON Data:", data);

      if (!res.ok) {
        console.error("Response status was not OK. Throwing an error.");
        throw new Error(data.error || 'Detection failed.')
      }

      sessionStorage.setItem('detectionResult', JSON.stringify(data));
      sessionStorage.setItem('originalImage', data.analyzed_image);
      router.push('/result');
    })
    .catch((err: any) => {
      console.error("FETCH FAILED in .catch() block:", err);
      alert(`⚠️ ${err.message}`);
    })
    .finally(() => {
      isLoading.value = false
    })
}

function goToCamera() {
  router.push('/camera')
}
</script>

<style scoped>
.home-container {
  background-color: #12151e;
  color: #e0e0e0;
  padding: 2rem 1.5rem 4rem;
  display: flex;
  justify-content: center;
  min-height: 100vh;
}

.home-content {
  width: 100%;
  max-width: 900px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* --- Hero Section (Updated) --- */
.hero-section {
  display: flex;
  flex-direction: column; /* Stacks the main group and subtext vertically */
  align-items: center; /* Horizontally centers everything */
  gap: 1.5rem; /* Creates space between the main group and the subtext */
  margin-bottom: 1rem;
  width: 100%;
}

.hero-main-group {
  display: flex;
  flex-direction: row; /* This keeps the icon and H1 side-by-side */
  align-items: center;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap; /* Allows wrapping on very small screens if necessary */
}

.hero-visual {
  flex-shrink: 0;
}

.hero-icon {
  width: 200px;
  height: auto;
}

.hero-text h1 {
  font-family: 'Segoe UI', 'Roboto', sans-serif;
  font-weight: 700;
  font-size: 3.5rem;
  line-height: 1.1;
  margin: 0;
  color: #ffffff;
}

.hero-subtext {
  font-size: 1rem;
  color: #3fe1ff;
  margin-top: 0; 
  font-weight: bold;
}

/* --- Action Card --- */
.action-card {
  background-color: #1a1d24;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 1rem;
  padding: 1rem;
  width: 100%;
}

.action-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  align-items: stretch;
}

.action-option {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 1.5rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 0.75rem;
}

.action-icon {
  width: 50px;
  height: 50px;
  margin-bottom: 1rem;
}

.action-option h3 {
  font-size: 1.5rem;
  color: #ffffff;
  margin: 0 0 0.5rem 0;
}

.action-option p {
  color: #adb5bd;
  margin: 0 0 1.5rem 0;
  flex-grow: 1;
}

/* --- Button Styles --- */
.btn {
  width: 100%;
  padding: 0.75rem 1rem;
  border: none;
  border-radius: 0.5rem;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary {
  background-color: #3fe1ff;
  color: #12151e;
}
.btn-primary:hover {
  background-color: #6ff8ff;
  transform: translateY(-2px);
}

.btn-secondary {
  background-color: #3a3f4b;
  color: #ffffff;
}
.btn-secondary:hover {
  background-color: #495057;
}

/* --- Spinner --- */
.spinner-container {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
}
.spinner {
  width: 3rem;
  height: 3rem;
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}

/* --- Responsive Design (Updated) --- */
@media (max-width: 768px) {
  .hero-main-group {
    gap: 1.5rem; /* Reduce gap on smaller screens */
  }
  .hero-icon {
    width: 120px; /* Make icon smaller */
  }
  .hero-text h1 {
    font-size: 2rem; /* Make text smaller */
  }
  
  /* THIS IS THE FIX: Changes the grid to a single column on screens
     narrower than 768px, stacking the boxes vertically. */
  .action-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
}
</style>