function parsePost(post){
    let data = {
        title: post.title,
        content: post.text_context,
        creationDate: post.creation_date,
        image: post.image,
        owner: post.owner.username
    }
    return data
}

function createSubscriptionPost(post) {
    let postItem = document.createElement('div');
    let titleBlock = document.createElement('div');
    let titleContent = document.createElement('h2');
    let postOwner = document.createElement('span');
    let contentBlock = document.createElement('div');
    let imageWrapper = document.createElement('div')
    let postImage = document.createElement('img');
    let contentText = document.createElement('p');
    let creationDateBlock = document.createElement('p');
    let postData = parsePost(post);

    postItem.className = 'post_item';
    titleBlock.className = 'title_block';
    postOwner.className = 'post_owner';
    contentBlock.className = 'content_block';

    titleContent.innerHTML = postData.title;
    postOwner.innerHTML = postData.owner;

    contentText.innerHTML = postData.content;
    if (postData.image) {
        imageWrapper.className = 'image_wrapper';
        postImage.className = 'post_image';
        postImage.src = postData.image;
        imageWrapper.appendChild(postImage);
    }

    creationDateBlock.innerHTML = postData.creationDate;

    titleBlock.appendChild(titleContent);
    titleBlock.appendChild(postOwner);

    contentBlock.appendChild(contentText);
    contentBlock.appendChild(imageWrapper);

    postItem.appendChild(titleBlock);
    postItem.appendChild(contentBlock);
    postItem.appendChild(creationDateBlock);

    $('.subscriptions_posts_container').append(postItem);
}

function createPlaceholder() {
    let placeholderElement = document.createElement('h1');
    placeholderElement.innerHTML = '<h1>Feed is empty</h1>';
    $('.subscriptions_posts_container').append(placeholderElement);
}

function getSubscriptionPost() {
    // let token = 'Token 0622be3e627d790e8fdece4916730c6831a2332c';
    let url_prefix = '/api/v1/'
    let url = 'users/feed/'
    // let headers = {
    //     Authorization: token
    // };
    $.ajax({
        url: url_prefix + url,
        method: 'get',
        // headers: headers,
        success: function (data){
            subscriptionPosts = data.followed_user_posts
            if (subscriptionPosts.length > 0) {
                subscriptionPosts.forEach((element) => {
                    createSubscriptionPost(element);
                })
            }
            else {
                createPlaceholder();
            }

        }
    })
}

getSubscriptionPost();
