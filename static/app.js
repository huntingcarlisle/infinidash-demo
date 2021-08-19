const container = document.querySelector('.container');

const URL = '/random_chart'

// get the images

function loadImages(numImages = 10){
   let i=0;
    while(i < numImages){
    fetch('/random_chart')
    .then(response=>response.json())
    .then(data=>{
    console.log(data)
    const img =  document.createElement('img');
    img.src = `${data.message}`
    container.appendChild(img)
    })
    i++;
    }   
    }

loadImages();


let end_reached = false;
    
        document.addEventListener('DOMContentLoaded', () => {
            loadImages();

            window.onscroll = () => {
                // check if we reached the bottom
                if(window.innerHeight + window.scrollY >= document.body.offsetHeight && end_reached == false) {
                    // alert("bottom");
                    loadImages();
                }
            }; 
        });

// // listen for scroll event and load more images if we reach the bottom of window
// window.addEventListener('scroll',()=>{
//     console.log("scrolled", window.scrollY) //scrolled from top
//     console.log(window.innerHeight) //visible part of screen
//     if(window.scrollY + window.innerHeight >= document.documentElement.scrollHeight){
//         loadImages();
//     }
// })