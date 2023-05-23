<template>
    <div>
        <header class="fill-height header-with-slideshow">
            <div class="overlay">
                <v-container>
                    <v-layout row wrap>
                        <v-flex xs3>
                            <nuxt-link class="logo-link" to="/">
                                <img src="../static/logo-icon.png" alt="Logo"/>
                            </nuxt-link>
                        </v-flex>

                        <v-flex xs9>
                            <nav class="top-nav" v-if="isAuthenticated">
                                <ul>
                                    <li><nuxt-link to="/">Home</nuxt-link></li>
                                    <li><nuxt-link to="/dashboard/favourites">Favourite Places</nuxt-link></li>
                                    <li><nuxt-link to="/dashboard">Bookings</nuxt-link></li>
                                    <li v-if="loggedInUser.is_host"><nuxt-link to="/hosting">Hosting</nuxt-link></li>
                                    <li><nuxt-link to="/hosting/list-your-place">List Your Place</nuxt-link></li>
                                    <li><nuxt-link to="/">Help</nuxt-link></li>
                                    <li>
                                        <AccountMenu/>
                                    </li>
                                </ul>
                            </nav>
                            <nav class="top-nav" v-else>
                                <ul>
                                    <li><nuxt-link to="/">Home</nuxt-link></li>
                                    <li><nuxt-link to="/login">Login</nuxt-link></li>
                                    <li><nuxt-link to="/signup">Sign up</nuxt-link></li>
                                    <li><nuxt-link to="/">Help</nuxt-link></li>
                                </ul>
                            </nav>
                        </v-flex>
                    </v-layout>

                    <div class="slideshow-cta">
                        <form action="#" @submit.prevent="Search" method="GET">
                            <div class="ctra-portlet">
                                <h1>Book unique places to stay and things to do.</h1>

                                <div class="form-group">
                                    <label>WHERE</label>
                                    <input class="form-control" v-model="search.search" name="search" type="text" placeholder="Search a place"/>
                                </div>

                                <div class="checkinout">
                                    <div class="form-group">
                                        <label>CHECK-IN</label>
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
                                                        readonly
                                                        label="Check-in Date"
                                                        solo
                                                        flat
                                                        :value="search.checkin"
                                                        name="checkin"
                                                        v-on="on"
                                                ></v-text-field>
                                            </template>
                                            <v-date-picker
                                                    :min="tomorrow"
                                                    no-title
                                                    v-model="search.checkin"
                                                    @input="picker.checkin = false"></v-date-picker>
                                        </v-menu>
                                    </div>

                                    <div class="form-group">
                                        <label>CHECKOUT</label>
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
                                                        name="checkout"
                                                        readonly
                                                        label="Checkout Date"
                                                        solo
                                                        flat
                                                        :value="search.checkout"
                                                        v-on="on"
                                                ></v-text-field>
                                            </template>
                                            <v-date-picker
                                                    :min="tomorrow"
                                                    no-title
                                                    v-model="search.checkout"
                                                    @input="picker.checkout = false"></v-date-picker>
                                        </v-menu>
                                    </div>
                                </div>

                                <div class="form-group">
                                    <label>GUESTS</label>
                                    <input class="form-control" type="number" name="guests" min="1" max="40" v-model="search.guest" placeholder="How many guests will come?"/>
                                </div>

                                <v-btn type="submit" color="primary" large class="searchBtn">Search</v-btn>
                            </div>
                        </form>
                    </div>
                </v-container>
            </div>
        </header>


        <v-container v-if="isAuthenticated && !loggedInUser.verified">
            <v-alert
                    color="blue-grey"
                    border="left"
                    elevation="1"
                    class="mt-12"
                    colored-border
            >
                You need to verify your account before proceed to reservation. This process may take few hours. Visit <nuxt-link to="/account-settings/verifications" >Account Verification</nuxt-link> for more details.
            </v-alert>
        </v-container>

        <div class="item-section" v-if="recent.created">
            <v-container class="grid-list-lg">
                <h2 class="section-title">Places you can stay</h2>

                <v-layout row wrap>
                    <v-flex sm6 md3 xs12 v-for="place in recent.places" :key="place.code">
                        <PlaceCard :place="place"/>
                    </v-flex>
                </v-layout>
            </v-container>
        </div>

        <div class="item-section" v-if="recent.created">
            <v-container class="grid-list-lg">
                <h2 class="section-title">Top Rated Places in Dhaka</h2>

                <v-layout row wrap>
                    <v-flex sm6 md3 xs12 v-for="place in recent.places" :key="place.code">
                        <PlaceCard :place="place"/>
                    </v-flex>
                </v-layout>
            </v-container>
        </div>

