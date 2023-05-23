<template>
    <div class="trip-details">
        <v-container grid-list-xl class="pa-0" v-if="created">

            <div class="page-head" v-if="reservation.status.id == $Settings.ReservationStatus.PENDING">
                <h1 class="section-title">{{reservation.guest.name}} is waiting for your response</h1>
                <div class="status-text">{{reservation.guest.fullname}} reserved your place and paid in advance. He is
                    waiting for your response.
                </div>
            </div>

            <template v-if="reservation.status.id == $Settings.ReservationStatus.ACCEPTED">

                <div class="page-head" v-if="reservation.timeline == 2">
                    <h1 class="section-title">{{reservation.guest.name}} will arrive in {{to_date(reservation.checkin)}}</h1>
                    <div class="status-text">{{reservation.guest.fullname}} will arrive in {{to_day(reservation.checkin)}},
                        {{to_date(reservation.checkin)}}. Keep your place clean and don't forget to welcome your guest
                    </div>
                </div>

                <div class="page-head" v-else-if="reservation.timeline == 1">
                    <h1 class="section-title">{{reservation.guest.name}} has arrived</h1>
                    <div class="status-text">{{reservation.guest.fullname}} has arrived. Don't forget to welcome your guest.
                    </div>
                </div>

                <div class="page-head" v-else-if="reservation.timeline == 0">
                    <h1 class="section-title">Reservation complete</h1>
                    <div class="status-text">Your reservation with {{reservation.guest.fullname}} has been completed.
                    </div>
                </div>

            </template>


            <v-layout wrap>
                <v-flex xs8>
                    <div class="reservation_left">
                        <div class="guest-quote-card">
                            <div class="guest-quote">{{reservation.wc_message}}</div>

                            <div class="guest-card">
                                <v-avatar :size="40">
                                    <img :src="reservation.guest.avatar"/>
                                </v-avatar>
                            </div>
                        </div>

                        <div class="check-meta">
                            <v-container fluid class="pl-0 pr-0">
                                <v-layout row wrap>
                                    <v-flex xs6>
                                        <div class="checkin-meta">
                                            <strong>Check-in</strong>
                                            <div class="day">{{to_day(reservation.checkin)}}</div>
                                            <div class="date">{{to_date(reservation.checkin)}}</div>
                                        </div>
                                    </v-flex>

                                    <v-flex xs6>
                                        <div class="checkout-meta text-right">
                                            <strong>Checkout</strong>
                                            <div class="day">{{to_day(reservation.checkout)}}</div>
                                            <div class="date">{{to_date(reservation.checkout)}}</div>
                                        </div>
                                    </v-flex>
                                </v-layout>
                            </v-container>


                        </div>

                        <hr class="mb-8 mt-3">

                        <div class="action-btns" v-if="reservation.status.id == $Settings.ReservationStatus.PENDING">
                            <v-btn color="primary" large class="mr-2" @click.prevent="accept">Accept This Reservation
                            </v-btn>
                            <v-btn color="error" @click.prevent="decline" large>Decline This Reservation</v-btn>
                        </div>

                        <template v-if="reservation.timeline == 0 && reservation.status.id == $Settings.ReservationStatus.ACCEPTED">
                            <div class="write-review" v-if="!reservation.guest_review" >
                                <h3>Rate your guest</h3>

                                <div class="form-group">
                                    <label>On scale 1-5, how much will you rate {{reservation.guest.name}}?</label>
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
                                                :label="`Share your experience with ${reservation.guest.name}`"
                                                solo
                                                flat ></v-textarea>
                                </div>

                                <v-btn @click.prevent="rate" :disabled="!review.rating || review.review.length == 0" color="primary">Submit</v-btn>
                            </div>

                            <div class="your-rating" v-else>
                                <div><strong>You rated your guest:</strong> {{reservation.guest_review.rating}}</div>
                                <div><strong>You review:</strong> {{reservation.guest_review.review}}</div>
                            </div>
                        </template>
                    </div>
                </v-flex>

                <v-flex xs4>
                    <div class="reservation-right">
                        <div class="res-item">
                            <div class="item-title">Status</div>
                            <div class="item-content">
                                <v-chip :color="reservation.status.color" label small>{{reservation.status.text}}
                                </v-chip>
                            </div>
                        </div>

                        <div class="res-item">
                            <div class="item-title">Guests</div>
                            <div class="item-content">{{reservation.guests}} Guests</div>
                        </div>

                        <div class="res-item">
                            <div class="item-title">You will earn</div>
                            <div class="item-content">{{$Settings.Price(reservation.invoice.subtotal)}}</div>
                        </div>

                        <div class="res-item">
                            <div class="item-title">Reservation Code</div>
                            <div class="item-content">{{reservation.reference}}</div>
                        </div>

                        <div class="res-item">
                            <div class="item-title">{{reservation.guest.fullname}} is your guest</div>
                            <div class="item-content">
                                <div class="content-with-action">
                                    <div class="content">Contact {{reservation.guest.name}} to coordinate the arrival
                                        time and key exchange
                                    </div>
                                    <div class="action error--text">{{reservation.guest.mobile}}</div>
                                </div>
                            </div>
                        </div>

                        <div class="res-item">
                            <div class="item-title">Reservation Adjustments</div>
                            <nuxt-link :to="{name: 'hosting-reservations-ref-adjustments', params:{ref: $route.params.ref}}" class="item-content">View Adjustments</nuxt-link>
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
        name: "HostReservationDetails",
        layout: 'hosting',
        data: () => {
            return {
                created: false,
                working: true,
                reservation: {},
                review: {
                    rating: 0,
                    review: ""
                }
            }
        },
        mounted() {
            this.$axios.get(this.$api.Reservation.Details(this.$route.params.ref))
                .then((r) => {
                    this.reservation = r.data
                    this.created = true
                })
        },
        methods: {
            to_date(date) {
                return moment(date, this.$Settings.MySqlDate).format("MMMM DD, YYYY")
            },
            to_day(date) {
                return moment(date, this.$Settings.MySqlDate).format("dddd")
            },
            accept() {
                this.$axios.put(this.$api.Reservation.Accept(this.reservation.reference))
                    .then((r) => {
                        this.reservation.status = r.data.status
                    })
            },
            decline() {
                this.$axios.put(this.$api.Reservation.Reject(this.reservation.reference))
                    .then((r) => {
                        this.reservation.status = r.data.status
                    })
            },
            rate(){
                let api = this.$api.Reservation.ReviewYourGuest
                let data = {
                    reservation: this.reservation.reference,
                    rating: this.review.rating,
                    review: this.review.review,
                }

                this.$axios.post(api, data)
                    .then((r)=> {
                        this.reservation.guest_review = r.data
                    })
            }
        }
    }
</script>

<style lang="scss" scoped>
    .write-review h3 {
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 10px;
    }


    .section-title{
        font-size: 22px;
        line-height: 38px;
        font-weight: 500;
    }
    .guest-quote {
        background-color: #f4f4f4;
        font-size: .95rem;
        padding: 15px;
        width: calc(100% - 60px);
        float: left;
        position: relative;
    }

    .guest-quote-card {
        position: relative;
        overflow: hidden;
        margin-top: 10px;
        margin-bottom: 40px;
    }

    .guest-card {
        float: right;
        width: 60px;
        text-align: right;
    }

    .guest-quote:after {
        border-style: solid;
        content: "";
        border-color: transparent transparent transparent #f4f4f4;
        border-width: 14px;
        position: absolute;
        top: 5px;
        right: -24px;
    }


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
                        font-size: 16px;
                        line-height: 22px;
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
