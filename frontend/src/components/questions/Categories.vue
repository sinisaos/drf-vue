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
    </div>
</template>

<script>
import axios from "axios"
import { defineComponent } from "vue"

export default defineComponent({
    data() {
        return {
            tags: []
        }
    },
    methods: {
        getTags() {
            axios
                .get("/api/categories")
                .then((res) => {
                    this.tags = res.data
                })
                .catch((error) => {
                    console.error(error)
                })
        }
    },
    created() {
        this.getTags()
    }
})
</script>

