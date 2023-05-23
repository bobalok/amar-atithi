<template>
    <div class="EmailVerifyWrap">
        <div class="WrapInner">

            <template v-if="complete">
                <div v-if="valid" class="WrapContainer">
                    <div class="SuccessResult">
                        <i class="la la-user"></i>
                        <h2 class="title">Success</h2>
                        <div class="Result">{{message}}</div>
                        <v-btn class="SuccessBtn" :to="{ name: 'login', query: {action: 'login'} }" large color="primary">Continue</v-btn>
                    </div>
                </div>

                <div v-else class="WrapContainer">
                    <div class="ErrorResult">
                        <v-icon class="ErrorIcon" color="error">warning</v-icon>
                        <h2 class="title">Error</h2>
                        <div class="Result">This link is no longer valid. Please try again later.</div>
                        <v-btn to="/" class="SuccessBtn" large color="primary">Back to Home</v-btn>
                    </div>
                </div>
            </template>
            <template v-else>
                <v-progress-circular
                        :size="45"
                        width="3"
                        style="margin-top: 10px;"
                        color="primary"
                        indeterminate
                ></v-progress-circular>

                <div class="mt-3">Processing your request. <br> Please wait....</div>
            </template>

        </div>
    </div>
</template>

<script>
    export default {
        name: "VerifyEmail",
        data: () => {
            return {
                valid: false,
                complete: false,
                message : ""
            }
        },
        mounted() {
            const email = this.$route.params.email;
            const code = this.$route.params.code;

            this.$axios.post( this.$api.Users.VerifyEmail, {email, code})
                .then((response)=> {
                    this.valid = true
                    this.message = response.data
                })
                .catch()
                .finally(()=> {
                    this.complete = true
                })
        }
    }
</script>

<style scoped>

    .SuccessResult i {
        border: 2px solid #00897B;
        border-radius: 100%;
        width: 65px;
        height: 65px;
        font-size: 32px;
        line-height: 60px;
    }

    .ErrorIcon{
        border-color: red !important;
        border-width: 1.25px;
    }
    .SuccessBtn{
        font-size: 16px;
    }

    .EmailVerifyWrap {
        width: 500px;
        display: table;
        margin: 0 auto;
        height: calc(100vh - 140px);
    }

    .WrapInner {
        text-align: center;
        vertical-align: middle;
        display: table-cell;
        height: auto;
    }

    .WrapContainer {
        background: #fff;
        padding: 30px;
        border-radius: 4px;
        overflow: hidden;
    }

    h2.WrapTitle {
        color: #999;
        font-weight: 700;
        margin: 0 0 10px 0;
    }

    h2.title {
        font-weight: normal;
        font-size: 22px !important;
        margin: 20px 0;
        border-bottom: 1px solid #ddd;
        padding-bottom: 20px;
    }

    .Result {
        margin-bottom: 20px;
    }
</style>