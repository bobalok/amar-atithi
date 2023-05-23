<template>
    <div class="change-reservation">
        <v-container grid-list-xl class="pa-0  mt-8 mb-8">
            <nuxt-link class="regular-link font-weight-bold" :to="{name: 'hosting-reservations-ref', params:{ref: $route.params.ref}}" >Back to the reservation</nuxt-link>

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
                        <v-chip :to="{name: 'hosting-reservations-ref-adjustments-code', params: {ref: $route.params.ref, code: adjustment.reference}}"
                                label small color="primary">View Details
                        </v-chip>
                    </td>
                </tr>
                </tbody>
            </table>



        </v-container>
    </div>
</template>

<script>
    export default {
        name: "HostingAdjustments",
        layout: 'hosting',
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

        }
    }
</script>

<style scoped>

</style>
