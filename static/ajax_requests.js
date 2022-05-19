function getUserPosts(user_id, handleResult, is_other_profile) {
    // AJAX request to server to get users posts.
    // user_id - user id
    // handleResult - function that handles the returned data
    let url_prefix = '/api/v1';
    let url = `${url_prefix}/users/${user_id}/posts/`;
    console.log(url);
    $.ajax({
        method: "GET",
        url: url,
        dataType: "json",
        async: false,
        success: function(data) {
            handleResult(data, is_other_profile);
        }
    });
}

function deletePost(post_id, handleResult) {
    const csrftoken = getCookie('csrftoken');

    let url_prefix = '/api/v1';
    let url = `${url_prefix}/posts/${post_id}/destroy/`;

    $.ajax({
        type: "DELETE",
        url: url,
        dataType: "json",
        async: false,
        headers:{"X-CSRFToken": csrftoken },
        success: function(data) {
            handleResult(data, post_id);
        }
    });
}

function subAction(user_id, handleResult) {
    const csrftoken = getCookie('csrftoken');

    let url_prefix = '/api/v1';
    let url = `${url_prefix}/users/${user_id}/subscribe/`;

    $.ajax({
        type: "POST",
        url: url,
        dataType: "json",
        async: false,
        headers:{"X-CSRFToken": csrftoken },
        success: function(data) {
            handleResult(data, user_id);
        },
        error: function (data) {
            alert('Error:' + data.message);
        }
    });
}

// take it from https://stackoverflow.com/questions/68414729/django-rest-framework-ajax-form-submit-error-403-forbidden
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
