<template>

    <div class="user-bookings">
        <v-container>

            <div class="page-header d-flex mt-6 mb-4">
                <h1 class="section-title">Your Reservations</h1>

                <div class="page-filter"></div>
            </div>

            <div class="trips-list">


                <v-data-table
                        :headers="headers"
                        :items="bookings"
                        class="elevation-0"
                >
                    <template v-slot:item.place.title="{ item }">

                        <div class="trip-table-place">
                            <div class="place-image">
                                <v-img
                                        :src="item.place.cover.file"
                                        :lazy-src="require(`@/assets/media/lazy-placeholder.jpg`)"
                                        aspect-ratio="1.5"
                                        class="grey lighten-2"
                                >
                                    <template v-slot:placeholder>
                                        <v-row
                                                class="fill-height ma-0"
                                                align="center"
                                                justify="center"
                                        >
                                            <v-progress-circular indeterminate color="grey lighten-5"></v-progress-circular>
                                        </v-row>
                                    </template>
                                </v-img>
                            </div>
                            <div class="place-details">
                                <div class="place-title">
                                    <nuxt-link
                                            class="regular-link font-weight-medium"
                                            :to="{name: 'dashboard-reservations-ref', params: {ref: item.reference}}" > {{item.place.title}}
                                    </nuxt-link>
                                </div>
                            </div>
                        </div>
                    </template>

                    <template v-slot:item.checkin="{ item }">{{ to_date(item.checkin) }} - {{ to_date(item.checkout) }}</template>

                    <template v-slot:item.status="{ item }">
                        <v-chip label small :color="item.status.color" >{{item.status.text}}</v-chip>
                    </template>

                    <template v-slot:no-data="" >
                        <div v-if="!loaded" style="position:relative; height: 150px;" >
                            <IonLoading :size="40" />
                        </div>
                        <div v-else class="text-xs-center">
                            No Reservation Found
                        </div>
                    </template>
                </v-data-table>

            </div>
        </v-container>
    </div>

</template>

<script>
    import StarRating from "../../../components/general/StarRating";
    import moment from "moment";
    import IonLoading from "../../../components/general/IonLoading";

    export default {
        name: "bookings",
        components: {IonLoading, StarRating},
        layout: 'dashboard',
        data () {
            return {
                headers: [
                    { text: 'Place', value: 'place.title' },
                    { text: 'Area', value: 'place.city.name' },
                    { text: 'Date', value: 'checkin' },
                    { text: 'Status', value: 'status' },
                ],
                desserts: [
                    {
                        place: 'BEAUTIFUL FULLY INDEPENDENT STUDIO APT - GULSHAN 2',
                        area: 'Gulshan',
                        date: "20 July 2019 - 22 July 2019",
                        status: "Completed",
                    },
                    {
                        place: 'Hector Cave House',
                        area: 'Dhanmondi',
                        date: "20 July 2019 - 22 July 2019",
                        status: "Completed",
                    },
                    {
                        place: 'Unique Architecture Cave House',
                        area: 'Banani',
                        date: "20 July 2019 - 22 July 2019",
                        status: "Completed",
                    },
                ],
                bookings:[],
                loaded: false,
            }
        },
        methods: {
            getColor (calories) {
                if (calories > 400) return 'red'
                else if (calories > 200) return 'orange'
                else return 'green'
            },
            to_date( date){
                return moment(date, this.$Settings.MySqlDate).format("DD MMMM YYYY")
            },
        },

        mounted() {
            this.$axios.get(this.$api.Users.Bookings)
                .then((r)=> {
                    this.bookings = r.data
                    this.loaded = true
                })
        }

    }
</script>

<style lang="scss" scoped>

    .trips-list{
        margin-bottom: 50px;
    }

    img {}

    .trip-table-place {
        display: table;
    }

    .place-image {
        height: 50px;
        width: 75px;
        margin-right: 12px;
    }

    .place-details {
        vertical-align: middle;
        display: table-cell;
    }

    .place-image img {
        object-fit: cover;
    }

    table.IonTable {
        width: 100%;
        border: 1px solid rgba(225, 225, 225, 1);
        font-size: 13px;
        border-collapse: collapse;
    }

    .IonTable tbody tr:nth-child(2n - 1) {
        background-color: rgba(244, 244, 244, 1);
    }

    .IonTable tbody tr td {padding: 10px 15px;}

    .IonTable thead tr th {
        text-align: left;
        font-weight: 600;
        color: #4a4a4a;
        padding: 15px 15px;
    }
</style>
