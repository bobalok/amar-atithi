<template>


    <div v-if="loaded">

        <v-container class="grid-list-lg">
            <div class="search-bar">
                <v-layout row wrap>
                    <v-flex sm9 lg10>
                        <input class="form-control search-keyword" type="text" v-model="sidebar.search"
                               placeholder="Search...."/>
                    </v-flex>

                    <v-flex sm3 lg2>
                        <div class="ml-2">
                            <v-btn color="primary" @click="ApplyFilter">Search</v-btn>
                        </div>
                    </v-flex>
                </v-layout>
            </div>
        </v-container>


        <v-container class="grid-list-xl">
            <!--<h2 class="section-title">Showing you results for "{{params.get('search')}}"</h2>-->

            <v-layout row wrap>
                <v-flex xs12 sm3 lg2 class="search-sidebar">

                    <div class="form-group">
                        <label>Check-in</label>

                        <v-menu
                                v-model="picker.checkin"
                                :close-on-content-click="false"
                                :nudge-right="40"
                                transition="scale-transition"
                                offset-y
                                full-width
                                min-width="290px"
                        >
                            <template v-slot:activator="{ on }">
                                <v-text-field
                                        label="Check-in Date"
                                        solo
                                        flat
                                        v-model="sidebar.checkin"
                                        v-on="on"
                                        clearable
                                ></v-text-field>
                            </template>
                            <v-date-picker
                                    :min="tomorrow"
                                    no-title
                                    v-model="sidebar.checkin"
                                    @input="picker.checkin = false"></v-date-picker>
                        </v-menu>
                    </div>

                    <div class="form-group">
                        <label>Checkout</label>

                        <v-menu
                                v-model="picker.checkout"
                                :close-on-content-click="false"
                                :nudge-right="40"
                                transition="scale-transition"
                                offset-y
                                full-width
                                min-width="290px"
                        >
                            <template v-slot:activator="{ on }">
                                <v-text-field
                                        label="Checkout Date"
                                        solo
                                        flat
                                        v-model="sidebar.checkout"
                                        v-on="on"
                                        clearable
                                ></v-text-field>
                            </template>
                            <v-date-picker
                                    :min="sidebar.checkin"
                                    no-title
                                    scrollable
                                    v-model="sidebar.checkout"
                                    @input="picker.checkout = false"></v-date-picker>
                        </v-menu>
                    </div>

                    <div class="form-group">
                        <label>Checkin Time</label>
                        <v-select
                                label="Check-in start time"
                                solo
                                flat
                                item-text="text"
                                item-value="value"
                                :items="times.in"
                                clearable
                                v-model="sidebar.checkin_time"
                        ></v-select>
                    </div>

                    <div class="form-group">
                        <label>Number of Guests</label>
                        <input type="number" min="1" v-model="sidebar.guest" class="form-control">
                    </div>

                    <div class="form-group">
                        <label>Price</label>
                        <div class="price-group">
                            <input type="number" min="1" v-model="sidebar.min" placeholder="Min" class="form-control">
                            <span>-</span>
                            <input type="number" min="1" v-model="sidebar.max" placeholder="Max" class="form-control">
                        </div>
                    </div>

                    <div class="form-group">
                        <label>Types of Place</label>
                        <v-select
                                chips
                                solo
                                flat
                                multiple
                                :items="types"
                                item-text="name"
                                item-value="pk"
                                v-model="sidebar.type"
                        ></v-select>
                    </div>

                    <div class="form-group">
                        <label>Types of Space</label>
                        <v-select
                                chips
                                solo
                                flat
                                multiple
                                :items="spaces"
                                item-text="name"
                                item-value="pk"
                                v-model="sidebar.spaces"
                        ></v-select>
                    </div>

                    <div class="form-group">
                        <v-btn @click="ApplyFilter" block color="primary">Apply Filter</v-btn>
                    </div>


                </v-flex>

                <v-flex xs12 sm9 lg10>
                    <v-layout row wrap>
                        <template v-if="places && places.length">
                            <v-flex xs3 v-for="place in places" :key="place.code">
                                <PlaceCard :place="place"/>
                            </v-flex>
                        </template>
                        <template v-else>
                            <v-flex xs12>
                                <v-alert
                                        color="blue-grey"
                                        border="left"
                                        elevation="1"
                                        class="mt-6"
                                        colored-border
                                >No matching places found. Please try with different parameter.
                                </v-alert>
                            </v-flex>
                        </template>
                    </v-layout>
                </v-flex>
            </v-layout>
        </v-container>
    </div>


