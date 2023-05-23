<template>
    <div class="change-reservation">
        <v-container grid-list-xl class="pa-0  mt-8 mb-8" >
            <nuxt-link class="regular-link font-weight-bold" :to="{name: 'dashboard-reservations-ref', params:{ref: $route.params.ref}}" ><< Back to the reservation</nuxt-link>


            <h1 class="section-title mb-6 mt-4">Change Reservation</h1>


            <div class="quote-form">
                <v-form lazy-validation v-model="form.valid" ref="form" @submit.prevent="FormSubmit">
                    <div class="form-group">
                        <label>Guests</label>
                        <v-select
                                :rules="[rules.required]"
                                :items="GuestsList"
                                label="Number of guests"
                                solo
                                flat
                                v-model="form.guest"
                        ></v-select>
                    </div>

                    <v-container class="pa-0" fluid>
                        <v-layout wrap>
                            <v-flex xs6 v-if="!isPast(reservation.checkin)">
                                <div class="form-group">
                                    <label>Check-in</label>

                                    <v-menu
                                            v-model="picker.checkin"
                                            :close-on-content-click="false"
                                            :nudge-right="40"
                                            transition="scale-transition"
                                            offset-y
                                            full-width
                                            min-width="290px"
                                    >
                                        <template v-slot:activator="{ on }">
                                            <v-text-field
                                                    :rules="[rules.required]"
                                                    label="Check-in Date"
                                                    solo
                                                    flat
                                                    v-model="form.checkin"
                                                    v-on="on"
                                            ></v-text-field>
                                        </template>
                                        <v-date-picker
                                                :min="tomorrow"
                                                no-title
                                                v-model="form.checkin"
                                                @input="picker.checkin = false"></v-date-picker>
                                    </v-menu>
                                </div>
                            </v-flex>

                            <v-flex xs6>
                                <div class="form-group">
                                    <label>Checkout</label>

                                    <v-menu
                                            v-model="picker.checkout"
                                            :close-on-content-click="false"
                                            :nudge-right="40"
                                            transition="scale-transition"
                                            offset-y
                                            full-width
                                            min-width="290px"
                                    >
                                        <template v-slot:activator="{ on }">
                                            <v-text-field
                                                    :rules="[rules.required]"
                                                    label="Checkout Date"
                                                    solo
                                                    flat
                                                    v-model="form.checkout"
                                                    v-on="on"
                                            ></v-text-field>
                                        </template>
                                        <v-date-picker
                                                :min="form.checkin"
                                                no-title
                                                scrollable
                                                v-model="form.checkout"
                                                @input="picker.checkout = false"></v-date-picker>
                                    </v-menu>
                                </div>
                            </v-flex>
                        </v-layout>
                    </v-container>

                    <v-btn
                            type="submit"
                            color="primary"
                            class="tall wider"
                            :disabled="form.working"
                            :loading="form.working"
                    >Get a Quote</v-btn>
                </v-form>
            </div>

            <div class="font-size-lg error--text mt-4" v-if="form.response.error">{{form.response.message}}</div>

            <template v-if="form.QueryComplete && !form.response.error">
                <div class="changes-tab">
                    <v-container class="pa-0" fluid>
                        <v-layout wrap>
                            <v-flex xs6>
                                <h3 class="details-title">Original Details</h3>
                                <table class="changes-table">
                                    <tbody>
                                    <tr>
                                        <td class="font-weight-bold">Check-In</td>
                                        <td>{{reservation.checkin}}</td>
                                    </tr>

                                    <tr>
                                        <td class="font-weight-bold">Checkout</td>
                                        <td>{{reservation.checkout}}</td>
                                    </tr>
                                    <tr>
                                        <td class="font-weight-bold">Number of Guests</td>
                                        <td>{{reservation.guests}}</td>
                                    </tr>
                                    </tbody>
                                </table>
                            </v-flex>

                            <v-flex xs6>
                                <h3 class="details-title">New Details</h3>

                                <table class="changes-table">
                                    <tbody>
                                    <tr>
                                        <td class="font-weight-bold">Check-In</td>
                                        <td>{{query.checkin}}</td>
                                    </tr>

                                    <tr>
                                        <td class="font-weight-bold">Checkout</td>
                                        <td>{{query.checkout}}</td>
                                    </tr>
                                    <tr>
                                        <td class="font-weight-bold">Number of Guests</td>
                                        <td>{{query.guests}}</td>
                                    </tr>
                                    </tbody>
                                </table>
                            </v-flex>
                        </v-layout>
                    </v-container>
                </div>

                <div class="additional-charges" v-if="form.response.type != 'NONE'">
                    <h3 class="details-title">{{form.response.type == 'DEBIT' ? "Additional Charges": "Refund Charges"}}</h3>

                    <div class="price-list" >
                        <div class="price-item d-flex" v-for="item in form.response.breakdown" >
                            <span>{{item.label}}</span>
                            <span class="tCost">{{ $Settings.Price(item.total_cost)}}</span>
                        </div>

                        <div class="price-item d-flex">
                            <span>Sub Total</span>
                            <strong class="tCost">{{ $Settings.Price(form.response.subtotal)}}</strong>
                        </div>
                    </div>
                </div>

                <div class="submit-wrap">
                    <v-container grid-list-xl class="pa-0" >
                        <v-layout row wrap>
                            <v-flex xs12 sm8>
                                <div class="d-flex" v-if="form.response.type != 'NONE'">
                                    <v-checkbox class="ma-0" v-model="agree" color="primary"></v-checkbox>
                                    <div class="notes" v-if="form.response.type =='DEBIT'">If you host accept the changes, I have pay additional {{form.response.subtotal}} BDT to confirm this adjustment.</div>
                                    <div class="notes" v-if="form.response.type =='CREDIT'">If you host accept the changes, I have receive {{form.response.subtotal}} BDT as Amar Atithi Credit.</div>
                                </div>
                            </v-flex>

                            <v-flex xs12 sm4 class="text-right">
                                <v-btn :disabled="(form.response.type != 'NONE' && !agree) || form.working" @click="SubmitRequest" color="primary" large>Submit Request</v-btn>
                            </v-flex>
                        </v-layout>
                    </v-container>
                </div>
            </template>

        </v-container>
    </div>
