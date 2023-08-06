$(function () {
    $('#id_site').change(function () {
        let site_id = $(this).val();
        $.get('/autopost/category_tree/' + site_id, function (data) {
            render_category(data);
        });
    });
    $.get('/autopost/category_tree/' + $('#id_site').val(), function (data) {
        render_category(data);
    });
});

/**
 * 渲染分类下拉
 * @param data
 */
function render_category(data) {
    $('#id_parent').empty();
    let category_tree = data['tree'];
    $('#id_parent').append('<option value>-----</option>');
    $.each(category_tree, function (index, item) {
        $.each(item, function (i, node) {
            let opt = $('<option value="' + node.id + '">' + node.name + '</option>');
            $('#id_parent').append(opt);
        })
    });
}