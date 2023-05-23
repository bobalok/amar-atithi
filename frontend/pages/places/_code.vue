<template>
    <div class="place-view-page" v-if="created">
        <ThumbGallery :images="place.images"/>

        <v-container grid-list-lg>
            <div class="PlaceDetailsWithSidebar">
                <div class="DetailsSide">
                    <div class="AboutPlace">
                        <div class="PlaceHeader mb-5">
                            <div class="PlaceMeta">
                                <h1 class="place-title mb-1">{{place.title}}</h1>

                                <div class="place-position">
                                    <nuxt-link to="/">{{place.state}}</nuxt-link>
                                </div>
                            </div>

                            <div class="PlaceHost">

                            </div>
                        </div>

                        <div class="PlaceBody">
                            <div class="glance">
                                <div class="glance-item d-flex mb-3">
                                    <div class="glance-icon mr-3">
                                        <i class="la la-home"></i>
                                    </div>

                                    <div class="item-body">
                                        <div class="ib-title">{{place.space.name}} in {{place.type.name}}</div>
                                        <div class="ib-content">
                                            <span><i class="la la-dot-circle-o"></i> {{place.max_guest}} guests</span>
                                            <span><i class="la la-dot-circle-o"></i> {{place.beds}} bed</span>
                                            <span><i class="la la-dot-circle-o"></i> {{place.baths}} bath</span>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <hr class="hr24"/>

                            <div class="excerpt">{{place.description}}</div>
                        </div>
                    </div>

                    <div class="section-amenities mt-8">
                        <!--                        <h2 class="section-title">Amenities</h2>-->

                        <div class="amenities-list mt-5">
                            <h4 class="amenities-list-title mb-2">Amenities</h4>

                            <div class="amenities-list-item pt-2 pb-2" v-for="amenity in place.amenities">
                                <div class="item-name">{{amenity.name}}</div>
                                <div class="item-desc" v-if="amenity.description">{{amenity.description}}</div>
                            </div>
                        </div>
                    </div>

                    <div class="policies-section mt-8">
                        <!--                        <h2 class="section-title mb-4">Policies</h2>-->

                        <div class="sec-rules">
                            <h4 class="section-subtitle mb-1">House Rules</h4>

                            <ul class="house-rules">
                                <li class="hr-item" v-for="rule in place.rules">{{rule.name}}</li>
                            </ul>
                        </div>

<!--                        <hr class="hr24" style="width: 75px;">-->

<!--                        <div class="sec-acknowledgements">-->
<!--                            <h4 class="section-subtitle mt-4 mb-1">You must also acknowledge</h4>-->

