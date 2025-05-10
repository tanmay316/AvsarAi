<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const canvasRef = ref<HTMLCanvasElement | null>(null);
const ctx = ref<CanvasRenderingContext2D | null>(null);
const mouseX = ref(0);
const mouseY = ref(0);
const targetX = ref(0);
const targetY = ref(0);

const config = {
  radius: 200,
  brightness: 0.15,
  color: '#ffffff',
  smoothing: 0.1
};

const handleMouseMove = (e: MouseEvent) => {
  targetX.value = e.clientX;
  targetY.value = e.clientY;
};

const animate = () => {
  if (!ctx.value || !canvasRef.value) return;

  // Smooth the cursor movement
  mouseX.value += (targetX.value - mouseX.value) * config.smoothing;
  mouseY.value += (targetY.value - mouseY.value) * config.smoothing;

  // Clear the canvas
  ctx.value.clearRect(0, 0, canvasRef.value.width, canvasRef.value.height);

  // Create gradient
  const gradient = ctx.value.createRadialGradient(
    mouseX.value,
    mouseY.value,
    0,
    mouseX.value,
    mouseY.value,
    config.radius
  );

  gradient.addColorStop(0, `rgba(255, 255, 255, ${config.brightness})`);
  gradient.addColorStop(1, 'rgba(0, 0, 0, 0)');

  // Draw the spotlight
  ctx.value.fillStyle = gradient;
  ctx.value.fillRect(0, 0, canvasRef.value.width, canvasRef.value.height);

  requestAnimationFrame(animate);
};

onMounted(() => {
  if (canvasRef.value) {
    canvasRef.value.width = window.innerWidth;
    canvasRef.value.height = window.innerHeight;
    ctx.value = canvasRef.value.getContext('2d');
    window.addEventListener('mousemove', handleMouseMove);
    animate();
  }
});

onUnmounted(() => {
  window.removeEventListener('mousemove', handleMouseMove);
});

const stats = ref({
  jobsApplied: 2500,
  users: 5
});

const features = ref([
  {
    title: 'Share a Job Link',
    description: 'Simply paste any job listing URL from any job board or company career page. Avsar AI immediately analyzes the job requirements and company details.',
    icon: '🔗'
  },
  {
    title: 'AI Fills Applications',
    description: 'Our advanced AI controls your browser to complete application forms, tailoring your resume and answers to match the job requirements perfectly.',
    icon: '🤖'
  },
  {
    title: 'Review and Submit',
    description: 'Before final submission, you can review and make any adjustments. With one click, your application is submitted.',
    icon: '✅'
  }
]);

const benefits = ref([
  {
    title: 'Works with company career pages',
    icon: '🏢'
  },
  {
    title: 'Compatible with all major job boards',
    icon: '📋'
  },
  {
    title: 'Handles complex application forms',
    icon: '📝'
  }
]);
</script>

