<template>
    <div class="page-view pa-6">
        <div class="page-header mb-3">
            <div class="subheader-main">
                <h3>Dashboard</h3>
            </div>
        </div>

        <div class="page-content">
            <v-layout row wrap>
                <v-flex xs6>
                    <div class="ion-portlet">
                        <div class="portlet-head">
                            <div class="portlet-head-label">
                                <v-icon class="portlet-head-icon">dashboard</v-icon>
                                <h3 class="portlet-head-title">Welcome</h3>
                            </div>
                        </div>
                        <div class="portlet-body">
                            Welcome to Amar Atithi Admin Panel.
                        </div>
                    </div>
                </v-flex>


            </v-layout>

        </div>
    </div>
</template>

<script>
    import simplebar from "simplebar-vue";
    import 'simplebar/dist/simplebar.css';

    export default {
        name: "Dashboard",
        components: {simplebar},
        data: () => {
            return {
                selected: [],
                options: [],
                timer: null
            }
        },
        methods: {}
    }
</script>

<style scoped>
    .CommentListOutter{

        overflow: hidden;
    }
    .CommentList{
        height: 250px;
    }

    .CreateTeamBox i {
        font-size: 75px;
        color: #2b2b2b;
    }
</style>
