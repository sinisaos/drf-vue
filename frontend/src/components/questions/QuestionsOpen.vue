<template>
    <div class="container">
        <div class="col-md-8 offset-md-2" v-if="empty">
            <div class="form-group">
                <input
                    type="text"
                    class="form-control"
                    v-model="query"
                    @keyup.enter="getQuestions"
                    placeholder="Search questions"
                />
                <i class="fa fa-search errspan" aria-hidden="true"></i>
            </div>
        </div>
        <div class="col-md-8 offset-md-2" v-if="questions.length !== 0">
            <button class="btn btn-link">
                <router-link :to="{ name: 'questions' }">Newest</router-link>
            </button>
            <button class="btn btn-link" @click="getQuestions">Open</button>
            <button class="btn btn-link">
                <router-link :to="{ name: 'questionsSolved' }"
                    >Solved</router-link
                >
            </button>
            <button class="btn btn-link" @click="sortOldest">Oldest</button>
            <button class="btn btn-link" @click="sortMostViewed">Viewed</button>
            <button class="btn btn-link" @click="sortMostLiked">Popular</button>
        </div>
        <br />
        <div class="col-md-8 offset-md-2" v-if="questions.length !== 0">
            <div
                class="col-md-12"
                v-for="(item, index) in questions"
                :key="index"
            >
                <h4>
                    <router-link
                        :to="{
                            name: 'question',
                            params: { id: item.id, slug: item.slug }
                        }"
                    >
                        <b>{{ item.title }}</b>
                    </router-link>
                </h4>
                <span>
                    asked on
                    <i>{{ formatDate(item.created) }}</i> by
                    <b>{{ item.question_author }}</b>
                    <b></b>
                </span>
                <hr />
                <p class="mb-1">{{ item.content }}</p>
                <br />
                <div
                    class="btn-group"
                    v-for="(tag, idx) in item.tags"
                    :key="idx"
                >
                    <router-link
                        :to="{ name: 'questionsByTag', params: { name: tag } }"
                        class="btn btn-primary"
                        >{{ tag }}</router-link
                    >
                </div>
                <br />
                <br />
                <span
                    v-if="item.get_accepted_answer"
                    class="badge badge-badge-pill-lg badge-success float-right"
                    style="float: right"
                    >Solved</span
                >
                <span v-else>
                    <i
                        class="fa fa-exclamation-circle"
                        aria-hidden="true"
                        style="color: red; float: right"
                        >&ensp;Unanswered</i
                    >&ensp;
                </span>
                <i class="fa fa-eye" aria-hidden="true" title="Views"
                    >&ensp;{{ item.views }}</i
                >&ensp;
                <i class="fa fa-comment" aria-hidden="true" title="Answers"
                    >&ensp;{{ item.get_answer_count }}</i
                >&ensp;
                <i class="fa fa-thumbs-up" aria-hidden="true" title="Likes"
                    >&ensp;{{ item.likes }}</i
                >
                &ensp;
                <br />
                <hr />
            </div>
            <div class="col-md-12" v-if="orderingId">
                <b-pagination
                    size="sm"
                    :total-rows="total"
                    align="right"
                    first-number
                    last-number
                    v-model="currentPage"
                    :per-page="3"
                    @input="sortOldest(currentPage)"
                ></b-pagination>
            </div>
            <div class="col-md-12" v-else-if="orderingViews">
                <b-pagination
                    size="sm"
                    :total-rows="total"
                    align="right"
                    first-number
                    last-number
                    v-model="currentPage"
                    :per-page="3"
                    @input="sortMostViewed(currentPage)"
                ></b-pagination>
            </div>
            <div class="col-md-12" v-else-if="orderingLikes">
                <b-pagination
                    size="sm"
                    :total-rows="total"
                    align="right"
                    first-number
                    last-number
                    v-model="currentPage"
                    :per-page="3"
                    @input="sortMostLiked(currentPage)"
                ></b-pagination>
            </div>
            <div class="col-md-12" v-else>
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
        </div>
        <div class="col-md-8 offset-md-2" v-else>
            <h3>No results.</h3>
        </div>
    </div>
</template>

