<template>
    <div class="booking-page payment-page  mt-8 mb-8">
        <v-container grid-list-xl v-if="created">
            <v-layout wrap>
                <v-flex xs8>
                    <div class="payment-form">
                        <h1 class="page-title mb-12">Complete Your Payment</h1>


                        <div class="payment-method-section">
                            <div class="pm-title mb-3">Choose your payment method?</div>

                            <v-radio-group style="width: 100%;" :mandatory="true" v-model="payment_method">
                                <div class="payment-method-list">
                                    <div class="payment-method-item">
                                        <div class="check">
                                            <v-radio value="bkash"></v-radio>
                                        </div>

                                        <div class="method-details">
                                            <div class="method-title">bKash</div>
                                            <div class="method-description">Pay with your personal or merchant bKash
                                                account.
                                            </div>
                                        </div>
                                    </div>

                                    <div class="payment-method-item">
                                        <div class="check">
                                            <v-radio value="card"></v-radio>
                                        </div>


                                        <div class="method-details">
                                            <div class="method-title">Card</div>
                                            <div class="method-description">Pay with visa/mastercard/american express.
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </v-radio-group>

                        </div>

                        <div class="payment-method-details mt-2">
                            <div v-if="payment_method == 'bkash'" class="payment-form-view">
                                <div class="payment-title">Payment Instruction</div>

                                <ol class="instruction-list pl-8">
                                    <li>Pay by USSD</li>
                                    <li>Dial *247# to view bKash Menu</li>
                                    <li>Press 3 for "Payments"</li>
                                    <li>Enter Amar Atithi Merchant Number: <strong>01711111111</strong></li>
                                    <li>Enter total amount : $250</li>
                                    <li>Enter Reference Number : <strong>{{ $route.params.ref }}</strong></li>
                                    <li>Enter 1 for the bKash Counter No</li>
                                    <li>Verify your payment by entering your pin</li>
                                    <li>Enter the TrxID below</li>
                                </ol>

                                <div class="form-group mt-6 mb-3">
                                    <label>TrxID</label>
                                    <v-text-field
                                            solo
                                            flat
                                            label="Enter the bKash Transaction ID"
                                            v-model="payment.bkash.ref"
                                    ></v-text-field>
                                </div>

                                <v-btn
                                        color="primary"
                                        @click="VerifyBkash"
                                        :working="payment.bkash.working"
                                        :loading="payment.bkash.working"
                                        class="tall">Request to Book
                                </v-btn>
                            </div>

                            <div v-if="payment_method == 'card'" class="payment-form-view">

                                <v-alert v-if="payment.card.error" type="error">{{payment.card.error}}</v-alert>

                                <v-form lazy-validation v-model="payment.card.valid" ref="CardForm" @submit.prevent="CardFormSubmit" >
                                    <div class="form-group">
                                        <label>Card Number</label>
                                        <v-text-field
                                                v-model="payment.card.form.ccNo"
                                                :rules="[rules.required]"
                                                solo
                                                flat
                                                label="1234 5678 9012 3456"></v-text-field>
                                    </div>

                                    <div class="form-group">
                                        <label>Name on the card</label>
                                        <v-text-field
                                                v-model="payment.card.form.name"
                                                :rules="[rules.required]"
                                                solo
                                                flat
                                                label="Ex: Jhon Doe"></v-text-field>
                                    </div>

                                    <v-layout row wrap>
                                        <v-flex xs6>
                                            <div class="form-group">
                                                <label>Expire Date</label>
                                                <div class="oh">
                                                    <div class="w50">
                                                        <v-select
                                                                v-model="payment.card.form.expMonth"
                                                                :items="months"
                                                                :rules="[rules.required]"
                                                                solo
                                                                flat
                                                                label="Month"></v-select>
                                                    </div>
                                                    <div class="w50">
                                                        <v-select
                                                                v-model="payment.card.form.expYear"
                                                                :items="year"
                                                                :rules="[rules.required]"
                                                                solo
                                                                flat
                                                                label="Year"></v-select>
                                                    </div>
                                                </div>
                                            </div>
                                        </v-flex>

                                        <v-flex xs6>
                                            <div class="form-group">
                                                <label>CVV</label>
                                                <v-text-field
                                                        v-model="payment.card.form.cvv"
                                                        :rules="[rules.required]"
                                                        label="* * *"
                                                        solo
                                                        flat></v-text-field>
                                            </div>
                                        </v-flex>
                                    </v-layout>

                                    <div class="form-group">
                                        <v-btn
                                                :disabled="this.payment.card.working"
                                                :loading="this.payment.card.working"
                                                type="submit"
                                                block
                                                color="primary"
                                                large class="tall">
                                            <i class="la la-lock mr-2"></i>
                                            <span>Pay Now</span>
                                        </v-btn>
                                    </div>

                                </v-form>
                            </div>
                        </div>
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

    export default {
        name: "GuestResPayment",
        components: {BookingPageSidebar},
        data: () => {
            return {
                created: false,
                rules: [],
                payment_method: "card",
                payment: {
                    bkash: {
                        ref: "",
                        working: false
                    },
                    card: {
                        valid: false,
                        form: {
                            sellerId: "901412706",
                            publishableKey: "336B023A-60D6-4EDA-A0D6-B3AECC7C8B8C",
                            ccNo: "",
                            name: "",
                            expMonth: "",
                            expYear: "",
                            cvv: "",
                            token: null,
                        },
                        working: false,
                        error: ""
                    }
                },
                reservation: {
                    checkin: "",
                    checkout: ""
                },
            }
        },
        methods: {
            VerifyBkash() {
                let res_ref = this.$route.params.ref
                let api = this.$api.Reservation.Payment.VerifyBkash(res_ref)

                this.payment.bkash.working = true

                this.$axios.put(api, {bkash_ref: this.payment.bkash.ref})
                    .then(() => {
                        this.$router.push({name: "dashboard-reservations-ref", params: {ref: res_ref}})
                    })
                    .finally(() => {
                        this.working = false
                    })
            },
            CardFormSubmit(){

                let check = new Promise((resolve, reject) => {
                    this.$refs.CardForm.validate();
                    resolve();
                });

                check.then(() => {
                    if ( this.payment.card.valid )
                        this.PayWithCard();
                });
            },
            PayWithCard(){
                let args = this.payment.card.form
                let $that = this;
                let ref = $that.$route.params.ref

                this.payment.card.working = true
                this.payment.card.error = ""

                window.TCO.loadPubKey("sandbox", function() {
                    console.log("loaded")

                    window.TCO.requestToken(function (data) {

                        $that.payment.card.form.token = data.response.token.token
                        let apiRoute = $that.$api.Reservation.Payment.Card( ref )

                        console.log(apiRoute)
                        console.log($that.payment.card.form)

                        $that.$axios.post( apiRoute, $that.payment.card.form)
                            .then((r)=> {
                                console.log("Success")
                                $that.$router.push({name: 'dashboard-reservations-ref', params: {ref: ref}})
                            })
                            .catch((error)=> {

                                if ( error.response )
                                    $that.payment.card.error = error.response.data

                            })
                            .finally(()=> {
                                $that.payment.card.working = false
                            })


                    }, function (error) {
                        console.log(error.errorMsg)

                        $that.payment.card.error = error.errorMsg
                        $that.payment.card.working = false

                    }, args);
                })


            }
        },
        computed: {
            months(){
                let list = []

                for ( let i = 1; i <= 12; i++ )
                    list.push(i)

                return list
            },
            year(){
                let list = []

                for ( let i = 2019; i <= 2050; i++ )
                    list.push(i)

                return list
            }
        },
        mounted() {
            this.rules = this.$validator.rules

            let api = this.$api.Reservation.Details(this.$route.params.ref)

            this.$axios.get(api)
                .then((r) => {
                    this.reservation = r.data
                    this.created = true
                })
        },
    }
</script>

<style lang="scss" scoped>

    .subtitle {
        font-size: 20px;
        font-weight: 600;
    }

    .pm-title {
        font-size: 18px;
        font-weight: 600;
    }

    .payment-method-item {
        display: table;
        border: 1px solid rgb(235, 235, 235);
        padding: 25px;
        margin-bottom: 10px;
        border-radius: 4px;
        width: 100%;


        .check {
            display: table-cell;
            vertical-align: middle;
            width: 30px;
            text-align: center;
            max-width: 40px;
        }

        .method-title {
            font-weight: 600;
            margin-bottom: 2px;
            display: block;
        }
    }

    .payment-form-view {
        .payment-title {
            margin-bottom: 10px;
            font-weight: 600;
        }


        .oh {
            overflow: hidden;
            margin: 0 -4px;
        }

        .w50 {
            width: 50%;
            float: left;
            padding: 0 5px;
        }
    }


</style>