<template>
    <v-container>
        <div class="payments mb-12">
            <div class="head">
                <h1>Account Verification</h1>
            </div>

            <template v-if="loaded">

                <div class="content font-size-lg">


                    <div class="form-group">
                        <label class="font-weight-regular">Select Verification Method</label>
                        <v-select v-model="method" @change="ChangeMethod" :items="items" solo flat></v-select>
                    </div>

                    <v-form v-if="method" lazy-validation v-model="valid" ref="form" @submit.prevent="FormSubmit">
                        <div v-if="method == 2" class="mt-5">

                            <div class="form-group mb-8">
                                <label class="d-block font-weight-regular">Passport No</label>
                                <input
                                        :rules="[rules.required]"
                                        :error-messages="no_error"
                                        @change="no_error = ''"
                                        type="text"
                                        v-model="no"
                                        placeholder="Enter your Passport number"
                                        class="form-control">
                            </div>


                            <div class="form-group">
                                <v-alert color="grey lighten-2" class="mb-3">Please upload a scan copy of your passport.
                                    Acceptable formats are : JPG, PNG
                                </v-alert>

                                <label class="d-block font-weight-regular">Scan copy of your Passport</label>

                                <div class="form-file mt-2">
                                    <input @change="FileSelected($event)" accept=".jpg,.jpeg,.png" type="file"
                                           ref="passport_selector">
                                    <v-btn @click="PassportSelector" color="grey lighten-2">Select a file</v-btn>
                                </div>
                            </div>



                            <div v-if="url" class="preview">
                                <img :src="url"/>
                            </div>
                        </div>

                        <div v-if="method == 1" class="mt-5">


                            <div class="form-group mb-8">
                                <label class="d-block font-weight-regular">Government ID No</label>
                                <input :rules="[rules.required]"
                                       :error-messages="no_error"
                                       @change="no_error = ''"
                                       type="text"
                                       v-model="no"
                                       placeholder="Enter your Government ID number" class="form-control">
                            </div>

                            <div class="form-group">
                                <v-alert color="grey lighten-2" class="mb-3">Please upload a scan copy of your government
                                    ID.
                                    Acceptable formats are : JPG, PNG
                                </v-alert>

                                <label class="d-block font-weight-regular">Scan copy of Your Government ID Card</label>

                                <div class="form-file mt-2">
                                    <input @change="FileSelected($event)" accept=".jpg,.jpeg,.png" type="file"
                                           ref="nid_selector">
                                    <v-btn @click="NIDSelector" color="grey lighten-2">Select a file</v-btn>
                                </div>
                            </div>

                            <div v-if="url" class="preview">
                                <img :src="url"/>
                            </div>
                        </div>

                        <hr class="mt-8 mb-8"/>

                        <v-btn color="primary" type="submit" large>Submit Verification Request</v-btn>
                    </v-form>


                    <!--                <div class="form-row">-->
                    <!--                    <div class="row-label d-flex">-->
                    <!--                        <div class="label-name font-weight-bold">Government ID</div>-->
                    <!--                        <a href="#" @click="ExpandArea('nid')" class="label-action">Add</a>-->
                    <!--                    </div>-->

                    <!--                    <div class="row-details mt-5" v-if="expand == 'nid'">-->

                    <!--                        -->
                    <!--                    </div>-->
                    <!--                </div>-->
                </div>
            </template>
        </div>
    </v-container>
</template>


<script>
    import {mapGetters} from 'vuex'

    export default {
        name: "ProceedToVerify",
        middleware: 'auth',
        computed: {
            ...mapGetters(['isAuthenticated', 'loggedInUser'])
        },
        created() {
            this.rules = this.$validator.rules

            this.$axios.get(this.$api.Users.SubmittedDocuments)
                .then((res)=> {
                    this.loaded = true
                    this.documents = res.data

                    if( res.data && res.data.status != 2){
                        this.$router.push("/account-settings/verifications")
                    }
                })

        },
        data: () => {
            return {
                rules: [],
                expand: "",
                steps: 1,
                method: "",
                items: [
                    {
                        text: "Government ID Card",
                        value: 1
                    },
                    {
                        text: "Passport",
                        value: 2
                    }
                ],
                no: "",
                image: "",
                url: "",
                no_error: "",
                valid: false,
                working: true,
                loaded: false,
                documents: {}
            }
        },

        methods: {
            ExpandArea(param) {
                this.expand = param
            },
            NIDSelector() {
                this.$refs.nid_selector.click()
            },
            PassportSelector() {
                this.$refs.passport_selector.click()
            },
            ChangeMethod(value) {
                this.no = "";
                this.image = "";
                this.url = "";
            },
            FormSubmit() {

                let check = new Promise((resolve, reject) => {
                    this.$refs.form.validate();
                    resolve();
                });

                check.then(() => {
                    this.SubmitRequest();
                });
            },
            SubmitRequest() {

                this.working = true;

                let url = this.$api.Users.RequestVerification
                let formData = new FormData();

                if (this.method == 2) {
                    formData.append("passport", this.image);
                    formData.append("passport_no", this.no);
                } else {

                    formData.append("nid", this.image);
                    formData.append("nid_no", this.no);
                }

                formData.append("method", this.method)

                let heads = {
                    headers: {'Content-Type': 'multipart/form-data'},
                    onUploadProgress: progressEvent => {
                        let uploadPercentage = parseInt(Math.round((progressEvent.loaded * 100) / progressEvent.total))
                        console.log(uploadPercentage)
                    }
                }

                this.$axios.post(url, formData, heads).then((response) => {
                    console.log(response)
                    this.$router.push("/account-settings/verifications")
                }).catch((error) => {

                }).then(() => {
                    console.log("Done")
                    this.working = false;
                })


            },
            FileSelected(event) {
                let file = event.target.files[0]
                let filename = file.name
                let filesize = file.size
                let filext = filename.split('.').pop();
                const allowed_ext = ['png', 'jpg', 'jpeg']
                let file_error = undefined

                if (this.$refs.nid_selector)
                    this.$refs.nid_selector.value = ""

                if (this.$refs.passport_selector)
                    this.$refs.passport_selector.value = ""

                if (!allowed_ext.includes(filext))
                    file_error = {
                        title: 'File format not allowed',
                        'desc': 'The file you selected cannot be uploaded. Please select a valid file. Allowed extensions are ' + allowed_ext.join(", ")
                    }

                if (filesize > 2097152)
                    file_error = {
                        title: 'File is too big',
                        'desc': 'The file you selected is too big. Maximum allowed size is 2 MB. Please consider optimizing the file before upload.'
                    }

                if (file_error) {
                    this.$store.commit("alert/SetIonDialogue", {
                        show: true,
                        title: file_error.title,
                        NoCancel: true,
                        content: file_error.desc,
                        buttons: [
                            {
                                text: "I understand",
                                action: () => {
                                    this.$store.commit("alert/CloseIonDialogue")
                                }
                            }
                        ]
                    });

                    return
                }

                this.image = file
                this.url = URL.createObjectURL(file);
            }
        }
    }
</script>

<style lang="scss" scoped>
    .head {
        margin: 36px 0 54px 0;

        h1 {
            font-size: 32px;
            font-weight: 800;
        }

        .handle {
            font-size: 16px;
            margin-top: 16px;
        }
    }

    .content {
        max-width: 768px;
    }

    .preview img {
        border: 1px solid #ddd;
        max-height: 300px;
    }


</style>
