<template>
    <div class="right-side">
        <div class="place-card">
            <div class="place-image">
                <img :src="reservation.place.cover.file" alt="">

                <div class="host-image">
                    <img :src="reservation.place.host.avatar" alt="">
                </div>
            </div>

            <div class="place-meta">
                <div class="host-name">Hosted by {{reservation.place.host.name}}</div>
                <h2 class="section-title">{{reservation.place.title}}</h2>
                <div class="place-type">{{reservation.place.space.name}}</div>
                <div class="rating-review d-flex">
                    <StarRating />
                    <span>94 Reviews</span>
                </div>
            </div>
        </div>

        <div class="check-block">
            <v-container class="pa-0" fluid>
                <v-layout wrap>
                    <v-flex xs6>
                        <div class="checkitem">
                            <div><strong>Check-in</strong></div>
                            <div>{{checkin}}</div>
                        </div>
                    </v-flex>

                    <v-flex xs6>
                        <div class="checkitem text-right">
                            <div><strong>Checkout</strong></div>
                            <div>{{checkout}}</div>
                        </div>
                    </v-flex>
                </v-layout>
            </v-container>
        </div>

        <div class="charges">
            <div class="charge-item" v-for="charge in reservation.invoice.charges_details">
                <span class="item">{{ charge.label }}</span>
                <span class="cost">{{ $Settings.Price(charge.amount) }}</span>
            </div>

            <div class="charge-item charge-total">
                <span class="item">Total</span>
                <span class="cost">{{$Settings.Price(reservation.invoice.subtotal )}}</span>
            </div>
        </div>
    </div>
</template>

<script>
    import StarRating from "../../components/general/StarRating";
    import moment from "moment";
    export default {
        name: "BookingPageSidebar",
        components: {StarRating},
        props: ['reservation'],
        computed: {
            checkin(){
                return this.reservation.checkin ? moment(this.reservation.checkin, this.$Settings.MySqlDate).format("MMM DD, YYYY") : ""
            },
            checkout(){
                return this.reservation.checkout ? moment(this.reservation.checkout, this.$Settings.MySqlDate).format("MMM DD, YYYY") : ""
            }
        }
    }
</script>

<style lang="scss" scoped>
    .right-side {
        border: 1px solid #dadada;
        padding: 20px;



        .host-image {
            float: right;
            margin-top: -27px;
            position: relative;
            z-index: 1;
            margin-right: 20px;

            img {
                width: 50px;
                height: 50px;
                border-radius: 100%;
                border: 3px solid #fff;
            }
        }

        .place-image {
            margin: -20px -20px 15px -20px;
        }

        .place-meta .section-title {
            font-size: 20px;
            line-height: 24px;
            font-weight: 600;
            margin-top: 5px;
            margin-bottom: 7px;
        }

        .rating-review {
            margin-top: 2px;

            > span {
                margin-top: -3px;
                margin-left: 10px;
            }
        }



        .check-block {
            padding: 15px 0;
            border-top: 1px solid #dadada;
            border-bottom: 1px solid #dadada;
            margin-top: 15px;


        }
        .charges {
            margin-top: 20px;

            .charge-item {
                padding: 0 0 8px 0;

                &.charge-total {
                    border-top: 1px solid #ddd;
                    padding-top: 8px;
                    margin-top: 8px;
                    font-weight: 600;
                }

                .cost {
                    float: right;
                }
            }
        }





    }
</style>