<!--        <div class="item-section">-->
<!--            <v-container class="grid-list-lg">-->
<!--                <h2 class="section-title">Top Rated Places in Dhaka</h2>-->

<!--                <v-layout row wrap>-->
<!--                    <v-flex xs3 v-for="i in 8" key=`1${i}`>-->
<!--                        <PlaceCard/>-->
<!--                    </v-flex>-->
<!--                </v-layout>-->
<!--            </v-container>-->
<!--        </div>-->



    </div>
</template>

<script>
    import PlaceCard from "../components/places/PlaceCard";
    import SiteFooter from "../components/general/SiteFooter";
    import {mapGetters} from 'vuex'
    import AccountMenu from "../components/general/AccountMenu";
    import moment from "moment";

    export default {
        components: {AccountMenu, SiteFooter, PlaceCard},
        layout: "front",
        head() {
            return {
                title: `${this.$Settings.SiteName} - ${this.$Settings.SiteTagline}`
            }
        },
        data: () => {
            return {
                recent: {
                    working: true,
                    created: false,
                    places: [],
                },
                picker: {
                    checkin: false,
                    checkout: false
                },
                search: {
                    checkin: "",
                    checkout: "",
                    search: "",
                    guest: ""
                }
            }
        },
        mounted() {
            this.$axios.get(this.$api.Place.Recent)
                .then((r) => {
                    this.recent.created = true
                    this.recent.places = r.data
                })
                .finally(() => this.recent.working = false)

        },
        computed: {
            ...mapGetters(['isAuthenticated', 'loggedInUser']),
            tomorrow() {
                var today = moment();
                var tomorrow = moment(today).add(1, 'days');
                return tomorrow.format(this.$Settings.MySqlDate)
            },
        },
        methods: {
            Search(){
                let params = this.search
                let queryString = "";
                Object.keys(params).map((key) => {
                    let value = params[key]

                    if (value)
                        queryString += `&${key}=${value}`
                })

                this.$router.push("search/?" + queryString)
            }
        }
    }
</script>

<style lang="scss" >
    .header-with-slideshow {
        height: 100vh;
        background-size: cover;
        background-image: url("https://a0.muscache.com/4ea/air/r:w3100-h2074-sfit,e:fjpg-c80/pictures/0ffd8594-f123-43f0-85bb-7ef88c6f0624.jpg");
        background-position: center center;

        .logo-link {
            img {
                height: 55px;
            }
        }

        .top-nav {
            float: right;
            font-weight: 600;

            ul {
                margin: 0;
                padding: 0;


                li {
                    float: left;
                    list-style: none;
                    padding-left: 20px;
                    height: 40px;
                    line-height: 40px;

                    .nav-user{
                        cursor: pointer;
                    }

                    a {
                        color: #fff;
                        text-decoration: none;
                    }
                }
            }
        }

        .ctra-portlet {
            max-width: 450px;
            background: #fff;
            box-sizing: border-box;
            box-shadow: 0 16px 40px rgba(0, 0, 0, 0.12) !important;
            padding: 32px;
            border-radius: 4px;
            margin-top: 150px;
            overflow: hidden;

            h1 {
                color: #484848;
                font-size: 1.7rem;
                font-weight: 600;
                line-height: normal;
                margin: 0 0 20px;
                padding: 0;
            }
        }

        .searchBtn {
            font-size: 15px;
            float: right;
        }

        .checkinout .form-group {
            width: 50%;
            float: left;
            margin-left: -1px;
            margin-right: -1px;
        }

        .form-group {
            margin-bottom: 14px;

            label {
                font-weight: 600;
                color: #484848 !important;
                font-size: 13px;
                margin: 0 0 5px;
            }
        }

    }

    .item-section {
        background-color: #fff;
        margin-top: 30px;

        .section-title {
            font-size: 24px;
            font-weight: 800;
            margin: 0 0 12px 0;
            line-height: 1.25;
        }


    }




    .v-list.account_dropdown {
        padding: 5px 0;

        .v-list-item {
            min-width: 200px;
            border-bottom: 1px solid #eaeaea;
            padding: 0 20px;

            &:last-child{
                border-bottom: 0;
            }

            .v-list-item__title{
                font-size: .95rem;
                font-weight: 600;
                color: rgb(118, 118, 118)
            }
        }

    }


    .ctra-portlet .v-text-field__slot {
        font-size: 13px;
    }

    .checkinout:after,
    .checkinout:before{
        clear: both;
        display: table;
        content: '';
    }
</style>
