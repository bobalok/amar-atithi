<template>
    <v-container>
        <div class="account-settings">
            <div class="head">
                <h1>Account settings</h1>
                <div class="handle">
                    Ifty Rahman, iftyrofficial@gmail.com · Go to profile
                </div>
            </div>

            <div class="settings-grid">
                <v-container grid-list-xl fluid class="pa-0">
                    <v-layout row wrap>
                        <v-flex xs4>
                            <nuxt-link to="/account-settings/personal-info" class="settings-item">
                                <div class="item-icon">
                                    <img src="../../assets/media/account-settings/user-id.svg" alt="User ID">
                                </div>

                                <h3>Personal Info</h3>
                                <div class="detail">Provide personal details and how we can reach you</div>
                            </nuxt-link>
                        </v-flex>

                        <v-flex xs4>
                            <nuxt-link to="/account-settings/verifications" class="settings-item">
                                <div class="item-icon">
                                    <img src="../../assets/media/account-settings/verification.svg" alt="Verifications">
                                </div>

                                <h3>Account Verification</h3>
                                <div class="detail">Provide necessary documents to get your account verified.</div>
                            </nuxt-link>
                        </v-flex>

                        <v-flex xs4>
                            <nuxt-link to="/account-settings/payment" class="settings-item">
                                <div class="item-icon">
                                    <img src="../../assets/media/account-settings/payments.svg" alt="Payments">
                                </div>

                                <h3>Payments & payouts</h3>
                                <div class="detail">Review all things money, including coupons, gift cards, and taxes
                                </div>
                            </nuxt-link>
                        </v-flex>
                    </v-layout>
                </v-container>
            </div>
        </div>


    </v-container>
</template>

<script>
    export default {
        name: "index"
    }
</script>

<style scoped lang="scss">

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


    .settings-item {
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.16) !important;
        padding: 30px;
        border-radius: 8px;
        display: block;
        color: inherit;
        .item-icon img {
            height: 35px;
        }

        h3 {
            font-size: 18px;
            font-weight: 800;
            margin: 0 0 6px 0;
        }

        .item-icon {
            margin: 0 0 15px 0;
        }

        .detail {
            font-size: 16px;
            height: 45px;
        }

    }


</style>