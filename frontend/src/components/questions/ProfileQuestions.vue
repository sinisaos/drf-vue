<template>
    <div class="container">
        <div class="row">
            <div class="col-md-3">
                <div class="list-group">
                    <router-link
                        :to="{ name: 'profile' }"
                        class="list-group-item list-group-item-action"
                        >Profile</router-link
                    >
                    <router-link
                        :to="{ name: 'profileQuestions' }"
                        class="list-group-item list-group-item-action"
                        >Questions</router-link
                    >
                    <router-link
                        :to="{ name: 'profileAnswers' }"
                        class="list-group-item list-group-item-action"
                        >Answers</router-link
                    >
                </div>
                <br />
                <br />
            </div>
            <div class="col-md-9">
                <div class="table-responsive">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>Title</th>
                                <th>Content</th>
                                <th>Created</th>
                                <th>Views</th>
                                <th>Likes</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(item, index) in questions" :key="index">
                                <td>{{ item.title }}</td>
                                <td>
                                    <p>{{ item.content.slice(0, 20) }}...</p>
                                </td>
                                <td>{{ item.created }}</td>
                                <td>{{ item.views }}</td>
                                <td>{{ item.likes }}</td>
                                <td>
                                    <router-link
                                        :to="{
                                            name: 'profileQuestionsEdit',
                                            params: {
                                                id: item.id,
                                                title: item.title,
                                                content: item.content
                                            }
                                        }"
                                        class="btn btn-info"
                                    >
                                        <i class="fa fa-edit"></i>
                                    </router-link>
                                    <button
                                        class="btn btn-danger"
                                        @click="questionDelete(item.id)"
                                    >
                                        <i class="fa fa-trash"></i>
                                    </button>
                                    <br />
                                </td>
                            </tr>
                        </tbody>
                    </table>
                    <br />
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
        </div>
    </div>
</template>

<script>
import axios from "axios"
import { defineComponent } from "vue"
import { mapGetters } from "vuex"

export default defineComponent({
    data() {
        return {
            get token() {
                return localStorage.getItem("token") || 0
            },
            title: "",
            content: "",
            currentPage: 1,
            total: 0,
            questions: [],
            paginate: ["questions"]
        }
    },
    computed: {
        ...mapGetters(["authUser"])
    },
    methods: {
        getQuestions() {
            const token = "Token " + this.token
            axios
                .get(
                    "/api/users/" +
                        this.authUser.id +
                        "/questions?page=" +
                        this.currentPage,
                    { headers: { Authorization: token } }
                )
                .then((res) => {
                    this.questions = res.data.results
                    this.total = res.data.count
                })
                .catch((error) => {
                    console.error(error)
                })
        },
        questionDelete(id) {
            const token = "Token " + this.token
            axios
                .delete("/api/users/" + this.authUser.id + "/questions/" + id, {
                    headers: { Authorization: token }
                })
                .then((res) => {
                    this.questions = res.data.questions
                    this.getQuestions()
                })
                .catch((error) => {
                    console.error(error)
                })
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

.modal-backdrop.show {
    opacity: 0.8;
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