<!--                            <ul class="house-rules">-->
<!--                                <li class="hr-item">Potential for noise - Friday nights until 10pm there is sometimes-->
<!--                                    noise from downstairs-->
<!--                                </li>-->
<!--                                <li class="hr-item">Must climb stairs - Two flights of stairs</li>-->
<!--                            </ul>-->
<!--                        </div>-->
                    </div>

                    <!--                    <div class="sleeping-arrangements mt-8">-->
                    <!--                        <h2 class="section-title mb-6">Sleeping Arrangement</h2>-->
                    <!--                        <v-container fluid class="pa-0">-->
                    <!--                            <v-layout row wrap>-->
                    <!--                                <v-flex xs4>-->
                    <!--                                    <div class="arrangement-item pa-4">-->
                    <!--                                        <i class="la la-bed"></i>-->

                    <!--                                        <div class="room-name mt-2">Bedroom 1</div>-->
                    <!--                                        <div class="room-capacity">1 Master Bed</div>-->
                    <!--                                    </div>-->
                    <!--                                </v-flex>-->

                    <!--                                <v-flex xs4>-->
                    <!--                                    <div class="arrangement-item pa-4">-->
                    <!--                                        <i class="la la-bed "></i>-->

                    <!--                                        <div class="room-name mt-2">Bedroom 2</div>-->
                    <!--                                        <div class="room-capacity">1 Single Bed</div>-->
                    <!--                                    </div>-->
                    <!--                                </v-flex>-->
                    <!--                            </v-layout>-->
                    <!--                        </v-container>-->
                    <!--                    </div>-->
                    <hr class="hr24 mt-10 mb-10">

                    <div class="about-host mt-8">
                        <div class="host-header d-flex">
                            <div class="host-meta">
                                <h2 class="section-title mb-2">Hosted by {{place.host.name}}</h2>
                                <!--                                <div class="host-meta">New York, NY · Joined in November 2012</div>-->
                                <div class="host-meta">Joined in {{place.host.joined}}</div>
                                <!--                                <div class="host-review-count"><i class="la la-star"></i> 320 Reviews</div>-->
                            </div>

                            <div class="host-avatar">
                                <nuxt-link :to="{name: 'users-userid', params: {userid: place.host.userid}}">
                                    <v-avatar :size="60">
                                        <img :src="place.host.avatar" :alt="place.host.name">
                                    </v-avatar>
                                </nuxt-link>
                            </div>
                        </div>

                        <div class="host-bio">{{place.host.bio}}</div>
                    </div>


                </div>

                <div class="FixedSidebar">
                    <div class="ReservePortlet pa-6">
                        <div class="PortletHeader">
                            <div class="PriceTag">
                                <span class="amount">{{ $Settings.Price(place.price)}}</span> per night
                            </div>

                            <div class="RatingsCount d-flex">
                                <div class="rating">
                                    <StarRating :value="place.rating"/>
                                </div>
                                <div class="ml-2 count">{{place.rating_count}}</div>
                            </div>
                        </div>

                        <v-form lazy-validation v-model="sidebar.valid" ref="form" @submit.prevent="FormSubmit">
                            <div class="PortletBody">

                                <v-container class="pa-0" fluid>
                                    <v-layout wrap>
                                        <v-flex xs6>
                                            <div class="form-group">
                                                <label>Check-in</label>

                                                <v-menu
                                                        v-model="picker.checkin"
                                                        :close-on-content-click="false"
                                                        :nudge-right="40"
                                                        transition="scale-transition"
                                                        offset-y
                                                        full-width
                                                        min-width="290px"
                                                >
                                                    <template v-slot:activator="{ on }">
                                                        <v-text-field
                                                                :rules="[rules.required]"
                                                                label="Check-in Date"
                                                                solo
                                                                flat
                                                                v-model="sidebar.checkin"
                                                                v-on="on"
                                                        ></v-text-field>
                                                    </template>
                                                    <v-date-picker
                                                            @change="CheckInChanged"
                                                            :min="tomorrow"
                                                            no-title
                                                            v-model="sidebar.checkin"
                                                            @input="picker.checkin = false"></v-date-picker>
                                                </v-menu>
                                            </div>
                                        </v-flex>

                                        <v-flex xs6>
                                            <div class="form-group">
                                                <label>Checkout</label>

                                                <v-menu
                                                        v-model="picker.checkout"
                                                        :close-on-content-click="false"
                                                        :nudge-right="40"
                                                        transition="scale-transition"
                                                        offset-y
                                                        full-width
                                                        min-width="290px"
                                                >
                                                    <template v-slot:activator="{ on }">
                                                        <v-text-field
                                                                :rules="[rules.required]"
                                                                label="Checkout Date"
                                                                solo
                                                                flat
                                                                v-model="sidebar.checkout"
                                                                v-on="on"
                                                        ></v-text-field>
                                                    </template>
                                                    <v-date-picker
                                                            :min="min_checkout"
                                                            @change="ClearQuery"
                                                            no-title
                                                            scrollable
                                                            v-model="sidebar.checkout"
                                                            @input="picker.checkout = false"></v-date-picker>
                                                </v-menu>
                                            </div>
                                        </v-flex>
                                    </v-layout>
                                </v-container>

                                <div class="form-group">
                                    <label>Guests</label>
                                    <v-select
                                            :rules="[rules.required]"
                                            :items="GuestsList"
                                            label="Number of guests"
                                            solo
                                            flat
                                    ></v-select>
                                </div>

                                <div class="price-list" v-if="sidebar.QueryComplete && sidebar.response.available">
                                    <div class="price-item d-flex" v-for="item in sidebar.response.breakdown">
                                        <span>{{item.label}}</span>
                                        <span class="tCost">{{ $Settings.Price(item.amount)}}</span>
                                    </div>

                                    <div class="price-item d-flex">
                                        <strong>Total</strong>
                                        <strong class="tCost">{{ $Settings.Price(sidebar.response.subtotal)}}</strong>
                                    </div>
                                </div>

                                <div class="error--text mb-3"
                                     v-if="sidebar.QueryComplete && !sidebar.response.available">
                                    {{sidebar.response.message}}
                                </div>

                                <div class="error--text mb-3" v-html="reservation_error" v-if="reservation_error"> </div>

                                <v-btn
                                        v-if="!sidebar.QueryComplete || !sidebar.response.available"
                                        type="submit"
                                        color="primary"
                                        large
                                        block
                                        class="tall mt-3"
                                        :disabled="sidebar.working"
                                        :loading="sidebar.working"
                                >Check Availability
                                </v-btn>
                                <div v-else>
                                    <v-btn
                                            v-if="isAuthenticated"
                                            @click="CreateReservation"
                                            color="primary"
                                            large
                                            block
                                            class="tall mt-3"
                                            :disabled="sidebar.working"
                                            :loading="sidebar.working"
                                    >Reserve
                                    </v-btn>
                                    <v-btn
                                            v-else
                                            to="/login"
                                            color="primary"
                                            large
                                            block
                                            class="tall mt-3"
                                    >Login to Reserve</v-btn>
                                </div>
                            </div>
                        </v-form>
                    </div>
                </div>
            </div>


            <div class="more-places mt-12 mb-8" v-if="recommendation.places.length">
                <h2 class="section-title mb-2">More places to stay</h2>

                <v-layout row wrap>
                    <v-flex xs3 v-for="item in recommendation.places " :key="place.code">
                        <PlaceCard :place="item"/>
                    </v-flex>
                </v-layout>
            </div>

        </v-container>


    </div>
