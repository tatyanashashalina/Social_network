function addPosts2Page(data, is_other_profile) {
    // Function that handles the returned data by AJAX request. The function adds the post to the page as an html
    // element.
    //
    // data - dictionary with posts, structure - {1: {"id": 1, ...}}

    let content_area = document.getElementById("id_content_area");

    for (let index in data){
        let post = data[index]
        let html_container_post = createPostElement(post, is_other_profile);
        html_container_post.id = "post_id_" + post.id;
        content_area.append(html_container_post);
    }

    let amount_of_posts = document.getElementById('amount_of_posts');
    amount_of_posts.innerHTML = "Amount of posts: "+ data.length.toString();
}

function createPostElement(post, is_other_profile) {
    // Function creates post like HTML element
    // post - object whose attributes contain information about the post

    // create 'div' container for whole post
    let container_post = document.createElement('div');
    container_post.className = "container_post";


    // create 'div' container for title
    let container_title = document.createElement('div');
    container_title.className = "container_title";

    let title = document.createElement("p");
    title.className = "title";
    title.innerHTML = post.title;

    container_title.append(title);


    // create 'div' container for text content
    let container_text_content = document.createElement('div');
    container_text_content.className = "container_text_content";

    let text_content = document.createElement("p");
    text_content.className = "text_content";
    text_content.innerHTML = post.text_context;

    container_text_content.append(text_content);

    // append title and text_content to post container
    container_post.append(container_title);
    container_post.append(container_text_content);

    if (post.edited) {
            // create 'div' container for edited
            let container_edited = document.createElement('div');
            container_edited.className = "container_edited";

            let edited = document.createElement("p");
            edited.className = "edited";
            edited.innerHTML = post.edited;
            container_edited.append('edited');
            // append title and change flag to post container
            container_post.append(container_edited);
        }

    if (post.image) {
        // create 'div' container for image
        let container_image = document.createElement("div");
        container_image.className = "container_image";

        let image = document.createElement("img");
        image.src = "data:image/png;base64," + post.image;

        container_image.append(image);

        container_post.append(container_image);

    }

    if (!is_other_profile) {
        // append delete button
        let container_buttons = document.createElement('div');
        container_buttons.className = "container_buttons";

        let delete_button = document.createElement("button");
        delete_button.className = "btn_delete";
        delete_button.innerHTML = "Delete";
        delete_button.onclick = function() { deletePost(post.id, hideDeletedPost) };
        container_buttons.append(delete_button);

        // append delete button to post container
        container_post.append(container_buttons);

        // create 'div' container for link
        let container_link = document.createElement('div');
        container_link.className = "container_link";

        //create link
        link = "post/edit/" + post.id;
        let element = document.createElement("a");
        element.setAttribute("href", link);
        element.innerHTML = "Edit";

        container_link.append(element);

        // append link to post container
        container_post.append(container_link);
    }

    return container_post;
}

function hideDeletedPost(data, post_id) {
    console.log('delete post_' + post_id);
    document.getElementById("post_id_" + post_id).style.display = 'none';
}

<<<<<<< HEAD:user/static/user/profile.js
// Function that handles the button to create a new post
=======
function changeSubButton(data, user_id) {
    if (data.message == 'subscribed') {
        document.getElementById('btn_action').value = 1;
        document.getElementById('btn_action').innerText = 'Unfollow';
    } else {
        document.getElementById('btn_action').value = 0;
        document.getElementById('btn_action').innerText = 'Follow';
    }
}

>>>>>>> 792b6c700bd4aa107a64929b931d414dff190757:user/static/user/js/profile.js
function callbackProfileButton() {
   document.location.href = "post/new";
}
