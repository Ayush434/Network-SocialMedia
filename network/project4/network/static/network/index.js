document.addEventListener('DOMContentLoaded', function() {

    // if someone post a New Post then save_post function should be triggered
    document.querySelector("#compose-form").addEventListener("submit", save_post);

    // Load index page by default
    load_page();
  
  });



  function save_post(event){

    event.preventDefault();
  
    const content = document.querySelector("#postContent").value;

    fetch('/posts', {
      method: 'POST',
      body: JSON.stringify({
          content: content
      })
    })
    .then(response => response.json())
    .then(result => {
        // Clear the posts so we can have updated list without refreshing the page
        document.querySelector("#posts-view").innerHTML = "";
        load_page();
    });
  
  }


  function load_page(){
    //make the new post text area empty
    document.querySelector("#postContent").value = "";
    document.querySelector("#posts-view").innerHTML = "";
    document.querySelector('#page-number').innerHTML = "";

    // get new posts and add them as a div under #posts-view
    getUser();
    pagination();
  }

function getUser(){
    
    fetch(`/currentUser`)
    .then((response) => response.json())
    .then((user) => {
        // console.log(user.username);
        var username = user.username;
        getPosts(1, username);
    });
    
}

function getPosts(counter, currentUser){
    
    document.querySelector("#postContent").value = "";
    document.querySelector("#posts-view").innerHTML = "";


    fetch(`/posts/posts?page=${counter}`)
    .then((response) => response.json())
    .then((page_obj) => {
        
        console.log(page_obj);
        page_obj.forEach((element) => {


        var item = document.createElement("div");
        item.className = `card  my-1 items`;

        item.innerHTML = `<div class="card-body" id="item-${element.id}">
        <a href="http://127.0.0.1:8000/%2Fprofile/${element.user}" class="green-link" id="user_link_${element.id}">
                    <strong>${element.user}</strong>
                    
        </a>
        <hr>
        <div id="post_contentgroup_${element.id}">
        
            <p id="post_content_${element.id}">${element.description}</p>

        </div>

        <br>
        
        <p id="post_time_${element.id}">${element.timestamp}</p>
        <p id="post_num_likes_${element.id}">${element.likes}</p>

        <div id="post_likes_${element.id}">

            

        </div>
        
        </div>`;
        
        
        document.querySelector("#posts-view").appendChild(item);

        
        
        if(currentUser === element.user){
            // create button to edit posts
            let next = document.createElement('btn');

            next.innerHTML = `<button id="edit-${element.id}" class="btn btn-primary" >Edit</button>`
            next.setAttribute(
                'style',
                'margin-left: 90%;'
            );

            next.addEventListener("click", () => {
                edit_post(element);

            });

            let saveButton = document.createElement("btn");
            saveButton.id = `post_save_${element.id}`;
            saveButton.innerHTML = `<button > Save Post</button> `
            saveButton.setAttribute(
                'style',
                'margin-left: 90%; color: blue; display: none;'
            );
    
    
            saveButton.addEventListener("click", () => {
                update_post(element.id);
            });

            item.appendChild(next);
            item.appendChild(saveButton);

        };

        fetch(`/postLikedByUser/${element.id}`)
        .then((response) => response.text())
        .then((text) => {
            
            result = JSON.parse(text);
            console.log(result["liked"]);

            var ans = result["liked"]
            let likeBtn = document.createElement('btn');

            if(element.likes > 0 && ans === true){
                likeBtn.innerHTML = `<button id ="like_${element.id}" value ="${element.id}" >
                <i id="current_like_${element.id}" class="likeicon fa-heart fas"></i>
                </button>`;
            }else{
                likeBtn.innerHTML = `<button id ="like_${element.id}" value ="${element.id}" >
                <i id="current_like_${element.id}" class="likeicon fa-heart far"></i>
                </button>`;
            }

            

            likeBtn.addEventListener("click", () => {
                update_likes(element);
            });

            document.querySelector(`#post_likes_${element.id}`).appendChild(likeBtn);



        });   
        
        })
        

    });
}


function update_likes(element){

    var currentLike = document.querySelector(`#current_like_${element.id}`);
    var likes = document.querySelector(`#post_num_likes_${element.id}`);

    console.log(likes);

    var likesInt = parseFloat(likes.innerHTML);
    console.log(likesInt);
    console.log(likesInt+1);

    if(currentLike.className === "likeicon fa-heart far"){
        currentLike.className = "likeicon fa-heart fas";
        makeLike = true;
        likes.innerHTML = likesInt+1;
        
    }else{
        currentLike.className = "likeicon fa-heart far";
        makeLike = false;
        likes.innerHTML = likesInt-1;
    }

    
    console.log(makeLike);
    UpdateLike(element.id);
    
}

