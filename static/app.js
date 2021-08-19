const container = document.querySelector('.container');

// const URL = '/random_chart'

// // get the images

function loadImages(numImages = 10){
   let i=0;
    while(i < numImages){
    fetch('/random_chart')
    .then(response=>response.json())
    .then(data=>{
    console.log(data)
    let div = document.createElement('div')
    div.setAttribute('class', Math.floor(Math.random() * 2) ? 'grid-item':'grid-item--width2')

    let img =  document.createElement('img');
    img.src = `${data.message}`

    div.appendChild(img)
    container.appendChild(div)
    })
    i++;
    }   
    }

loadImages();


// let end_reached = false;
    
//         document.addEventListener('DOMContentLoaded', () => {
//             loadImages();

//             window.onscroll = () => {
//                 // check if we reached the bottom
//                 if(window.innerHeight + window.scrollY >= document.body.offsetHeight && end_reached == false) {
//                     // alert("bottom");
//                     loadImages();
//                 }
//             }; 
//         });

// init Packery
var grid = document.querySelector('.grid');
var pckry = new Packery( grid, {
  itemSelector: '.grid-item',
  percentPosition: true
});
// layout Packery after each image loads
imagesLoaded( grid ).on( 'progress', function() {
  pckry.layout();
});  
  
// var infScroll = new InfiniteScroll( '.grid', {
//     // Infinite Scroll options...
//     append: '.grid__item',
//     outlayer: pckry,
//   });

