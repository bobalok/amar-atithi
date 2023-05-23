<template>

    <div class="booking-item">
        <div class="item-image">
            <img v-if="place.cover" :src="place.cover.file" alt="">
            <div class="image-placeholder blue-grey lighten-2" v-else>
                <div class="placeholder-wrap">
                    <i class="la la-camera"></i>
                </div>
            </div>
        </div>

        <div class="item-details ">
            <div class="item-details-top">
                <h2 class="item-title mb-1">
                    <nuxt-link :to='{name: "hosting-manage-your-space-code", params: {code: place.code}}' >{{place.title}}</nuxt-link>
                </h2>

                <div class="item-type" v-if="place.space">{{place.space.name}}</div>
                <div class="item-meta mb-3 d-flex">
                    <RatingWithCount/>
                    <div class="ml-3 item-price">{{$Settings.Price(place.price)}}/night</div>
                </div>

                <div class="place-excerpt">{{place.summary}}</div>
            </div>

            <div class="item-footer">
                <v-btn color="primary" :to='{name: "hosting-manage-your-space-code", params: {code: place.code}}' small>Edit Listing</v-btn>
            </div>
        </div>
    </div>
</template>

<script>
    import StarRating from "../general/StarRating";
    import RatingWithCount from "../general/RatingWithCount";
    export default {
        name: "BookingItem",
        props:['place'],
        components: {RatingWithCount, StarRating}
    }
</script>

<style lang="scss" scoped>
    .booking-item {
        display: flex;
        background: #fff;
        padding: 8px;
        border: 1px solid #ebebeb;
        border-radius: 3px;
        margin-bottom: 25px;

        &:hover {
            box-shadow: rgba(0, 0, 0, 0.12) 0 0 12px;
        }

        .item-image {
            width: 300px;
            height: 200px;
            overflow: hidden;
            border-radius: 2px;
            flex-basis: 300px;
            flex-grow: 1;
            flex-shrink: 0;
            max-width: 300px;

           img {
                object-fit: cover;
                height: 100%;
                width: 100%;
            }
        }


        .item-details {
            padding: 8px 20px 8px 20px;
            flex-grow: 1;
            display: flex;
            flex-direction: column;

            .item-details-top {

                .item-title {
                    font-size: 20px;
                    font-weight: 600;
                    line-height: 28px;

                    a{
                        color: inherit;
                    }
                }

                .place-excerpt{
                }

                .meta-item {
                    line-height: 1em;
                    margin-bottom: 8px;
                }


            }


            .item-footer {
                display: flex;
                width: 100%;
                margin-top: auto;

                .item-price {
                    margin-left: auto;
                }
            }
        }

        .image-placeholder {
            height: 100%;
            text-align: center;
            color: #fff;
            display: table;
            width: 100%;
        }

        .placeholder-wrap {
            display: table-cell;
            vertical-align: middle;
            font-size: 50px;
        }

    }
</style>