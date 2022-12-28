document.addEventListener('DOMContentLoaded', function() {

    // if someone post a New Post then save_post function should be triggered
    // document.querySelector("#following").addEventListener("click", load_page());
    load_page()

  
  });


  function load_page(){
    document.querySelector("#following-posts-view").innerHTML = "";
    document.querySelector('#following-page-number').innerHTML = "";

    // get new posts and add them as a div under #posts-view
    console.log("following js is triggered");
    getPosts(1);
    pagination();
  }


function getPosts(counter){
    
    document.querySelector("#following-posts-view").innerHTML = "";

    console.log("happening");
    fetch(`/following/posts?page=${counter}`)
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
            console.log(item);
            document.querySelector("#following-posts-view").appendChild(item);
        
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

    console.log(likes.innerHTML);

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

function pagination(){

    fetch(`/following/pages`)
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
                    document.querySelector('#following-page-number').append(previous)
                    document.querySelector('#following-page-number').append(next)
        }


    })


}
  







  