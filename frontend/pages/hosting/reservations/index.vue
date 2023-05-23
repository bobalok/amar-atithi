<template>

    <div class="user-bookings">
        <v-container>

            <div class="page-header d-flex mt-6 mb-4">
                <h1 class="section-title">Reservations of Your Places</h1>

                <div class="page-filter"></div>
            </div>

            <div class="trips-list">
                <v-data-table
                        :headers="headers"
                        :items="reservations"
                        class="elevation-0"
                >
                    <template v-slot:item.place="{ item }">

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
                                    <nuxt-link class="regular-link" :to="{name: 'hosting-reservations-ref', params: {ref: item.reference}}" > {{item.place.title}}
                                    </nuxt-link>
                                </div>
                            </div>
                        </div>
                    </template>

                    <template v-slot:item.guests="{ item }">
                        {{item.guests == 1 ? "1 Guest" : `${item.guests} Guests`}}
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

    export default {
        name: "HostingReservations",
        components: {StarRating},
        layout: 'hosting',
        data() {
            return {
                headers: [
                    {text: 'Place', value: 'place'},
                    {text: 'Area', value: 'place.state'},
                    {text: 'checkin', value: 'checkin'},
                    {text: 'checkout', value: 'checkout'},
                    {text: 'Number of Guests', value: 'guests'},
                ],
                created: false,
                working: true,
                loaded: false,
                reservations: []
            }
        },
        methods: {
            getColor(calories) {
                if (calories > 400) return 'red'
                else if (calories > 200) return 'orange'
                else return 'green'
            },
        },

        mounted() {
            this.$axios.get(this.$api.Reservation.List).then((r) => {
                this.reservations = r.data
                this.created = true
                this.working = false
            })
            .finally(()=> {
                this.loaded = true
            })
        }

    }
</script>

<style lang="scss" scoped>

    .trips-list {
        margin-bottom: 50px;
    }

    img {
    }

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

    .IonTable tbody tr td {
        padding: 10px 15px;
    }

    .IonTable thead tr th {
        text-align: left;
        font-weight: 600;
        color: #4a4a4a;
        padding: 15px 15px;
    }
</style>
