<template>
    <div class="booking-page confirm-reservation  mt-8 mb-8">
        <v-container grid-list-xl v-if="created">
            <v-layout wrap>
                <v-flex xs8>
                    <v-form lazy-validation v-model="valid" ref="form" @submit.prevent="FormSubmit">
                        <div class="booking-content">
                            <h1 class="page-title mb-12">Who is Coming?</h1>

                            <div class="form-group mb-5">
                                <label>Guests</label>
                                <v-select
                                        :rules="[rules.required]"
                                        :items="$Settings.GuestsList(reservation.place.max_guest)"
                                        v-model="form.guests"
                                        label="Number of guests"
                                        solo
                                        flat
                                ></v-select>
                            </div>

                            <div class="form-group mb-5">
                                <label>Say hello to your guest</label>
                                <p>Let {{reservation.place.host.name}} know a little about yourself and why you’re
                                    coming.</p>

                                <v-textarea
                                        :rules="[rules.required]"
                                        v-model="form.wc_message"
                                        label=""
                                        solo
                                        flat
                                ></v-textarea>
                            </div>

                            <div class="form-group mb-5">
                                <label>Reason for travel?</label>
                                <p>Tell us why you’re traveling. It will help us suggest activities for your trip and
                                    improve our product.</p>

                                <v-text-field
                                        :rules="[rules.required]"
                                        v-model="form.reason"
                                        label="Tell us why you’re traveling"
                                        solo
                                        flat
                                ></v-text-field>
                            </div>

                            <div class="form-group">
                                <v-checkbox
                                        color="primary"
                                        v-model="agree"
                                        label="I agree to the House Rules and Cancellation Policy. I also agree to pay the total amount shown, which includes Service Fees."
                                        solo
                                        flat
                                ></v-checkbox>

                            </div>

                            <v-btn color="primary"
                                   v-if="reservation.invoice.subtotal > 0"
                                   type="submit"
                                   :disabled="working || !agree"
                                   :loading="working"
                                   class="tall wider"><i class="la la-lock mr-2"></i> Proceed to Payment
                            </v-btn>
                            <v-btn color="primary"
                                   v-else
                                   @click="PayWithCredit"
                                   :disabled="working || !agree"
                                   :loading="working"
                                   class="tall wider"><i class="la la-lock mr-2"></i> Pay using Amar Atithi Credit
                            </v-btn>

                        </div>
                    </v-form>
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
        name: "WhoIsComing",
        components: {BookingPageSidebar},
        data: () => {
            return {
                valid: false,
                working: false,
                rules: [],
                created: false,
                agree: true,
                reservation: {
                    checkin: "",
                    checkout: ""
                },
                form: {
                    guests: 2,
                    wc_message: "",
                    reason: ""
                }
            }
        },
        created() {
            this.rules = this.$validator.rules
        },
        mounted() {
            let api = this.$api.Reservation.Details(this.$route.params.ref)

            this.$axios.get(api)
                .then((r) => {
                    this.reservation = r.data
                    this.created = true
                    this.form.guests = this.reservation.guests
                    this.form.reason = this.reservation.reason
                    this.form.wc_message = this.reservation.wc_message
                })
        },
        methods: {
            FormSubmit() {
                let check = new Promise((resolve, reject) => {
                    this.$refs.form.validate();
                    resolve();
                });

                check.then(() => {
                    if (this.valid) {
                        this.SaveAndProceed();
                    }
                });
            },

            SaveAndProceed() {

                this.working = true;

                this.$axios.put(this.$api.Reservation.Confirm(this.$route.params.ref), this.form)
                    .then((response) => {

                        this.$axios.post(this.$api.Reservation.Payment.GetPaymentURL, {reservation: this.$route.params.ref})
                            .then((response) => {
                                window.location = response.data
                            })
                            .finally(() => this.working = false)

                    })
                    .finally(() => this.working = false)
            },

            PayWithCredit(){
                this.working = true;
                let ref = this.$route.params.ref

                this.$axios.post(this.$api.Reservation.PayWithCredit(ref))
                    .then(()=> {
                        this.$router.push("/dashboard/reservations/"+ ref)
                    }).finally(() => this.working = false)
            }
        }
    }
</script>

<style lang="scss" scoped>

    .subtitle {
        font-size: 20px;
        font-weight: 600;
    }


</style>
