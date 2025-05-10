<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const user = ref({
  name: '',
  email: '',
  full_name: '',
  address: '',
  phone_number: '',
  gender: '',
  education: '',
  work_experience: '',
  skills: '',
  linkedin: '',
  portfolio: '',
  github: '',
  projects: '',
  disabilities: '',
  credentials: {
    gmail: '',
    password: ''
  },
  resume: null as File | null,  // New field to hold the resume file
});
const error = ref('');
const success = ref('');
const loading = ref(false);

const fetchUserProfile = async () => {
  try {
    loading.value = true;
    const response = await axios.get('http://localhost:5000/api/profile', {
      withCredentials: true
    });
    user.value = response.data;
  } catch (err: any) {
    error.value = err.response?.data?.error || 'Failed to fetch profile';
    if (err.response?.status === 401) {
      router.push('/login');
    }
  } finally {
    loading.value = false;
  }
};

const handleSubmit = async () => {
  const formData = new FormData();
  formData.append('full_name', user.value.full_name);
  formData.append('address', user.value.address);
  formData.append('phone_number', user.value.phone_number);
  formData.append('gender', user.value.gender);
  formData.append('education', user.value.education);
  formData.append('work_experience', user.value.work_experience);
  formData.append('skills', user.value.skills);
  formData.append('linkedin', user.value.linkedin);
  formData.append('portfolio', user.value.portfolio);
  formData.append('github', user.value.github);
  formData.append('projects', user.value.projects);
  formData.append('disabilities', user.value.disabilities);
  formData.append('gmail', user.value.credentials.gmail);
  formData.append('password', user.value.credentials.password);

  // Check if resume file is selected and append it to form data
  if (user.value.resume) {
    formData.append('resume', user.value.resume);
  }

  try {
    loading.value = true;
    error.value = '';
    success.value = '';
    await axios.post('http://localhost:5000/api/profile', formData, {
      withCredentials: true,
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    success.value = 'Profile updated successfully';
  } catch (err: any) {
    error.value = err.response?.data?.error || 'Failed to update profile';
    if (err.response?.status === 401) {
      router.push('/login');
    }
  } finally {
    loading.value = false;
  }
};

const handleLogout = async () => {
  try {
    await axios.post('/api/logout');
    router.push('/login');
  } catch (err: any) {
    error.value = err.response?.data?.error || 'Failed to logout';
  }
};

onMounted(() => {
  fetchUserProfile();
});
</script>

<template>
  <div class="profile-container">
    <h2>Profile</h2>

    <div v-if="error" class="error-message">
      {{ error }}
    </div>

    <div v-if="success" class="success-message">
      {{ success }}
    </div>

    <form @submit.prevent="handleSubmit" class="profile-form" enctype="multipart/form-data">
      <div class="form-group">
        <label for="full_name">Full Name:</label>
        <input type="text" id="full_name" v-model="user.full_name" required placeholder="Enter your full name" />
      </div>

      <div class="form-group">
        <label for="address">Address:</label>
        <input type="text" id="address" v-model="user.address" required placeholder="Enter your address" />
      </div>

      <div class="form-group">
        <label for="phone_number">Phone Number:</label>
        <input type="tel" id="phone_number" v-model="user.phone_number" required
          placeholder="Enter your phone number" />
      </div>

      <div class="form-group">
        <label for="gender">Gender:</label>
        <select id="gender" v-model="user.gender">
          <option value="">Select gender</option>
          <option value="male">Male</option>
          <option value="female">Female</option>
          <option value="other">Other</option>
        </select>
      </div>

      <div class="form-group">
        <label for="education">Education:</label>
        <textarea id="education" v-model="user.education" placeholder="Enter your education details"></textarea>
      </div>

      <div class="form-group">
        <label for="work_experience">Work Experience:</label>
        <textarea id="work_experience" v-model="user.work_experience"
          placeholder="Enter your work experience"></textarea>
      </div>

      <div class="form-group">
        <label for="skills">Skills:</label>
        <input type="text" id="skills" v-model="user.skills" placeholder="Enter your skills (comma separated)" />
      </div>

      <div class="form-group">
        <label for="linkedin">LinkedIn:</label>
        <input type="url" id="linkedin" v-model="user.linkedin" placeholder="Enter your LinkedIn profile URL" />
      </div>

      <div class="form-group">
        <label for="portfolio">Portfolio:</label>
        <input type="url" id="portfolio" v-model="user.portfolio" placeholder="Enter your portfolio URL" />
      </div>

      <div class="form-group">
        <label for="github">GitHub:</label>
        <input type="url" id="github" v-model="user.github" placeholder="Enter your GitHub profile URL" />
      </div>

      <div class="form-group">
        <label for="projects">Projects:</label>
        <textarea id="projects" v-model="user.projects" placeholder="Describe your projects"></textarea>
      </div>

      <div class="form-group">
        <label for="disabilities">Disabilities (if any):</label>
        <input type="text" id="disabilities" v-model="user.disabilities" placeholder="Enter any disabilities" />
      </div>

      <!-- Resume upload -->
      <div class="form-group">
        <label for="resume">Upload Resume (PDF format):</label>
        <input type="file" id="resume" @change="(event: Event) => { 
          const target = event.target as HTMLInputElement;
          if (target && target.files) user.resume = target.files[0];
        }" accept=".pdf" />
      </div>

      <div class="credentials-section">
        <h3>Credentials</h3>
        <div class="form-group">
          <label for="gmail">Gmail:</label>
          <input type="email" id="gmail" v-model="user.credentials.gmail" placeholder="Enter your Gmail" />
        </div>

        <div class="form-group">
          <label for="password">Password:</label>
          <input type="password" id="password" v-model="user.credentials.password" placeholder="Enter your password" />
        </div>
      </div>

      <button type="submit" class="submit-button" :disabled="loading">
        {{ loading ? 'Updating...' : 'Update Profile' }}
      </button>
      <button @click="handleLogout" class="logout-button">Logout</button>
    </form>
  </div>
</template>



<style scoped>
.profile-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.profile-form {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin-top: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 20px;
}

label {
  font-weight: bold;
}

input, select, textarea {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

textarea {
  resize: vertical;
  min-height: 100px;
}

.credentials-section {
  margin-top: 20px;
  padding: 20px;
  background-color: #f5f5f5;
  border-radius: 4px;
}

.credentials-section h3 {
  color: #42b983;
  margin-bottom: 15px;
}

.error-message {
  color: #ff4444;
  margin: 10px 0;
  padding: 10px;
  background-color: #ffebee;
  border-radius: 4px;
}

.success-message {
  color: #42b983;
  margin: 10px 0;
  padding: 10px;
  background-color: #e8f5e9;
  border-radius: 4px;
}

.submit-button {
  padding: 12px 24px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
}

.submit-button:hover {
  background-color: #3aa876;
}

.submit-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.logout-button {
  padding: 12px 24px;
  background-color: #ff4444;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
}

.logout-button:hover {
  background-color: #cc0000;
}
</style> 