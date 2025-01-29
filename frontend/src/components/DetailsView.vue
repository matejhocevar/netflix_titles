<template>
  <div class="detail-container">
    <button @click="$router.go(-1)" class="back-button">⬅ Back</button>
    <h1>{{ title.title }}</h1>
    <p><strong>Type:</strong> {{ title.type }}</p>
    <p><strong>Director:</strong> {{ title.director || '-' }}</p>
    <p><strong>Cast:</strong> {{ title.cast || '-' }}</p>
    <p><strong>Country:</strong> {{ title.country || '-' }}</p>
    <p><strong>Release Year:</strong> {{ title.release_year }}</p>
    <p><strong>Rating:</strong> {{ title.rating || '-' }}</p>
    <p><strong>Duration:</strong> {{ title.duration || '-' }}</p>
    <p><strong>Description:</strong> {{ title.description }}</p>
    <p><strong>Date Added:</strong> {{ title.date_added || '-' }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: ['show_id'],
  data() {
    return {
      title: {},
    };
  },
  async mounted() {
    try {
      const response = await axios.get(`http://localhost:8888/api/titles/${this.show_id}/`);
      this.title = response.data;
    } catch (error) {
      console.error('Error fetching title details:', error);
    }
  },
};
</script>

<style>
.detail-container {
  max-width: 600px;
  margin: 40px auto;
  padding: 20px;
  background: #141414;
  color: white;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(255, 0, 0, 0.5);
  text-align: left;
}

h1 {
  color: #e50914;
}

.back-button {
  background: #e50914;
  color: white;
  padding: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.back-button:hover {
  background: #b20710;
}
</style>