<template>
  <div class="about-container">
    <div class="about-content">
      <div class="about-visual">
        <img :src="eyeIcon" alt="LeukoLook Eye Icon" />
      </div>
      <div class="about-text">
        <h1>About LeukoLook</h1>
        <p class="tagline">
          A real-time detection system for early signs of leukocoria.
        </p>
        <div class="divider"></div>
        <p class="description">
          LeukoLook is a system designed to detect signs of leukocoria in
          real-time using a photo as input. Powered by a CNN-based model
          trained to recognize leukocoria with reliable accuracy, the app allows
          users to either upload or capture a clear image that visibly includes
          the eyes. Based on the analysis, the system provides a result
          indicating whether leukocoria may be present.
        </p>
        <p class="description">
          These results can help users determine if they should consult an
          ophthalmologist for further evaluation. LeukoLook is available in
          two formats: a mobile web version for quick access, and a mobile app
          version that offers additional features such as saving test results
          and viewing patient history.
        </p>
      </div>
    </div>

    <section class="info-section">
      <div class="info-card">
        <h2>What is Leukocoria?</h2>
        <p>
          Leukocoria means “white pupil.” It is an abnormal pupillary reflex
          usually more prominent after pupillary dilation and is often the first
          sign of a range of serious intraocular disorders. Immediate diagnosis and
          management are mandatory as most conditions are vision-threatening,
          and some may be life-threatening.
        </p>
        <div class="sources">
          <h3>Sources:</h3>
          <ul>
            <li>
              <a href="https://www.ncbi.nlm.nih.gov/books/NBK560794/" target="_blank" rel="noopener noreferrer">
                ncbi.nlm.nih.gov/books/NBK560794/
              </a>
            </li>
            <li>
              <a href="https://www.aapos.org/glossary/leukocoria" target="_blank" rel="noopener noreferrer">
                aapos.org/glossary/leukocoria
              </a>
            </li>
          </ul>
        </div>
      </div>
    </section>

    <section class="cta-section">
      <router-link to="/camera" class="cta-button">
        Check for Signs Now
      </router-link>
    </section>

  </div>
</template>

<script setup lang="ts">
// Note: Make sure the path to your eye icon is correct.
import eyeIcon from '../assets/eye.svg'
</script>

<style scoped>
.about-container {
  background-color: #12151e;
  color: #e0e0e0;
  padding: 2rem 1.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 80px);
}

/* --- Section 1: About the App --- */
.about-content {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 1rem;
  max-width: 900px;
  width: 100%;
  margin-bottom: 2rem;
}

.about-visual {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 0;
}

.about-visual img {
  width: 100%;
  max-width: 250px;
  opacity: 0.8;
}

.about-text {
  flex: 2;
  text-align: left;
}

.about-text h1 {
  color: #3fe1ff;
  font-size: 2.5rem;
  font-weight: 700;
  margin-top: 0;
  margin-bottom: 0.5rem;
}

.about-text .tagline {
  font-size: 1.2rem;
  color: #adb5bd;
  margin-bottom: 1.5rem;
  font-style: italic;
}

.divider {
  height: 2px;
  width: 100px;
  background-color: #3fe1ff;
  margin-bottom: 1.5rem;
}

.about-text .description {
  font-size: 1rem;
  line-height: 1.7;
  color: #e0e0e0;
  margin-bottom: 1rem;
}

/* --- Section 2: Info Card --- */
.info-section {
  width: 100%;
  display: flex;
  justify-content: center;
  max-width: 900px;
}

.info-card {
  background-color: #1a1d24;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 1rem;
  padding: 1.5rem 2rem;
  width: 100%;
}

.info-card h2 {
  color: #3fe1ff;
  text-align: center;
  margin-top: 0;
  margin-bottom: 1.5rem;
  font-size: 1.8rem;
}

.info-card p {
  line-height: 1.7;
  text-align: left;
}

.sources {
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.sources h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1rem;
  color: #adb5bd;
}

.sources ul {
  margin: 0;
  padding: 0;
  list-style: none;
}

.sources a {
  color: #3fe1ff;
  text-decoration: none;
  font-size: 0.9rem;
}

.sources a:hover {
  text-decoration: underline;
}

/* --- Section 3: Call to Action (NEW) --- */
.cta-section {
  width: 100%;
  text-align: center;
  padding: 3rem 0 2rem 0;
}

.cta-button {
  display: inline-block;
  background-color: #3fe1ff;
  color: #12151e;
  font-size: 1.1rem;
  font-weight: bold;
  padding: 0.8rem 2rem;
  border-radius: 0.5rem;
  text-decoration: none;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.cta-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(63, 225, 255, 0.2);
}


/* --- Responsive adjustments --- */
@media (max-width: 768px) {
  .about-content {
    flex-direction: column;
    text-align: center;
    margin-bottom: 2rem;
  }
  .about-visual {
    margin-bottom: 2rem;
  }
  .about-visual img {
    max-width: 150px;
  }
  .about-text, .info-card p {
    text-align: center;
    align-items: center;
    display: flex;
    flex-direction: column;
  }
  .about-text h1 {
    font-size: 2rem;
  }
}
</style>