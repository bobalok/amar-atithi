<template>
    <v-container>
        <div class="personal-info">
            <div class="head">
                <h1>Personal info</h1>
            </div>

            <v-container fluid grid-list-xl class="pa-0">
                <v-layout row wrap>
                    <v-flex xs8>
                        <v-form class="mb-10" lazy-validation v-model="valid" ref="form" @submit.prevent="FormSubmit">

                            <v-container class="pa-0" grid-list-sm fluid>
                                <v-layout row wrap>
                                    <v-flex xs6>
                                        <div class="form-group">
                                            <label>First Name</label>
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
                                    </v-flex>

                                    <v-flex xs6>
                                        <div class="form-group">
                                            <label>Last Name</label>
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
                                    </v-flex>
                                </v-layout>
                            </v-container>

                            <div class="form-group">
                                <label>Nickname</label>
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
                                <label>Email Address</label>
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
                                <label>Mobile No.</label>
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
                                <label>Address</label>
                                <v-text-field
                                        :rules="[rules.required, rules.max(form.address, 250)]"
                                        label="Gulshan, Dhaka, Bangladesh"
                                        rows="3"
                                        solo
                                        flat
                                        class="with-counter"
                                        :counter="250"
                                        v-model="form.address"
                                        :error-messages="hints.address"
                                        @change="hints.address = ''"
                                ></v-text-field>
                            </div>


                            <div class="form-group last-item">
                                <label>About Yourself</label>
                                <v-textarea
                                        :rules="[rules.required, rules.max(form.bio, 500)]"
                                        label="Write few words about yourself"
                                        rows="5"
                                        solo
                                        flat
                                        class="with-counter"
                                        :counter="500"
                                        v-model="form.bio"
                                        :error-messages="hints.bio"
                                        @change="hints.bio = ''"
                                ></v-textarea>
                            </div>

                            <v-btn color="primary" type="submit" large>Update Info</v-btn>
                        </v-form>

                    </v-flex>

                    <v-flex xs4>
                       <div class="form-group">
                           <label class="mb-1">Profile Photo</label>
                           <div class="avatar-block">
                               <img :src="form.avatar" >
                               <input type="file" ref="image_selector" class="selector">

                               <div class="action-btn">
                                   <i class="la la-edit"></i>
                                   <span class="ml-1">Edit</span>
                               </div>
                           </div>
                       </div>
                    </v-flex>
                </v-layout>
            </v-container>


        </div>
    </v-container>
</template>

<script>
    export default {
        name: "personal-info",
        data: () => {
            return {
                valid: false,
                rules: [],
                created: false,
                working: true,

                form: {
                    first_name: "",
                    last_name: "",
                    nickname: "",
                    email: "",
                    mobile: "",
                    gender: "",
                    dob: "",
                    address: "",
                    bio: "",
                },
                hints: {
                    first_name: "",
                    last_name: "",
                    nickname: "",
                    email: "",
                    mobile: "",
                    gender: "",
                    dob: "",
                    address: "",
                    bio: "",
                }

            }
        },
        created() {
            this.rules = this.$validator.rules
        },
        methods: {
            FormSubmit() {
                let check = new Promise((resolve, reject) => {
                    this.$refs.form.validate();
                    resolve();
                });

                check.then(() => {
                    if (this.valid)
                        this.Save()
                });
            },
            Save() {
                let api = this.$api.Users.SelfUpdate

                this.$axios.put(api, this.form)
                    .then((r) => {
                        this.$store.dispatch("alert/Snack", "Info Updated")
                    })
                    .catch((error) => {
                        if (error.response.status == 400) {
                            this.hints = error.response.data
                        }
                    })
            }
        },
        mounted() {
            let api = this.$api.Users.SelfUpdate

            this.$axios.get(api).then((r) => {
                this.form = r.data
                this.created = true
                this.working = false
            })
        }
    }
</script>

<style lang="scss" scoped>
    .head {
        margin: 36px 0 54px 0;

        h1 {
            font-size: 32px;
            font-weight: 800;
        }

        .handle {
            font-size: 16px;
            margin-top: 16px;
        }
    }


    .avatar-block {
        position: relative;
        border-radius: 8px;
        overflow: hidden;
        width: 200px;
        height: 200px;
        cursor: pointer;

        img {
            object-fit: cover;
        }

        .action-btn {
            position: absolute;
            bottom: 10px;
            left: 10px;
            background: rgba(0,0,0,0.7);
            color: #fff;
            font-size: 13px;
            padding: 2px 10px;
            border-radius: 4px;
        }

        input.selector {
            display: none;
        }
    }


</style>