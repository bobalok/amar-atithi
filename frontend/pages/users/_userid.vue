<template>
    <v-container grid-list-xl>
        <div class="user-profile mt-10 mb-10">
            <v-layout row wrap>
                <v-flex lg4 md12>
                    <div class="user-sidebar">
                        <div class="user-avatar">
                            <v-avatar :size="115">
                                <img :src="user.avatar" :alt="user.name"/>
                            </v-avatar>
                        </div>

                        <hr class="mt-6 mb-6">

                        <div class="items">
                            <div class="item" v-if="user.email_verified">
                                <i class="la la-check-circle primary--text"></i>
                                <span>Email Verified</span>
                            </div>

                            <div class="item" v-if="user.mobile_verified">
                                <i class="la la-check-circle primary--text"></i>
                                <span>Mobile Verified</span>
                            </div>
                        </div>
                    </div>
                </v-flex>

                <v-flex lg8 md12>
                    <div class="content-side pl-6">
                        <div class="about-user">
                            <h1>Hi, I’m {{user.fullname}}</h1>
                            <div class="joined">Joined in {{user.joined}}</div>

                            <div class="bio mt-6" v-html="user.bio"></div>
                        </div>

                        <template v-if="places && places.length">
                            <hr class="mt-8">

                            <div class="user-listing mt-8" >
                                <h2 class="listing-title mb-6">{{user.fullname}}’s listings</h2>

                                <v-container fluid class="pa-0">
                                    <v-layout row wrap>
                                        <v-flex lg4 sm6 v-for="place in places" :key="place.code">
                                            <PlaceCard :place="place" />
                                        </v-flex>
                                    </v-layout>
                                </v-container>
                            </div>
                        </template>

                    </div>
                </v-flex>
            </v-layout>
        </div>
    </v-container>
</template>

<script>
    import {mapGetters} from 'vuex'
    import PlaceCard from "../../components/places/PlaceCard";

    export default {
        name: "UserProfile",
        components: {PlaceCard},
        computed: {
            ...mapGetters(['isAuthenticated', '$user'])
        },
        data: ()=> {
            return {
                user: {},
                places:[]
            }
        },
        mounted() {
            this.$axios.get(this.$api.Users.Details(this.$route.params.userid))
                .then((r)=> {
                    this.user = r.data
                })

            this.$axios.get(this.$api.Users.Listings(this.$route.params.userid)).then( r => this.places = r.data )
        }

    }
</script>

<style lang="scss" scoped>


    .user-profile {
        font-size: 16px;
    }


    h1 {
        font-size: 46px;
        font-weight: 400;
        line-height: 1.4;
    }


    .user-sidebar {
        border: 1px solid #eaeaea;
        padding: 25px;

        .user-avatar {
            text-align: center;
            padding: 10px 0;
        }

        .items {
            .item {
                margin-bottom: 8px;
            }
        }

    }



    h2.listing-title {
        font-size: 24px;
        font-weight: 600;
    }
</style>