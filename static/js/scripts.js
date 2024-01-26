$(document).ready(function() {

    profile_search = $('#profile-search');

    var icone_menu = $('#open-lateral-menu')
    var menu_lateral = $('#lateral-menu');

    icone_menu.click(function() {
        if(menu_lateral.css('display') === 'none') {
            menu_lateral.css('display', 'block');
        } else {
            menu_lateral.css('display', 'none');
        }
    });

    $('#profile-search').on('input', function () {
        var caracteres = $(this).val();
        console.log(caracteres);
        var profile_list = $('#profile-list');
        
        if (caracteres) {
            $('#profile-list').css('display', 'flex');
            $('#search-bar').addClass('search-bar-background');
            $.ajax({
                url: '/pesquisar/perfis/',
                method: 'GET',
                data: {search: caracteres},
                contentType: 'application/json',
                dataType: 'json',
                success: function (data) {
                    profile_list.empty();

                    if (data.perfis.length == 0) {
                        profile_list.append('<li id="no-results">Nenhum Resultado Encontrado</li>');
                    } else {
                        for (var i = 0; i < data.perfis.length; i++) {
                            var profile = data.perfis[i];
                            var list_item = '<li><a href="/perfil/' + profile.perfil_username + '">';
                            if (profile.foto_perfil) {
                                list_item += '<img src="' + profile.foto_perfil + '" alt="">';
                            } else {
                                list_item += '<img src="../static/img/perfil-generico.png" alt="">';
                            }
                            list_item += '<div class="profile-results">';
                            list_item += '<span class="profile-name">' + profile.nome_completo + '</span>';
                            if (profile.atribuicao) {
                                list_item += '<span class="do">' + profile.atribuicao + '</span>';
                            }
                            list_item += '</div>';
                            list_item += '<a></li>';
                            
                            profile_list.append(list_item);
                        } 
                        profile_list.append('<li id="see-all-results"><a href="/perfis/resultados?search=' + caracteres + '"><div id="item-search"><div><i class="fa fa-search"></i></div></div> Ver todos os resultados </a></li>');
                    }
                    console.log(data.perfis);
                },
                error: function (xhr, status, error) {
                    console.error(error);
                }
            });
        } else {
            profile_list.empty();
            $('#profile-list').css('display', 'none');
            $('#search-bar').removeClass('search-bar-background');
        }
    });

});