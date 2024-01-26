$(document).ready(function() {
    var textarea = $('#id_texto');
    var text_label = $('#post-placeholder');
    var tamanho_anterior = textarea.prop('scrollHeight');

    /* $("#texto-publicacao, #foto-publicacao, #video-publicacao").on("input change", function() {
        // Verifica se pelo menos um dos campos possui valor
        var texto_publicacao = $("#texto-publicacao").val();
        var foto_publicacao = $("#foto-publicacao").val();
        var video_publicacao = $("#video-publicacao").val();

        if (texto_publicacao || foto_publicacao || video_publicacao) {
          $("#btn-publicar").prop("disabled", false);
          
          $('.post-form').addClass('post-altura');
        } else {
          $("#btn-publicar").prop("disabled", true);
        }
    }); */


    $('#id_imagem, #id_video').on('change', function(e) {
      if ($('#id_imagem').val() !== '' || $('#id_video').val() !== '') {
        $('fotos-videos-box').css('height', '300px');
      }
      var input = e.target;
      if (input.files && input.files[0]) {
      var reader = new FileReader();

      reader.onload = function(e) {
          // Define a imagem de pré-visualização
          $('#inserir-imagem').attr('src', e.target.result);
      };

      // Carrega o arquivo de imagem
      reader.readAsDataURL(input.files[0]);
      }
  });

    textarea.focus(function() {
      //tela_publicacao.css('height', '300px');
      textarea.css('height', '100px');
    });

    textarea.blur(function() {
      if (textarea.val() === '') {
        textarea.css('height', '100%');
      }
    });

    $('.btn-ellipsis').on('click', function() {
      var post_id = $(this).data('post-id');
      
      var options_post = $('#options_post_' + post_id);

      if (options_post.css('display') === 'none') {
        options_post.css('display', 'block');
      } else {
        options_post.css('display', 'none');
      }

    });

    // var select = $('#privacidade-publicacao');

    // var opcao_selecionada = select.find('option:selected').val();
    // console.log(opcao_selecionada);

    // if (opcao_selecionada === 'Público') {
    //     $('#publico-icone').removeClass('icones-select').addClass('icone-selecionado');
    // }

});