<template>
    <div class="ion-portlet">
        <div class="portlet-head">
            <div class="portlet-head-label">
                <div class="portlet-head-icon">
                    <i class="la la-bullhorn"></i>
                </div>
                <h3 class="portlet-head-title">Title Defense - Summer 2019</h3>
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
                    <div class="font-weight-medium mb-1">Instructions:</div>

                    <div class="mce-content">
                        <p>Lorem Ipsum is simply dummy text of the printing and typesetting scrambled a type specimen book text of the dummy text of the printing printing and typesetting industry scrambled dummy text of the printing.
                            .Sed ut perspiciatis unde omnis iste natus error sit voluptatem, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto.</p>
                    </div>
                </div>


                <div class="mb-4">
                    <div class="subtitle mb-1 font-weight-medium">Attachments</div>
                    <div class="widget-desc">
                        <div class="atc-list d-flex">
                            <div class="attachment-inline d-flex mr-4">
                                <i class="la la-thumb-tack mr-1"></i>
                                <nuxt-link to="" class="regular-link">Title Defense Notice.pdf</nuxt-link>
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
        name: "GrandFollowupContent"
    }
</script>

<style scoped>

</style>
