<template>
    <v-container>
        <div class="verifications mb-12">
            <div class="head">
                <h1>Account Verification</h1>
            </div>

            <template v-if="loaded">

                <div class="v-status d-flex mb-6">
                    <div>Account Verification Status</div>

                    <div style="margin-left: auto;">
                        <v-chip v-if="loggedInUser.verified" label small color="success">Verified</v-chip>
                        <v-chip v-else label small color="error">Unverified</v-chip>
                    </div>
                </div>

                <div class="submitted-documents" v-if="documents">
                    <div>Submitted Documents</div>

                    <table class="table-bordered table">
                        <tbody>
                        <tr>
                            <td>Status:</td>
                            <td>

                                <v-chip
                                        v-if="documents.status == 0"
                                        color="warning"
                                        label
                                        small
                                        disabled
                                        class="active-flat constant tall ma-0 font-weight-regular"
                                >Pending</v-chip>

                                <v-chip
                                        v-else-if="documents.status == 1"
                                        color="success"
                                        label
                                        small
                                        disabled
                                        class="active-flat constant tall ma-0 font-weight-regular"
                                >Accepted</v-chip>

                                <v-chip
                                        v-else-if="documents.status == 2"
                                        color="error"
                                        label
                                        small
                                        disabled
                                        class="active-flat constant tall ma-0 font-weight-regular"
                                >Rejected</v-chip>

                            </td>
                        </tr>

                        <tr v-if="documents.status == 2">
                            <td >Reason for Decline:</td>
                            <td>{{documents.notes}}</td>
                        </tr>

                        <tr>
                            <td>Method:</td>
                            <td>{{documents.method_detail}}</td>
                        </tr>



                        <template v-if="documents.method == 1">
                            <tr>
                                <td>Government ID No:</td>
                                <td>{{documents.nid_no}}</td>
                            </tr>

                            <tr>
                                <td>Government ID</td>
                                <td><img :src="documents.nid" style="max-height: 250px;" alt=""></td>
                            </tr>
                        </template>

                        <template v-if="documents.method == 2">
                            <tr>
                                <td>Passport No:</td>
                                <td>{{documents.passport_no}}</td>
                            </tr>

                            <tr>
                                <td>Passport</td>
                                <td><img :src="documents.passport" style="max-height: 250px;" alt=""></td>
                            </tr>
                        </template>


                        </tbody>
                    </table>
                </div>

                <div class="mt-6" v-if="!loggedInUser.verified ">
                    <v-btn v-if="!documents" to="/account-settings/verifications/proceed" color="primary" large >Proceed to Verification</v-btn>
                    <v-btn v-if="documents && documents.status == 2" to="/account-settings/verifications/proceed" color="primary" large >Resubmit Documents</v-btn>
                </div>



            </template>
        </div>
    </v-container>
</template>


<script>
    import {mapGetters} from 'vuex'

    export default {
        name: "AccountVerification",
        middleware: 'auth',
        computed: {
            ...mapGetters(['isAuthenticated', 'loggedInUser']),

            CanSubmitDocuments(){
                if ( this.documents && this.documents.status == 'REJECTED' )
                    return true

                if ( !this.loggedInUser.verified && !this.documents )
                    return true

                return false
            }
        },
        created() {
            this.rules = this.$validator.rules

            this.$axios.get(this.$api.Users.SubmittedDocuments)
                .then((res)=> {
                    this.loaded = true
                    this.documents = res.data
                })

        },
        data: () => {
            return {
                valid: false,
                working: true,
                loaded: false,
                documents: {}
            }
        },

        methods: {

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

    .verifications {
        max-width: 890px;
    }

    .preview img {
        border: 1px solid #ddd;
        max-height: 300px;
    }


</style>
