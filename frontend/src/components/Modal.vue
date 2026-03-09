<template>
  <div class="modal-backdrop">
    <div class="modal-panel">
      <h2>Preview</h2>
      <img :src="imageSrc" alt="Captured Preview" class="preview-image" />

      <div v-if="warnings && warnings.length > 0" class="warnings">
        <p v-for="(warning, index) in warnings" :key="index">{{ warning }}</p>
      </div>

      <div class="modal-actions">
        <button @click="emit('retake')" class="btn btn-retake">Retake</button>
        <button @click="emit('confirm')" class="btn btn-confirm">Upload</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  imageSrc: string
  warnings: string[]
}>()

const emit = defineEmits(['confirm', 'retake'])
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.modal-panel {
  background-color: #1a1d24; /* Dark panel background */
  color: #e0e0e0; /* Light text */
  border: 1px solid rgba(255, 255, 255, 0.1); /* Subtle border */
  border-radius: 1rem;
  padding: 1.5rem;
  width: 90%;
  max-width: 400px;
  text-align: center;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.modal-panel h2 {
  margin-top: 0;
  margin-bottom: 1rem;
  color: #3fe1ff; /* Accent color for the header */
  font-weight: 600;
}

.preview-image {
  width: 100%;
  max-height: 50vh;
  object-fit: contain;
  border-radius: 0.5rem;
  margin-bottom: 1.5rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.warnings {
  background-color: #444033;
  border: 1px solid #d4b108;
  border-radius: 0.5rem;
  padding: 0.75rem;
  margin-bottom: 1.5rem;
  color: #fffbe6;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.btn {
  padding: 0.75rem 1rem;
  border: none;
  border-radius: 0.5rem;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  width: 100%;
  transition: background-color 0.2s ease;
}

/* Primary "Upload" button style */
.btn-confirm {
  background-color: #3fe1ff;
  color: #12151e;
}
.btn-confirm:hover {
  background-color: #6ff8ff;
}

/* Secondary "Retake" button style */
.btn-retake {
  background-color: #3a3f4b;
  color: #ffffff;
}
.btn-retake:hover {
  background-color: #495057;
}
</style>