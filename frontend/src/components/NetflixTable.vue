<template>
  <div class="container">
    <div class="search-container">
      <select v-model="searchProvider" class="search-select" @change="fetchTitles(1)">
        <option value="django">Django</option>
        <option value="algolia">Algolia</option>
        <option value="elasticsearch">Elasticsearch</option>
      </select>

      <input v-model="search" @input="fetchTitles(1)" placeholder="Search titles..." class="search-input" />
    </div>

    <!-- Table -->
    <table class="styled-table">
      <thead>
        <tr>
          <th @click="sort('title')">Title</th>
          <th @click="sort('release_year')">Release Year</th>
          <th @click="sort('type')">Type</th>
          <th @click="sort('duration')">Duration</th>
          <th @click="sort('director')">Director</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="title in titles" :key="title.show_id" @click="goToDetail(title.show_id)" class="clickable-row">
          <td>{{ title.title }}</td>
          <td>{{ title.release_year }}</td>
          <td>{{ title.type }}</td>
          <td>{{ title.duration || '-' }}</td>
          <td>{{ title.director || '-' }}</td>
        </tr>
      </tbody>
    </table>

    <!-- Pagination Controls -->
    <div class="pagination-container">
      <p>
        Showing page {{ currentPage }} of {{ totalPages }} | Total titles: {{ totalCount }}
      </p>
      <div>

      <label>Items per page:  </label>
      <select v-model="pageSize" @change="fetchTitles(1)" class="page-size-selector">
        <option :value="10">10</option>
        <option :value="20">20</option>
        <option :value="50">50</option>
        <option :value="100">100</option>
      </select>
      </div>
    </div>

    <div class="button-container">
      <button :disabled="!previous" @click="fetchTitles(currentPage - 1)" class="pagination-btn">Previous</button>
      <button :disabled="!next" @click="fetchTitles(currentPage + 1)" class="pagination-btn">Next</button>
    </div>
  </div>
</template>


<script>
import axios from 'axios';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const router = useRouter();

    const goToDetail = (show_id) => {
      router.push(`/${show_id}`);
    };

    return { goToDetail };
  },
  data() {
    return {
      titles: [],
      search: '',
      searchProvider: 'django',
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
      const host = 'http://localhost:8888';
      let path;
      switch (this.searchProvider) {
        case 'algolia':
          path = '/api/search/algolia/';
          break;
        case 'elasticsearch':
          path = '/api/search/elasticsearch/';
          break;
        default:
          path = '/api/titles/'; // Default to Django
      }

      const params = {
        search: this.search,
        page: page,
        page_size: this.pageSize,
        // ordering: `${this.sortDirection === 'asc' ? '' : '-'}${this.sortField}`, // Temporary disabled because of Algolia
      };

      try {
        const response = await axios.get(host + path, { params });
        this.titles = response.data.results;
        this.previous = response.data.previous;
        this.next = response.data.next;
        this.currentPage = page;
        this.totalCount = response.data.count;
        this.totalPages = Math.ceil(this.totalCount / this.pageSize);
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
/* Netflix Color Theme */
:root {
  --netflix-red: #E50914;
  --netflix-black: #141414;
  --dark-gray: #222;
  --light-gray: #b3b3b3;
  --white: #ffffff;
}

/* General Styles */
.container {
  width: 90%;
  max-width: 1200px;
  margin: 20px auto;
  font-family: Arial, sans-serif;
  color: var(--white);
  background: var(--netflix-black);
  padding: 20px;
  border-radius: 10px;
}

/* Search Container */
.search-container {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

/* Search Select (Dropdown) */
.search-select {
  background-color: #e50914; /* Netflix red */
  color: white;
  border: none;
  padding: 10px;
  font-size: 16px;
  margin-right: 10px;
  cursor: pointer;
  border-radius: 4px;
}

.search-select option {
  background: black;
  color: white;
}

/* Search Input */
.search-input {
  flex-grow: 1;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #e50914;
  border-radius: 4px;
  background-color: #333;
  color: white;
}

/* Search Bar */
.search-input {
  width: 100%;
  padding: 10px;
  border: 2px solid var(--netflix-red);
  border-radius: 5px;
  font-size: 16px;
  background: var(--dark-gray);
  color: var(--white);
  outline: none;
  transition: 0.3s;
}

.search-input:focus {
  border-color: var(--white);
  box-shadow: 0 0 5px var(--netflix-red);
}

/* Table Styles */
.styled-table {
  width: 100%;
  border-collapse: collapse;
  background: var(--dark-gray);
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 0 10px rgba(255, 0, 0, 0.3);
}

.styled-table th, .styled-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid var(--netflix-black);
}

.styled-table th {
  background: var(--netflix-red);
  color: var(--white);
  cursor: pointer;
  transition: 0.3s;
}

.styled-table th:hover {
  background: #b20710;
}

.styled-table tbody tr:nth-child(even) {
  background: #181818;
}

.styled-table tbody tr:hover {
  background: #222;
}

.clickable-row {
  cursor: pointer;
  transition: 0.2s;
}

.clickable-row:hover {
  background: #b20710;
  color: white;
}

/* Truncate long descriptions */
.truncate {
  max-width: 250px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Pagination Controls */
.pagination-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 15px 0;
  font-size: 14px;
}

.page-size-selector {
  padding: 5px;
  border-radius: 5px;
  border: 1px solid var(--netflix-red);
  background: var(--dark-gray);
  color: var(--white);
}

/* Pagination Buttons */
.button-container {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-top: 10px;
}

.pagination-btn {
  background: var(--netflix-red);
  color: var(--white);
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  transition: 0.3s;
}

.pagination-btn:hover {
  background: #b20710;
}

.pagination-btn:disabled {
  background: #444;
  cursor: not-allowed;
}
</style>