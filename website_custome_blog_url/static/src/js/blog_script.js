$(function() {
  $('.list-group-item').on('click', function() {
    $('.fa', this).toggleClass('fa-angle-right arrow').toggleClass('fa-angle-down arrow');
  });
});
