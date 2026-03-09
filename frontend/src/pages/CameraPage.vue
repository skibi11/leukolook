<template>
  <div class="camera-page">
    <div v-if="isLoading" class="spinner-container">
      <div class="spinner"></div>
    </div>

    <video
      v-else-if="!showModal"
      ref="video"
      autoplay
      playsinline
      muted
      class="camera-view"
    ></video>
    <div v-else class="camera-view error-bg"></div>

    <div v-if="error" class="error-text">
      Unable to access the camera
    </div>

    <div class="bottom-bar" v-if="!showModal && !isLoading">
      <button
        class="btn-control"
        @click="toggleZoom"
        :disabled="!supportsZoom"
        :title="supportsZoom ? `${zoomLevel}x` : 'Zoom not supported'"
      >
        {{ zoomLevel }}x
      </button>

      <button class="btn-capture" @click="captureAndShowPreview">
        <img :src="fullCameraIcon" alt="Capture" class="capture-img" />
      </button>
    </div>

    <Modal
      v-if="showModal"
      :imageSrc="capturedImage"
      :warnings="modalWarnings"
      @confirm="submitPhoto"
      @retake="retakePhoto"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import Modal from '../components/Modal.vue'
import fullCameraIcon from '../assets/full-preview.png'

const router = useRouter()
const video = ref<HTMLVideoElement>()
const trackRef = ref<MediaStreamTrack | null>(null)

const isLoading = ref(false)
const error = ref(false)
const showModal = ref(false)
const capturedImage = ref('')
const modalWarnings = ref<string[]>([])
const detectionResult = ref<any>(null) // This line was added back

const zoomLevel = ref(1)
const supportsZoom = ref(false)

// Central cleanup function for camera and torch
function stopStream() {
  if (trackRef.value) {
    // This stops all functionalities of the track, including the torch.
    trackRef.value.stop();
    trackRef.value = null;
  }
}

async function startStream() {
  stopStream(); // Always stop any previous stream first

  error.value = false
  supportsZoom.value = false
  zoomLevel.value = 1

  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: 'environment' }
    })
    const [track] = stream.getVideoTracks()
    trackRef.value = track
    if (video.value) video.value.srcObject = stream

    // After stream starts, check for capabilities
    const caps = track.getCapabilities?.() as any;
    if (caps) {
      if (caps.zoom && caps.zoom.max > caps.zoom.min) {
        supportsZoom.value = true
      }
      // The torch block that was here is now gone.
    }
  } catch {
    error.value = true
  }
}

onMounted(startStream)

onBeforeUnmount(() => {
  stopStream(); // Cleanup when leaving the page
});

function toggleZoom() {
  if (!supportsZoom.value || !trackRef.value) {
    zoomLevel.value = zoomLevel.value === 1 ? 2 : 1
    return
  }
  zoomLevel.value = zoomLevel.value === 1 ? 2 : 1
  trackRef.value
    .applyConstraints({ advanced: [{ zoom: zoomLevel.value }] } as any)
    .catch(() => {
      zoomLevel.value = zoomLevel.value === 1 ? 2 : 1
    })
}

async function captureAndShowPreview() {
  if (!video.value) return;
  const vid = video.value;
  const canvas = document.createElement('canvas');
  canvas.width = vid.videoWidth;
  canvas.height = vid.videoHeight;
  const ctx = canvas.getContext('2d')!;
  ctx.drawImage(vid, 0, 0);
  capturedImage.value = canvas.toDataURL('image/png');
  stopStream();
  showModal.value = true;
}

async function submitPhoto() {
  showModal.value = false;
  stopStream(); // Turn off camera and torch before leaving the page
  isLoading.value = true;
  try {
    const blob = await fetch(capturedImage.value).then(res => res.blob());
    const formData = new FormData();
    formData.append('image', blob, 'captured.png');
    const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/eye-detect/`, {
      method: 'POST',
      body: formData,
    });
    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.error || 'Detection failed.');
    }
    sessionStorage.setItem('detectionResult', JSON.stringify(data));
    // Instead of using the original image, use the one returned by the API
    sessionStorage.setItem('originalImage', data.analyzed_image);
    
    router.push('/result');

  } catch (err: any) {
    alert(`⚠️ ${err.message}`);
    retakePhoto();
  } finally {
    isLoading.value = false;
  }
}

function retakePhoto() {
  showModal.value = false
  capturedImage.value = ''
  detectionResult.value = null
  modalWarnings.value = []
  startStream(); // This will stop the old stream and start a new one
}
</script>

<style scoped>
.camera-page {
  position: relative;
  width: 100%;
  height: 100vh;
  background: #000;
  overflow: hidden;
}
.camera-view {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.error-bg {
  background: #000;
}
.error-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #fff;
  font-size: 1.2rem;
}
.bottom-bar {
  position: absolute;
  bottom: 1.5rem;
  left: 0;
  right: 0;
  display: flex;
  gap: 1.5rem;
  justify-content: center;
  align-items: center;
  padding: 0 1rem;
  z-index: 10;
}
.btn-control {
  background: rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: #fff;
  font-size: 1.2rem;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}
.btn-control:disabled {
  opacity: 0.5;
  cursor: default;
}
.btn-capture {
  background: transparent;
  border: none;
  padding: 0;
  cursor: pointer;
}
.capture-img {
  width: 4.5rem;
  height: 4.5rem;
  object-fit: contain;
  border-radius: 50%;
  box-shadow: 0 0 0 0.25rem rgba(255, 255, 255, 0.4);
}
.spinner-container {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #000;
  z-index: 20;
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
</style>