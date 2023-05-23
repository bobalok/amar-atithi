<template>
    <v-app>
        <v-content>
            <UserDashHeader/>

            <div class="UserDashboardContent">
                <nuxt/>
            </div>

            <SiteFooter/>
        </v-content>
    </v-app>
</template>

<script>
    import SiteHeader from "../components/general/SiteHeader";
    import SiteFooter from "../components/general/SiteFooter";
    import UserDashHeader from "../components/general/UserDashHeader";

    export default {
        name: "dashboard",
        components: {UserDashHeader, SiteFooter, SiteHeader}
    }
</script>

<style scoped>
    .UserDashboardContent {
        min-height: calc(100vh - 140px);
        /*background-color: #f2f3f8;*/
        border-bottom: 1px solid #eee;
    }
</style>
