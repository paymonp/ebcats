
$(document).ready(function() {
    // category form event handler
    $('.categories #viewEvents').click(function() {
        console.log("Click");
        var selectedCats = $('.categories input:checkbox:checked')
        var numSelected = selectedCats.length;
        if (numSelected === 3) {
            // ajax request
            catIds = Array(3);
            selectedCats.each(function(index, elem) {
                catIds[index] = elem.value;
            });

            $.ajax({
                method: "GET",
                url: "/results",
                data: { cats: catIds },
                dataType: 'html'
            }).done(function(data) {
                $('.contentContainer').html(data);
            });
        }
        else {
            showError("Please pick exactly 3 categories");
        }
    });
});

function showError(errorText) {
    console.log("ero");
    $('.error').text(errorText);
}