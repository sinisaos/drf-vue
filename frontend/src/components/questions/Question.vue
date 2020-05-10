<template>
  <div class="container">
    <div class="col-md-8 offset-md-2">
      <h4>
        <div class="vld-parent">
          <loading :active.sync="isLoading" :is-full-page="fullPage" :opacity="1"></loading>
        </div>
        <b>{{ question.title }}</b>
      </h4>
      <span>
        asked on
        <i>{{ question.created | dateFormat }}</i> by
        <b>{{ question.question_author }}</b>
        <b></b>
      </span>
      <hr />
      <p class="mb-1">{{ question.content }}</p>
      <br />
      <div class="btn-group" v-for="(tag,idx) in question.tags" :key="idx">
        <router-link
          :to="{ name: 'questionsByTag', params: { name: tag }}"
          tag="button"
          class="btn btn-primary"
        >{{ tag }}</router-link>
      </div>
      <router-link
        v-if="!isLoggedIn"
        to="/login"
        class="float-right"
        style="color:#33cc33;cursor:pointer;"
      >
        <i
          class="fa fa-thumbs-up"
          aria-hidden="true"
          title="Question likes"
        >&ensp;{{ question.likes }}&ensp;</i>
      </router-link>
      <form
        method="POST"
        v-else
        @click="questionLike(question.id, question.likes)"
        class="float-right"
        style="color:#33cc33; cursor:pointer;"
      >
        <i class="fa fa-thumbs-up" aria-hidden="true" title="Question likes"></i>
        &ensp;{{ question.likes }}&ensp;
      </form>
      <br />
      <hr />
    </div>
    <div class="col-md-8 offset-md-2">
      <span v-if="!isLoggedIn">*Must be logged in to post answer</span>
      <b-form @submit.prevent="createAnswer" v-else class="w-100">
        <div class="form-group">
          <b-form-textarea
            id="content"
            v-model="content"
            name="content"
            class="form-control"
            placeholder="Answer..."
            rows="5"
            max-rows="10"
            :class="{ 'is-invalid': $v.content.$error }"
          ></b-form-textarea>
          <div v-if="$v.content.$error" class="invalid-feedback">
            <span v-if="!$v.content.required">Content is required</span>
          </div>
        </div>
        <div class="form-group">
          <button class="btn btn-primary">Submit</button>
        </div>
      </b-form>
      <br />
      <br />
      <h3 class="float-left">{{ question.get_answer_count }} answer(s)</h3>
      <br />
      <hr />
      <h6 v-for="(item, index) in question.answers" :key="index">
        <span>
          Answered on
          <i>{{ item.created | dateFormat }}</i> by
          <b>{{ item.answer_author }}</b>
          <br />
          <br />
        </span>
        <p class="mb-1">{{ item.content }}</p>
        <br />
        <router-link
          v-if="!isLoggedIn"
          to="/login"
          class="float-right"
          style="color:#33cc33; cursor:pointer;"
        >
          <i
            class="fa fa-thumbs-up"
            aria-hidden="true"
            title="Answer likes"
          >&ensp;{{ item.likes }}&ensp;</i>
        </router-link>
        <form
          v-else
          @click="answerLike(item.id, item.likes)"
          class="float-right"
          style="color:#33cc33; cursor:pointer;"
        >
          <i class="fa fa-thumbs-up" aria-hidden="true" title="Answer likes"></i>
          &ensp;{{ item.likes }}&ensp;
        </form>
        <div>
          <div
            v-if="authUser.username == question.question_author && question.get_accepted_answer === null && item.is_accepted === false"
          >
            <form
              @click="answerAccept(item.id, item.is_accepted)"
              class="btn btn-success float-left"
            >
              Accept
              Answer
            </form>
            <br />
          </div>
          <div v-else-if="question.question_author == authUser.username && item.is_accepted == 1">
            <span class="badge badge-badge-pill badge-success float-left">Accepted answer</span>
          </div>
          <div v-else-if="item.is_accepted == 1">
            <span class="badge badge-badge-pill badge-success float-left">Accepted answer</span>
          </div>
          <div v-else></div>
        </div>
        <br />
        <hr />
      </h6>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { mapGetters } from "vuex";
import { required } from "vuelidate/lib/validators";
// Import component
import Loading from "vue-loading-overlay";
// Import stylesheet
import "vue-loading-overlay/dist/vue-loading.css";

export default {
  data() {
    return {
      isLoading: true,
      fullPage: true,
      content: "",
      question: {},
      get token() {
        return localStorage.getItem("token") || 0;
      }
    };
  },
  components: {
    Loading
  },
  validations: {
    content: { required }
  },
  filters: {
    dateFormat: function(value) {
      let date = new Date(value);
      return date.toString().slice(4, 24);
    }
  },
  methods: {
    getQuestion() {
      axios
        .get("/api/questions/" + this.$route.params.id)
        .then(res => {
          this.question = res.data;
          this.isLoading = false;
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    createAnswer() {
      let data = {
        user: this.authUser.id,
        content: this.content,
        question: this.question.id
      };
      this.$v.$touch();
      if (this.$v.$invalid) {
        return;
      }
      axios
        .post("/api/answers", data)
        .then(res => {
          this.getQuestion();
          this.data = res.data;
          this.$router.push(
            "/questions/" +
              this.$route.params.id +
              "/" +
              this.$route.params.slug
          );
        })
        .catch(err => {
          this.message = err.response.data;
          this.showMessage = true;
          this.showDismissibleAlert = true;
        });
    },
    questionLike(id, likes) {
      let data = {
        likes: likes + 1
      };
      axios.patch("/api/questions/" + id, data).then(res => {
        this.data = res.data;
        this.getQuestion();
      });
    },
    answerLike(id, likes, has_accepted_answer) {
      let data = {
        likes: likes + 1,
        has_accepted_answer: has_accepted_answer + 1
      };
      axios.patch("/api/answers/" + id, data).then(res => {
        this.data = res.data;
        this.getQuestion();
      });
    },
    answerAccept(id, is_accepted) {
      let data = {
        is_accepted: is_accepted + 1
      };
      axios.patch("/api/answers/" + id, data).then(res => {
        this.data = res.data;
        this.getQuestion();
      });
    }
  },
  computed: {
    ...mapGetters(["isLoggedIn", "authUser"])
  },
  created() {
    this.getQuestion();
  }
};
</script>

<style lang="css" scoped>
.btn {
  margin-right: 5px;
}
</style>
