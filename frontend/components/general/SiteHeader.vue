<template>
    <header class="site-header">
        <v-container class="pt-0 pb-0" fluid>
            <v-layout row wrap>
                <v-flex xs4>
                    <nuxt-link to="/">
                        <img src="../../static/tw-logo.png" style="height: 75px">
                    </nuxt-link>
                </v-flex>

                <v-flex xs8>
                    <nav class="top-nav" v-if="isAuthenticated">
                        <ul>
                            <li><nuxt-link to="/">Home</nuxt-link></li>
                            <li><nuxt-link to="/dashboard/favourites">Favourite Places</nuxt-link></li>
                            <li><nuxt-link to="/dashboard">Bookings</nuxt-link></li>
                            <li v-if="loggedInUser.is_host"><nuxt-link to="/hosting">Hosting</nuxt-link></li>
                            <li><nuxt-link to="/hosting/list-your-place">List Your Place</nuxt-link></li>
                            <li><nuxt-link to="/">Help</nuxt-link></li>
                            <li class="ml-2">
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
        </v-container>
    </header>
</template>

<script>
    import {mapGetters} from 'vuex'
    import AccountMenu from "./AccountMenu";

    export default {
        name: "SiteHeader",
        components: {AccountMenu},
        computed: {
            ...mapGetters(['isAuthenticated', 'loggedInUser'])
        },
    }
</script>

<style lang="scss" scoped>

    .site-header{
        height: 75px;
        padding: 0 2rem;
        border-bottom: 1px solid #ddd;
    }

    nav.top-nav {
        float: right;

        ul {
            margin: 0;
            padding: 0;

            li {
                list-style: none;
                float: left;
                line-height: 75px;

                a {
                    color: #484848;
                    text-decoration: none;
                    padding: 0 10px;
                    font-weight: 600;
                }

            }
        }
    }


</style>