</template>

<script>
    import PlaceCard from "../components/places/PlaceCard";
    import moment from "moment";

    export default {
        name: "search",
        components: {PlaceCard},
        computed: {
            tomorrow() {
                var today = moment();
                var tomorrow = moment(today).add(1, 'days');
                return tomorrow.format(this.$Settings.MySqlDate)
            },
        },
        data: () => {
            return {
                working: true,
                loaded: false,
                types: [],
                spaces: [],
                cities: [],
                places: [],
                times: {
                    in: [],
                    out: []
                },
                params: null,
                sidebar: {
                    search: "",
                    checkin: null,
                    checkout: null,
                    guest: 1,
                    type: null,
                    spaces: null,
                    city: null,
                    min: null,
                    max: null,
                    checkin_time: null,
                },
                picker: {
                    checkin: false,
                    checkout: false
                },
            }
        },
        mounted() {

            this.$axios.get(this.$api.Place.Type.List).then(r => this.types = r.data)
            this.$axios.get(this.$api.Place.Space.List).then(r => this.spaces = r.data)
            this.$axios.get(this.$api.Place.Cities.List).then(r => this.cities = r.data)
            this.$axios.get(this.$api.Place.Times).then(r => this.times = r.data)

            let params = new URLSearchParams(location.search);
            this.sidebar.search = params.get("search")
            this.sidebar.checkin = params.get("checkin")
            this.sidebar.checkout = params.get("checkout")
            this.sidebar.guest = params.get("guest")
            this.sidebar.type = params.get("type") ? params.get("type").split(",").map(Number).filter(Boolean): []
            this.sidebar.spaces = params.get("spaces") ? params.get("spaces").split(",").map(Number).filter(Boolean): []

            this.$axios.post(this.$api.Place.Search, this.sidebar)
                .then((r) => {
                    this.loaded = true
                    this.places = r.data
                })
                .finally(() => this.working = false)
        },
        methods: {
            addHashToLocation(params) {
                history.pushState(
                    {},
                    null,
                    this.$route.path + params
                )
            },

            ApplyFilter() {
                let params = this.sidebar
                let queryString = "?5=5";

                //console.log(params)

                Object.keys(params).map((key) => {
                    let value = params[key]

                    if (value)
                        queryString += `&${key}=${value}`
                })


               // console.log(queryString)

                this.addHashToLocation(queryString)

                this.$axios.post(this.$api.Place.Search, params)
                    .then((r) => {
                        this.loaded = true
                        this.places = r.data
                    })
                    .finally(() => this.working = false)
            }
        }
    }
</script>

<style lang="scss">
    .item-section {
        margin-top: 0;
    }

    input.form-control.search-keyword {
        height: 40px;
        border-radius: 0;
    }

    .search-bar {
        padding: 20px 0 20px 0;
        border-bottom: 1px solid #ddd;
        font-size: 13px;
    }

    .search-sidebar {
        .price-group .form-control {
            width: 45%;
            float: left;
        }

        .price-group span {
            float: left;
            width: 10%;
            text-align: center;
            height: 40px;
            line-height: 40px;
            font-size: 18px;
        }

        .price-group {
            overflow: hidden;
        }


        .form-control, .v-input input, .v-text-field.v-text-field--solo:not(.v-select--chips) .v-input__control {
            height: 42px !important;
            font-size: 13px !important;
            min-height: 42px;
        }

        .v-text-field--solo-flat > .v-input__control .v-label {
            font-size: 13px;
        }

        .form-group {
            margin: 0 0 15px 0;
        }
    }
</style>
