$().ready(function() {
  $('#sidebar-username').on('click', function(e) {
    $(e.target).toggle();
    $('#change-username').toggle();
  });
  $('#sidebar-bio').on('click', function(e) {
    $(e.target).toggle();
    $('#change-bio').toggle();
  });
  $('#change-username').focusout(function() {
    $('#form-username').val();

    console.log($('#form-username').val());
    console.log('testing');
  });

  $('.likebutton').on('click', function(e) {
    let userid = e.target.attributes['data-userid'].value;
    let messageid = e.target.attributes['data-messageid'].value;

    if (e.target.innerHTML === 'Like') {
      let route = `/users/${userid}/messages/${messageid}/like`;
      $.get(route).then(function(response) {
        e.target.innerHTML = 'Unlike';
      });
    } else {
      let route = `/users/${userid}/messages/${messageid}/like?_method=DELETE`;
      $.post(route).then(function(response) {
        e.target.innerHTML = 'Like';
        console.log('Deleted!');
      });
    }
    $(e.target).toggleClass('btn-danger');
    $(e.target).toggleClass('btn-outline-primary');
  });
});
