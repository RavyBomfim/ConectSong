$(document).ready(function () {
    var container = $('#text-message-box');
    var textarea = $('#message-field');
    var text_label = $('#message-label');
    var tamanho_anterior = textarea.prop('scrollHeight');
    var chat_footer_altura = $('#chat-footer').height();

    console.log('Usuário atual ' + usuario_atual)

    $('#send-message').click(function() {
        $('#chat-box').css('display', 'block');
        $('#chat-body').css('height', 'calc(100% - ' + chat_footer_altura + 'px)');
        $('#chat-body').scrollTop($('#chat-body').prop("scrollHeight"));
    });

    $('#chat-close').click(function() {
        $('#chat-box').css('display', 'none');
    });

    textarea.on('input keydown', function() {
        if (textarea.val() !== '') {
            text_label.css('display', 'none');
        } else {
            text_label.css('display', 'block');
        }

        var tamanho_atual = textarea.prop('scrollHeight');
        autoResizeTextarea(textarea);
        if (tamanho_atual > tamanho_anterior && textarea.val() !== '') {
            container.css('height', 'auto');
            autoResizeTextarea(textarea);
            textarea.css('overflow-y', 'visible');
        } else  {
            container.css('height', '36px');
            textarea.css('height', '22px');
            textarea.css('overflow-y', 'hidden');
        }
        chat_footer_altura = $('#chat-footer').height();
        $('#chat-body').css('height', 'calc(100% - ' + chat_footer_altura + 'px)');

        var conteudo = $('#chat-body')[0];
        conteudo.scrollTop = conteudo.scrollHeight;
    });

    function autoResizeTextarea(textarea) {
        textarea.css('height', 'fit-content');
        var scrollHeight = textarea.get(0).scrollHeight;
        textarea.css('height', Math.min(scrollHeight, parseInt(textarea.css('max-height'))) + 'px');
    }

    $('#message-field').keypress(function (e) {
        if (e.which === 13) { 
            enviarMensagem();
        }
    });

    $('#btn-send').click(function() {
        enviarMensagem();
    });


    // Função para renderizar as mensagens no formato HTML
    function renderizarMensagem(mensagem) {
        var mensagemHTML = '<li class="messages';

        // Adiciona a classe de acordo com o remetente
        if (mensagem.enviou_id === usuario_atual) {
            mensagemHTML += ' sent-by-me">';
        } else {
            mensagemHTML += ' received-by-me">';
        }

        // Adiciona a foto do perfil
        if (mensagem.enviou_foto) {
            mensagemHTML += '<img class="photo-user" src="' + mensagem.enviou_foto + '" alt="Foto do Perfil">';
        } else {
            mensagemHTML += '<img src="../static/img/perfil-generico.png" alt="">';
        }

        mensagemHTML += '<div class="message-time-box">';
        mensagemHTML += '<div class="message-ballon">';
        mensagemHTML += mensagem.message;
        mensagemHTML += '</div>';

        mensagemHTML += '<div class="date-time-box">';
        mensagemHTML += '<span class="date-message">' + mensagem.data + '</span> &nbsp;';
        mensagemHTML += '<span class="time-message">' + mensagem.hora + '</span>';
        mensagemHTML += '</div>';

        mensagemHTML += '</div></li>';

        return mensagemHTML;
    }


    // Função para buscar mensagens com o usuário específico
    function carregarMensagens() {
        var id_usuario = $('#receive').val();  // Obtemos o ID do usuário do campo hidden

        $.ajax({
            type: 'GET',
            url: '/carregar-mensagens/' + id_usuario, 
            success: function (data) {
                // Limpa o conteúdo atual do #chat-body
                $('#chat-body ul.messages-container').empty();

                // Adiciona as mensagens ao #chat-body
                data.mensagens.forEach(function (mensagem) {
                    var mensagemHTML = renderizarMensagem(mensagem);
                    $('#chat-body ul.messages-container').append(mensagemHTML);
                });
            },
            error: function (error) {
                console.log('Erro ao carregar mensagens:', error);
            }
        });
    }


    // Função para enviar mensagens
    function enviarMensagem() {
        var mensagem = $('#message-field').val().trim();
        
        // Verifica se o campo de mensagem não está vazio
        if (mensagem !== '') {
            var dadosFormulario = $('#form-message').serialize();
        
            $.ajax({
                type: 'POST',
                url: '/enviar-mensagem',
                data: dadosFormulario,
                success: function (data) {
                    carregarMensagens();
                    $('#message-field').val('');
                },
                error: function (error) {
                    console.log('Erro ao enviar mensagem:', error);
                }
            });
        }
    }


    /*function enviarMensagem() {
        var mensagem = $('#message-field').val().trim();
    
        // Verifica se o campo de mensagem não está vazio
        if (mensagem !== '') {
            var dadosFormulario = $('#form-message').serialize();
    
            $.ajax({
                type: 'POST',
                url: '/ws/enviar-mensagem/',  // A URL da sua view Django
                data: dadosFormulario,
                success: function (data) {
                    // Lógica para atualizar o chat com a resposta 
                    // ...
    
                    // Limpe o campo de mensagem
                    $('#message-field').val('');
                },
                error: function (error) {
                    console.log('Erro ao enviar mensagem:', error);
                }
            });
        }
    }*/

});




