<template>
  <div class="container">
    <div class="col-md-8 offset-md-2">
      <div class="btn-group" v-for="(tag,idx) in tags" :key="idx">
        <router-link
          :to="{ name: 'questionsByTag', params: { name: tag.name }}"
          tag="button"
          class="btn btn-primary"
        >
          <b>
            {{ tag.name }}
            ({{ tag.count_tags }})
          </b>
        </router-link>
      </div>
    </div>
    <div class="vld-parent">
      <loading :active.sync="isLoading" :is-full-page="fullPage" :opacity="1"></loading>
    </div>
  </div>
</template>

<script>
import axios from "axios";
// Import component
import Loading from "vue-loading-overlay";
// Import stylesheet
import "vue-loading-overlay/dist/vue-loading.css";

export default {
  data() {
    return {
      isLoading: true,
      fullPage: true,
      tags: []
    };
  },
  components: {
    Loading
  },
  methods: {
    getTags() {
      axios
        .get("/api/categories")
        .then(res => {
          this.tags = res.data;
          this.isLoading = false;
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
          this.isLoading = false;
        });
    }
  },
  created() {
    this.getTags();
  }
};
</script>

<style lang="css">
.btn {
  margin: 5px 5px;
}
</style>