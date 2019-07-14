function showSubItems(id) {
    // showSubItems from cards to access submenu actions
    console.log(id);
    $('#sub_' + id + ' .subactions-items').toggle();
}