<template>
    <v-container>
        <div class="dashboard  mt-6">
            <!--            <h1 class="page-title">Dashboard</h1>-->

            <v-container fluid class="pt-0 pb-0">
                <v-layout row wrap>
                    <v-flex xs8>
                        <div class="section">
                            <h3 class="section-title">Dashboard</h3>

                            <div class="no-upcoming-reservation">
                                <div class="middle">
                                    <img src="../../assets/media/calendar.svg" alt="">
                                    <span>No upcoming reservations</span>
                                </div>
                            </div>
                        </div>
                    </v-flex>
                </v-layout>
            </v-container>
        </div>
    </v-container>
</template>

<script>
    export default {
        name: "HostingDashboard",
        layout: 'hosting'
    }
</script>


<style lang="scss" scoped>


    .page-title {
        font-size: 32px;
        font-weight: 800;
    }

    .section {
        margin-bottom: 30px;



        .section-title {
            margin: 0 0 20px 0;
        }
    }

    .no-upcoming-reservation {
        height: 200px;
        border: 1px solid #ddd;
        border-radius: 4px;
        box-shadow: rgba(0, 0, 0, 0.05) 0px 4px 4px 0px;
        text-align: center;
        display: table;
        width: 100%;

        .middle {
            display: table-cell;
            vertical-align: middle;
        }

        img {
            height: 42px;
            display: block;
            text-align: center;
            margin: 0 auto 8px;
        }
    }





</style>