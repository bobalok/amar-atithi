<template>
    <div class="booking-page house-rules  mt-8 mb-8">
        <v-container grid-list-xl v-if="created" >
            <v-layout wrap>
                <v-flex xs8>
                    <div class="booking-content" >
                        <h1 class="page-title mb-12">Review house rules</h1>

                        <div class="booking-data-view">
                            <h4 class="subtitle mb-5" v-if="reservation.nights.length < 2">{{reservation.nights}} Night in {{reservation.place.state}}</h4>
                            <h4 class="subtitle mb-5" v-else >{{reservation.nights}} Nights in {{reservation.place.state}}</h4>

                            <div class="check-in-out-data">
                                <v-container fluid class="pa-0">
                                    <v-layout wrap >
                                        <v-flex xs6>
                                            <div class="data-block d-flex">
                                                <div class="block-date">
                                                    <span class="month">{{checkin_month}}</span>
                                                    <span class="date">{{checkin_date}}</span>
                                                </div>

                                                <div class="block-meta">
                                                    <div class="day">{{checkin_day}} check-in</div>
                                                    <div class="times">{{reservation.place.checkin_from_time}} - {{reservation.place.checkin_to_time}}</div>
                                                </div>
                                            </div>
                                        </v-flex>

                                        <v-flex xs6>
                                            <div class="data-block d-flex">
                                                <div class="block-date">
                                                    <span class="month">{{checkout_month}}</span>
                                                    <span class="date">{{checkout_date}}</span>
                                                </div>

                                                <div class="block-meta">
                                                    <div class="day">{{checkout_day}} check-out</div>
                                                    <div class="times">{{reservation.place.checkout_time}}</div>
                                                </div>
                                            </div>
                                        </v-flex>
                                    </v-layout>
                                </v-container>
                            </div>
                        </div>

                        <hr class="mt-12 mb-12">

                        <div class="hr-section">
                            <h4 class="subtitle mb-5">Things to keep in mind</h4>

                            <div class="house-rules-list mb-12">
                                <div class="hr-list-item" v-for="rule in reservation.place.rules">{{rule.name}}</div>
                            </div>
                        </div>


                        <v-btn color="primary" class="tall wider" @click="Next" >Agree and Continue</v-btn>
                    </div>
                </v-flex>

                <v-flex xs4>
                    <BookingPageSidebar :reservation="reservation"/>
                </v-flex>
            </v-layout>
        </v-container>
    </div>
</template>

<script>
    import BookingPageSidebar from "../../../components/booking/BookingPageSidebar";
    import moment from "moment";
    export default {
        name: "BookHouseRules",
        components: {BookingPageSidebar},
        data: ()=> {
            return {
                created: false,
                reservation: {
                    checkin: "",
                    checkout: ""
                },
            }
        },
        computed: {
            checkin_day(){
                return this.reservation.checkin ? moment(this.reservation.checkin, this.$Settings.MySqlDate).format("dddd") : "";
            },
            checkout_day(){
                return this.reservation.checkout ? moment(this.reservation.checkout, this.$Settings.MySqlDate).format("dddd") : "";
            },
            checkin_date(){
                return this.reservation.checkin ? moment(this.reservation.checkin, this.$Settings.MySqlDate).format("DD") : "";
            },
            checkout_date(){
                return this.reservation.checkout ? moment(this.reservation.checkout, this.$Settings.MySqlDate).format("DD") : "";
            },
            checkin_month(){
                return this.reservation.checkin ? moment(this.reservation.checkin, this.$Settings.MySqlDate).format("MMM") : "";
            },
            checkout_month(){
                return this.reservation.checkout ? moment(this.reservation.checkout, this.$Settings.MySqlDate).format("MMM") : "";
            },
        },
        mounted() {
            let api = this.$api.Reservation.Details(this.$route.params.ref)

            this.$axios.get(api)
                .then((r)=> {
                    this.reservation = r.data
                    this.created = true
                })
        },
        methods: {
            Next(){
                this.$router.push({name: 'book-ref-who-is-coming', params: {ref: this.$route.params.ref}})
            }
        }
    }
</script>

<style lang="scss" scoped>

    .subtitle {
        font-size: 20px;
        font-weight: 600;
    }


    .check-in-out-data{
        .data-block {

            .block-meta {
                padding-top: 8px;
            }


            .block-date {
                background: #F2F2F2;
                width: 60px;
                height: 55px;
                flex-shrink: 0;
                font-weight: 600;
                text-align: center;
                border-radius: 3px;
                margin-right: 15px;

                .month {
                    display: block;
                    line-height: 1.15rem;
                    padding-top: 10px;
                }
            }

        }
    }

    .hr-list-item {
        margin-bottom: 8px;
        font-size: 16px;
    }

</style>