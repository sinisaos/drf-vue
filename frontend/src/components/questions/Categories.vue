<template>
    <div class="container">
        <div class="col-md-8 offset-md-2">
            <div class="btn-group" v-for="(tag, idx) in tags" :key="idx">
                <router-link
                    :to="{ name: 'questionsByTag', params: { name: tag.name } }"
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
            <loading
                :active="isLoading"
                :can-cancel="true"
                :on-cancel="onCancel"
                :is-full-page="fullPage"
            ></loading>
        </div>
    </div>
</template>

<script>
import axios from "axios"
import { defineComponent } from "vue"

export default defineComponent({
    // setup() {
    //     const isLoading = ref(false)
    //     const fullPage = ref(true)
    // },
    data() {
        return {
            isLoading: true,
            fullPage: true,
            tags: []
        }
    },
    methods: {
        getTags() {
            axios
                .get("/api/categories")
                .then((res) => {
                    this.tags = res.data
                    this.isLoading = false
                })
                .catch((error) => {
                    console.error(error)
                    this.isLoading = false
                })
        }
    },
    created() {
        this.getTags()
    }
})
</script>