<template>
  <div class="home">
    <canvas
      ref="canvasRef"
      class="spotlight-cursor"
    ></canvas>
    
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">
          Apply to Jobs with <span class="text-blue">One</span>
          <span class="text-cyan">Click</span>
        </h1>
        <p class="hero-description">
          Avsar AI automates your job applications, letting you apply to
          hundreds of positions with just a link. Built for the modern job seeker.
        </p>
      </div>
      <div class="floating-icons">
        <div class="icon-folder"><div class="icon-inner"></div></div>
        <div class="icon-document"><div class="icon-inner"></div></div>
        <div class="icon-user"><div class="icon-inner"></div></div>
        <div class="icon-chat"><div class="icon-inner"></div></div>
        <div class="glow-effect"></div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section">
      <button class="apply-now-btn" @click="router.push('/apply')">
        APPLY NOW <span class="arrow-icon">→</span>
      </button>
      <button class="how-it-works-btn">See How It Works</button>
      <div class="stats-container">
        <div class="user-avatars">
          <div class="avatar avatar-blue">JD</div>
          <div class="avatar avatar-purple">KP</div>
          <div class="avatar avatar-pink">AR</div>
          <div class="avatar avatar-blue-light">+5</div>
        </div>
        <div class="stats-text">
          <span class="stats-number">{{ stats.jobsApplied }}+</span> jobs applied to today
        </div>
      </div>
    </section>

    <!-- How It Works Section -->
    <section class="how-it-works-section">
      <h2 class="section-title">
        How <span class="text-blue">Avsar</span> <span class="text-cyan">AI</span> Works
      </h2>
      <p class="section-description">
        Our AI-powered platform streamlines your job search, making
        applications effortless and efficient.
      </p>
    </section>

    <!-- Steps Section -->
    <section class="steps-section">
      <div v-for="(feature, index) in features" :key="index" class="step-card">
        <div class="step-number">{{ index + 1 }}</div>
        <h3 class="step-title">{{ feature.title }}</h3>
        <p class="step-description">{{ feature.description }}</p>
      </div>
    </section>

    <!-- Save Time Section -->
    <section class="save-time-section">
      <div class="illustration-container">
        <div class="tech-illustration">
          <div class="tech-person"></div>
          <div class="tech-cube"></div>
          <div class="tech-sphere"></div>
        </div>
      </div>
      <div class="content-container">
        <h2 class="section-title">
          Save <span class="text-blue">Hours</span> of Application Time
        </h2>
        <p class="section-description">
          Stop spending hours filling out repetitive application forms.
          Avsar AI does it all for you in seconds.
        </p>
        <ul class="benefits-list">
          <li class="benefit-item">
            <span class="check-icon">✓</span>
            Apply to 50+ jobs in the time it takes to apply to one
          </li>
          <li class="benefit-item">
            <span class="check-icon">✓</span>
            Automated form filling and document uploads
          </li>
          <li class="benefit-item">
            <span class="check-icon">✓</span>
            Focus on interviews instead of applications
          </li>
        </ul>
      </div>
    </section>

    <!-- Any Job Section -->
    <section class="any-job-section">
      <div class="content-container">
        <h2 class="section-title">
          AI Agents for <span class="text-blue">Any</span> <span class="text-cyan">Job Posting</span>
        </h2>
        <p class="section-description">
          Unlike other platforms, Avsar AI works with any job posting
          on the internet, not just popular job boards.
        </p>
        <ul class="benefits-list">
          <li v-for="(benefit, index) in benefits" :key="index" class="benefit-item">
            <span class="check-icon">✓</span>
            {{ benefit.title }}
          </li>
        </ul>
      </div>
      <div class="network-illustration">
        <div class="network-circle"></div>
        <div class="network-icons">
          <div class="network-icon icon-briefcase"></div>
          <div class="network-icon icon-linkedin"></div>
          <div class="network-icon icon-user"></div>
        </div>
      </div>
    </section>

    <!-- Final CTA Section -->
    <section class="final-cta-section">
      <h2 class="section-title">
        Ready to <span class="text-gradient">Revolutionize</span> Your Job Search?
      </h2>
      <p class="section-description">
        Join thousands of Gen Z job seekers who are landing interviews faster with Avsar AI.
      </p>
      <button class="apply-now-btn" @click="router.push('/apply')">
        APPLY NOW <span class="arrow-icon">→</span>
      </button>
      <p class="no-credit-card">No credit card required</p>
    </section>
  </div>
</template>

<style scoped>
/* Base Styles */
.home {
  background: linear-gradient(135deg, #070F2B, #010038);
  color: white;
  min-height: 100vh;
  overflow-x: hidden;
  position: relative;
}

.spotlight-cursor {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
  mix-blend-mode: overlay;
}

/* Hero Section */
.hero-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
  position: relative;
  overflow: hidden;
  z-index: 1;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 800;
  margin-bottom: 1.5rem;
  line-height: 1.2;
}

.text-blue {
  color: #4169e1;
}

.text-cyan {
  color: #06b6d4;
}

.hero-description {
  font-size: 1.2rem;
  max-width: 800px;
  margin: 0 auto;
  opacity: 0.9;
  line-height: 1.6;
}

.floating-icons {
  position: relative;
  width: 100%;
  height: 200px;
  margin-top: 3rem;
}

.icon-folder,
.icon-document,
.icon-user,
.icon-chat {
  position: absolute;
  width: 60px;
  height: 60px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: float 6s ease-in-out infinite;
}

.icon-folder { top: 20%; left: 20%; animation-delay: 0s; }
.icon-document { top: 40%; right: 20%; animation-delay: 1s; }
.icon-user { bottom: 30%; left: 30%; animation-delay: 2s; }
.icon-chat { top: 60%; right: 30%; animation-delay: 3s; }

.glow-effect {
  position: absolute;
  width: 200px;
  height: 200px;
  background: radial-gradient(circle, rgba(6, 182, 212, 0.3) 0%, rgba(65, 105, 225, 0.1) 50%, transparent 70%);
  border-radius: 50%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  filter: blur(30px);
}

/* CTA Section */
.cta-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
  gap: 1.5rem;
  z-index: 1;
}