function UpdateLike(id){
    fetch(`/updateLikes/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            like: makeLike,
        }),
      });
}

function edit_post(element){

    // hide the user link
    let user_link = document.querySelector(`#user_link_${element.id}`);
    user_link.style.display = "none";

    // hide the original post content
    let originalContent = document.getElementById(`post_content_${element.id}`);
    // console.log(originalContent);
    var content = originalContent.innerHTML;
    // console.log(content);
    
    originalContent.style.display = "none";

    // hide the post timestamp
    let postTime = document.getElementById(`post_time_${element.id}`);
    postTime.style.display = "none";

    // hide the edit button
    let editBtn = document.getElementById(`edit-${element.id}`);
    editBtn.style.display = "none";



    // hide the likes button and number
    let likeDiv = document.querySelector(`#post_likes_${element.id}`);
    let likeP = document.querySelector(`#post_num_likes_${element.id}`);

    likeDiv.style.display = "none";
    likeP.style.display = "none";

    // unhide the edit button
    let saveBtn = document.getElementById(`post_save_${element.id}`);
    console.log(saveBtn);
    saveBtn.style.display = "block";


    var target = document.getElementById(`item-${element.id}`);

    var textArea = document.createElement("textarea");
    textArea.className = "form-control";
    textArea.innerHTML = content;

    textArea.id = `editContent_${element.id}`


    
    target.appendChild(textArea);
    console.log(target);
}


function update_post(id){

    var content = document.querySelector(`#editContent_${id}`).value;
    console.log(content);

    fetch('/updatePosts', {
        method: 'POST',
        body: JSON.stringify({
            content: content,
            postId: id
        })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);

             // unhide the user link            
            let user_link = document.querySelector(`#user_link_${id}`);
            console.log(user_link);
            user_link.style.display = "block";

            // unhide the original post content
            let originalContent = document.getElementById(`post_content_${id}`);
            originalContent.innerHTML = content;
            
            originalContent.style.display = "block";

            // unhide the post timestamp
            let postTime = document.getElementById(`post_time_${id}`);
            postTime.style.display = "block";

            // unhide the edit button
            let editBtn = document.getElementById(`edit-${id}`);
            editBtn.style.display = "block";


            // unhide the likes button and number
            let likeDiv = document.querySelector(`#post_likes_${id}`);
            let likeP = document.querySelector(`#post_num_likes_${id}`);
            
            likeDiv.style.display = "block";
            likeP.style.display = "block";

            // hide the edit button
            let saveBtn = document.getElementById(`post_save_${id}`);
            saveBtn.style.display = "none";

            // hide the edit button
            let textArea = document.getElementById(`editContent_${id}`);
            textArea.remove();


            var target = document.getElementById(`item-${id}`);
    
        });

  }


function pagination(){

    fetch(`/posts/pages`)
    .then(response => response.json())
    .then(result => {
        console.log(result);

        if(result.pages > 1){
                let counter = 1;
                let previous = document.createElement('li')
                previous.innerHTML = `<a class="page-link" href="#" aria-label="Next"><span aria-hidden="true">&laquo;</span></a>`
                previous.classList.add("page-item")
                
                
                let next = document.createElement('li')
                next.innerHTML = `<a class="page-link" href="#" aria-label="Next"><span aria-hidden="true">&raquo;</span></a>`
                next.classList.add("page-item")

                

                previous.addEventListener('click', function () {
                    counter--
                    getPosts(counter)
                    if (counter === 1) {
                        previous.style.display = 'none'
                        next.style.display = 'block'
                    } else {
                        next.style.display = 'block'
                    }
                })

                next.addEventListener('click', function () {
                    console.log(counter);
                console.log(result.pages);
                    if(counter < result.pages ){

                        counter++
                        getPosts(counter)
                        previous.style.display = 'block'
                    }
                    if (counter >= result.pages) {
                        console.log("i am in here");
                        next.style.display = 'none'
                        previous.style.display = 'block'
                    } 
                        
                    
                        console.log(counter);
                })
                    previous.style.display = 'none'
                    document.querySelector('#page-number').append(previous)
                    document.querySelector('#page-number').append(next)
        }


    })


}
  







  