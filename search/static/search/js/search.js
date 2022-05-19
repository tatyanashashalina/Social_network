function changeSubButton(data, user_id) {
    if (data.message == 'subscribed') {
        document.getElementById('sub_' + user_id).value = 1;
        document.getElementById('sub_' + user_id).innerText = 'Unfollow';
    } else {
        document.getElementById('sub_' + user_id).value = 0;
        document.getElementById('sub_' + user_id).innerText = 'Follow';
    }
}
