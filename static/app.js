function addRoom(category_id, category_name) {
  $('#selected_category').text(category_name);
  $('select[name="category"]').val(category_id).change();
}