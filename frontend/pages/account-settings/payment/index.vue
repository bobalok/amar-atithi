<template>
    <v-container>
        <div class="payments">
            <div class="head">
                <h1>Payments & payouts</h1>
            </div>

            <div class="payment-tab">
                <nuxt-link to="/account-settings/payment" class="tab-item current">PAYMENTS</nuxt-link>
                <nuxt-link to="/account-settings/payment/transaction-history" class="tab-item">TRANSACTION HISTORY</nuxt-link>
            </div>

            <div class="content">
                <div class="section">

                    <v-alert v-if="success" type="success">Your payment request has been received</v-alert>
                    <v-alert v-if="error" type="error">Your payment request cannot be accepted</v-alert>

                    <h3 class="section-title">Amar Atithi Credit Balance</h3>
                    <div class="section-caption">
                        When you receive a payment for a reservation, we call that payment to you a credit.
                    </div>

                    <div class="credit-balance mb-4">
                        <label>Current credit balance</label>
                        <span>{{$Settings.Price(loggedInUser.credit)}}</span>
                    </div>



                    <template v-if="toggle">
                        <hr class="mt-4 pb-3" />

                        <h3 class="section-title mt-5">Request Payment</h3>

                        <div class="form-group mt-6">
                            <v-select v-model="form.method" :items="items" solo flat label="Payment Method"  ></v-select>
                        </div>

                        <div class="form-group mt-4 mb-2">
                            <v-text-field v-model="form.amount" solo flat label="Amount" ></v-text-field>
                        </div>


                        <div class="form-group mt-4 mb-2">
                            <v-text-field v-model="form.number" solo flat label="Account Number" ></v-text-field>
                        </div>

                        <v-btn color="primary" @click="Request" large>Send Payment Request</v-btn>
                    </template>
                    <v-btn @click="toggle = true" v-else color="primary" large>Request Payment</v-btn>


                </div>
            </div>
        </div>
    </v-container>
</template>

<script>
    import {mapGetters} from 'vuex'

    export default {
        name: "AccountPayment",
        middleware: 'auth',
        computed: {
            ...mapGetters(['isAuthenticated', 'loggedInUser'])
        },
        created() {
            this.rules = this.$validator.rules
        },
        data: ()=> {
            return {
                rules: [],
                amount: 100,
                toggle: false,
                method: "BKASH",
                items: [ "Bkash", "DBBL Mobile Banking - Rocket"],
                error: false,
                success: false,
                form: {
                    method: "",
                    amount: "",
                    number: ""
                }
            }
        },
        methods: {
            Request(){
                this.toggle = false

                this.$axios.post(this.$api.Reservation.Payment.Request, this.form)
                    .then((response)=> {
                        if( response.status == 200 ){
                            this.error = false
                            this.success = true
                        } else {
                            this.error = true
                            this.success = false
                        }
                    })
                    .catch(()=> {
                        this.error = true
                        this.success = false
                    })
            }
        }
    }
</script>

<style lang="scss" scoped>
    .head {
        margin: 36px 0 54px 0;

        h1 {
            font-size: 32px;
            font-weight: 800;
        }

        .handle {
            font-size: 16px;
            margin-top: 16px;
        }
    }


    .section-caption {
        font-size: 16px;
    }

    .payment-tab {
        border-bottom: 2px solid #e7e7e7;
        margin-bottom: 30px;
    }

    .payments {
        max-width: 768px;
        font-size: 16px;
        margin-bottom: 75px;
    }

    .payment-tab a {
        color: #484848;
        font-weight: 500;
        padding: 12px 20px 14px 0;
        display: inline-block;
        font-size: 14px;
    }

    .payment-tab a.current {
        color: #00897b;
    }

    .payment-tab a.current {
        border-bottom: 2px solid #00897b;
        margin-bottom: -2px;
    }

    h3.section-title {
        margin-bottom: 4px;
    }

    .credit-balance {
        display: flex;
        width: 100%;
        margin: 30px 0 10px 0;
    }

    .credit-balance span {
        margin-left: auto;
    }
</style>