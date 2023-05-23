<template>
    <v-app class="dashboard">
        <v-navigation-drawer
                v-model="drawer"
                :mini-variant="miniVariant"
                app
                clipped
                left
                dark
                width="250"
                class="csdrawer"
        >
            <div class="ListOutter">
                <simplebar class="IonList" data-simplebar-auto-hide="true">
                    <nuxt-link to="/dashboard" class="ListItem active" href="#">
                        <div class="ItemIcon">
                            <v-icon>home</v-icon>
                        </div>
                        <div class="ItemContent">Dashboard</div>
                    </nuxt-link>


                    <div class="IonListGroup">
                        <div class="GroupTitle">Amar Otithi</div>

                        <div class="IonGroupItems">
                            <nuxt-link to="/account-verifications" class="ListItem" >
                                <div class="ItemIcon">
                                    <v-icon>dashboard</v-icon>
                                </div>
                                <div class="ItemContent">Account Verifications</div>
                            </nuxt-link>

                            <nuxt-link to="/payment-requests" class="ListItem" >
                                <div class="ItemIcon">
                                    <v-icon>money</v-icon>
                                </div>
                                <div class="ItemContent">Payment Requests</div>
                            </nuxt-link>


                            <nuxt-link to="/logout" class="ListItem" >
                                <div class="ItemIcon">
                                    <i class="la la-sign-out"></i>
                                </div>
                                <div class="ItemContent">Logout</div>
                            </nuxt-link>
                        </div>
                    </div>


                </simplebar>
            </div>
        </v-navigation-drawer>

        <v-app-bar
                app
                clipped-left
                dark
                fixed
        >
            <v-app-bar-nav-icon  @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
            <h3 style="font-weight: normal;">Amar Atithi Admin</h3>
            <v-spacer></v-spacer>
        </v-app-bar>



        <v-content>
            <v-container fluid class="main-container pa-0 grid-list-lg">
                <nuxt/>
            </v-container>

            <v-footer class="ion-footer ">
                <div>&copy; Copyright 2019 Amar Atithi Admin. All Right Reserved</div>
            </v-footer>
        </v-content>
    </v-app>
</template>

<script>
    import simplebar from "simplebar-vue";
    import 'simplebar/dist/simplebar.css';


    export default {
        components: {simplebar},
        data() {
            return {
                clipped: true,
                drawer: true,
                fixed: true,
                miniVariant: false,
                right: true,
                rightDrawer: false,
                title: 'Vuetify.js'
            }
        }
    }
</script>

<style  lang="scss">

    .ListOutter{
        overflow: hidden;
        position: absolute;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
    }

    .IonList{
        height: 100%;
        display: block;
    }

    .IonList {
        color: #9e9e9e;
        font-size: 11px;
        padding: 3em 0 2em 0;

        .IonListGroup {
            margin-top: 3em;

            .GroupTitle {
                padding: 0 2em;
                margin-bottom: 1em;
            }
        }

        .ListItem {
            color: #9899ac;
            overflow: hidden;
            display: block;
            text-decoration: none;
            font-size: 13px;
            height: 44px;
            line-height: 44px;
            padding: 0 2em;

            &:hover {
                background-color: #2f2e3c;


            }

            &.active {
                background-color: #DB1430;
                color: #fff;

                .ItemIcon {
                    color: #fff;
                }
            }

            .ItemIcon {
                float: left;
                color: #6b6c7f;
                line-height: 50px;
                margin-right: 10px;

                .la{
                    font-size: 22px;
                }

                .v-icon {
                    color: inherit;
                    line-height: 100%;
                    font-size: 22px;
                    margin-top: -5px;
                }
            }
        }
    }




</style>
