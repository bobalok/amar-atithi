<template>
    <v-container class="login-wrap">
        <div class="login-form">

            <div class="form-header">
                Welcome to Amar Atithi
            </div>

            <v-alert :value="success" class="mb-6" type="success">Registration Successful! Please check your email inbox
                for verification Link.
            </v-alert>

            <v-form lazy-validation v-model="valid" v-if="!success" ref="form" @submit.prevent="FormSubmit"
                    class="LoginForm">


                <div class="form-group">
                    <v-text-field
                            :rules="[rules.required, rules.name]"
                            label="First Name"
                            solo
                            flat
                            v-model="form.first_name"
                            :error-messages="hints.first_name"
                            @change="hints.first_name = ''"
                    ></v-text-field>
                </div>

                <div class="form-group">
                    <v-text-field
                            :rules="[rules.required, rules.name]"
                            label="Last Name"
                            solo
                            flat
                            v-model="form.last_name"
                            :error-messages="hints.last_name"
                            @change="hints.last_name = ''"
                    ></v-text-field>
                </div>

                <div class="form-group">
                    <v-text-field
                            :rules="[rules.required, rules.name]"
                            label="Nickname: What should your guests call you?"
                            solo
                            flat
                            v-model="form.nickname"
                            :error-messages="hints.nickname"
                            @change="hints.nickname = ''"
                    ></v-text-field>
                </div>


                <div class="form-group">
                    <v-text-field
                            :rules="[rules.required, rules.email]"
                            label="Email Address"
                            solo
                            flat
                            type="email"
                            v-model="form.email"
                            :error-messages="hints.email"
                            @change="hints.email = ''"
                    ></v-text-field>
                </div>


                <div class="form-group">
                    <v-text-field
                            :rules="[rules.required]"
                            label="Mobile Number"
                            solo
                            flat
                            type="text"
                            v-model="form.mobile"
                            :error-messages="hints.mobile"
                            @change="hints.mobile = ''"
                    ></v-text-field>
                </div>


                <div class="form-group">
                    <v-text-field
                            :rules="[rules.required]"
                            label="Choose a Password"
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

                <div class="form-group">
                    <v-text-field
                            :rules="[rules.required, rules.match(this.form.password, this.form.repassword)]"
                            label="Repeat Password"
                            solo
                            flat
                            v-model="form.repassword"
                            :type="show2 ? 'text' : 'password'"
                            :append-icon="show2 ? 'visibility' : 'visibility_off'"
                            @click:append="show2 = !show2"
                    ></v-text-field>
                </div>

                <div class="form-group">
                    <v-select
                            :rules="[rules.required]"
                            label="Gender"
                            solo
                            flat
                            v-model="form.gender"
                            :items="$Settings.Genders"
                            item-text="text"
                            item-value="value"
                    ></v-select>
                </div>

                <div class="form-group">
                    <v-menu
                            v-model="dob"
                            :close-on-content-click="false"
                            :nudge-right="40"
                            transition="scale-transition"
                            offset-y
                            full-width
                            min-width="290px"
                    >
                        <template v-slot:activator="{ on }">
                            <v-text-field
                                    :rules="[rules.required]"
                                    label="Date of Birth"
                                    solo
                                    flat
                                    v-model="form.dob"
                                    :error-messages="dob_error"
                                    v-on="on"
                            ></v-text-field>
                        </template>
                        <v-date-picker :max="todayDate" no-title v-model="form.dob" @input="dob = false"></v-date-picker>
                    </v-menu>
                </div>

                <div class="form-group">
                    <v-checkbox v-model="terms" color="primary" class="ma-0"
                                label="I agree to the terms and condition"></v-checkbox>
                </div>

                <div class="form-group mb-2">
                    <v-btn
                            type="submit"
                            color="primary"
                            block
                            large
                            :disabled="!terms || working || isAdult !== true"
                            :loading="working"
                    >Sign up
                    </v-btn>
                </div>
            </v-form>

            <div class="form-group last-item">Already have an account?
                <nuxt-link to="/login">Login</nuxt-link>
            </div>
        </div>
    </v-container>
</template>

<script>
    import moment from "moment";

    export default {
        name: "signup",
        middleware: 'guest',
        data: () => {
            return {
                valid: false,
                working: false,
                show1: false,
                show2: false,
                success: false,
                rules: [],
                dob: false,
                terms: false,
                form: {
                    first_name: "",
                    last_name: "",
                    nickname: "",
                    email: "",
                    mobile: "",
                    password: "",
                    repassword: "",
                    gender: "",
                    dob: "",
                },
                hints: {
                    first_name: "",
                    last_name: "",
                    nickname: "",
                    email: "",
                    mobile: "",
                    password: "",
                    repassword: "",
                    gender: "",
                    dob: "",
                }
            }
        },
        created() {
            this.rules = this.$validator.rules
        },
        computed: {
            todayDate(){
                var today = moment();
                return today.format(this.$Settings.MySqlDate)
            },
            isAdult() {
                if (!this.form.dob)
                    return null

                let age = moment().diff(this.form.dob, 'years');

                return age >= 18
            },
            dob_error(){
                if ( this.form.dob && this.isAdult != true)
                    return "You must be at least 18 years old in order to join Amar Atithi"
            }
        },
        methods: {
            FormSubmit() {
                let check = new Promise((resolve, reject) => {
                    this.$refs.form.validate();
                    resolve();
                });

                check.then(() => {
                    if (this.valid) {
                        this.CreateAccount();
                    }
                });
            },

            CreateAccount() {
                this.working = true;

                this.$axios.post(this.$api.Users.Register, this.form)
                    .then((response) => {
                        this.success = true;
                    })
                    .catch((error) => {
                        this.hints = error.response.data
                    })
                    .finally(() => this.working = false)
            },
        },
    }
</script>

<style scoped>

    .login-form {
        max-width: 450px;
        margin: 50px auto;
        border: 1px solid #dce0e0;
        padding: 32px;
    }


    .form-header {
        font-size: 1.45rem;
        text-align: center;
        border-bottom: 1px solid #ddd;
        padding: 0 0 20px 0;
        margin-bottom: 30px;
        font-weight: 400;
    }

    .v-input--checkbox label {
        font-weight: normal;
    }
</style>