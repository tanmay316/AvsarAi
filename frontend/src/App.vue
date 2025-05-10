<script setup lang="ts">
import { RouterView } from 'vue-router';
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const router = useRouter();
const isDarkMode = ref(true);
const mouseX = ref(0);
const mouseY = ref(0);
const isLoggedIn = ref(false);

const handleMouseMove = (e: MouseEvent) => {
  mouseX.value = e.clientX;
  mouseY.value = e.clientY;
};

const checkLoginStatus = async () => {
  try {
    const response = await axios.get('http://localhost:5000/api/profile', {
      withCredentials: true
    });
    isLoggedIn.value = true;
  } catch (error) {
    isLoggedIn.value = false;
  }
};

const handleLogout = async () => {
  try {
    await axios.post('http://localhost:5000/api/logout', {}, {
      withCredentials: true
    });
    isLoggedIn.value = false;
    router.push('/login');
  } catch (error) {
    console.error('Logout failed:', error);
  }
};

onMounted(() => {
  document.documentElement.classList.toggle('dark', isDarkMode.value);
  window.addEventListener('mousemove', handleMouseMove);
  checkLoginStatus();
});
</script>

<template>
  <div class="app dark" @mousemove="handleMouseMove">
    <div class="cursor-gradient" :style="{ 
      '--mouse-x': `${mouseX}px`,
      '--mouse-y': `${mouseY}px`
    }"></div>
    
    <header class="navbar">
      <div class="logo">
        <span class="logo-text">Avsar<span class="logo-highlight">AI</span></span>
      </div>
      <nav class="nav-links">
        <router-link to="/" class="nav-link">Home</router-link>
        <router-link to="/profile" class="nav-link">Profile</router-link>
        <router-link to="/apply" class="nav-link">Apply</router-link>
        <router-link to="/pricing" class="nav-link">Pricing</router-link>
        <router-link to="/about" class="nav-link">About</router-link>
      </nav>
      <button v-if="isLoggedIn" @click="handleLogout" class="sign-up-btn">Logout</button>
      <router-link v-else to="/register" class="sign-up-btn">Sign Up Free</router-link>
    </header>

    <main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<style>
/* Base Styles */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.app {
  background-color: #0c0c24;
  color: white;
  min-height: 100vh;
  overflow-x: hidden;
  position: relative;
}

.cursor-gradient {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(
    circle at var(--mouse-x) var(--mouse-y),
    rgba(65, 105, 225, 0.1) 0%,
    rgba(6, 182, 212, 0.1) 50%,
    transparent 70%
  );
  z-index: 0;
  pointer-events: none;
  transition: background-position 0.1s ease;
}

/* Navigation Bar */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(15, 15, 40, 0.5);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo-text {
  font-size: 1.8rem;
  font-weight: 700;
  color: white;
}

.logo-highlight {
  color: #4169e1;
}

.nav-links {
  display: flex;
  gap: 2rem;
}

.nav-link {
  color: white;
  text-decoration: none;
  font-size: 1.1rem;
  opacity: 0.8;
  transition: opacity 0.2s;
  position: relative;
}

.nav-link::after {
  content: '';
  position: absolute;
  bottom: -5px;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, #4169e1, #06b6d4);
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.nav-link:hover {
  opacity: 1;
}

.nav-link:hover::after {
  transform: scaleX(1);
}

.nav-link.router-link-active {
  opacity: 1;
}

.nav-link.router-link-active::after {
  transform: scaleX(1);
}

.sign-up-btn {
  background: linear-gradient(90deg, #6366f1, #06b6d4);
  color: white;
  border: none;
  padding: 0.8rem 1.5rem;
  border-radius: 2rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s;
  text-decoration: none;
}

.sign-up-btn:hover {
  transform: translateY(-2px);
}

.main-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
  position: relative;
  z-index: 1;
}

/* Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Responsive Design */
@media (max-width: 768px) {
  .navbar {
    flex-direction: column;
    gap: 1rem;
    padding: 1rem;
  }

  .nav-links {
    flex-wrap: wrap;
    justify-content: center;
    gap: 1rem;
  }

  .nav-link {
    font-size: 1rem;
  }

  .sign-up-btn {
    width: 100%;
    text-align: center;
  }
}
</style>
