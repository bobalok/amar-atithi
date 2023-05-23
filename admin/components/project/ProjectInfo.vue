<template>
    <div class="ion-portlet">
        <div class="portlet-head">
            <div class="portlet-head-label">
                <div class="portlet-head-icon">
                    <i class="la la-file-text-o"></i>
                </div>
                <h3 class="portlet-head-title">Ride Sharing Application using BlockChain</h3>
            </div>

            <div class="portlet-toolbar">
                <div class="portlet-actions">
                    <v-menu bottom left offset-y>
                        <template v-slot:activator="{ on }">
                            <v-btn v-on="on" :ripple="false" class="table-btn constant" text small>
                                <i class="la la-gear"></i>
                            </v-btn>
                        </template>

                        <v-list>
                            <v-list-item @click="">
                                <i class="la la-edit"></i>
                                <v-list-item-title>Edit Project Details</v-list-item-title>
                            </v-list-item>

                            <v-list-item @click="">
                                <i class="la la-tasks"></i>
                                <v-list-item-title>Assign Task</v-list-item-title>
                            </v-list-item>


                            <v-list-item @click="">
                                <i class="la la-user-times"></i>
                                <v-list-item-title>Schedule a Meeting</v-list-item-title>
                            </v-list-item>


                            <v-list-item @click="">
                                <i class="la la-users"></i>
                                <v-list-item-title>Schedule a Followup</v-list-item-title>
                            </v-list-item>


                            <v-list-item @click="">
                                <i class="la la-sign-out"></i>
                                <v-list-item-title>Take a Break</v-list-item-title>
                            </v-list-item>

                        </v-list>
                    </v-menu>
                </div>
            </div>
        </div>

        <div class="portlet-body">

            <div class="mb-2">
                <div class="subtitle">Project Description</div>
                <div class="widget-desc">
                    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc orci sem, euismod ut
                        sagittis sed, vestibulum eu nulla. Vivamus ullamcorper et nibh vitae facilisis. Praesent
                        mollis id est a gravida. Ut molestie lorem ut convallis efficitur. Donec vehicula, arcu
                        et dignissim ornare, quam arcu vestibulum nibh, et hendrerit dui dui non diam. Donec a
                        faucibus felis. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per
                        inceptos himenaeos.</p>

                    <p>Vestibulum aliquet, magna eget molestie finibus, enim magna egestas lorem, in egestas mi
                        sapien eu mauris. Aenean congue nulla sit amet tincidunt consequat. Morbi lacinia ex sit
                        amet auctor scelerisque. In et diam mattis, convallis dui nec, accumsan enim. Aenean ac
                        mauris ac enim congue malesuada eget in lorem. Sed posuere tincidunt tristique. Ut sit
                        amet libero pretium, efficitur turpis in, ultricies eros. Suspendisse neque nibh,
                        sodales eget justo eu, ultricies sollicitudin felis. Fusce pretium fermentum nibh, in
                        laoreet quam porta et.</p>
                </div>
            </div>

            <div class="mb-4">
                <div class="subtitle mb-0">Attachments</div>
                <div class="widget-desc">
                    <div class="atc-list d-flex">
                        <div class="attachment-inline d-flex mr-4">
                            <i class="la la-thumb-tack"></i>
                            <nuxt-link to="" class="regular-link">Research Paper 1.pdf</nuxt-link>
                        </div>

                        <div class="attachment-inline d-flex">
                            <i class="la la-thumb-tack"></i>
                            <nuxt-link to="" class="regular-link">Research Paper 1.pdf</nuxt-link>
                        </div>
                    </div>
                </div>
            </div>

            <div class="mb-4">
                <div class="subtitle mb-0">Field</div>
                <div class="widget-desc">BlockChain</div>
            </div>

            <div class="mb-6">
                <div class="subtitle mb-0">Google Site</div>
                <div class="widget-desc">
                    <a style="text-decoration: none;" class="primary--text" href="https://sites.google.com/diu.edu.bd/diu-blockchain">Ride Sharing Application using BlockChain</a>
                </div>
            </div>


            <div class="mb-8">
                <div class="subtitle mb-2">Team Members</div>
                <div class="widget-desc d-flex">
                    <div class="su-item mr-8">
                        <div class="d-flex">
                            <v-avatar size="40" style="max-width: 45px;" class="mr-2">
                                <img src="https://keenthemes.com/metronic/preview/demo12/custom/apps/user/assets/media/users/300_1.jpg"/>
                            </v-avatar>
                            <div class="table-card">
                                <div class="card-title">Ifty Rahman</div>
                                <div class="card-caption">153-15-6572</div>
                            </div>
                        </div>
                    </div>

                    <div class="su-item mr-8">
                        <div class="d-flex">
                            <v-avatar size="40" style="max-width: 45px;" class="mr-2">
                                <img src="https://keenthemes.com/metronic/preview/demo12/custom/apps/user/assets/media/users/300_2.jpg"/>
                            </v-avatar>
                            <div class="table-card">
                                <div class="card-title">A.I. Tazib</div>
                                <div class="card-caption">153-15-6683</div>
                            </div>
                        </div>
                    </div>

                    <div class="su-item mr-8">
                        <div class="d-flex">
                            <v-avatar size="40" style="max-width: 45px;" class="mr-2">
                                <img src="https://keenthemes.com/metronic/preview/demo12/custom/apps/user/assets/media/users/300_3.jpg"/>
                            </v-avatar>
                            <div class="table-card">
                                <div class="card-title">Zakir Hossain</div>
                                <div class="card-caption">153-15-6694</div>
                            </div>
                        </div>
                    </div>

                    <div class="su-item">
                        <div class="d-flex">
                            <v-avatar size="40" style="max-width: 45px;" class="mr-2">
                                <img src="https://keenthemes.com/metronic/preview/demo12/custom/apps/user/assets/media/users/300_3.jpg"/>
                            </v-avatar>
                            <div class="table-card">
                                <div class="card-title">Shakil Ahmed</div>
                                <div class="card-caption">153-15-6580</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="d-flex mb-4">
                <div class="su-item mr-5">
                    <div class="subtitle mb-2">Project Supervisor</div>
                    <div class="widget-desc d-flex">
                        <div class="su-item mr-8">
                            <div class="d-flex">
                                <v-avatar size="40" style="max-width: 45px;" class="mr-2">
                                    <img src="https://keenthemes.com/metronic/preview/demo12/custom/apps/user/assets/media/users/300_1.jpg"/>
                                </v-avatar>
                                <div class="table-card">
                                    <div class="card-title">Jhon Doe</div>
                                    <div class="card-caption">JDE</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="su-item">
                    <div class="subtitle mb-2">Project Co-Supervisor</div>
                    <div class="widget-desc d-flex">
                        <div class="su-item mr-8">
                            <div class="d-flex">
                                <v-avatar size="40" style="max-width: 45px;" class="mr-2">
                                    <img src="https://keenthemes.com/metronic/preview/demo12/custom/apps/user/assets/media/users/300_1.jpg"/>
                                </v-avatar>
                                <div class="table-card">
                                    <div class="card-title">Jhon Doe</div>
                                    <div class="card-caption">JDE</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>



        </div>
    </div>
</template>

<script>
    export default {
        name: "ProjectInfo"
    }
</script>

<style scoped>
    .subtitle {
        color: #7a7a7a;
        margin-bottom: 5px;
        font-size: .925rem;
    }

    .widget-desc {
        font-weight: 400;
        color: #3c3c3c;
    }

    .card-header img {
        margin: 0 auto;
    }

    .attachment-inline i {
        padding-top: 4px;
        padding-right: 4px;
    }
</style>
