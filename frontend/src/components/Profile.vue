<template>
    <div class="profile-container">
        <h2>Profile</h2>
        <form @submit.prevent="saveProfile">
            <input v-model="fullName" type="text" placeholder="Full Name" required />
            <input v-model="email" type="email" placeholder="Email" required />
            <textarea v-model="address" placeholder="Address" required></textarea>
            <input v-model="phoneNumber" type="text" placeholder="Phone Number" required />
            <input type="file" @change="handleFileUpload" />
            <button type="submit">Save Profile</button>
        </form>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

export default defineComponent({
    name: 'Profile',
    setup() {
        const router = useRouter();
        const fullName = ref('');
        const email = ref('');
        const address = ref('');
        const phoneNumber = ref('');
        const resume = ref<File | null>(null);

        const handleFileUpload = (event: Event) => {
            const input = event.target as HTMLInputElement;
            if (input?.files?.length) {
                resume.value = input.files[0];
            }
        };

        const saveProfile = async () => {
            const formData = new FormData();
            formData.append("full_name", fullName.value);
            formData.append("email", email.value);
            formData.append("address", address.value);
            formData.append("phone_number", phoneNumber.value);
            if (resume.value) {
                formData.append("resume", resume.value);
            }

            try {
                await axios.post("http://localhost:5000/profile", formData, {
                    headers: { "Content-Type": "multipart/form-data" }
                });
                router.push('/apply');
            } catch (error) {
                console.error('Error saving profile:', error);
            }
        };

        return {
            fullName,
            email,
            address,
            phoneNumber,
            resume,
            handleFileUpload,
            saveProfile
        };
    }
});
</script>

<style scoped>
.profile-container {
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
    text-align: center;
    border-radius: 8px;
    background-color: #f7f7f7;
}

input,
textarea {
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
    background-color: #28a745;
    color: white;
    border: none;
}
</style>
