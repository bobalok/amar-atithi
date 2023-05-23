<template>
    <div>
        <div class="adjustment-place-card d-flex mt-4">
            <div class="place-card">
                <div class="place-image">
                    <img :src="adjustment.place.cover.file" alt="">
                </div>


            </div>

            <div class="place-meta ml-7 ">
                <div class="place-info mb-4">
                    <h2 class="section-title">{{adjustment.place.title}}</h2>
                    <div class="adj-date">Adjustment Issued on: {{adjustment.created}}</div>
                    <div class="adj-date">Reference: {{adjustment.reference}}</div>
                    <div class="ads-status">Adjustment Status: <v-chip label small :color="adjustment.status.color" >{{adjustment.status.details}}</v-chip></div>
                </div>

                <div class="place-host mb-1">Your Host</div>

                <div class="host-card d-flex">
                    <v-avatar size="65" >
                        <img :src="adjustment.place.host.avatar">
                    </v-avatar>

                    <div class="details ml-3">
                        <div class="name">{{adjustment.place.host.name}}</div>
                        <div class="email">{{adjustment.place.host.email}}</div>
                        <div class="mobile">{{adjustment.place.host.mobile}}</div>
                    </div>
                </div>
            </div>
        </div>

        <div class="changes-tab">
            <v-container class="pa-0" fluid>
                <v-layout wrap>
                    <v-flex xs6>
                        <h3 class="details-title">Original Details</h3>
                        <table class="changes-table">
                            <tbody>
                            <tr>
                                <td class="font-weight-bold">Check-In</td>
                                <td>{{adjustment.original_start}}</td>
                            </tr>

                            <tr>
                                <td class="font-weight-bold">Checkout</td>
                                <td>{{adjustment.original_end}}</td>
                            </tr>
                            <tr>
                                <td class="font-weight-bold">Number of Guests</td>
                                <td>{{adjustment.original_guests}}</td>
                            </tr>
                            </tbody>
                        </table>
                    </v-flex>

                    <v-flex xs6>
                        <h3 class="details-title">New Details</h3>

                        <table class="changes-table">
                            <tbody>
                            <tr>
                                <td class="font-weight-bold">Check-In</td>
                                <td>{{adjustment.start}}</td>
                            </tr>

                            <tr>
                                <td class="font-weight-bold">Checkout</td>
                                <td>{{adjustment.end}}</td>
                            </tr>
                            <tr>
                                <td class="font-weight-bold">Number of Guests</td>
                                <td>{{adjustment.guests}}</td>
                            </tr>
                            </tbody>
                        </table>
                    </v-flex>
                </v-layout>
            </v-container>
        </div>
    </div>
</template>

<script>
    export default {
        name: "AdjustmentDetailComponent",
        props: ['adjustment']
    }
</script>

<style lang="scss" scoped>
    .adjustment-place-card{
        .place-card{
            width: 400px;


        }

        .place-meta {

            .adj-date{
                margin-bottom: 2px;
            }

            .section-title{
                font-size: 20px;
                line-height: 24px;
                font-weight: 600;
                margin-top: 0px;
                margin-bottom: 7px;
            }

            .place-host{
                font-weight: 600;
                font-size: 16px;
            }

        }


    }

    .changes-table {
        width: 100%;
        border-collapse: collapse;

        tr td {
            border-bottom: 1px solid #ddd;
            padding: 10px 0px;
            margin: 0;
        }
    }
    .changes-tab {
        margin: 30px 0 50px 0;
    }
</style>
