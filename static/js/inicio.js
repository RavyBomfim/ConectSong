$(document).ready(function() {

    $("#btn-publicar").prop("disabled", true);

    $("#texto-publicacao, #foto-publicacao, #video-publicacao").on("input change", function() {
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
    });

    var select = $('#privacidade-publicacao');

    var opcao_selecionada = select.find('option:selected').val();
    console.log(opcao_selecionada);

    // if (opcao_selecionada === 'Público') {
    //     $('#publico-icone').removeClass('icones-select').addClass('icone-selecionado');
    // }

});