<template>
    <v-container class="login-wrap">


        <div class="login-form">

            <div class="form-header">Login to Amar Atithi</div>

            <v-form lazy-validation v-model="valid" ref="form" @submit.prevent="FormSubmit" class="LoginForm">

                <v-alert v-if="auth_error" type="error" class="login_error" >{{error_msg}}</v-alert>

                <v-alert v-else-if="email_v_error" type="error" class="login_error" >
                    <div class="AlertText">You need to verify your email address in order to login. Please check your inbox for verification link.</div>
                    <v-btn class="ml-0 mb-0 mt-3"
                           style="padding: 0 15px;height: 32px;line-height: 32px;font-size: 13px;"
                           color="grey lighten-4">Resend Verification Email</v-btn>
                </v-alert>

                <div class="form-group form-email">
                    <v-text-field
                            :rules="[rules.required, rules.email]"
                            label="Email Address"
                            solo
                            flat
                            v-model="form.email"
                            :error-messages="hints.email"
                            @change="hints.email = ''"
                    ></v-text-field>

                    <!--                    <div v-if="hints.email" class="form-hint error&#45;&#45;text">{{hints.email}}</div>-->
                </div>

                <div class="form-group">
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

                <div class="form-group d-flex last-item">
                    <div class="remember">
                        <v-checkbox color="primary" class="ma-0" label="Remember me"></v-checkbox>
                    </div>

                    <nuxt-link class="fp-link" to="/forgot-password">Forgot password?</nuxt-link>
                </div>

                <div class="form-group mb-3">
                    <v-btn :disabled="working" :loading="working" type="submit" color="primary" block large>Log In
                    </v-btn>
                </div>

            </v-form>

            <v-dialog
                    v-model="md.show"
                    width="600"
            >
                <div class="IonModal white">
                    <div class="ModalHeader">
                        <h3 class="modal-title">Verify your phone</h3>
                    </div>

                    <div class="ModalBody pa-4">
                        <v-alert type="error" v-if="md.error">The code you entered is not correct.</v-alert>
                        <v-alert v-else type="info">A verification code has been sent to your phone. Please enter the code below to continue.</v-alert>

                        <div class="form-group mt-6">
                            <v-text-field solo flat label="Enter the code" v-model="md.input" ></v-text-field>
                        </div>
                    </div>

                    <div class="ModalFooter">
                        <v-btn color="primary" outlined @click="CloseMDialogue" >Cancel</v-btn>
                        <v-btn :disabled="md.input.length == 0" style="float: right;" color="primary" @click="VerifyPhone" >Verify</v-btn>
                    </div>
                </div>
            </v-dialog>

            <div class="form-group last-item">Don't have an account?
                <nuxt-link to="/signup">Sign up</nuxt-link>
            </div>
        </div>

    </v-container>
</template>

<script>
    export default {
        name: "login",
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
                md: {
                    show: false,
                    input: "",
                    error: false
                },
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

                        if( code == 406 ){
                            this.email_v_error = true
                        } else if( code == 403 ){
                            this.md.show = true
                        } else if( code == 410 ){
                            this.auth_error = true
                            this.error_msg = "Your account has been disabled"
                        } else {
                            this.auth_error = true
                            this.error_msg = "Incorrect email or password"
                        }
                    })
                    .finally(() => {
                        this.working = false
                    })
            },
            VerifyPhone(){
                this.md.error = false

                this.$axios.post(this.$api.Users.VerifyPhone, {email: this.form.email, code: this.md.input})
                    .then(()=> {
                        this.$auth.login({data: this.form})
                            .finally(()=> {
                                this.CloseMDialogue()
                            })
                    })
                    .catch((error)=> {
                        this.md.error = true
                    })
            },
            CloseMDialogue(){
                this.md.input = ""
                this.md.show = false
            }
        }
    }
</script>

<style scoped>

    .login-form {
        max-width: 450px;
        margin: 50px auto;
        border: 1px solid #dce0e0;
        padding: 32px;
    }

    .fp-link {
        font-weight: 600;
        text-decoration: none;
        margin-left: auto;
    }

    .form-header {
        font-size: 1.45rem;
        text-align: center;
        border-bottom: 1px solid #ddd;
        padding: 0 0 20px 0;
        margin-bottom: 30px;
        font-weight: 400;
    }


</style>