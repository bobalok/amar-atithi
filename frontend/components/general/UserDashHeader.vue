<template>
    <header class="site-header">
        <v-container class="pa-0" fluid>
            <div class="d-flex">
                <div class="logo-wrap">
                    <nuxt-link to="/">
                        <img src="../../static/logo-icon.png" style="height: 65px;margin-top: 7px;">
                    </nuxt-link>
                </div>

                <nav class="top-nav">
                    <ul>
                        <li>
                            <nuxt-link to="/dashboard">Dashboard</nuxt-link>
                        </li>
                        <li>
                            <nuxt-link to="/dashboard/favourites">Favourites</nuxt-link>
                        </li>
                        <li>
                            <nuxt-link to="/dashboard/reservations">Reservations</nuxt-link>
                        </li>
                    </ul>
                </nav>

                <nav class="top-nav tnr">
                    <ul>
                        <li class="ml-2">
                            <AccountMenu/>
                        </li>
                    </ul>
                </nav>
            </div>
        </v-container>
    </header>
</template>

<script>
    import {mapGetters} from 'vuex'
    import AccountMenu from "./AccountMenu";

    export default {
        name: "UserDashHeader",
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

    .logo-wrap{
        border-right: 1px solid #ddd;
        padding-right: 20px;
    }

    nav.top-nav {
        float: left;
        padding: 0 20px;


        &.tnr{
            margin-left: auto;
        }

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