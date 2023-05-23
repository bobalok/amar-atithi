<template>
    <div class="page-view pa-6">
        <div class="page-header mb-3">
            <div class="subheader-main">
                <h3>Payment Requests</h3>
            </div>
        </div>

        <div class="page-content">
            <div class="ion-portlet">
                <div class="portlet-head">
                    <div class="portlet-head-label">
                        <div class="portlet-head-icon">
                            <i class="la la-dollar"></i>
                        </div>
                        <h3 class="portlet-head-title">List of Payment Requests</h3>
                    </div>
                </div>

                <div class="portlet-body">

                    <div class="table-search">
                        <v-layout row wrap>
                            <v-flex xs3>
                                <div class="form-group">
                                    <label>Status</label>
                                    <v-select flat solo :menu-props="{'offsetY': true}" :items="filter.fields.status" v-model="filter.values.status" placeholder="Status"></v-select>
                                </div>
                            </v-flex>

                            <v-flex xs1>
                                <div class="form-group">
                                    <label class="d-block">&nbsp;</label>
                                    <v-btn @click="ApplyFilter" class="tall" color="primary">Filter</v-btn>
                                </div>
                            </v-flex>

                            <v-flex xs3 offset-xs5 right>
                                <div class="form-group">
                                    <label class="d-block">&nbsp;</label>
                                    <div class="input-with-icon">
                                        <input type="text" class="form-control" placeholder="Search..">
                                        <i class="la la-search"></i>
                                    </div>
                                </div>
                            </v-flex>
                        </v-layout>
                    </div>

                    <v-data-table
                            :headers="headers"
                            :items="requests"
                            class="mt-2"
                            :sort-by="[]"
                            :footer-props="{
                              'items-per-page-options': rowsPerPageItems
                            }"
                            :page.sync="page"
                            no-data-text="No Data Found"
                            item-key="name"
                    >
                        <template v-slot:item.assigned_by.name="{ item }" >
                            <div class="d-flex">
                                <v-avatar size="40" style="max-width: 45px;" class="mr-2">
                                    <img :src="item.user.avatar"/>
                                </v-avatar>

                                <div class="table-card">
                                    <div class="card-title">{{ item.user.fullname}}</div>
                                    <div class="card-caption">{{ item.user.fullname}}</div>
                                </div>
                            </div>
                        </template>

                        <template v-slot:item.status="{item}" >
                            <v-chip
                                    :color="item.status.color"
                                    label
                                    small
                                    disabled
                                    class="tall ma-0 font-weight-regular"
                            >{{item.status.text}}</v-chip>

                        </template>

                        <template v-slot:item.action="{item}" >
                            <v-btn :to="{name: 'payment-requests-id', params: {id: item.id}}" class=" table-btn constant" text small>
                                <i class="la la-gear"></i>
                            </v-btn>
                        </template>

                    </v-data-table>
                </div>
            </div>


        </div>
    </div>
</template>

<script>
    export default {
        name: "PaymentRequests",
        middleware: 'auth',
        data() {
            return {
                filter: {
                    fields: {
                        status: [
                            {
                                text: "All",
                                value: -1,
                            },
                            {
                                text: "Pending",
                                value: 0,
                            },
                            {
                                text: "Complete",
                                value: 1,
                            },
                            {
                                text: "Declined",
                                value: 2,
                            }
                        ]
                    },
                    values: {
                        status: 0
                    }
                },
                rowsPerPageItems: [10, 25, 50, 100],
                page: 1,
                headers: [
                    {text: 'User', value: 'user'},
                    {text: 'Method', value: 'method'},
                    {text: 'Amount', value: 'amount'},
                    {text: 'Number', value: 'number', sortable: false},
                    {text: 'Status',  value: 'status', sortable: false},
                    {text: 'Action', value: 'action', sortable: false},
                ],
                requests:[],
                requests_arc:[],
                loading: true,
            }
        },
        methods: {
            ApplyFilter(){
                let status = this.filter.values.status

                if( !isNaN(status) ){
                    if( status == -1 ){
                        this.requests = this.requests_arc
                    } else {
                        this.requests = this.requests_arc.filter( x => x.status.code == status)
                    }
                }
            }
        },
        mounted() {

            this.$axios.get(this.$api.Payment.List)
                .then((res)=> {
                    this.requests = res.data
                    this.requests_arc = res.data
                })
                .finally(()=> {
                    this.loading = false
                    this.loaded = true
                })
        }
    }
</script>

<style scoped>

</style>

