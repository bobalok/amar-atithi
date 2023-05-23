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
                        <h3 class="portlet-head-title">Request Details</h3>
                    </div>

                    <div class="portlet-toolbar">
                        <div class="portlet-actions">
                            <div class="btn-group">
                                <v-btn to="/payment-requests" color="primary" class="active-flat">
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
                                        :color="request.status.color"
                                        label
                                        small
                                        disabled
                                        class="tall ma-0 font-weight-regular"
                                >{{request.status.text}}</v-chip>
                            </div>
                        </div>

                        <div class="followup-desc mb-6" >
                            <div class="font-weight-medium mb-1">Method: </div>
                            <div class="mce-content">{{ request.method }}</div>
                        </div>

                        <div class="followup-desc mb-6">
                            <div class="font-weight-medium mb-1">Number: </div>
                            <div class="mce-content">{{ request.number }}</div>
                        </div>

                        <div class="followup-desc mb-6">
                            <div class="font-weight-medium mb-1">Amount: </div>
                            <div class="mce-content">{{ request.amount }}</div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="ion-portlet mt-2" v-if="request.status.code == 0">
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

                    <v-btn @click="SaveAction" color="primary" >Save Changes</v-btn>
                </div>
            </div>

        </div>

    </div>
</template>

<script>
    export default {
        name: "PaymentRequestDetail",
        middleware: 'auth',
        data() {
            return {
                actions: [
                    {text: "Mark As Complete", value: 1},
                    {text: "Decline This Request", value: 2}
                ],
                action: undefined,
                reason: "",
                request: {},
                loaded: false,
                working: true,
            }
        },
        mounted() {

            this.$axios.get(this.$api.Payment.Detail(this.$route.params.id))
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
                    status: this.action
                }

                this.$axios.put(this.$api.Payment.Update(this.$route.params.id), data)
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