</template>

<script>
    import ThumbGallery from "../../components/places/ThumbGallery";
    import PlaceCard from "../../components/places/PlaceCard";
    import StarRating from "../../components/general/StarRating";
    import moment from "moment";
    import {mapGetters} from 'vuex'

    export default {
        name: "ViewPlaceDetails",
        components: {StarRating, PlaceCard, ThumbGallery},
        layout: "regular",
        data: () => {
            return {
                rules: [],
                picker: {
                    checkin: false,
                    checkout: false
                },
                sidebar: {
                    checkin: null,
                    checkout: null,
                    guest: 1,
                    working: false,
                    QueryComplete: false,
                    valid: false,
                    response: {
                        available: false
                    }
                },
                created: false,
                working: true,
                place: [],
                reservation_error: "",
                recommendation: {
                    created: false,
                    places: []
                }
            }
        },
        mounted() {
            this.rules = this.$validator.rules
            let code = this.$route.params.code
            let api = this.$api.Place.Details(code)
            let similar_api = this.$api.Place.Similar(code)

            this.$axios.get(api).then((r) => {
                this.place = r.data
                this.created = true
                this.working = true
            })

            this.$axios.get(similar_api).then((r) => {
               this.recommendation.places = r.data
                this.recommendation.created = true
            })
        },

        computed: {
            ...mapGetters(['isAuthenticated', 'loggedInUser']),
            GuestsList() {
                let items = []

                for (let i = 1; i <= this.place.max_guest; i++) {
                    items.push({
                        text: i > 1 ? `${i} guests` : `${i} guest`,
                        value: i
                    })
                }

                return items
            },
            tomorrow() {
                var today = moment();
                var tomorrow = moment(today).add(1, 'days');
                return tomorrow.format(this.$Settings.MySqlDate)
            },
            min_checkout() {
                let checkin = ""

                if (!this.sidebar.checkin)
                    checkin = moment(moment()).add(1, 'days')
                else
                    checkin = moment(this.sidebar.checkin);

                let next = checkin.add(this.place.min_stay, 'days');
                return next.format(this.$Settings.MySqlDate)
            }
        },
        methods: {
            CheckInChanged() {
                this.sidebar.checkout = null
                this.ClearQuery()
            },
            ClearQuery() {
                this.sidebar.QueryComplete = false;
                this.sidebar.response = {available: false}
            },
            FormSubmit() {
                this.sidebar.QueryComplete = false

                let check = new Promise((resolve, reject) => {
                    this.$refs.form.validate();
                    resolve();
                });

                check.then(() => {
                    if (this.sidebar.valid) {
                        this.GetAQuote();
                    }
                });
            },
            GetAQuote() {
                this.sidebar.working = true

                let data = {
                    checkin: this.sidebar.checkin,
                    checkout: this.sidebar.checkout,
                    place: this.$route.params.code
                }

                this.$axios.post(this.$api.Reservation.GetQuote, data)
                    .then(r => {
                        this.sidebar.response = r.data
                        this.sidebar.QueryComplete = true
                    })
                    .finally(() => {
                        this.sidebar.working = false
                    })
            },
            CreateReservation() {

                if (!this.sidebar.checkin || !this.sidebar.checkout)
                    return

                let data = {
                    checkin: this.sidebar.checkin,
                    checkout: this.sidebar.checkout,
                    place: this.$route.params.code,
                    guests: this.sidebar.guest
                }

                this.sidebar.working = true

                this.$axios.post(this.$api.Reservation.CreateDraft, data)
                    .then((res) => {
                        this.$router.push({name: "book-ref-house-rules", params: {ref: res.data.reference}})
                    })
                    .catch(( error )=> {
                        let errorRes = error.response

                        if( errorRes && errorRes.data.available == false ){
                            this.reservation_error = errorRes.data.message
                            this.working = false
                            this.sidebar.working = false
                        }
                    })
                    .finally(()=> {
                        this.working = false

                    })
            }
        }
    }
