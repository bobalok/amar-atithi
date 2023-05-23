<template>
    <div class="page-view pa-6" v-if="loaded">
        <div class="page-header mb-3">
            <div class="subheader-main">
                <h3>Request Details</h3>
            </div>
        </div>

        <div class="page-content">

            <div class="ion-portlet">
                <div class="portlet-head">
                    <div class="portlet-head-label">
                        <div class="portlet-head-icon">
                            <i class="la la-bullhorn"></i>
                        </div>
                        <h3 class="portlet-head-title">Submitted Documents</h3>
                    </div>

                    <div class="portlet-toolbar">
                        <div class="portlet-actions">
                            <div class="btn-group">
                                <v-btn to="/account-verifications" color="primary" class="active-flat">
                                    <i class="la la-arrow-left" ></i>
                                    <span class="ml-1">Go Back</span>
                                </v-btn>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="portlet-body">
                    <div class="notice-content">

                        <div class="followup-desc mb-6">
                            <div class="font-weight-medium mb-1">Status: </div>
                            <div class="mce-content">
                                <v-chip
                                        v-if="request.status == 0"
                                        color="warning"
                                        label
                                        small
                                        disabled
                                        class=" tall ma-0 font-weight-regular"
                                >Pending</v-chip>

                                <v-chip
                                        v-else-if="request.status == 1"
                                        color="success"
                                        label
                                        small
                                        disabled
                                        class=" tall ma-0 font-weight-regular"
                                >Accepted</v-chip>

                                <v-chip
                                        v-else-if="request.status == 2"
                                        color="error"
                                        label
                                        small
                                        disabled
                                        class=" tall ma-0 font-weight-regular"
                                >Rejected</v-chip>
                            </div>
                        </div>

                        <div class="followup-desc mb-6" v-if="request.status == 2">
                            <div class="font-weight-medium mb-1">Reason For Decline: </div>
                            <div class="mce-content">{{ request.notes }}</div>
                        </div>

                        <div class="followup-desc mb-6">
                            <div class="font-weight-medium mb-1">Method: </div>
                            <div class="mce-content">{{ request.method_detail }}</div>
                        </div>

                        <template v-if="request.method == 1">
                            <div class="followup-desc mb-6">
                                <div class="font-weight-medium mb-1">NID No: </div>
                                <div class="mce-content">{{ request.nid_no }}</div>
                            </div>

                            <div class="followup-desc mb-6">
                                <div class="font-weight-medium mb-1">NID: </div>
                                <div class="mce-content">
                                    <img style="max-height: 400px;" :src="request.nid" alt="">
                                </div>
                            </div>
                        </template>

                        <template v-if="request.method == 2">
                            <div class="followup-desc mb-6">
                                <div class="font-weight-medium mb-1">Passport No: </div>
                                <div class="mce-content">{{ request.passport_no }}</div>
                            </div>

                            <div class="followup-desc mb-6">
                                <div class="font-weight-medium mb-1">Passport: </div>
                                <div class="mce-content">
                                    <img style="max-height: 400px;" :src="request.passport" alt="">
                                </div>
                            </div>
                        </template>
                    </div>
                </div>
            </div>

            <div class="ion-portlet mt-2" v-if="request.status == 0">
                <div class="portlet-head">
                    <div class="portlet-head-label">
                        <div class="portlet-head-icon">
                            <i class="la la-gear"></i>
                        </div>

                        <h3 class="portlet-head-title">Action</h3>
                    </div>
                </div>
                <div class="portlet-body">

                    <div class="form-group">
                        <label>Select an action</label>

                        <v-select v-model="action" :items="actions" flat solo ></v-select>
                    </div>

                    <div class="form-group" v-if="action == 0">
                        <v-textarea v-model="reason" flat solo label="Reason for decline"></v-textarea>
                    </div>

                    <v-btn @click="SaveAction" color="primary" >Save Changes</v-btn>
                </div>
            </div>

        </div>

    </div>
</template>

<script>
    export default {
        name: "VerificationDetails",
        middleware: 'auth',
        data() {
            return {
                actions: [
                    {text: "Approve This Document", value: 1},
                    {text: "Reject This Document", value: 0}
                ],
                action: undefined,
                reason: "",
                request: {},
                loaded: false,
                working: true,
            }
        },
        mounted() {

            this.$axios.get(this.$api.Documents.Detail(this.$route.params.id))
                .then((res)=> {
                    this.request = res.data
                })
                .finally(()=> {
                    this.loaded = true
                    this.working = false
                })
        },
        methods: {
            SaveAction(){
                if( this.action == undefined ){
                    alert("Please select an action")
                    return
                }

                this.working = true

                let data = {
                    pk: this.$route.params.id,
                    reason: this.reason ,
                    action: this.action
                }

                this.$axios.post(this.$api.Documents.ChangeVerdict, data)
                    .then((response)=> {
                        this.request = response.data
                    })
                    .finally(()=> {
                        this.working = false
                    })

            }
        }
    }
</script>

<style scoped>

</style>
