<template>
  <div class="list-container">
    <header class="list-header">
      <h2>List of Ophthalmologists</h2>
      <p>
        If the result indicates possible leukocoria, you may consider consulting
        one of the ophthalmologists listed below for further evaluation.
      </p>
    </header>

    <div class="doctors-list">
      <div v-for="doctor in doctors" :key="doctor.name" class="doctor-card">
        <div class="doctor-avatar">
          <img :src="doctor.avatar" :alt="doctor.name" />
        </div>
        <div class="doctor-info">
          <h2 class="doctor-name">{{ doctor.name }}</h2>
          <p class="doctor-title">{{ doctor.title }}</p>
          <div class="doctor-details">
            <p class="detail-item">
              <span class="detail-label">Specialty:</span>
              {{ doctor.specialty }}
            </p>
            <p class="detail-item">
              <span class="detail-label">Experience:</span>
              {{ doctor.experience }}
            </p>
            <div class="detail-item">
              <span class="detail-label">Clinics:</span>
              <ul class="clinics-list">
                <li v-for="clinic in doctor.clinics" :key="clinic">
                  {{ clinic }}
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const doctors = ref([
  {
    name: 'Dr. Lois Agnes Espa Lumontod',
    title: 'Dipl.Ophth.',
    specialty: 'Pediatric Ophthalmology, Strabismus Specialist, Comprehensive Adult Ophthalmology',
    experience: '6 yrs',
    clinics: ['Internist Hub', 'Adventist Medical Center'],
    avatar: '../default-female.png',
  },
  {
    name: 'Dr. Jomael Leandro Timonera Roxas',
    title: 'MD, DPBO',
    specialty: 'Ophthalmology',
    experience: '10 yrs',
    clinics: ['Mercy Community Hospital', 'Dr. Uy Hospital Eye Clinic'],
    avatar: '../default-male.png',
  },
  {
    name: 'Dr. Vincent Arthur Uy Valdez',
    title: 'MD, DPBO',
    specialty: 'Ophthalmology',
    experience: '7 yrs',
    clinics: ['Mercy Community Hospital', 'Lagas Eye Clinic'],
    avatar: '../default-male.png',
  },
  {
    name: 'Dr. Cielo Maria Roxas',
    title: 'MD, DPBO',
    specialty: 'Pediatric Ophthalmology',
    experience: '7 yrs',
    clinics: ['Mercy Community Hospital', 'Polymedic Medical Plaza'],
    avatar: '../default-female.png',
  },
  {
    name: 'Dr. Emmanuel Lee Boniao',
    title: 'MD, DPBO, FPSOPRS',
    specialty: 'Pediatric Ophthalmology',
    experience: '7 yrs',
    clinics: ['Boniao Eye Clinic',
            'CDO Polymedic General Hospital',
            'Davao Eye and Surgical Center',
            'Medicus Medical Center'],
    avatar: '../default-male.png',
  },
])
</script>

<style scoped>
/* General container for the page */
.list-container {
  background-color: #12151e;
  color: #e0e0e0;
  padding: 1.5rem;
  min-height: 100vh;
}

/* Header and intro text */
.list-header {
  text-align: center;
  margin-bottom: 2rem;
}

.list-header h2 {
  color: #3fe1ff; /* Accent color */
  margin-bottom: 0.85rem;
  font-weight: bold;
  font-size: 1.5rem;
}

.list-header p {
  color: #adb5bd;
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.5;
  font-size: 0.9rem;
}

/* --- RESPONSIVE SINGLE-COLUMN LIST --- */
.doctors-list {
  display: flex;
  flex-direction: column; /* This ensures it's always a single column */
  gap: 1rem;
  max-width: 700px; /* Allows the list to span wider on large screens */
  margin: 0 auto; /* Centers the list on the page */
}

/* --- COMPACT CARD STYLES --- */

/* Individual doctor card styling */
.doctor-card {
  background-color: #1a1d24;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 0.75rem;
  padding: 0.75rem 1rem; /* Reduced padding for compact height */
  display: flex;
  gap: 1rem;
  align-items: center; 
  transition: transform 0.2s ease;
}

.doctor-card:hover {
  transform: scale(1.01);
}

/* Doctor's avatar image - SMALLER */
.doctor-avatar img {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  border: 2px solid #3fe1ff;
  object-fit: cover;
  flex-shrink: 0;
}

/* Container for all text info */
.doctor-info {
  flex: 1;
}

/* Doctor's name - SMALLER */
.doctor-name {
  color: #ffffff;
  font-size: 0.95rem; /* Smaller font */
  font-weight: bold;
  margin: 0 0 0.2rem 0;
}

/* Doctor's degree/title - SMALLER */
.doctor-title {
  color: #adb5bd;
  font-size: 0.8rem; /* Smaller font */
  margin-bottom: 0.6rem;
  display: block;
}

/* Details like Specialty and Experience - SMALLER */
.doctor-details {
  font-size: 0.85rem; /* Smaller font */
  line-height: 1.5;
}

.detail-item {
  display: flex;
  flex-wrap: wrap; /* Allows long text to wrap gracefully */
  margin-bottom: 0.4rem;
}

/* Styling for the labels */
.detail-label {
  font-weight: 600;
  color: #3fe1ff;
  margin-right: 0.5rem;
  flex-shrink: 0;
}

/* Clinics list styling */
.clinics-list {
  list-style: none;
  padding-left: 0;
  margin: 0;
}

.clinics-list li {
  position: relative;
  padding-left: 1.2rem;
  font-size: 0.85rem; /* Smaller font */
  margin-top: 0.2rem;
}

/* Custom bullet point */
.clinics-list li::before {
  content: '•';
  color: #3fe1ff;
  font-weight: bold;
  font-size: 1rem; /* Smaller bullet */
  position: absolute;
  left: 0;
  top: -1px;
}
</style>