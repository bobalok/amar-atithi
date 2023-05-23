<template>
    <div  class="project-item">

        <div class="project-toolbar">
            <v-menu bottom left offset-y>
                <template v-slot:activator="{ on }">
                    <v-btn v-on="on" :ripple="false" class="table-btn constant" text small>
                        <i class="la la-gear"></i>
                    </v-btn>
                </template>

                <v-list class="menu_list">
                    <v-list-item @click="">
                        <i class="la la-edit"></i>
                        <v-list-item-title>Edit Project Details</v-list-item-title>
                    </v-list-item>

                    <v-list-item @click="">
                        <i class="la la-tasks"></i>
                        <v-list-item-title @click="$router.push('/dashboard/tasks/add-new-task')">Assign Task</v-list-item-title>
                    </v-list-item>


                    <v-list-item @click="">
                        <i class="la la-user-times"></i>
                        <v-list-item-title>Schedule a Meeting</v-list-item-title>
                    </v-list-item>


                    <v-list-item @click="">
                        <i class="la la-users"></i>
                        <v-list-item-title @click="$router.push('/dashboard/followups/add-new-followup')">Schedule a Followup</v-list-item-title>
                    </v-list-item>

                    <v-list-item @click="">
                        <i class="la la-arrow-right"></i>
                        <v-list-item-title @click.prevent="">Migrate to Next Phase</v-list-item-title>
                    </v-list-item>

                    <v-list-item @click="">
                        <i class="la la-sign-out"></i>
                        <v-list-item-title>Take a Break</v-list-item-title>
                    </v-list-item>

                </v-list>
            </v-menu>
        </div>

        <div class="project-details">
            <div class="project-meta mb-4">
                <h2 class="project-title mb-2">Ride Sharing Application using BlockChain</h2>

                <div class="excerpt">
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                    Nunc orci sem, euismod ut sagittis sed, vestibulum eu nulla.
                    Vivamus ullamcorper et nibh vitae facilisis. Praesent mollis id est a gravida.
                    Ut molestie lorem ut convallis efficitur.
                    Donec vehicula, arcu et dignissim ornare, quam arcu vestibulum nibh, et hendrerit dui dui non diam.
                    Donec a faucibus felis. Class aptent taciti sociosqu ad litora torquent
                    per conubia nostra, per inceptos himenaeos.
                </div>
            </div>

            <div class="item-stats d-flex mb-4">
                <div class="summary-item mr-5">
                    <h4 class="item-title mb-2">Tasks Completed</h4>
                    <div class="item-value">12</div>
                </div>

                <div class="summary-item mr-5">
                    <h4 class="item-title mb-2">Followup Completed</h4>
                    <div class="item-value">2</div>
                </div>

                <div class="summary-item mr-5">
                    <h4 class="item-title mb-2">Team Members</h4>
                    <div class="item-value">
                        <div class="TeamAvatars">
                            <UserAvatar size="30" name="Zakir Hossain" avatar="https://keenthemes.com/metronic/preview/demo12/custom/apps/user/assets/media/users/300_21.jpg"/>
                            <UserAvatar size="30" name="Shakil Ahmed" avatar="https://keenthemes.com/metronic/preview/demo12/custom/apps/user/assets/media/users/300_21.jpg"/>
                            <UserAvatar size="30" name="Zakir Hossain" avatar="https://keenthemes.com/metronic/preview/demo12/custom/apps/user/assets/media/users/300_21.jpg"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import UserAvatar from "../general/UserAvatar";
    export default {
        name: "SuCard",
        components: {UserAvatar}
    }
</script>

<style scoped>
    .item-title {
        font-weight: 500;
        color: #595d6e;
    }


    .project-meta .project-title {
        font-size: 1.15rem !important;
        font-weight: 500;
        color: #48465b;
    }




    .project-item + .project-item {
        margin-top: 25px;
        padding-top: 25px;
        border-top: 1px solid #ddd;
    }
    .project-item{
        overflow: hidden;
        position: relative;
    }

    .project-toolbar {
        position: absolute;
        right: 0;
        top: 0;
    }
</style>
