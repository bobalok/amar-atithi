<template>
    <div class="change-reservation">
        <v-container grid-list-xl class="pa-0 mt-8 mb-8" >

            <div class="pending-request" v-if="adjustment && loaded">
                <!--<h2 class="mb-6">Adjustment Request: #{{adjustment.reference}}</h2>-->
                <nuxt-link class="regular-link font-weight-bold" :to="{name: 'hosting-reservations-ref-adjustments', params:{ref: adjustment.reservation.reference}}" ><< Back to all adjustments</nuxt-link>

                <AdjustmentDetailComponent :adjustment="adjustment" />


                <div class="submit-wrap" v-if="adjustment.status.code == 0">
                    <v-btn
                            @click="CancelRequest"
                            type="submit"
                            color="error"
                            class="tall wider"
                            :disabled="working"
                    >Decline Changes</v-btn>

                    <v-btn
                            @click="Accept"
                            type="submit"
                            color="primary"
                            class="tall wider ml-2"
                            :disabled="working"
                    >Accept Changes</v-btn>
                </div>

            </div>


        </v-container>
    </div>
</template>

<script>
    import AdjustmentDetailComponent from "../../../../../components/general/AdjustmentDetail";

    export default {
        name: "HostingAdjustmentView",
        layout: 'hosting',
        components: {AdjustmentDetailComponent},
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
            },

            Accept(){
                this.working = true
                this.cancel_loading = true

                this.$axios.put(this.$api.Reservation.Adjustments.Accept(this.adjustment.reference))
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
    .submit-wrap{
        text-align: right;
        hr {
            margin-bottom: 20px;
        }

        > div {
            margin-bottom: 15px;
        }
    }
</style>
