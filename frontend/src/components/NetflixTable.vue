<template>
  <div>
    <input v-model="search" @input="fetchTitles(1)" placeholder="Search titles..." />

    <table>
      <thead>
        <tr>
          <th @click="sort('show_id')">#</th>
          <th @click="sort('title')">Title</th>
          <th @click="sort('type')">Type</th>
          <th @click="sort('director')">Director</th>
          <th @click="sort('duration')">Duration</th>
          <th @click="sort('release_year')">Release Year</th>
          <th @click="sort('country')">Country</th>
          <th @click="sort('description')">Description</th>
          <th @click="sort('rating')">Rating</th>
          <th @click="sort('date_added')">Date Added</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="title in titles" :key="title.show_id">
          <td>{{ title.show_id }}</td>
          <td>{{ title.title }}</td>
          <td>{{ title.type }}</td>
          <td>{{ title.director }}</td>
          <td>{{ title.duration }}</td>
          <td>{{ title.release_year }}</td>
          <td>{{ title.country }}</td>
          <td>{{ title.description }}</td>
          <td>{{ title.rating }}</td>
          <td>{{ title.date_added }}</td>
        </tr>
      </tbody>
    </table>

    <div>
      <p>
        Showing page {{ currentPage }} of {{ totalPages }} | Total titles: {{ totalCount }}
      </p>
      <label>Items per page:</label>
      <select v-model="pageSize" @change="fetchTitles(1)">
        <option :value="10">10</option>
        <option :value="20">20</option>
        <option :value="50">50</option>
        <option :value="100">100</option>
      </select>
    </div>

    <button :disabled="!previous" @click="fetchTitles(currentPage - 1)">Previous</button>
    <button :disabled="!next" @click="fetchTitles(currentPage + 1)">Next</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      titles: [],
      search: '',
      pageSize: 10,
      currentPage: 1,
      previous: null,
      next: null,
      totalCount: 0,
      totalPages: 0,
      sortField: 'title',
      sortDirection: 'asc',
    };
  },
  methods: {
    async fetchTitles(page = 1) {
      const params = {
        search: this.search,
        page: page,
        page_size: this.pageSize,
        ordering: `${this.sortDirection === 'asc' ? '' : '-'}${this.sortField}`,
      };
      try {
        const response = await axios.get('http://localhost:8000/api/titles/', { params });
        this.titles = response.data.results;
        this.previous = response.data.previous;
        this.next = response.data.next;
        this.currentPage = page;
        this.totalCount = response.data.count; // Total number of items
        this.totalPages = Math.ceil(this.totalCount / this.pageSize); // Calculate total pages
      } catch (error) {
        console.error('Error fetching titles:', error);
      }
    },
    sort(field) {
      this.sortField = field;
      this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
      this.fetchTitles();
    },
  },
  mounted() {
    this.fetchTitles();
  },
};
</script>

<style>
table {
  width: 100%;
  border-collapse: collapse;
}
th {
  cursor: pointer;
}
th, td {
  padding: 10px;
  border: 1px solid #ddd;
}
</style>