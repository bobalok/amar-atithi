<template>
    <div class="trip-details">
        <v-container grid-list-xl class="pa-0" v-if="loaded">



            <div class="page-head" v-if="reservation.status.id == $Settings.ReservationStatus.PAYMENT_COMPLETE">
                <v-alert type="success" >Your payment has been received. It may take few minutes to hours to verify the transaction.</v-alert>
            </div>

            <div class="page-head" v-if="reservation.status.id == $Settings.ReservationStatus.PAYMENT_FAILED">
                <v-alert type="error" >Your payment has been failed or denied by the payment processor. Please try with a different method.</v-alert>
            </div>


            <div class="page-head" v-if="reservation.status.id == $Settings.ReservationStatus.PENDING">
                <h1 class="section-title">Your Reservation has been placed</h1>
                <div class="status-text">Waiting for your host's approval</div>
            </div>


            <div class="page-head" v-if="reservation.status.id == $Settings.ReservationStatus.DECLINED">
                <div class="page-head" >
                    <h1 class="section-title">Reservation declined</h1>
                    <div class="status-text">{{reservation.guest.fullname}} declined your reservation request.
                    </div>
                </div>
            </div>

            <div class="page-head" v-if="reservation.status.id == $Settings.ReservationStatus.CANCELLED">
                <div class="page-head" >
                    <h1 class="section-title">Reservation cancelled</h1>
                    <div class="status-text">You have cancelled this reservation.
                    </div>
                </div>
            </div>


            <template v-if="reservation.status.id == $Settings.ReservationStatus.ACCEPTED">
                <div class="page-head" v-if="reservation.timeline == 0">
                    <h1 class="section-title">Reservation complete</h1>
                    <div class="status-text">Your reservation with {{reservation.guest.fullname}} has been completed.
                    </div>
                </div>

                <div class="page-head" v-else>
                    <h1 class="section-title">{{reservation.place.host.fullname}} accepted your reservation request</h1>
                    <div class="status-text">Your reservation has been confirmed. Please contact with your host to coordinate the arrival time and key exchange</div>
                </div>

            </template>

            <v-layout wrap>
                <v-flex xs8>
                    <div class="reservation_left">
                        <div class="place-card">
                            <div class="place-image">
                                <v-img
                                        :src="reservation.place.cover.file"
                                        :lazy-src="require(`@/assets/media/lazy-placeholder.jpg`)"
                                        :aspect-ratio="1.75"
                                        class="grey lighten-2"
                                >
                                    <template v-slot:placeholder>
                                        <v-row
                                                class="fill-height ma-0"
                                                align="center"
                                                justify="center"
                                        >
                                            <v-progress-circular indeterminate color="grey lighten-5"></v-progress-circular>
                                        </v-row>
                                    </template>
                                </v-img>
                            </div>

                            <div class="place-meta">
                                <h3 class="place-title">{{reservation.place.title}}</h3>
                                <div class="place-type">{{reservation.place.space.name}}</div>

                                <div class="host-profile">
                                    <div class="host-avatar">
                                        <img :src="reservation.place.host.avatar" alt="">
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="check-meta">
                            <v-container fluid class="pl-0 pr-0">
                                <v-layout row wrap>
                                    <v-flex xs6>
                                        <div class="checkin-meta">
                                            <div class="day">{{to_day(reservation.checkin)}}</div>
                                            <div class="date">{{to_date(reservation.checkin)}}</div>
                                            <div class="time">Check-in time is {{reservation.place.checkin_from_time}}-{{reservation.place.checkin_to_time}}</div>
                                        </div>
                                    </v-flex>

                                    <v-flex xs6>
                                        <div class="checkout-meta text-right">
                                            <div class="day">{{to_day(reservation.checkout)}}</div>
                                            <div class="date">{{to_date(reservation.checkout)}}</div>
                                            <div class="time">Check-out {{reservation.place.checkout_time}}</div>
                                        </div>
                                    </v-flex>
                                </v-layout>
                            </v-container>
                        </div>

                        <div class="modify-reservation">
                            <v-container fluid class="pl-0 pr-0">
                                <v-layout row wrap>
                                    <v-flex xs12 sm6>
                                        <div class="modify-wrap" v-if="reservation.status.id == $Settings.ReservationStatus.ACCEPTED">
                                            <v-icon medium>home</v-icon>
                                            <div class="modify-title font-weight-bold mt-2">Change Reservation</div>
                                            <div class="modify-description mb-3">Change travel dates or number of guests.</div>

                                            <v-btn v-if="reservation.has_adjustment" :to="{name: 'dashboard-reservations-ref-adjustments', params:{ref: $route.params.ref}}" large outlined color="primary">View Adjustments</v-btn>
                                            <v-btn v-else large outlined color="primary" :to="{name: 'dashboard-reservations-ref-change-reservation', params:{ref: $route.params.ref}}">Change Reservation</v-btn>
                                        </div>
                                    </v-flex>

                                    <v-flex xs12 sm6 v-if="reservation.status.id == $Settings.ReservationStatus.PENDING">
                                        <div class="modify-wrap text-right">
                                            <v-icon medium>cancel</v-icon>
                                            <div class="modify-title font-weight-bold mt-2">Cancel Reservation</div>
                                            <div class="modify-description mb-3">Only select if changing the reservation is not an option.</div>
                                            <v-btn @click="cancel" large outlined color="primary">Cancel reservation</v-btn>
                                        </div>
                                    </v-flex>
                                </v-layout>
                            </v-container>
                        </div>

                        <template v-if="reservation.timeline == 0 && reservation.status.id == $Settings.ReservationStatus.ACCEPTED">
                            <div class="write-review mt-6" v-if="!reservation.host_review" >
                                <h3 class="mb-4">Rate your trip</h3>

                                <div class="form-group">
                                    <label>On scale 1-5, how much will you rate this place?</label>
                                    <v-select
                                            v-model="review.rating"
                                            solo
                                            flat
                                            label="Select a rating"
                                            :items="[1,2,3,4,5]" ></v-select>
                                </div>

                                <div class="form-group">
                                    <label>Share your experience</label>
                                    <v-textarea rows="4"
                                                v-model="review.review"
                                                :label="`Share your experience about this place`"
                                                solo
                                                flat ></v-textarea>
                                </div>

                                <v-btn @click.prevent="rate" :disabled="!review.rating || review.review.length == 0" color="primary">Submit</v-btn>
                            </div>

                            <div class="your-rating" v-else>
                                <div><strong>You rated this place:</strong> {{reservation.host_review.rating}}</div>
                                <div><strong>You review:</strong> {{reservation.host_review.review}}</div>
                            </div>
                        </template>
                    </div>
                </v-flex>

                <v-flex xs4>
                    <div class="reservation-right">
                        <div class="res-item pt-0">
                            <div class="item-title">Address</div>
                            <div class="item-content">
                                {{reservation.place.address_two}}
                                <br>
                                {{reservation.place.address_one}}
                            </div>
                        </div>

                        <div class="res-item">
                            <div class="item-title">Guests</div>
                            <div class="item-content">{{reservation.guests}} Guests</div>
                        </div>

                        <div class="res-item">
                            <div class="item-title">Amount</div>
                            <div class="item-content">{{$Settings.Price(reservation.invoice.subtotal_without_credit)}}</div>
                        </div>

                        <div class="res-item">
                            <div class="item-title">Reservation Code</div>
                            <div class="item-content">{{reservation.reference}}</div>
                        </div>

