<template>
    <div>
        <div class="container">
            <div class="row">
                <div class="col-sm-6 offset-md-3">
                    <b-alert v-model="showDismissibleAlert" variant="danger">{{
                        message
                    }}</b-alert>
                    <h1>Login</h1>
                    <br />
                    <b-form @submit.prevent="login" class="w-100">
                        <div class="form-group">
                            <label for="username">Username</label>
                            <input
                                type="text"
                                v-model="username"
                                id="username"
                                name="username"
                                class="form-control"
                                :class="{ 'is-invalid': v$.username.$error }"
                            />
                            <div
                                v-if="!v$.username.required"
                                class="invalid-feedback"
                            >
                                Username is required
                            </div>
                        </div>
                        <div class="form-group">
                            <label for="password">Password</label>
                            <input
                                type="password"
                                v-model="password"
                                id="password"
                                name="password"
                                class="form-control"
                                :class="{ 'is-invalid': v$.password.$error }"
                            />
                            <div
                                v-if="v$.password.$error"
                                class="invalid-feedback"
                            >
                                <span v-if="!v$.password.required"
                                    >Password is required</span
                                >
                                <span v-if="!v$.password.minLength"
                                    >Password must be at least 4
                                    characters</span
                                >
                            </div>
                        </div>
                        <br />
                        <div class="form-group">
                            <button class="btn btn-primary">Submit</button>
                        </div>
                    </b-form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { useVuelidate } from "@vuelidate/core"
import { required, minLength } from "@vuelidate/validators"
import { defineComponent } from "vue"

export default defineComponent({
    setup() {
        return { v$: useVuelidate() }
    },
    data() {
        return {
            username: "",
            password: "",
            showDismissibleAlert: false,
            message: "",
            showMessage: false
        }
    },
    validations: {
        username: { required },
        password: { required, minLength: minLength(8) }
    },
    methods: {
        login() {
            let username = this.username
            let password = this.password
            this.v$.$touch()
            if (this.v$.$invalid) {
                return
            }
            this.$store
                .dispatch("login", { username, password })
                .then(() => this.$router.replace("/"))
                .catch((err) => {
                    this.message = err.response.data.toString()
                    this.showMessage = true
                    this.showDismissibleAlert = true
                    console.log(err.response.data)
                })
        }
    }
})
</script>
