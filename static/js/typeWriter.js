
//typeWriter Style H1
function typeWriter(text, n) {
  if (n < (text.length)) {
    $('.test').html(text.substring(0, n+1));
    n++;
    setTimeout(function() {
      typeWriter(text, n)
    }, 80);
  }
}

$( document ).ready(function(e) {
  var text = $('.test').data('text');
  typeWriter(text, 0);
});
