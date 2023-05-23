<template>
    <div class="page-view pa-6">
        <div class="page-header mb-3">
            <div class="subheader-main">
                <h3>Verification Requests</h3>
            </div>
        </div>

        <div class="page-content">
            <div class="ion-portlet">
                <div class="portlet-head">
                    <div class="portlet-head-label">
                        <div class="portlet-head-icon">
                            <i class="la la-users"></i>
                        </div>
                        <h3 class="portlet-head-title">List of Verification Requests</h3>
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
                                    v-if="item.status == 0"
                                    color="warning"
                                    label
                                    small
                                    disabled
                                    class="tall ma-0 font-weight-regular"
                            >Pending</v-chip>

                            <v-chip
                                    v-else-if="item.status == 1"
                                    color="success"
                                    label
                                    small
                                    disabled
                                    class="tall ma-0 font-weight-regular"
                            >Accepted</v-chip>

                            <v-chip
                                    v-else-if="item.status == 2"
                                    color="error"
                                    label
                                    small
                                    disabled
                                    class="tall ma-0 font-weight-regular"
                            >Rejected</v-chip>

                        </template>

                        <template v-slot:item.action="{item}" >
                            <v-btn :to="{name: 'account-verifications-id', params: {id: item.pk}}" class=" table-btn constant" text small>
                                <i class="la la-file-text"></i>
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
        name: "AccountVerifications",
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
                                text: "Accepted",
                                value: 1,
                            },
                            {
                                text: "Rejected",
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
                    {text: 'User', value: 'assigned_by.name'},
                    {text: 'Method', value: 'method_detail'},
                    {text: 'Status', value: 'status'},
                    {text: 'Action', align: 'center', value: 'action', sortable: false}
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
                    if( status === -1 ){
                        this.requests = this.requests_arc
                    } else {
                        this.requests = this.requests_arc.filter( x => x.status == status)
                    }
                }
            }
        },
        mounted() {

            this.$axios.get(this.$api.Documents.List)
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

