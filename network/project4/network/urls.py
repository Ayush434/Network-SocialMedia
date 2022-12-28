
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),    
    path("posts/<str:endpoint>", views.show_posts, name="show_posts"),
    path("following/<str:endpoint>", views.userFollowingPosts, name="userFollowingPosts"),
    path("following", views.followingIndex, name="followingIndex"),
    path("/profile/<str:username>", views.profileIndex, name="profileIndex"),
    path("profilePosts/<str:endpoint>", views.profilePosts, name="profilePosts"),
    path("follow/<str:username>", views.follow, name="follow"),
    path("unfollow/<str:username>", views.unfollow, name="unfollow"),
    path("updateLikes/<int:postId>", views.updateLikes, name="updateLikes"),
    path("postLikedByUser/<int:postId>", views.postLikedByUser, name="postLikedByUser"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("posts", views.save_post, name="save_post"),
    path("updatePosts", views.update_post, name="update_post"),
    path("currentUser", views.currentUser, name="currentUser"),
]
