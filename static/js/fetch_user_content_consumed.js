//
//function fetch_user_consumed_content(user_id) {
////        console.log('in')
////    fetch('/users_content' + '/' + user_id)
////            .then(function (response) {
////                return response.json();
////            }).then(function (data) {
////
////                console.log(data.movie_list)
////
////                $('#user_content').append(
////                    `{% for movie in data.movie_list %}
////                        <div>{{movie}}</div>
////                        {% endfor %}
////                    `
////
////                )
////
////
////            });
//
//
//
//
//        $.ajax({
//                url: "users_content/"  + user_id,
//                method: 'GET',
//                success: function (data) {
//                    console.log(data.movie_list["movie_list"])
//                    // Insert the dynamic content into the placeholder div
//                    add = `<p>"${data.movie_list['movie_list']['name']}"</p>`
//                    $('#user_content').html("{% for movie in data.movie_list['movie_list'] %}{{movie}}{% endfor %}")
//                }
//            });
//
//
//}
