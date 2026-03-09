<template>
  <div id="app">
    <!-- 1) Transparent header with logo + toggle -->
    <header class="site-header">
      <router-link to="/" class="logo-link">
        <div class="logo">
          <span class="logo-text">Leuko</span><span class="logo-accent">Look</span>
        </div>
      </router-link>
      <button class="menu-btn" @click="isOpen = !isOpen" aria-label="Toggle menu">
        <FontAwesomeIcon :icon="isOpen ? 'times' : 'bars'" />
      </button>
    </header>

    <!-- 2) Backdrop (click to close) -->
    <div class="backdrop" v-if="isOpen" @click="isOpen = false" />

    <!-- 3) Sidebar from right -->
    <aside class="sidebar" :class="{ open: isOpen }">
      <!-- Sidebar header / logo -->
      <router-link to="/" class="sidebar-header-link" @click.native="isOpen = false">
        <div class="sidebar-header">
          <FontAwesomeIcon icon="eye" class="sidebar-logo" />
          <span class="sidebar-title">LeukoLook</span>
        </div>
      </router-link>

      <nav>
        <ul class="menu-list">
          <li>
            <router-link to="/" @click.native="isOpen = false">
              <FontAwesomeIcon icon="home" class="icon" />
              <span>Home</span>
            </router-link>
          </li>
          <li>
            <router-link to="/list" @click.native="isOpen = false">
              <FontAwesomeIcon icon="stethoscope" class="icon" />
              <span>Ophthalmologists</span>
            </router-link>
          </li>
          <li>
            <router-link to="/about" @click.native="isOpen = false">
              <FontAwesomeIcon icon="info-circle" class="icon" />
              <span>About</span>
            </router-link>
          </li>
        </ul>
      </nav>
    </aside>

    <!-- 4) Page content under header -->
    <main class="page-content">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
//import { useRouter } from 'vue-router'
import { library } from '@fortawesome/fontawesome-svg-core'
import {
  faBars,
  faTimes,
  faHome,
  faStethoscope,
  faHistory,
  faCog,
  faInfoCircle,
  faSignOutAlt,
  faEye
} from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

// register FontAwesome icons
library.add(
  faBars,
  faTimes,
  faHome,
  faStethoscope,
  faHistory,
  faCog,
  faInfoCircle,
  faSignOutAlt,
  faEye
)

const isOpen = ref(false)
//const router = useRouter()

/**function logout() {
  // TODO: handle your logout logic here
  router.push('/login')
}**/
</script>

<style scoped>
/* 1) Reset & full-screen */
*, *::before, *::after { box-sizing: border-box; }
html, body, #app {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
  background: #12151e;
  /* background: linear-gradient(135deg, #1b1e2a 0%, #12151e 100%); */
  font-family: system-ui, Avenir, Helvetica, Arial, sans-serif;
  color: #fff;
}

/* 2) Transparent header */
.site-header {
  position: fixed;
  top: 0; left: 0; right: 0;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 1.5rem;
  background: transparent;
  z-index: 1000;
}
.logo-link {
  text-decoration: none; /* This removes the underline */
}
.logo {
  font-size: 2rem;
  font-weight: bold;
}
.logo-text { color: #fff; }
.logo-accent { color: #3fe1ff; }

/* 3) Menu button */
.menu-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.5rem;
  color: #fff;
  padding: 0;
  display: flex;
  align-items: center;
  z-index: 1100;
}

/* 4) Backdrop */
.backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  z-index: 900;
}

/* 5) Sidebar sliding in from right */
.sidebar {
  position: fixed;
  top: 0; right: 0;
  width: 280px;
  height: 100%;
  background: #1f2430;
  padding: 1rem;
  transform: translateX(100%);
  transition: transform 0.3s ease;
  z-index: 1000;
}
.sidebar.open {
  transform: translateX(0);
}

/* Sidebar header */
.sidebar-header-link {
  text-decoration: none; /* Removes the underline */
  color: #fff; /* Ensures the text stays white */
}
.sidebar-header {
  display: flex;
  align-items: center;
  margin-bottom: 2rem;
}
.sidebar-logo {
  font-size: 1.75rem;
  color: #3fe1ff;
  margin-right: 0.5rem;
}
.sidebar-title {
  font-size: 1.25rem;
  font-weight: bold;
  color: #fff;
}

/* Menu list */
.menu-list {
  list-style: none;
  margin: 0;
  padding: 0;
}
.menu-list li + li {
  margin-top: 1rem;
}
.menu-list a {
  display: flex;
  align-items: center;
  color: #fff;
  text-decoration: none;
  font-size: 1rem;
  padding: 0.5rem;
  border-radius: 0.375rem;
  transition: background 0.2s;
}
.menu-list a:hover {
  background: rgba(255,255,255,0.1);
}
.icon {
  margin-right: 0.75rem;
  width: 1.25em;
  height: 1.25em;
  color: #3fe1ff;
}

/* Sidebar footer */
.sidebar-footer {
  margin-top: auto;
  padding-top: 1rem;
  border-top: 1px solid rgba(255,255,255,0.1);
}
.logout-btn {
  display: flex;
  align-items: center;
  background: none;
  border: none;
  color: #fff;
  font-size: 1rem;
  padding: 0.5rem;
  width: 100%;
  cursor: pointer;
  border-radius: 0.375rem;
  transition: background 0.2s;
}
.logout-btn:hover {
  background: rgba(255,255,255,0.1);
}

/* 6) Push content below header */
.page-content {
  margin-top: 80px;
  padding: 1rem;
  background: #12151e;
  min-height: calc(100% - 80px);
  overflow-y: auto;
}
</style>