</template>

<script>
    import moment from "moment";
    import {mapGetters} from 'vuex'

    export default {
        name: "change-reservation",
        layout: 'dashboard',
        data: () => {
            return {
                rules: [],
                picker: {
                    checkin: false,
                    checkout: false
                },
                form: {
                    checkin: null,
                    checkout: null,
                    guest: 1,
                    working: false,
                    QueryComplete: false,
                    valid: false,
                    response: {
                        error: false,
                        type: ""
                    }
                },
                query: {},
                agree: false,
                reservation: {
                    place: {}
                }
            }
        },
        computed: {
            ...mapGetters(['isAuthenticated', 'loggedInUser']),
            GuestsList() {
                let items = []

                for (let i = 1; i <= this.reservation.place.max_guest; i++) {
                    items.push({
                        text: i > 1 ? `${i} guests` : `${i} guest`,
                        value: i
                    })
                }

                return items
            },
            tomorrow() {
                var today = moment();
                var tomorrow = moment(today).add(1, 'days');
                return tomorrow.format(this.$Settings.MySqlDate)
            },
        },
        mounted() {
            this.rules = this.$validator.rules

            this.$axios.get(this.$api.Reservation.Details(this.$route.params.ref))
                .then((r)=> {
                    this.reservation = r.data
                    this.form.guest = this.reservation.guests
                    this.form.checkin = this.reservation.checkin
                    this.loaded = true
                })
        },
        methods: {
            isPast(){
                if ( !this.reservation )
                    return

                let date = moment(this.reservation.checkin).format('YYYY-MM-DD');

                return moment().diff(date) > 0
            },
            FormSubmit() {
                this.form.QueryComplete = false

                let check = new Promise((resolve, reject) => {
                    this.$refs.form.validate();
                    resolve();
                });

                check.then(() => {
                    if (this.form.valid) {
                        this.GetAQuote();
                    }
                });
            },
            GetAQuote() {
                this.form.working = true

                let data = {
                    guests: this.form.guest,
                    checkin: this.form.checkin,
                    checkout: this.form.checkout,
                    reference: this.$route.params.ref
                }

                this.query = data

                this.$axios.post(this.$api.Reservation.Change, data)
                    .then(r => {
                        this.form.response = r.data
                        this.form.QueryComplete = true
                    })
                    .finally(() => {
                        this.form.working = false
                    })
            },

            SubmitRequest(){
                this.form.working = false

                this.$axios.post(this.$api.Reservation.ChangeRequest, this.query)
                    .then(r => {
                        let rref = this.$route.params.ref
                        let aref = r.data.adjustment.reference

                        this.$router.push({name: 'dashboard-reservations-ref-adjustments-code', params: {ref: rref, code: aref}})
                    })
                    .finally(() => {
                        this.form.working = false
                    })
            }
        }
    }
</script>

<style lang="scss" scoped>
    h3.details-title {
        font-size: 18px;
        margin: 0 0 10px;
    }

    table.changes-table {
        width: 100%;
        border-collapse: collapse;
    }

    table.changes-table tr td {
        border-bottom: 1px solid #ddd;
        padding: 10px 0px;
        margin: 0;
    }

    .changes-tab {
        margin: 50px 0;
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





    .submit-wrap {
        padding: 20px 0 0;
        border-top: 1px solid #ddd;
        margin-top: 35px;
    }

    .additional-charges {
        max-width: 600px;
        /* float: right; */
    }


    .notes {
        margin-top: 5px;
    }

    .section-title{
        font-size: 22px;
        line-height: 24px;
        font-weight: 600;
        margin-top: 0px;
        margin-bottom: 7px;
    }

</style>
