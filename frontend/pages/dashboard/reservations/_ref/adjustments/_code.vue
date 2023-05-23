<template>
    <div class="change-reservation">
        <v-container grid-list-xl class="pa-0 mt-8 mb-8" >

            <div class="pending-request" v-if="adjustment && loaded">
                <!--<h2 class="mb-6">Adjustment Request: #{{adjustment.reference}}</h2>-->
                <nuxt-link class="regular-link font-weight-bold" :to="{name: 'dashboard-reservations-ref-adjustments', params:{ref: adjustment.reservation.reference}}" ><< Back to all adjustments</nuxt-link>

                <AdjustmentDetailComponent :adjustment="adjustment" />


                <div class="additional-charges" v-if="adjustment.ttype != 'NONE' && (adjustment.status.code < 2 ||  adjustment.status.code <= 5)">

                    <v-alert type="warning" class="mb-6" v-if="adjustment.status.code == 1 && !adjustment.confirmed" >Your request has been accepted. Please complete the additional payment to adjust the changes.</v-alert>

                    <h3 class="details-title">{{ adjustment.ttype == 'DEBIT' ? "Additional Charges": "Refund Charges"}}</h3>

                    <div class="price-list" >
                        <div class="price-item d-flex" v-for="item in adjustment.invoice.charges_details" >
                            <span>{{item.label}}</span>
                            <span class="tCost">{{ $Settings.Price(item.amount)}}</span>
                        </div>

                        <div class="price-item d-flex">
                            <span>Sub Total</span>
                            <strong class="tCost">{{ $Settings.Price(adjustment.invoice.subtotal)}}</strong>
                        </div>
                    </div>

                    <template v-if="adjustment.confirmed == false && adjustment.status.code == 1">
                        <v-btn
                                @click="ConfirmPayment"
                                type="submit"
                                color="primary"
                                class="tall wider"
                                :disabled="working"
                                :loading="payment_loading" ><v-icon small class="mr-3">lock</v-icon> Pay and Confirm</v-btn>

                        <div v-if="payment_error" class="font-size-lg error--text mt-3">{{payment_error}}</div>
                    </template>
                </div>

                <div class="submit-wrap" v-if="adjustment.status.code <= 1 && adjustment.confirmed == false">
                    <hr>

                    <div v-if="adjustment.status.code == 0" >The alternation request is pending. You will be notified when there is a response.</div>
                    <div v-if="adjustment.status.code == 1 && adjustment.confirmed == false" >The alternation request has been accepted. However you can still choose to cancel it.</div>
                    <v-btn
                            @click="CancelRequest"
                            type="submit"
                            color="error"
                            class="tall wider"
                            :disabled="working"
                            :loading="cancel_loading"
                    >Cancel Request</v-btn>
                </div>

            </div>


        </v-container>
    </div>
</template>

<script>
    import AdjustmentDetailComponent from "../../../../../components/general/AdjustmentDetail";
    export default {
        name: "AdjustmentDetailPage",
        components: {AdjustmentDetailComponent},
        layout: 'dashboard',
        data: ()=> {
            return {
                adjustment: {},
                working: false,
                loaded: false,
                payment_loading: false,
                cancel_loading: false,
                payment_error: ""
            }
        },
        mounted() {
            this.$axios.get(this.$api.Reservation.Adjustments.Details(this.$route.params.code))
                .then((r)=> {
                    this.adjustment = r.data
                    this.loaded = true
                })
        },
        methods:{
            ConfirmPayment(){
                this.working = true
                this.payment_loading = true

                this.$axios.post(this.$api.Reservation.Adjustments.PaymentURL(this.adjustment.reference))
                    .then((res)=> {
                        if( res.data.error == false ){
                          window.location = res.data.url
                        } else {
                            this.payment_error = res.data.message
                        }
                    })
                    .finally(()=> {
                        this.working = false
                        this.payment_loading = false
                    })
            },
            CancelRequest(){
                this.working = true
                this.cancel_loading = true

                this.$axios.put(this.$api.Reservation.Adjustments.Cancel(this.adjustment.reference))
                    .then((res)=> {
                        this.adjustment = res.data
                    })
                    .finally(()=> {
                        this.working = false
                        this.cancel_loading = false
                    })
            }
        }
    }
</script>

<style lang="scss" scoped>

    .details-title{
        margin-bottom: 10px;
    }







    .submit-wrap{
        text-align: right;
        hr {
            margin-bottom: 20px;
        }

        > div {
            margin-bottom: 15px;
        }
    }


    .additional-charges {
        max-width: 600px;
        margin: 0 0 50px 0;
    }

    .price-list {
        margin: 0 0 15px;
    }

    .price-item {
        padding: 10px 0;
        border-bottom: 1px solid #ddd;
        font-weight: 700;

        &:last-child{
            border-bottom: 0;
        }

        .tCost {
            margin-left: auto;
            font-weight: normal;
        }
    }


</style>
