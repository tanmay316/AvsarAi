<template>
    <div class="register-container">
        <h2>Register</h2>
        <form @submit.prevent="registerUser">
            <input v-model="username" type="text" placeholder="Username" required />
            <input v-model="email" type="email" placeholder="Email" required />
            <input v-model="password" type="password" placeholder="Password" required />
            <button type="submit">Register</button>
        </form>
        <p>Already have an account? <router-link to="/login">Login here</router-link></p>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import axios from 'axios';
import router from '../router';

export default defineComponent({
    name: 'Register',
    setup() {
        const username = ref('');
        const email = ref('');
        const password = ref('');

        const registerUser = async () => {
            try {
                const response = await axios.post('http://localhost:5000/register', {
                    username: username.value,
                    email: email.value,
                    password: password.value
                });
                console.log(response);
                // Navigate to profile after successful registration
                router.push('/profile');
            } catch (error) {
                console.error('Registration failed:', error);
            }
        };

        return {
            username,
            email,
            password,
            registerUser
        };
    }
});
</script>

<style scoped>
.register-container {
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
    text-align: center;
    border-radius: 8px;
    background-color: #f7f7f7;
}

input {
    width: 100%;
    padding: 10px;
    margin: 10px 0;
    border-radius: 5px;
    border: 1px solid #ddd;
}

button {
    width: 100%;
    padding: 10px;
    border-radius: 5px;
    background-color: #007BFF;
    color: white;
    border: none;
}

p {
    margin-top: 15px;
}
</style>
