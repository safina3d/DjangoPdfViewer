/**
 * Created by zze on 04/03/16.
 */
var svc = function (token, id, idPDF, resolution, width, height) {
    var livre = $("#" + id);

    var callService = function (serviceName, obj) {
        return $.ajax({
            type: 'post',
            url: serviceName,
            dataType: 'json',
            data: obj
        }).promise();
    };


    var getImagesService = function (pageDebut, pageFin) {
        var obj = {
            csrfmiddlewaretoken: token,
            pdf_id : idPDF,
            from_page : pageDebut,
            to_page : pageFin || pageDebut,
            quality : resolution || 110
        };
        livre.addClass("loader");
        callService('svc_images', obj).then(function(resp){
           livre.removeClass("loader");
            $("#nbMaxPages").attr("nbMaxPages", resp.nb_pages);
            ajouterPagesPDF(resp.images, resp.error);
        });
    };


    var ajouterPagesPDF = function (listeImages, error) {
        listeImages = listeImages || [];

        if (listeImages.length === 0) {
            $("#errmsg").html('<hr/>ERROR<hr/>'+error);
            return;
        }
        $.each(listeImages, function (index, value) {
            var image = "data:image/png;base64," + value;
            var el = '<div style="background-image:url(\'' + image + '\')"></div>';
            //var nbPages = $("#"+idLivre + " .page-wrapper").length;

            nbPages = livre.turn("pages");
            if (nbPages == 1) {
                if ($("#emptyBook").length) {
                    livre.turn('removePage', 1);
                }
            }

            livre.turn('addPage', $(el));

        });
    };

    var loadApp = function () {
        var h = height || '100%';
        var w = width || '100%';


        livre.turn({
            height: h,
            width: w,
            elevation: 100,
            acceleration: !isChrome(),
            gradients: true,
            autoCenter: false,
            when : {
                	turned: function(event, page, view) {
                        if(page>1){
                            nbPages = livre.turn("pages");
                            var nbMaxPages = $("#nbMaxPages").attr("nbMaxPages");
                            if(nbMaxPages && nbPages < nbMaxPages){
                                getImagesService(nbPages + 1, nbPages + 2);
                            }
                        }
                    }
            }
        });

        getImagesService(1, 4);
    };

    return {
        loadApp : loadApp,
        getImages : getImagesService
    };


};




