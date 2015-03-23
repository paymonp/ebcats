var loading = false;
var catIds = Array(3);
var currentPage = 1;

$(function() {
    // category form event handler
    $('.categories #viewEvents').click(function() {
        if (loading) {
            return;
        }
        var selectedCats = $('.categories input:checkbox:checked')
        var numSelected = selectedCats.length;

        if (numSelected === 3) {
            loading = true;
            setError(false, "");
            $('.loadingGif').show();
            // get the ids of the selected categories
            selectedCats.each(function(index, elem) {
                catIds[index] = elem.value;
            });
            // send ajax request to load page 1 of the search results
            loadEvents(1);
        }
        else {
            setError(true, "Please pick exactly 3 categories");
        }
    });
});

function bindPaginationEvents() {
    function getNumPages() {
        return parseInt($('.resultsPagination .numPages').html())
    }
    $('.resultsPagination .first').click(function() {
        loadEventsFromPaginationLink(1);
    });
    $('.resultsPagination .prev').click(function() {
        loadEventsFromPaginationLink(Math.max(1, currentPage - 1));
    });
    $('.resultsPagination .next').click(function() {
        loadEventsFromPaginationLink(Math.min(getNumPages(), currentPage + 1));
    });
    $('.resultsPagination .last').click(function() {
        loadEventsFromPaginationLink(getNumPages());
    });
}

function loadEventsFromPaginationLink(pageNum) {
    if (loading) {
        return;
    }
    loading = true;
    $('.content').html('');
    $('.loadingGif').show();
    loadEvents(pageNum);
}

/*
 Using the catIds array and a given page_num.
 performs an ajax request to load the page
 of events.

 If the page number is out of bounds,
 the server will find the closest page
 (either the first or last) to it.
*/
function loadEvents(pageNum) {
    $.ajax({
        method: "GET",
        url: "/results",
        data: { cats: catIds, page: pageNum },
        dataType: 'html'
    }).done(function(data) {
        $('.loadingGif').hide();
        $('.content').html(data);
        loading = false;
        currentPage = parseInt($('.resultsPagination .curr').html());
        // bind pagination events here now that the pagination content is in the DOM
        bindPaginationEvents();
    });
}

/*
Sets the error text on the categories page

Params:
show - set true to make the error message visible
errorText - the new error text
*/
function setError(show, errorText) {
    $('.error').toggle(show);
    $('.error').text(errorText);
}
