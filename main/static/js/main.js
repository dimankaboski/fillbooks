function openModalProp() {
    $('.all_content').addClass('overlay_blur');
    $('.overlay_dark').css('display', 'block');
    $('.modal').css('display', 'block');
}
function closeModalProp() {
    $('.all_content').removeClass('overlay_blur');
    $('.overlay_dark').css('display', 'none');
    $('.modal').css('display', 'none');
}
function getCookie(name) {
    var cookie = " " + document.cookie;
    var search = " " + name + "=";
    var setStr = null;
    var offset = 0;
    var end = 0;
    if (cookie.length > 0) {
        offset = cookie.indexOf(search);
        if (offset != -1) {
            offset += search.length;
            end = cookie.indexOf(";", offset)
            if (end == -1) {
                end = cookie.length;
            }
            setStr = unescape(cookie.substring(offset, end));
        }
    }
    return (setStr);
}