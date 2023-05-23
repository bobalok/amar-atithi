<template>
    <div class="login">
        <v-container>
            <v-form lazy-validation v-model="valid" ref="form" @submit.prevent="FormSubmit" class="login_form">

                <div class="ion-portlet">
                    <div class="portlet-head">
                        <div class="portlet-head-label">
                            <div class="portlet-head-icon">
                                <i class="la la-user-plus"></i>
                            </div>
                            <h3 class="portlet-head-title">Login</h3>
                        </div>
                    </div>
                    <div class="portlet-body pa-8">

                        <v-alert v-if="auth_error" type="error" class="login_error" >{{error_msg}}</v-alert>

                        <div class="form-group">
                            <label>Email Address</label>


                                <v-text-field
                                        :rules="[rules.required, rules.email]"
                                        label="Enter your email"
                                        solo
                                        flat
                                        v-model="form.email"
                                        :error-messages="hints.email"
                                        @change="hints.email = ''"
                                ></v-text-field>
                        </div>

                        <div class="form-group last-item">
                            <label>Password</label>
                            <v-text-field
                                    :rules="[rules.required]"
                                    label="Password"
                                    :type="show1 ? 'text' : 'password'"
                                    solo
                                    flat

                                    v-model="form.password"
                                    :error-messages="hints.password"
                                    @change="hints.password = ''"
                                    :append-icon="show1 ? 'visibility' : 'visibility_off'"
                                    @click:append="show1 = !show1"
                            ></v-text-field>
                        </div>
                    </div>

                    <div class="portlet-footer">
                        <v-btn class="wider" color="primary" :disabled="working" :loading="working" type="submit">Login</v-btn>
                    </div>
                </div>
            </v-form>
        </v-container>
    </div>
</template>

<script>
    export default {
        name: "login",
        layout: "front",
        middleware: 'guest',
        data: () => {
            return {
                rules: [],
                working: false,
                valid: false,
                show1: false,
                auth_error: false,
                error_msg: "",
                email_v_error: false,
                form: {
                    email: "",
                    password: ""
                },
                hints: {
                    email: "",
                    password: "",
                }
            }
        },
        created() {
            this.rules = this.$validator.rules
        },
        methods: {
            FormSubmit() {
                this.working = true;
                this.auth_error = false
                this.email_v_error = false
                this.error_msg = ""

                let check = new Promise((resolve, reject) => {
                    this.$refs.form.validate();
                    resolve();
                });

                check.then(() => {
                    if (this.valid) {
                        this.Authenticate();
                    } else {
                        this.working = false;
                    }
                });
            },
            Authenticate() {
                this.$auth.login({data: this.form})
                    .catch((error) => {
                        let code = error.response.status
                        this.auth_error = true
                        this.error_msg = "Incorrect email or password"
                    })
                    .finally(() => {
                        this.working = false
                    })
            },
        }
    }
</script>

<style scoped>
    .login_form {
        max-width: 768px;
        margin: 70px auto;
    }
</style>
