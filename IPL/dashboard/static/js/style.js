
$('.teams_slide').slick({
    autoplay:true,
    autoplaySpeed: 1000,
    slidesToShow: 7,
    prevArrow: false,
    nextArrow: false,
    pauseOnHover:true,
    responsive: [
      {
        breakpoint: 768,
        settings: {
          arrows: false,
          autoplay: true,
          autoplaySpeed: 1000,
          prevArrow: false,
          centerMode:false,
          nextArrow: false,
          slidesToShow: 4
        }
      },
      {
        breakpoint: 480,
        settings: {
          arrows: false,
          autoplay:true,
          autoplaySpeed: 1000,
          centerMode:false,
          prevArrow: false,
          nextArrow: false,
          slidesToShow: 2
        }
      }
    ]
  });


  $('.points').slick({
    autoplay:true,
    autoplaySpeed: 1000,
    slidesToShow:3,
    prevArrow: false,
    nextArrow: false,
    pauseOnHover:true,
    dots: true,
    responsive: [
      {
        breakpoint: 768,
        settings: {
          arrows: false,
          autoplay: true,
          autoplaySpeed: 1000,
          prevArrow: false,
          centerMode:false,
          nextArrow: false,
          slidesToShow: 2
        }
      },
      {
        breakpoint: 480,
        settings: {
          arrows: false,
          autoplay:true,
          autoplaySpeed: 1000,
          centerMode:false,
          prevArrow: false,
          nextArrow: false,
          slidesToShow: 1
        }
      }
    ]
  });


  $('.dropdown-menu').on( 'click', 'a', function() {
    var text = $(this).html();
    var htmlText = text + ' <span class="caret"></span>';
    $(this).closest('.dropdown').find('.dropdown-toggle').html(htmlText);
});


// home-cmplted-upcmng-bx-buttons


function hmlive(){
  document.getElementById('home-live').style.display='block'
  document.getElementById('home-pg-upcoming').style.display='none'
  document.getElementById('home-completed').style.display='none'
  document.getElementById('home-lve').style.backgroundColor='red'
  document.getElementById('home-lve').style.color='white'
  document.getElementById('home-upcmng').style.backgroundColor='#FFFCFC'
  document.getElementById('home-upcmng').style.color='red'
  document.getElementById('home-cmplt').style.backgroundColor='#FFFCFC'
  document.getElementById('home-cmplt').style.color='red'
  // document.getElementById('home-upcmng').style.backgroundColor='#FFFCFC'
  // document.getElementById('home-cmplt').style.backgroundColor='red'
}

function completed(){
  document.getElementById('home-completed').style.display='block'
  document.getElementById('home-pg-upcoming').style.display='none'
  document.getElementById('home-live').style.display='none'
  document.getElementById('home-cmplt').style.backgroundColor='red'
  document.getElementById('home-cmplt').style.color='white'
  document.getElementById('home-upcmng').style.backgroundColor='#FFFCFC'
  document.getElementById('home-upcmng').style.color='red'
  document.getElementById('home-lve').style.backgroundColor='#FFFCFC'
  document.getElementById('home-lve').style.color='red'
  // document.getElementById('home-upcmng').style.backgroundColor='#FFFCFC'
  // document.getElementById('home-cmplt').style.backgroundColor='red'
}

function upcoming(){
  document.getElementById('home-pg-upcoming').style.display='block'
  document.getElementById('home-live').style.display='none'
  document.getElementById('home-completed').style.display='none'
  document.getElementById('home-upcmng').style.backgroundColor='red'
  document.getElementById('home-upcmng').style.color='white'
  document.getElementById('home-cmplt').style.backgroundColor='#FFFCFC'
  document.getElementById('home-cmplt').style.color='red'
  document.getElementById('home-lve').style.backgroundColor='#FFFCFC'
  document.getElementById('home-lve').style.color='red'

  // document.getElementById('home-cmplt').style.backgroundColor='red'


}

// live-section buttons

// function live(){
//   document.getElementById('live-sctn-active-sctn').style.display='none'
//   document.getElementById('live-score-card').style.display='block'
//   document.getElementById('live-cmntry').style.display='none'
//   document.getElementById('live-btn').style.backgroundColor='red'
//   document.getElementById('live-btn').style.color='white'
//   document.getElementById('scorecard-btn').style.backgroundColor='white'
//   document.getElementById('scorecard-btn').style.color='red'
//   document.getElementById('commentry-btnn').style.backgroundColor='white'
//   document.getElementById('commentry-btnn').style.color='red'


// }

function scorecard(){
  document.getElementById('live-score-card').style.display='block'
  document.getElementById('live-cmntry').style.display='none'
  // document.getElementById('live-sctn-active-sctn').style.display='none'
  document.getElementById('scorecard-btn').style.backgroundColor='red'
  document.getElementById('scorecard-btn').style.color='white'
  document.getElementById('commentry-btnn').style.backgroundColor='white'
  document.getElementById('commentry-btnn').style.color='red'
  // document.getElementById('live-btn').style.backgroundColor='white'
  // document.getElementById('live-btn').style.color='red'
}  

function commentry(){
  document.getElementById('live-cmntry').style.display='block'
  document.getElementById('live-score-card').style.display='none'
  // document.getElementById('live-sctn-active-sctn').style.display='none'
  document.getElementById('commentry-btnn').style.backgroundColor='red'
  document.getElementById('commentry-btnn').style.color='white'
  // document.getElementById('live-btn').style.backgroundColor='white'
  // document.getElementById('live-btn').style.color='red'
  document.getElementById('scorecard-btn').style.backgroundColor='white'
  document.getElementById('scorecard-btn').style.color='red'

}  
/* background-color: #c21515; */

