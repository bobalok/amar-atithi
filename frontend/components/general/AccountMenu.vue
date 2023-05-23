<template>
    <v-menu style=" font-size: .9em;" offset-y left bottom>
        <template v-slot:activator="{ on }">
            <v-btn fab small v-on="on">
                <v-avatar :size="35">
                    <img :src="loggedInUser.avatar"  >
                </v-avatar>
            </v-btn>
        </template>
        <v-list class="account_dropdown">
            <v-list-item :to="`/users/${loggedInUser.userid}`" >
                <v-list-item-title>Profile</v-list-item-title>
            </v-list-item>

            <v-list-item to="/account-settings" >
                <v-list-item-title>Account</v-list-item-title>
            </v-list-item>

            <v-list-item to="/logout"  >
                <v-list-item-title>Logout</v-list-item-title>
            </v-list-item>
        </v-list>
    </v-menu>
</template>

<script>
    import {mapGetters} from 'vuex'

    export default {
        name: "AccountMenu",
        computed: {
            ...mapGetters(['isAuthenticated', 'loggedInUser'])
        },
    }
</script>

<style scoped>

</style>