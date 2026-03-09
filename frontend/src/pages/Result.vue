<template>
  <div class="result-page">
    <div class="result-content">
      <img :src="mainImage" alt="Uploaded Photo" class="main-photo" />

      <div v-if="leftEyeImage && rightEyeImage" class="eye-results">
        
        <div class="eye-block">
          <img :src="rightEyeImage" alt="Right Eye" class="eye-thumb" />
          <div class="eye-info">
            <h2>Right eye:</h2>
            <p :class="{ flagged: rightHas, normal: !rightHas }">
              {{ rightHas ? 'Has leukocoria' : 'Normal eye' }}
            </p>
          </div>
        </div>

        <div class="eye-block">
          <img :src="leftEyeImage" alt="Left Eye" class="eye-thumb" />
          <div class="eye-info">
            <h2>Left eye:</h2>
            <p :class="{ flagged: leftHas, normal: !leftHas }">
              {{ leftHas ? 'Has leukocoria' : 'Normal eye' }}
            </p>
          </div>
        </div>
        
      </div>

<div v-else class="eye-results-placeholder">
  <p>Could not isolate eyes for detailed analysis.<br>The model's insight is shown below.</p>
</div>

      <section class="insights">
        <h3>Insights and Recommendations</h3>
        <div class="insight-box">
          <p>{{ insights }}</p>
          <small>
            <em>Disclaimer: This app is a tool for detection, not a medical diagnosis.</em>
          </small>
        </div>
      </section>

      <div class="actions">
        <button @click="downloadScreenshot" class="btn btn-download">
          Download Results
        </button>
      </div>
      <div class="actions">
        <router-link to="/list" class="btn btn-primary">
          See List of Nearby Doctors →
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
// The 'qrcode.vue' import has been removed
import html2canvas from 'html2canvas'

const mainImage = ref('')
const leftEyeImage = ref('')
const rightEyeImage = ref('')
const leftHas = ref(false)
const rightHas = ref(false)
const insights = ref('Analysis complete. Please see results above.')
// The 'shareLink' ref has been removed

onMounted(() => {
  const resultData = sessionStorage.getItem('detectionResult');
  
  mainImage.value = sessionStorage.getItem('originalImage') || '';

  if (resultData) {
    const data = JSON.parse(resultData);
    // --- ADD THIS LINE FOR DEBUGGING ---
    console.log("Received API Data:", data);
    
    if (data.warnings && data.warnings.length > 0) {
        insights.value = data.warnings[0];
        return; 
    }

    if (data.two_eyes) {
        leftEyeImage.value = data.two_eyes.left || '';
        rightEyeImage.value = data.two_eyes.right || '';
    }
    if (data.leukocoria) {
        leftHas.value = data.leukocoria.left === true;
        rightHas.value = data.leukocoria.right === true;
    }

    if (leftHas.value || rightHas.value) {
        insights.value = 'Potential leukocoria signs detected. Please consult an eye specialist.';
    } else {
        insights.value = 'No clear signs of leukocoria detected. Regular eye check-ups are still recommended.';
    }
  }
});

const downloadScreenshot = async () => {
  const element = document.querySelector('.result-page') as HTMLElement;
  if (!element) return;

  const clone = element.cloneNode(true) as HTMLElement;

  clone.style.position = 'absolute';
  clone.style.top = '0';
  clone.style.left = '-9999px';
  clone.style.width = '800px';
  clone.style.height = 'auto';

  document.body.appendChild(clone);

  try {
    await new Promise(resolve => setTimeout(resolve, 50));

    const canvas = await html2canvas(clone, {
      width: 800,
      windowWidth: 800,
      backgroundColor: '#12151e',
      scale: 2,
    });

    const link = document.createElement('a');
    link.href = canvas.toDataURL('image/png');
    link.download = 'leukolook_results.png';
    link.click();
  } finally {
    document.body.removeChild(clone);
  }
};
</script>

<style scoped>
/* Your existing styles will work fine here */
.result-page {
  background: #12151e;
  color: #fff;
}
.result-content {
  padding: 1rem;
}
.main-photo {
  width: 100%;
  border-radius: 0.75rem;
  object-fit: cover;
}
.eye-results {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin: 1rem 0;
}
.eye-block {
  display: flex;
  background: #12151e;
  border-radius: 0.75rem;
  overflow: hidden;
}
.eye-thumb {
  width: 80px;
  object-fit: cover;
}
.eye-info {
  flex: 1;
  padding: 0.75rem;
}
.eye-info h2 {
  margin: 0;
  font-size: 1rem;
}
.eye-info p {
  margin: 0.25rem 0 0;
  font-weight: bold;
}
.eye-info p.flagged {
  color: #ff5c5c;
}
.eye-info p.normal {
  color: #4cd137;
}
.insights {
  margin-bottom: 1rem;
}
.insights h3 {
  margin: 0 0 0.5rem;
  color: #3fe1ff;
  font-size: 1rem;
}
.insight-box {
  background: #12151e;
  border-radius: 0.5rem;
  padding: 0.75rem;
  font-size: 0.9rem;
  line-height: 1.3;
}
.insight-box small {
  display: block;
  margin-top: 0.5rem;
  color: #aaa;
}
.actions {
  display: flex;
  justify-content: center;
  margin: 1rem 0;
}
.btn {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: bold;
  text-decoration: none;
}
.btn-primary {
  background: #3fe1ff;
  color: #12151e;
}
.btn-download {
  background: none;
  border: 1px solid #3fe1ff;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: bold;
  color: #3fe1ff;
  text-decoration: none;
  background-clip: text;
  -webkit-background-clip: text;
}
@media (max-width: 480px) {
  .btn-download,
  .btn-primary {
    padding: 0.5rem 1rem;
    font-size: 0.9rem;
  }
}
</style>