<!--                        <div class="res-item pt-5 pb-5 ">-->
<!--                            <v-btn color="error" large class="tall" block outlined >Cancel Reservation</v-btn>-->
<!--                        </div>-->

                        <div class="res-item">
                            <div class="item-title">{{reservation.place.host.fullname}} is your host</div>
                            <div class="item-content">
                                <div class="content-with-action">
                                    <div class="content">Contact {{reservation.place.host.name}} to coordinate the arrival time and key exchange</div>
                                    <div class="action error--text">{{reservation.place.host.mobile}}</div>
                                </div>
                            </div>
                        </div>

                        <div class="res-item">
                            <div class="item-title">Know what to expect</div>
                            <div class="item-content">
                                <div class="content-with-action">
                                    <div class="content">Make sure to review the house rules</div>
                                    <nuxt-link :to="`/places/${reservation.place.code}`" class="action error--text">View House Rules</nuxt-link>
                                </div>
                            </div>
                        </div>
                    </div>
                </v-flex>
            </v-layout>
        </v-container>
    </div>
</template>

<script>
    import moment from "moment";

    export default {
        name: "GuestReservationDetails",
        layout: 'dashboard',
        data: ()=> {
            return{
                reservation: {},
                loaded: false,
                review: {
                    rating: 0,
                    review: ""
                }
            }
        },
        mounted() {
            this.$axios.get(this.$api.Reservation.Details(this.$route.params.ref))
                .then((r)=> {
                    this.reservation = r.data
                    this.loaded = true
                })
        },
        methods: {
            to_date( date){
                return moment(date, this.$Settings.MySqlDate).format("MMMM DD, YYYY")
            },
            to_day( date){
                return moment(date, this.$Settings.MySqlDate).format("dddd")
            },
            cancel() {
                this.$axios.put(this.$api.Reservation.Cancel(this.reservation.reference))
                    .then((r) => {
                        this.reservation.status = r.data.status
                    })
            },
            rate(){
                let api = this.$api.Reservation.ReviewTrip
                let data = {
                    reservation: this.reservation.reference,
                    rating: this.review.rating,
                    review: this.review.review,
                }

                this.$axios.post(api, data)
                    .then((r)=> {
                        this.reservation.host_review = r.data
                    })
            }
        }
    }
</script>

<style lang="scss" scoped>
    .trip-details {
        padding: 2rem 0;

        .reservation_left {
            .status-text {
                margin-top: 4px;
            }

            .place-card {
                margin-top: 8px;

                .place-meta {
                    position: relative;
                    padding-right: 70px;
                    margin-top: 12px;
                    height: 60px;


                    h3.place-title {
                        font-size: 18px;
                        line-height: 26px;
                        font-weight: 600;
                    }


                    .host-avatar {
                        width: 60px;
                        height: 60px;
                        position: absolute;
                        right: 0;
                        top: 0;

                        img {
                            border-radius: 100%;
                        }
                    }


                }


            }

            .check-meta {
                margin-top: 18px;
                border-top: 1px solid #ededed;
            }

            /*.modify-wrap {*/
                /*border: 1px solid #ddd;*/
                /*padding: 25px;*/
            /*}*/

            .modify-reservation{
                border-top: 1px solid #ddd;
                padding-top: 10px;
                margin-top: 20px;
            }
        }

        .reservation-right {
            .item-title {
                font-size: 16px;
                font-weight: 600;
                color: #5a5a5a;
                display: block;
                line-height: 26px;
            }

            .item-content {
                font-size: 14px;
                line-height: 20px;
                margin-top: 4px;
            }

            .res-item {
                padding: 12px 0;

                &:not(.no-border) {
                    border-bottom: 1px solid rgba(234, 234, 234, 1);
                }

                .content-with-action {
                    display: flex;
                    margin-top: 3px;

                    .action {
                        width: 160px;
                        margin-left: auto;
                        text-align: right;
                    }
                }


            }


        }





    }
</style>
