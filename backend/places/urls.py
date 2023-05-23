from django.urls import path

from places.components.views import TypeList, SpaceList, CityList, CheckInOutTimes, AmenityList, RulesList
from places.views import CreatePlaceView, PlaceListView, PlaceUpdateView, UploadImageView, DeleteImageView, \
    PlaceDetailView, RecentlyAddedPlaces, SimilarPlaceView, PlaceSearchView

app_name = 'places'

urlpatterns = [

    path("types", TypeList.as_view()),
    path("spaces", SpaceList.as_view()),
    path("cities", CityList.as_view()),
    path("amenities", AmenityList.as_view()),
    path("rules", RulesList.as_view()),
    path("check-times", CheckInOutTimes.as_view()),

    path("create", CreatePlaceView.as_view()),
    path("list", PlaceListView.as_view()),
    path("search", PlaceSearchView.as_view()),
    path("update/<code>", PlaceUpdateView.as_view()),
    path("details/<code>", PlaceDetailView.as_view()),
    path("similar/<code>", SimilarPlaceView.as_view()),

    path("details/<code>", PlaceDetailView.as_view()),

    path("add-image", UploadImageView.as_view()),
    path("remove-image/<pk>", DeleteImageView.as_view()),


    # places query
    path("recent-places", RecentlyAddedPlaces.as_view())


]
