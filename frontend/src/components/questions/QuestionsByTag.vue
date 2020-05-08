<template>
  <div class="container">
    <div class="col-md-8 offset-md-2">
      <h4>Result(s) for tag: "{{ this.$route.params.name }}"</h4>
    </div>
    <br />
    <div class="col-md-8 offset-md-2" v-for="(item, index) in questions" :key="index">
      <h4>
        <router-link :to="{ name: 'question', params: { id: item.id, slug: item.slug }}">
          <b>{{ item.title }}</b>
        </router-link>
      </h4>
      <span>
        asked on
        <i>{{ item.created | dateFormat }}</i> by
        <b>{{ item.question_author }}</b>
        <b></b>
      </span>
      <hr />
    </div>
    <div class="col-md-8 offset-md-2">
      <b-pagination
        size="sm"
        :total-rows="total"
        align="right"
        first-number
        last-number
        v-model="currentPage"
        :per-page="3"
        @input="getQuestions(currentPage)"
      ></b-pagination>
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
      currentPage: 1,
      total: 0,
      questions: []
    };
  },
  components: {
    Loading
  },
  filters: {
    dateFormat: function(value) {
      let date = new Date(value);
      return date.toString().slice(4, 24);
    }
  },
  methods: {
    getQuestions() {
      axios
        .get(
          "/api/tags/" + this.$route.params.name + "?page=" + this.currentPage
        )
        .then(res => {
          this.questions = res.data.results;
          this.total = res.data.count;
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
    this.getQuestions();
  }
};
</script>

<style lang="css" scoped>
.btn {
  margin-right: 5px;
}
</style>
