<template>
    <div class="change-reservation">
        <v-container grid-list-xl class="pa-0  mt-8 mb-8">
            <nuxt-link class="regular-link font-weight-bold" :to="{name: 'dashboard-reservations-ref', params:{ref: $route.params.ref}}" >Back to the reservation</nuxt-link>

            <h1 class="section-title mb-6 mt-2">Reservation Adjustments</h1>

            <table class="mb-6 table table-bordered">
                <thead>
                <tr>
                    <th class="text-left">Adjustment Reference</th>
                    <th class="text-left">Date</th>
                    <th>Status</th>
                    <th>Action</th>
                </tr>
                </thead>

                <tbody>
                <tr v-for="adjustment in adjustments">
                    <td>{{adjustment.reference}}</td>
                    <td>{{adjustment.created}}</td>
                    <td class="text-center">
                        <v-chip label small :color="adjustment.status.color">{{adjustment.status.details}}</v-chip>
                    </td>
                    <td style="width: 200px;" class="text-center">
                        <v-chip :to="{name: 'dashboard-reservations-ref-adjustments-code', params: {ref: $route.params.ref, code: adjustment.reference}}"
                                label small color="primary">View Details
                        </v-chip>
                    </td>
                </tr>
                </tbody>
            </table>

            <v-btn @click="CanRequestForChanges" :disbled="working" :loading="working" large color="primary" >
                Request Additional Change
            </v-btn>

            <div v-if="request_error" class="error--text mt-3 font-size-lg">{{request_error}}</div>

            <!--<div class="pending-request" v-if="reservation && pending && pending != undefined">-->
            <!--<h2>Recent Adjustment Request</h2>-->

            <!--<div class="changes-tab">-->
            <!--<v-container class="pa-0" fluid>-->
            <!--<v-layout wrap>-->
            <!--<v-flex xs6>-->
            <!--<h3 class="details-title">Original Details</h3>-->
            <!--<table class="changes-table">-->
            <!--<tbody>-->
            <!--<tr>-->
            <!--<td class="font-weight-bold">Check-In</td>-->
            <!--<td>{{pending.original_start}}</td>-->
            <!--</tr>-->

            <!--<tr>-->
            <!--<td class="font-weight-bold">Checkout</td>-->
            <!--<td>{{pending.original_end}}</td>-->
            <!--</tr>-->
            <!--<tr>-->
            <!--<td class="font-weight-bold">Number of Guests</td>-->
            <!--<td>1</td>-->
            <!--</tr>-->
            <!--</tbody>-->
            <!--</table>-->
            <!--</v-flex>-->

            <!--<v-flex xs6>-->
            <!--<h3 class="details-title">New Details</h3>-->

            <!--<table class="changes-table">-->
            <!--<tbody>-->
            <!--<tr>-->
            <!--<td class="font-weight-bold">Check-In</td>-->
            <!--<td>{{pending.start}}</td>-->
            <!--</tr>-->

            <!--<tr>-->
            <!--<td class="font-weight-bold">Checkout</td>-->
            <!--<td>{{pending.end}}</td>-->
            <!--</tr>-->
            <!--<tr>-->
            <!--<td class="font-weight-bold">Number of Guests</td>-->
            <!--<td>1</td>-->
            <!--</tr>-->
            <!--</tbody>-->
            <!--</table>-->
            <!--</v-flex>-->
            <!--</v-layout>-->
            <!--</v-container>-->
            <!--</div>-->


            <!--<div class="additional-charges" v-if="pending.ttype != 'NONE'">-->

            <!--<v-alert type="warning" class="mb-6" v-if="pending.status.code == 1 && !pending.confirmed" >Your request has been accepted. Please complete the additional payment to adjust the changes.</v-alert>-->

            <!--<h3 class="details-title">{{ pending.ttype == 'DEBIT' ? "Additional Charges": "Refund Charges"}}</h3>-->

            <!--<div class="price-list" >-->
            <!--<div class="price-item d-flex" v-for="item in pending.invoice.charges_details" >-->
            <!--<span>{{item.label}}</span>-->
            <!--<span class="tCost">{{ $Settings.Price(item.amount)}}</span>-->
            <!--</div>-->

            <!--<div class="price-item d-flex">-->
            <!--<span>Sub Total</span>-->
            <!--<strong class="tCost">{{ $Settings.Price(pending.invoice.subtotal)}}</strong>-->
            <!--</div>-->
            <!--</div>-->

            <!--<v-btn-->
            <!--@click="ConfirmPayment"-->
            <!--type="submit"-->
            <!--color="primary"-->
            <!--class="tall wider"-->
            <!--:disabled="working"-->
            <!--:loading="payment_loading" ><v-icon small class="mr-3">lock</v-icon> Pay and Confirm</v-btn>-->
            <!--</div>-->

            <!--<div class="submit-wrap" v-if="pending.status.code <= 1 && pending.confirmed == false">-->
            <!--<hr>-->

            <!--<div v-if="pending.status.code == 0" >The alternation request is pending. You will be notified when there is a response.</div>-->
            <!--<div v-if="pending.status.code == 1 && pending.confirmed == false" >The alternation request has been accepted. However you can still choose to cancel it.</div>-->
            <!--<v-btn-->
            <!--@click="CancelRequest"-->
            <!--type="submit"-->
            <!--color="error"-->
            <!--class="tall wider"-->
            <!--:disabled="working"-->
            <!--:loading="cancel_loading"-->
            <!--&gt;Cancel Request</v-btn>-->
            <!--</div>-->
            <!--</div>-->
        </v-container>
    </div>
</template>

<script>
    export default {
        name: "ReservationAdjustments",
        layout: 'dashboard',
        data: () => {
            return {
                adjustments: [],
                pending: undefined,
                reservation: {},
                working: false,
                loaded: false,
                request_error: ""

            }
        },
        computed: {
            hasPendingAdjustment() {

            }
        },
        mounted() {
            this.$axios.get(this.$api.Reservation.Details(this.$route.params.ref))
                .then((r) => {
                    this.reservation = r.data
                    this.loaded = true
                })

            this.$axios.get(this.$api.Reservation.Adjustments.List(this.$route.params.ref))
                .then((res) => {
                    this.adjustments = res.data

                    if (this.adjustments.length) {
                        this.pending = this.adjustments[this.adjustments.length - 1]
                    }

                    //
                    //
                    // res.data.forEach((adj)=> {
                    //     if (adj.status.code <= 1 && adj.confirmed == false){
                    //         this.pending = adj
                    //     }
                    // })
                })
        },
        methods: {
            CanRequestForChanges(){
                this.working = true

                let api = this.$api.Reservation.Adjustments.CanRequestForChanges
                let data = {reference: this.$route.params.ref}

                this.$axios.post(api, data)
                    .then((response)=> {
                        if( response.data.error ){
                            this.request_error = response.data.message
                        } else {
                            this.$router.push({name: 'dashboard-reservations-ref-change-reservation', params:{ref: this.$route.params.ref}})
                        }
                    })
                    .finally(()=> {
                        this.working = false
                    })
            }
        }
    }
</script>

<style lang="scss" scoped>
    .section-title {
        font-size: 22px;
        line-height: 24px;
        font-weight: 600;
        margin-top: 0px;
        margin-bottom: 7px;
    }
</style>
