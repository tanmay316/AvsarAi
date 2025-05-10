<template>
    <div class="login-container">
        <h2>Login</h2>
        <form @submit.prevent="loginUser">
            <input v-model="email" type="email" placeholder="Email" required />
            <input v-model="password" type="password" placeholder="Password" required />
            <button type="submit">Login</button>
        </form>
        <p>Don't have an account? <router-link to="/register">Register here</router-link></p>
    </div>
</template>

<script lang="ts">
import axios from 'axios';
import { defineComponent, ref } from 'vue';
import { useRouter } from 'vue-router';

export default defineComponent({
    name: 'Login',
    setup() {
        const router = useRouter();
        const email = ref('');
        const password = ref('');

        const loginUser = async () => {
            try {
                const response = await axios.post('http://localhost:5000/login', {
                    email: email.value,
                    password: password.value
                });
                console.log(response);
                // Navigate to the profile page after login
                router.push('/profile');
            } catch (error) {
                console.error('Login failed:', error);
            }
        };

        return {
            email,
            password,
            loginUser
        };
    }
});
</script>

<style scoped>
.login-container {
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
