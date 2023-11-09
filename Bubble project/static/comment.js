$(document).ready(function () {
  $('.comment-icon').on('click', function (e) {
    e.preventDefault();
    const cardId = $(this).data('card-id');
    const card = $(`#card-${cardId}`);

    card.toggleClass('flipped');
  });

  $('.back-icon').on('click', function () {
    $(this).closest('.card').toggleClass('flipped');
  });
});
