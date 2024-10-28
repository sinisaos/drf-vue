<template>
    <div class="container">
        <div class="col-md-8 offset-md-2">
            <h4>Result(s) for tag: "{{ this.$route.params.name }}"</h4>
        </div>
        <br />
        <div
            class="col-md-8 offset-md-2"
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
    </div>
</template>

<script>
import axios from "axios"
import dayjs from "dayjs"
import { defineComponent } from "vue"

export default defineComponent({
    data() {
        return {
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
            axios
                .get(
                    "/api/tags/" +
                        this.$route.params.name +
                        "?page=" +
                        this.currentPage
                )
                .then((res) => {
                    this.questions = res.data.results
                    this.total = res.data.count
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

<style lang="css" scoped>
.btn {
    margin-right: 5px;
}
</style>
