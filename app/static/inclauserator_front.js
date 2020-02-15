function to_clipboard(target) {
    var copy_text = document.getElementById(target);
    copy_text.select();
    document.execCommand("copy");
}

function redirect(to) {
    window.location.href = location.origin + to
}


function tabs_control(unhide) {
    let tabs = document.getElementById('tabs');
    let element = document.getElementById(unhide);
    let element_nav = document.getElementById('nav_' + unhide);

    element.style.display = 'block';
    element.style.visibility = 'visible';
    element_nav.classList.add('active');
    element_nav.children[0].classList.add('active');

    let tabs_children = tabs.children;
    for (i = 0; i < tabs_children.length; i++) {
        let child_id = tabs_children[i].children[0].id;
        if (child_id !== unhide) {
            tabs.querySelector('#' + child_id).style.display = 'none';
            tabs.querySelector('#' + child_id).style.visibility = 'hidden';
            document.querySelector('#nav_' + child_id).classList.remove('active');
            document.querySelector('#nav_' + child_id).children[0].classList.remove('active');
        }
    }
}


let pattern = document.getElementById('case_when_then_pattern');
let case_when_excel = document.getElementById('case_when_then_inclause_excel');
case_when_excel.onfocus = function () {
    let str = pattern.value;
    let arr = ['when', 'then', 'or', 'and'];
    arr.forEach(item => str = str.replace(item, item.toUpperCase()));
    pattern.value = str;
};