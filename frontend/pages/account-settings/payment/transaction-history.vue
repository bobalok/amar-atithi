<template>
    <v-container>
        <div class="payments">
            <div class="head">
                <h1>Payments & payouts</h1>
            </div>

            <div class="payment-tab">
                <nuxt-link to="/account-settings/payment" class="tab-item ">PAYMENTS</nuxt-link>
                <nuxt-link to="/account-settings/payment/transaction-history" class="tab-item current">TRANSACTION HISTORY</nuxt-link>
            </div>

            <div class="content">

                <v-alert v-if="requests.length == 0" type="grey lighten-2 text--primary">No transaction history has been found.</v-alert>

                <table class="table table-bordered">
                    <thead>
                        <tr>
                            <th>Payment Method</th>
                            <th>Amount</th>
                            <th>Account Number</th>
                            <th>Status</th>
                        </tr>
                    </thead>

                    <tbody>
                    <tr v-for="req in requests">
                        <td>{{req.method}}</td>
                        <td>{{req.amount}}</td>
                        <td>{{req.number}}</td>
                        <td><v-chip label small :color="req.status.color" >{{req.status.text}}</v-chip></td>
                    </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </v-container>
</template>

<script>
    export default {
        name: "transaction-history",
        data: ()=> {
            return {
                requests: []
            }
        },
        mounted() {
            this.$axios.get(this.$api.Reservation.Payment.RequestsList)
                .then((response)=> {
                    this.requests = response.data
                })
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

</style>
