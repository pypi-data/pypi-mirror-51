function slugFollowNameOrEmpty(slug, name) {
    /*Return True if the slug follow name or is empty*/

    if (!slug) {
        return true;
    }
    if (slug == cleanForSlug(name, true)) {
        return true;
    }
    return false;
}


function initSlugAutoPopulateFromName() {
    /* When name is focused, check if slug follow name or if it is
     * empty. Then, if yes, update the slug when the name change*/

    var slugUpdateTrigger = false;

    $('#id_name').on('focus', function() {
        var slug = $('#slug_id').val();
        slugUpdateTrigger = slugFollowNameOrEmpty(slug, this.value);
    });

    $('#id_name').on('change', function() {
        if (slugUpdateTrigger) {
            $('#id_slug').val(
                cleanForSlug(this.value, true)
            );
        }
    });
}

$(function() {
    /* Only update slug on non-live page*/
    if (!$('body').hasClass('page-is-alive')) {
        initSlugAutoPopulateFromName();
    }
}
);
