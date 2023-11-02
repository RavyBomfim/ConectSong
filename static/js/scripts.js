$(document).ready(function() {

    var icone_menu = $('#abrir-menu-lateral')
    var menu_lateral = $('#menu-lateral');

    icone_menu.click(function() {
        if(menu_lateral.css('display') === 'none') {
            menu_lateral.css('display', 'block');
        } else {
            menu_lateral.css('display', 'none');
        }
    });
    
});