

function to_clipboard(target){
    var copy_text = document.getElementById(target);
    copy_text.select();
    document.execCommand("copy");
}

function redirect(to){
    window.location.href = location.origin + to
}