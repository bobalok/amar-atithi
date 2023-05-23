<template>
    <v-container grid-list-lg class="pa-0">
        <div class="list-your-place">
            <h1 class="section-title">Let's get started listing your place</h1>

            <div class="page-subsection">
                <div class="first">First thing first</div>
                <h4 class="subtitle">What kind of place do you have?</h4>
            </div>

            <div class="list-form">
                <v-form lazy-validation v-model="valid" ref="form" @submit.prevent="FormSubmit" >
                    <v-layout wrap>
                        <v-flex xs12 class="pb-0">
                            <v-select
                                    :rules="[rules.required]"
                                    label="What kind of place do you have?"
                                    solo
                                    flat
                                    :items="types"
                                    item-text="name"
                                    item-value="pk"
                                    v-model="form.type"
                            ></v-select>
                        </v-flex>

                        <v-flex xs6 class="pb-0">
                            <v-select
                                    :rules="[rules.required]"
                                    label="What will your guests have?"
                                    solo
                                    flat
                                    item-text="name"
                                    item-value="pk"
                                    :items="spaces"
                                    v-model="form.space"
                            ></v-select>
                        </v-flex>

                        <v-flex xs6 class="pb-0">
                            <v-select
                                    :rules="[rules.required]"
                                    label="How many guests can you serve?"
                                    solo
                                    flat
                                    item-text="text"
                                    item-value="value"
                                    :items="GuestsList"
                                    v-model="form.max_guest"
                            ></v-select>
                        </v-flex>

                        <v-flex xs12 class="pb-0">
                            <v-select
                                    :rules="[rules.required]"
                                    label="Where does your place located?"
                                    solo
                                    flat
                                    item-text="name"
                                    item-value="code"
                                    :items="cities"
                                    v-model="form.city"
                            ></v-select>
                        </v-flex>

                        <v-flex xs12>
                            <v-btn type="submit" color="primary">Continue</v-btn>
                        </v-flex>
                    </v-layout>
                </v-form>
            </div>
        </div>
    </v-container>
</template>

<script>
    export default {
        name: "list-your-place",
        layout: 'hosting',
        middleware: 'auth',
        computed: {
            GuestsList() {
                let items = []

                for (let i = 1; i <= 40; i++) {
                    items.push({
                        text: i > 1 ? `for ${i} guests` : `for ${i} guest`,
                        value: i
                    })
                }

                return items
            }
        },
        data: () => {
            return {
                rules: [],
                types: [],
                spaces: [],
                cities: [],
                valid: false,
                form: {
                    type: "",
                    space: "",
                    max_guest: "",
                    city: "",
                }
            }
        },
        mounted() {
            this.rules = this.$validator.rules
            this.$axios.get(this.$api.Place.Type.List).then(r => this.types = r.data)
            this.$axios.get(this.$api.Place.Space.List).then(r => this.spaces = r.data)
            this.$axios.get(this.$api.Place.Cities.List).then(r => this.cities = r.data)
        },
        methods: {
            FormSubmit() {
                new Promise((resolve, reject) => {
                    this.$refs.form.validate();
                    resolve();
                })
                    .then(() => this.valid ? this.Create() : '')
            },
            Create() {
                this.$axios.post(this.$api.Place.Create, this.form)
                    .then((r)=> {
                        this.$router.push({name: "hosting-manage-your-space-code", params: {code: r.data.code}})
                    })
            }
        }
    }
</script>

<style lang="scss" scoped>


    .list-your-place {
        max-width: 550px;
        margin: 60px 0;
    }

    h1.section-title {
        font-weight: 500;
        font-size: 30px;
        margin-bottom: 24px;
        color: rgba(90, 90, 90, 1);
    }

    .page-subsection {
        margin-bottom: 20px;

        .first {
            text-transform: uppercase;
            font-weight: 600;
            color: #8a8a8a;
            font-size: 12px;
        }

        .subtitle {
            font-size: 19px;
            font-weight: normal;
            margin-top: 2px;
            color: #666;
        }
    }


</style>