</script>

<style lang="scss" scoped>

    .PlaceDetailsWithSidebar {
        margin: 18px 0;
        font-size: 16px;
        position: relative;


        .DetailsSide {
            padding-right: 450px;

            .section-title {
                font-size: 24px;
                line-height: 1.2;
                margin: 0;
            }

            .glance {
                .ib-title {
                    margin-bottom: 2px;
                    font-weight: 600;
                    font-size: 16px;
                    line-height: 1.375em !important;
                }

                .ib-content {
                    span {
                        margin-right: 12px;

                        i {
                            font-size: 12px;
                        }
                    }
                }
            }

            hr.hr24 {
                border-color: #eaeaea;
                display: block;
                height: 1px;
                width: 100%;
                overflow: hidden;
                margin: 24px 0;
            }


        }

        .RatingsCount {
            .rating {
                margin-top: 3px;
            }
        }
    }


    .FixedSidebar {
        position: absolute;
        right: 0;
        top: 0;
        width: 450px;
        padding-left: 50px;

        .ReservePortlet {
            border: 1px solid #E6E6E6;

            .PortletHeader {
                border-bottom: 1px solid #E6E6E6;
                padding-bottom: 16px;
                margin-bottom: 24px;

                .PriceTag {
                    margin-bottom: 4px;

                    span {
                        font-size: 1.75rem;
                        font-weight: 600;
                        letter-spacing: -1px;
                    }
                }
            }

            .CheckInOutPicket {
                display: flex;
                flex-direction: row;
                width: 100%;
                border: 1px solid #cacaca;

                input {
                    border: none;
                    height: 41px;
                    font-size: 15px;
                }

                .MidIcon {
                    font-size: 1.65rem;
                    padding: 0 10px;
                    height: 41px;
                    line-height: 41px;
                    color: #808080;
                }
            }


        }
    }


    .amenities-list-title {
        font-weight: 800;
        font-size: 1.15rem;
    }


    .place-title {
        font-size: 2.25rem;
        font-weight: 600;
        display: block;
        line-height: 1.15;
    }

    .item-name {
        font-size: 16px;
    }
    .item-desc {
        font-size: 14px;
        margin-top: 5px;
    }


    .arrangement-item {
        border: 1px solid #ededed;

        i {
            font-size: 1.75rem;
        }
    }


    .place-position {

        a {
            color: inherit;
            text-decoration: none;
        }
    }


    .about-host {
        .host-meta {
            margin-bottom: 4px;
        }

        .host-avatar {
            margin-left: auto;
        }

        .host-review-count {
            margin-top: 6px;

            i {
                margin-right: 4px;
            }
        }


        .host-bio {
            margin-top: 12px;
        }
    }

    .price-list {
        margin-bottom: 12px;

        .price-item {
            padding: 10px 0;
            border-bottom: 1px solid #ddd;

            &:last-child {
                border-bottom: 0;
            }

            .tCost {
                margin-left: auto;
            }
        }
    }


    .policies-section {
        .house-rules {
            margin: 16px 0 0 0;
            padding: 0;
            list-style: none;
        }

        .hr-item {
            margin: 6px 0 0 0;
        }
    }


</style>
