<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

// Router setup
const router = useRouter();

// State variables
const jobUrl = ref('');
const error = ref('');
const success = ref('');
const loading = ref(false);
const applicationStatus = ref('');
const applicationId = ref('');
const captchaRequest = ref<{ image_url: string; application_id?: string } | null>(null);
const captchaSolution = ref('');

// Status messages mapping
const statusMessages = computed(() => ({
  processing: 'Starting application process...',
  navigating: 'Navigating to job site...',
  logging_in: 'Logging in to career portal...',
  filling_form: 'Filling application form...',
  uploading_resume: 'Uploading resume...',
  reviewing: 'Final review before submission...',
  awaiting_captcha: 'CAPTCHA verification required',
  completed: 'Application completed successfully!',
  failed: 'Application process failed',
  cancelled: 'Application cancelled'
}));

// Progress bar mapping
const progressWidth = computed(() => {
  const statusProgressMap: Record<string, string> = {
    [statusMessages.value.processing]: '10%',
    [statusMessages.value.navigating]: '25%',
    [statusMessages.value.logging_in]: '40%',
    [statusMessages.value.filling_form]: '55%',
    [statusMessages.value.uploading_resume]: '70%',
    [statusMessages.value.reviewing]: '85%',
    [statusMessages.value.awaiting_captcha]: '90%',
    [statusMessages.value.completed]: '100%',
    [statusMessages.value.failed]: '0%',
    [statusMessages.value.cancelled]: '0%'
  };

  return statusProgressMap[applicationStatus.value] || '0%';
});

// Handle form submission (Job URL)
const handleSubmit = async () => {
  try {
    loading.value = true;
    error.value = '';
    success.value = '';
    applicationStatus.value = statusMessages.value.processing;

    const response = await axios.post('http://localhost:5000/api/apply', {
      job_url: jobUrl.value
    }, {
      withCredentials: true
    });

    if (response.data.message === 'AI agent started job application') {
      applicationId.value = response.data.application_id;
      success.value = 'AI agent initialized. Starting job application process...';
      pollApplicationStatus(applicationId.value);
    }
  } catch (err: any) {
    error.value = err.response?.data?.error || 'Failed to submit job application';
    applicationStatus.value = '';
  } finally {
    loading.value = false;
  }
};

// Poll application status (track progress)
const pollApplicationStatus = async (appId: string) => {
  try {
    const response = await axios.get(`http://localhost:5000/api/apply/status/${appId}`, {
      withCredentials: true
    });

    if (response.status === 401) {
      router.push('/login');
      return;
    }

    if (response.data.error) {
      if (response.data.error.includes('context')) {
        error.value = 'Session expired - please restart the application';
        applicationStatus.value = 'failed';
        return;
      }
      handleApplicationError(response.data.error);
      return;
    }

    applicationStatus.value = statusMessages.value[response.data.status as keyof typeof statusMessages.value] || '';

    if (!['completed', 'failed', 'cancelled'].includes(response.data.status)) {
      setTimeout(() => pollApplicationStatus(appId), 3000);
    }
  } catch (err: any) {
    if (err.response?.status === 401) {
      router.push('/login');
    } else {
      error.value = 'Connection error - ensure backend is running';
    }
  }
};

// Handle errors during application process
const handleApplicationError = (errorMsg: string) => {
  if (errorMsg.includes('credentials')) {
    error.value = `${errorMsg} - Please update your credentials in profile settings`;
  } else if (errorMsg.includes('resume')) {
    error.value = `${errorMsg} - Please upload a resume in PDF format`;
  } else {
    error.value = errorMsg;
  }
  applicationStatus.value = statusMessages.value.failed;
};

// Submit CAPTCHA solution
const submitCaptcha = async () => {
  try {
    await axios.post('/api/assistance', {
      application_id: applicationId.value,
      solution: captchaSolution.value
    });
    captchaRequest.value = null;
    captchaSolution.value = '';
    applicationStatus.value = 'Resuming application process...';
    pollApplicationStatus(applicationId.value);
  } catch (err: any) {
    error.value = 'Failed to submit CAPTCHA';
  }
};

