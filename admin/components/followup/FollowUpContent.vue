<template>
    <div class="ion-portlet">
        <div class="portlet-head">
            <div class="portlet-head-label">
                <div class="portlet-head-icon">
                    <i class="la la-bullhorn"></i>
                </div>
                <h3 class="portlet-head-title">Phase II - Follow-up I</h3>
            </div>

            <div class="portlet-toolbar">
                <div class="portlet-actions">
                    <div class="btn-group">
                        <v-btn to="/student-panel/followups" color="primary" class="active-flat">
                            <i class="la la-arrow-left" ></i>
                            <span class="ml-1">Go Back</span>
                        </v-btn>
                    </div>
                </div>
            </div>
        </div>
        <div class="portlet-body">
            <div class="notice-content">

                <div class="followup-desc">
                    <div class="font-weight-medium mb-1">Description:</div>

                    <div class="mce-content">
                        <p>Lorem Ipsum is simply dummy text of the printing and typesetting scrambled a type specimen book text of the dummy text of the printing printing and typesetting industry scrambled dummy text of the printing.
                            .Sed ut perspiciatis unde omnis iste natus error sit voluptatem, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto.</p>
                    </div>
                </div>


                <div class="mb-4">
                    <div class="subtitle mb-1 font-weight-medium">Materials</div>
                    <div class="widget-desc">
                        <div class="atc-list d-flex">
                            <div class="attachment-inline d-flex mr-4">
                                <i class="la la-thumb-tack mr-1"></i>
                                <nuxt-link to="" class="regular-link">Research Paper 1.pdf</nuxt-link>
                            </div>

                            <div class="attachment-inline d-flex">
                                <i class="la la-thumb-tack mr-1"></i>
                                <nuxt-link to="" class="regular-link">Research Paper 1.pdf</nuxt-link>
                            </div>
                        </div>
                    </div>
                </div>

                <v-container fluid class="pa-0 mt-6 pb-3">
                    <v-layout row wrap>
                        <v-flex xs4>
                            <div class="meta-item">
                                <strong class="meta-label">Date</strong>
                                <div class="meta-value">
                                    <div class="meta-icon d-inline-block">
                                        <i class="primary--text la la-calendar"></i>
                                    </div>

                                    <span class="meta-text">Saturday 20 July 2019</span>
                                </div>
                            </div>
                        </v-flex>

                        <v-flex xs4>
                            <div class="meta-item">
                                <strong class="meta-label">Time</strong>
                                <div class="meta-value">
                                    <div class="meta-icon d-inline-block">
                                        <i class="error--text la la-clock-o"></i>
                                    </div>

                                    <span class="meta-text">04:45pm - 05:20pm</span>
                                </div>
                            </div>
                        </v-flex>

                        <v-flex xs4>
                            <div class="meta-item">
                                <strong class="meta-label">Venue</strong>
                                <div class="meta-value">
                                    <div class="meta-icon d-inline-block">
                                        <i class="warning--text la la-map-marker"></i>
                                    </div>

                                    <span class="meta-text">CSE Confeence Room</span>
                                </div>
                            </div>
                        </v-flex>
                    </v-layout>
                </v-container>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "FollowUpContent"
    }
</script>

<style scoped>

</style>
