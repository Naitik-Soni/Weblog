window.onload = function(){
    getStories("__");
};

var blogdata;

function getStories(q){
    var query;
    if(q=="__"){
        query = "*";
    }
    else{
        query = document.getElementById("search-blog").value;
    }

    if(query == ''){
        query = "*";
    }

    var xhr = new XMLHttpRequest();
    xhr.open('GET', './getblog/' + query);

    xhr.onload = function(){
        if(xhr.status === 200){
            var container = document.getElementsByClassName('container')[0];
            while(container.firstChild){
                container.removeChild(container.firstChild);
            }

            blogdata = JSON.parse(xhr.responseText);

            if(blogdata.blogData.length == 0){
                var h2 = document.createElement("h2");
                h2.innerHTML = "No Blogs Found!";
                container.appendChild(
                    h2
                );
            }

            for(data of blogdata.blogData){
            (function(data) {
                const outerdiv = document.createElement("div");
                const innerdiv = document.createElement("div");
                const head = document.createElement("h2");
                const image = document.createElement("img");
                const para = document.createElement("p");

                outerdiv.className = "blog";
                innerdiv.className = "img";

                outerdiv.addEventListener("click", function(){
                    location.replace("../Blog/" + data.blog_title);
                });

                image.src = "/media/" + data.blog_image;

                head.innerHTML = data.blog_title;
                para.innerHTML = data.blog_content;

                innerdiv.appendChild(image);
                outerdiv.appendChild(innerdiv);
                outerdiv.appendChild(head);
                outerdiv.appendChild(para);

                container.appendChild(outerdiv);
            })(data);

            }
        }
    };
    xhr.send();
}