// Cancel application process
const cancelApplication = async () => {
  try {
    loading.value = true;
    await axios.post('http://localhost:5000/api/apply/cancel', {}, {
      withCredentials: true
    });
    applicationStatus.value = statusMessages.value.cancelled;
  } catch (err: any) {
    error.value = err.response?.data?.error || 'Failed to cancel application';
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="apply-container">
    <h2>AI Job Application Assistant</h2>

    <form @submit.prevent="handleSubmit" class="apply-form">
      <div class="form-group">
        <label for="job_url">Job Posting URL:</label>
        <input type="url" id="job_url" v-model="jobUrl" required placeholder="https://company.com/careers/job-id"
          pattern="https?://.+" />
        <p class="help-text">
          Our AI will automatically analyze the job requirements and fill the application
          using your profile data.
        </p>
      </div>

      <!-- CAPTCHA Section -->
      <div v-if="captchaRequest" class="captcha-section">
        <h3>Human Verification Required</h3>
        <img :src="captchaRequest.image_url" alt="CAPTCHA" class="captcha-image">
        <input v-model="captchaSolution" placeholder="Enter CAPTCHA text" class="captcha-input" />
        <button @click="submitCaptcha" class="captcha-button">
          Submit Verification
        </button>
      </div>

      <!-- Error Message -->
      <div v-if="error" class="error-message">
        {{ error }}
      </div>

      <!-- Success Message -->
      <div v-if="success" class="success-message">
        {{ success }}
      </div>

      <!-- Application Status Progress -->
      <div class="status-container">
        <div class="status-indicator" :class="applicationStatus.toLowerCase()">
          {{ applicationStatus }}
        </div>
        <div class="progress-bar">
          <div class="progress" :style="{ width: progressWidth }"></div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="button-group">
        <button type="submit" class="submit-button" :disabled="loading">
          {{ loading ? 'Processing...' : 'Start AI Application' }}
        </button>
        <button v-if="applicationStatus && !['completed', 'cancelled'].includes(applicationStatus)"
          @click="cancelApplication" class="cancel-button" :disabled="loading">
          Cancel Application
        </button>
      </div>
    </form>
  </div>
</template>

<style scoped>
.apply-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 2rem;
  background: #f8f9fa;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.apply-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group label {
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #2c3e50;
}

input[type="url"] {
  padding: 0.8rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

input[type="url"]:focus {
  border-color: #42b983;
  outline: none;
}

.help-text {
  font-size: 0.9rem;
  color: #6c757d;
  margin-top: 0.5rem;
}

.captcha-section {
  padding: 1.5rem;
  background: #fff;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
  margin: 1rem 0;
}

.captcha-image {
  margin: 1rem 0;
  border-radius: 6px;
  max-width: 200px;
}

.captcha-input {
  padding: 0.8rem;
  width: 200px;
  margin: 0.5rem 0;
  border: 2px solid #e0e0e0;
  border-radius: 6px;
}

.captcha-button {
  background: #42b983;
  color: white;
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.captcha-button:hover {
  background: #3aa876;
}

.status-container {
  margin: 1.5rem 0;
}

.status-indicator {
  padding: 1rem;
  border-radius: 8px;
  font-weight: 500;
  margin-bottom: 1rem;
}

.status-indicator.processing {
  background: #e3f2fd;
  color: #1976d2;
}

.status-indicator.completed {
  background: #e8f5e9;
  color: #43a047;
}

.status-indicator.failed {
  background: #ffebee;
  color: #e53935;
}

.progress-bar {
  height: 8px;
  background: #f0f0f0;
  border-radius: 4px;
  overflow: hidden;
}

.progress {
  height: 100%;
  background: #42b983;
  transition: width 0.3s ease;
}

.button-group {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

.submit-button {
  background: #42b983;
  color: white;
  padding: 1rem 2rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.3s ease;
}

.submit-button:hover {
  background: #3aa876;
}

.submit-button:disabled {
  background: #a0d9b8;
  cursor: not-allowed;
}

.cancel-button {
  background: #ef476f;
  color: white;
  padding: 1rem 2rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.3s ease;
}

.cancel-button:hover {
  background: #d93a5e;
}

.error-message {
  color: #ef476f;
  padding: 1rem;
  background: #ffebee;
  border-radius: 8px;
  border: 1px solid #ffcdd2;
}

.success-message {
  color: #06d6a0;
  padding: 1rem;
  background: #e8f5e9;
  border-radius: 8px;
  border: 1px solid #c8e6c9;
}
</style>
