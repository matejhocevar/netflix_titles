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

    <div class="content-wrapper">
      <!-- Filters Sidebar -->
      <div class="filters-container">
        <h3>Filters</h3>

        <!-- Type Filter -->
        <div class="filter-group">
          <label>Type:</label>
          <select v-model="filters.type" multiple @change="fetchTitles(1)" class="filter-select">
            <option value="">All</option>
            <option v-for="type in availableTypes" :key="type" :value="type">
              {{ type }}
            </option>
          </select>
        </div>

        <!-- Release Year Filter -->
        <div class="filter-group">
          <label>Release Year:</label>
          <div class="filters-inline">

          <input type="number" v-model="filters.releaseYearMin" placeholder="Min Year" @input="fetchTitles(1)" class="filter-input" />
          <input type="number" v-model="filters.releaseYearMax" placeholder="Max Year" @input="fetchTitles(1)" class="filter-input" />
          </div>
        </div>

        <!-- Country Filter -->
        <div class="filter-group">
          <label>Country:</label>
          <select v-model="filters.country" multiple @change="fetchTitles(1)" class="filter-select">
            <option value="">All</option>
            <option v-for="country in availableCountries" :key="country" :value="country">
              {{ country }}
            </option>
          </select>
        </div>

        <!-- Rating Filter -->
        <div class="filter-group">
          <label>Rating:</label>
          <select v-model="filters.rating" multiple @change="fetchTitles(1)" class="filter-select">
            <option value="">All</option>
            <option v-for="rating in availableRatings" :key="rating" :value="rating">
              {{ rating }}
            </option>
          </select>
        </div>

        <!-- Duration Filter -->
        <div class="filter-group">
          <label>Duration:</label>
          <select v-model="filters.duration" @change="fetchTitles(1)" class="filter-select">
            <option value="">All</option>
            <option value="short">Less than 60 min</option>
            <option value="medium">60-120 min</option>
            <option value="long">More than 120 min</option>
            <option value="1 Season">1 Season</option>
            <option value="2 Seasons">2 Seasons</option>
            <option value="3 Seasons">3 Seasons</option>
            <option value="4 Seasons">4 Seasons</option>
            <option value="5 Seasons">5 Seasons</option>
            <option value="5/ Seasons">5+ Seasons</option>
          </select>
        </div>
      </div>

      <!-- Main Content -->
      <div class="content-container">
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
            <tr v-for="title in titles" :key="title.show_id" @click="goToDetail(host, searchProvider, title.show_id)" class="clickable-row">
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
            <label>Items per page:</label>
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
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const router = useRouter();

    const goToDetail = (host, searchProvider, show_id) => {
      router.push(`/api/${searchProvider}/${show_id}`);
    };

    return { goToDetail };
  },
  data() {
    return {
      host: 'http://localhost:8888/api',
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
      filters: {
        type: [],
        releaseYearMin: '',
        releaseYearMax: '',
        country: [],
        rating: [],
      },
      availableCountries: [],
      availableRatings: [],
      availableTypes: [],
    };
  },
  methods: {
    async fetchTitles(page = 1) {
      const params = {
        search: this.search,
        page: page,
        page_size: this.pageSize,
        ordering: `${this.sortDirection === 'asc' ? '' : '-'}${this.sortField}`,
        // type: this.filters.type.length ? this.filters.type.join(',') : undefined,  // Temporarily disabled due to Algolia index definition issue
        release_year_gte: this.filters.releaseYearMin || undefined,
        release_year_lte: this.filters.releaseYearMax || undefined,
        country: this.filters.country.length ? this.filters.country.join(',') : undefined,
        rating: this.filters.rating.length ? this.filters.rating.join(',') : undefined,
      };

      try {
        const response = await axios.get(`${this.host}/${this.searchProvider}/`, {params});
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
    async fetchFilters() {
      // Fetch available filters dynamically
      try {
        const response = await axios.get(`${this.host}/${this.searchProvider}/filters/`);
        this.availableCountries = response.data.countries;
        this.availableRatings = response.data.ratings;
        this.availableTypes = response.data.types;
      } catch (error) {
        console.error('Error fetching filter options:', error);
      }
    },
  },
  mounted() {
    this.fetchTitles();
    this.fetchFilters();
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

.content-wrapper {
  display: flex;
  gap: 20px;
}

/* Filters Sidebar */
.filters-container {
  flex: 1;
  padding: 15px;
  background: var(--dark-gray);
  border-radius: 10px;
}

.filters-inline {
  display: flex;
}

.filter-select,
.filter-input {
  width: 100%;
  margin-bottom: 10px;
  padding: 8px;
  border-radius: 5px;
  border: 1px solid var(--netflix-red);
  background: var(--dark-gray);
  color: var(--white);
}

.filter-group select[multiple] {
  height: 80px;
}

.content-container {
  flex: 4;
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