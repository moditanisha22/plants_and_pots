// vw = $(window).outerWidth();

// $('#cart').click(flip);

// if (vw > 768) {
//  $('.card').hover(
// function() {
//   $('.description').toggleClass('show');
//   $('.image-wrapper').toggleClass('shrink');
// }
// ) 
// }

// function flip() {
//   $('#cart').addClass('flipped');
//   $('#cart').addClass('added');
//   $('.backside').addClass('show');
//   $('.front').addClass('hide');


// Image taken from 1924 - http://www.1924.us/post/110067977427


function increaseValue() {
  var value = parseInt(document.getElementById('number').value, 10);
  value = isNaN(value) ? 0 : value;
  value++;
  document.getElementById('number').value = value;
}

function decreaseValue() {
  var value = parseInt(document.getElementById('number').value, 10);
  value = isNaN(value) ? 0 : value;
  value < 1 ? value = 1 : '';
  value--;
  document.getElementById('number').value = value;
}