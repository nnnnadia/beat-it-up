<template>
  <div class="container">
    <h1>OCR Table Extractor</h1>
    <form @submit.prevent="onSubmit">
      <input type="file" @change="onFileChange" accept="image/*" />
      <button type="submit" :disabled="!selectedFile || loading">Upload</button>
    </form>
    <div v-if="selectedFile">
      <p>Selected file: {{ selectedFile.name }}</p>
    </div>
    <div v-if="ocrResult">
      <h2>OCR Result</h2>
      <pre>{{ ocrResult }}</pre>
    </div>
    <div v-if="error" class="error">
      <p>{{ error }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const selectedFile = ref(null)
const ocrResult = ref('')
const error = ref('')
const loading = ref(false)

// API URL switch: use localhost for dev, backend API for prod
const API_URL = import.meta.env.MODE === 'production'
     ? 'https://beat-it-up-yqv1.onrender.com/ocr'
     : 'http://localhost:8000/ocr'

function onFileChange(event) {
  selectedFile.value = event.target.files[0]
}

async function onSubmit() {
  if (!selectedFile.value) return;
  ocrResult.value = ''
  error.value = ''
  loading.value = true
  const formData = new FormData();
  formData.append('file', selectedFile.value);
  try {
    const response = await fetch(API_URL, {
      method: 'POST',
      body: formData,
    });
    if (!response.ok) throw new Error('Failed to get OCR result');
    const data = await response.json();
    ocrResult.value = data.text;
  } catch (err) {
    error.value = 'Error uploading file: ' + err.message;
  } finally {
    loading.value = false;
  }
}
</script>

<style>
.container {
  max-width: 500px;
  margin: 2rem auto;
  padding: 2rem;
  border: 1px solid #eee;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  background: #fff;
}
h1 {
  text-align: center;
  margin-bottom: 1.5rem;
}
form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
button {
  padding: 0.5rem 1rem;
  border: none;
  background: #42b983;
  color: #fff;
  border-radius: 4px;
  cursor: pointer;
}
button:disabled {
  background: #ccc;
  cursor: not-allowed;
}
pre {
  background: #f4f4f4;
  padding: 1rem;
  border-radius: 4px;
  white-space: pre-wrap;
  word-break: break-word;
}
.error {
  color: #c00;
  margin-top: 1rem;
}
</style>