<script>
import axios from "axios"
import dayjs from "dayjs"
import { defineComponent } from "vue"

export default defineComponent({
    data() {
        return {
            empty: true,
            query: null,
            orderingId: false,
            orderingViews: false,
            orderingLikes: false,
            currentPage: 1,
            total: 0,
            questions: []
        }
    },

    methods: {
        formatDate(dateString) {
            const date = dayjs(dateString)
            return date.format("dddd MMMM D, YYYY")
        },
        getQuestions() {
            if (!this.query) {
                axios
                    .get("/api/open?page=" + this.currentPage)
                    .then((res) => {
                        this.questions = res.data.results
                        this.total = res.data.count
                        this.orderingId = false
                        this.orderingViews = false
                        this.orderingLikes = false
                    })
                    .catch((error) => {
                        console.error(error)
                    })
            } else {
                axios
                    .get(
                        "/api/open?search=" +
                            this.query +
                            "&page=" +
                            this.currentPage
                    )
                    .then((res) => {
                        this.questions = res.data.results
                        this.total = res.data.count
                        this.orderingId = false
                        this.orderingViews = false
                        this.orderingLikes = false
                    })
                    .catch((error) => {
                        this.questions = []
                        console.log(error.response.data)
                    })
            }
        },
        sortOldest() {
            if (!this.query) {
                axios
                    .get("/api/open?ordering=id&page=" + this.currentPage)
                    .then((res) => {
                        this.questions = res.data.results
                        this.total = res.data.count
                        this.orderingId = true
                        this.orderingViews = false
                        this.orderingLikes = false
                    })
                    .catch((error) => {
                        console.error(error)
                    })
            } else {
                axios
                    .get(
                        "/api/open?ordering=id&page=" +
                            this.currentPage +
                            "&search=" +
                            this.query
                    )
                    .then((res) => {
                        this.questions = res.data.results
                        this.total = res.data.count
                        this.orderingId = true
                        this.orderingViews = false
                        this.orderingLikes = false
                    })
                    .catch((error) => {
                        this.questions = []
                        console.log(error.response.data)
                    })
            }
        },
        sortMostViewed() {
            if (!this.query) {
                axios
                    .get("/api/open?ordering=-views&page=" + this.currentPage)
                    .then((res) => {
                        this.questions = res.data.results
                        this.total = res.data.count
                        this.orderingId = false
                        this.orderingViews = true
                        this.orderingLikes = false
                    })
                    .catch((error) => {
                        console.error(error)
                    })
            } else {
                axios
                    .get(
                        "/api/open?ordering=-views&page=" +
                            this.currentPage +
                            "&search=" +
                            this.query
                    )
                    .then((res) => {
                        this.questions = res.data.results
                        this.total = res.data.count
                        this.orderingId = false
                        this.orderingViews = true
                        this.orderingLikes = false
                    })
                    .catch((error) => {
                        this.questions = []
                        console.log(error.response.data)
                    })
            }
        },
        sortMostLiked() {
            if (!this.query) {
                axios
                    .get("/api/open?ordering=-likes&page=" + this.currentPage)
                    .then((res) => {
                        this.questions = res.data.results
                        this.total = res.data.count
                        this.orderingId = false
                        this.orderingViews = false
                        this.orderingLikes = true
                    })
                    .catch((error) => {
                        console.error(error)
                    })
            } else {
                axios
                    .get(
                        "/api/open?ordering=-likes&page=" +
                            this.currentPage +
                            "&search=" +
                            this.query
                    )
                    .then((res) => {
                        this.questions = res.data.results
                        this.total = res.data.count
                        this.orderingId = false
                        this.orderingViews = false
                        this.orderingLikes = true
                    })
                    .catch((error) => {
                        this.questions = []
                        console.log(error.response.data)
                    })
            }
        }
    },
    created() {
        this.getQuestions()
    }
})
</script>

<style lang="css">
.btn {
    margin-right: 5px;
}

.errspan {
    float: right;
    margin-right: 12px;
    margin-top: -27px;
    position: relative;
    z-index: 2;
}

ul {
    list-style-type: none;
    padding: 0;
    cursor: pointer;
    border: 1px black;
}
</style>
