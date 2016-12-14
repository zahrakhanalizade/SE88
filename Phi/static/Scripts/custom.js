$("#popover").popover({ trigger: "hover" });

$("#popover1").popover({ trigger: "hover" });
$("#popover2").popover({ trigger: "hover" });

$('form').on('submit', function () {
    if ($('#pass').val() != $('#confirm-pass').val()) {
        $('#pass').addClass('glyphicon-error').removeClass('has-success');
    } else {
        $('#pass').addClass('glyphicon-ok').removeClass('has-error');
    }

    $('input').each(function () {
        var formGroup = $(this).parents('.form-group');

        var glyphicon = formGroup.find('.glyphicon');

        if (this.checkValidity()) {
            formGroup.addClass('has-success').removeClass('has-error');
            glyphicon.addClass('glyphicon-ok').removeClass('glyphicon-remove');
        } else {
            formGroup.addClass('glyphicon-error').removeClass('has-success');
            glyphicon.addClass('glyphicon-remove').removeClass('glyphicon-ok');
        }
    });
});


function openCommentBox() {
    var text = "You gave " + $(this).text().length + " star";
    if ($(this).text().length > 1)
        text += "s. Leave a comment if you wish.";
    else
        text += ". Leave a comment if you wish.";
    
    document.querySelector('.modal-content .modal-header h4').innerHTML = text;
    var moviePoster = document.querySelector('#poster-img');
    document.querySelector('.modal-body img').setAttribute('src', moviePoster.getAttribute('src'));
    
    document.querySelector('#rate').value = $(this).text().length;
};
$('#rating li').click(openCommentBox);