.apply-now-btn {
  background: linear-gradient(90deg, #f43f5e, #8b5cf6);
  color: white;
  border: none;
  padding: 1rem 2.5rem;
  border-radius: 2rem;
  font-weight: 600;
  font-size: 1.1rem;
  cursor: pointer;
  transition: transform 0.2s;
  box-shadow: 0 0 20px rgba(244, 63, 94, 0.5);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.apply-now-btn:hover {
  transform: translateY(-2px);
}

.how-it-works-btn {
  background: transparent;
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 0.8rem 1.5rem;
  border-radius: 2rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.how-it-works-btn:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.stats-container {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-top: 1rem;
}

.user-avatars {
  display: flex;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  margin-left: -10px;
  border: 2px solid #0c0c24;
}

.avatar:first-child {
  margin-left: 0;
}

.avatar-blue {
  background-color: #4169e1;
}

.avatar-purple {
  background-color: #8b5cf6;
}

.avatar-pink {
  background-color: #f43f5e;
}

.avatar-blue-light {
  background-color: #60a5fa;
}

.stats-number {
  font-weight: 700;
}

/* How It Works Section */
.how-it-works-section {
  padding: 4rem 2rem 2rem;
  text-align: center;
  z-index: 1;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 1rem;
}

.section-description {
  font-size: 1.2rem;
  max-width: 800px;
  margin: 0 auto;
  opacity: 0.9;
  line-height: 1.6;
}

/* Steps Section */
.steps-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  z-index: 1;
}

.step-card {
  background-color: rgba(15, 15, 40, 0.5);
  border-radius: 1rem;
  padding: 2rem;
  position: relative;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: transform 0.3s ease;
}

.step-card:hover {
  transform: translateY(-5px);
}

.step-number {
  background-color: #4169e1;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.step-title {
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.step-description {
  opacity: 0.8;
  line-height: 1.6;
}

/* Save Time Section */
.save-time-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 3rem;
  padding: 4rem 2rem;
  align-items: center;
  z-index: 1;
}

.tech-illustration {
  position: relative;
  width: 100%;
  height: 400px;
}

.tech-person {
  position: absolute;
  width: 200px;
  height: 200px;
  background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z" fill="%236C63FF"/></svg>') no-repeat center center;
  background-size: contain;
  animation: float 6s ease-in-out infinite;
  filter: drop-shadow(0 0 20px rgba(108, 99, 255, 0.5));
}

.tech-cube {
  position: absolute;
  width: 100px;
  height: 100px;
  background: linear-gradient(45deg, #4169e1, #06b6d4);
  transform: rotate(45deg);
  animation: float 4s ease-in-out infinite reverse;
  filter: drop-shadow(0 0 15px rgba(108, 99, 255, 0.4));
}

.tech-sphere {
  position: absolute;
  width: 80px;
  height: 80px;
  background: radial-gradient(circle at 30% 30%, #4169e1, #06b6d4);
  border-radius: 50%;
  right: 0;
  bottom: 0;
  animation: float 3s ease-in-out infinite;
  filter: drop-shadow(0 0 15px rgba(0, 217, 255, 0.4));
}

.benefits-list {
  list-style: none;
  margin-top: 2rem;
}

.benefit-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
  font-size: 1.1rem;
}

.check-icon {
  color: #10b981;
  font-weight: bold;
}

/* Any Job Section */
.any-job-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 3rem;
  padding: 4rem 2rem;
  align-items: center;
  z-index: 1;
}

.network-illustration {
  position: relative;
  height: 300px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.network-circle {
  width: 200px;
  height: 200px;
  background: linear-gradient(135deg, rgba(65, 105, 225, 0.3), rgba(6, 182, 212, 0.3));
  border-radius: 50%;
  position: relative;
  animation: rotate 20s linear infinite;
}

.network-icons {
  position: absolute;
  width: 100%;
  height: 100%;
}

.network-icon {
  position: absolute;
  width: 50px;
  height: 50px;
  background-color: white;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-briefcase {
  top: 20%;
  right: 30%;
  background-color: #f0f4f8;
}

.icon-linkedin {
  bottom: 30%;
  left: 25%;
  background-color: #e0e7ff;
}

.icon-user {
  top: 50%;
  left: 40%;
  background-color: #fce7f3;
}

/* Final CTA Section */
.final-cta-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 6rem 2rem;
  gap: 1.5rem;
  z-index: 1;
}

.text-gradient {
  background: linear-gradient(90deg, #4169e1, #06b6d4);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.no-credit-card {
  opacity: 0.7;
  margin-top: 0.5rem;
}

/* Animations */
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-20px); }
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Responsive Adjustments */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }
  
  .section-title {
    font-size: 2rem;
  }
  
  .steps-section {
    grid-template-columns: 1fr;
  }
  
  .save-time-section,
  .any-job-section {
    grid-template-columns: 1fr;
  }
}
</style> 