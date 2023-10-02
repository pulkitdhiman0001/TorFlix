

function get_conversion_status(torrent_id) {
    $('#converticonmylist' + torrent_id).css({'display':'none'})
    $('#converticonmylistformultiplefiles' + torrent_id).css({'display':'none'})
    $('#converticonslider' + torrent_id).css({'display':'none'})
    $('#convertspinnermylist' + torrent_id).css({'display':'initial'})
    $('#convertspinnermylistformultiplefiles' + torrent_id).css({'display':'initial'})
    $('#convertspinnerslider' + torrent_id).css({'display':'initial'})


    $('#convertmylist' + torrent_id).prop('disabled', true);
    $('#convertmylistformultiplefiles' + torrent_id).prop('disabled', true);
    $('#convertslider' + torrent_id).prop('disabled', true);
    $('#convertsliderformultiplefiles' + torrent_id).prop('disabled', true);

    $('#convertmylist' + torrent_id).css({'background-color': '#28a745', 'color': 'white', 'cursor':' not-allowed', 'opacity': '1'})
    $('#convertmylist' + torrent_id).css({'background-color': '#28a745', 'color': 'white', 'cursor':' not-allowed', 'opacity': '1'})
    $('#convertslider' + torrent_id).css({'background-color': '#28a745', 'color': 'white', 'cursor':' not-allowed', 'opacity': '1'})

    const intervalId = setInterval(function call() {
        console.log('conversion');
        fetch('/get_download_status' + '/' + torrent_id)
            .then(function (response) {
                return response.json();
            }).then(function (text) {
            $('#convertmylist' + torrent_id).hide()
            $('#convertmylistformultiplefiles' + torrent_id).hide()
            $('#convertslider' + torrent_id).hide()
            $('#downloadmylist' + torrent_id).hide()
            $('#downloadmylistformultiplefiles' + torrent_id).hide()
            $('#downloadslider' + torrent_id).hide()
            $('#delete_btnmylist' + torrent_id).hide()
            $('#delete_btnmylistformultiplefiles' + torrent_id).hide()
            $('#delete_btnslider' + torrent_id).hide()

            $('#download_btn_divmylist' + torrent_id).hide()
            $('#download_btn_divmylistformultiplefiles' + torrent_id).hide()
            $('#download_btn_divslider' + torrent_id).hide()
            $('#watch_btnmylist' + torrent_id).hide()
            $('#watch_btnslider' + torrent_id).hide()
            $('#cancel_btn_divmylist' + torrent_id).hide()
            $('#cancel_btn_divslider' + torrent_id).hide()
            $('#download_progressmylist' + torrent_id).hide()
            $('#download_progressmylistformultiplefiles' + torrent_id).hide()
            $('#download_progressslider' + torrent_id).hide()


            $('#download_btn_divmylist' + torrent_id).css({'background-color': '#28a745', 'color': 'white', 'cursor':' not-allowed', 'opacity': '1'})
            $('#download_btn_divmylistformultiplefiles' + torrent_id).css({'background-color': '#28a745', 'color': 'white', 'cursor':' not-allowed', 'opacity': '1'})
                $('#download_btn_divmylist' + torrent_id).css({'margin-right':'0px'})
                $('#download_btn_divmylistformultiplefiles' + torrent_id).css({'margin-right':'0px'})
                $('#download_btn_divslider' + torrent_id).css({'margin-right':'0px'})
                if(text.conversion_percentage == 0){
                    $('#download_btn_divmylist' + torrent_id).show()
                    $('#download_btn_divmylistformultiplefiles' + torrent_id).show()
                    $('#download_btn_divslider' + torrent_id).show()
                    $('#download_btn_divmylist' + torrent_id).prop('disabled', true);
                    $('#download_btn_divmylistformultiplefiles' + torrent_id).prop('disabled', true);
                    $('#download_btn_divslider' + torrent_id).prop('disabled', true);
                    $('#download_progressmylistformultiplefiles' + torrent_id).show()
                    $('#download_progressmylist' + torrent_id).show()
                    $('#download_progressslider' + torrent_id).show()

                }

                if (text.conversion_percentage != 100) {
                    $('#checkingmylist' + torrent_id).hide()
                    $('#checkingmylistformultiplefiles' + torrent_id).hide()
                    $('#checkingslider' + torrent_id).hide()
                     $('#download_btn_divmylist' + torrent_id).show()
                     $('#download_btn_divmylistformultiplefiles' + torrent_id).show()
                     $('#download_btn_divslider' + torrent_id).show()
                     $('#download_progressmylist' + torrent_id).show()
                     $('#download_progressmylistformultiplefiles' + torrent_id).show()
                     $('#download_progressslider' + torrent_id).show()

                    $('#download_progressmylist' + torrent_id).css({"border-left": "2px solid #28a745", 'max-width':'100%', 'width': text.conversion_percentage +'%'})
                    $('#download_progressmylistformultiplefiles' + torrent_id).css({"border-left": "2px solid #28a745", 'max-width':'100%', 'width': text.conversion_percentage +'%'})
                    $('#download_progressslider' + torrent_id).css({"border-left": "2px solid #28a745", 'max-width':'100%', 'width': text.conversion_percentage +'%'})
                    $('#download_btnmylist' + torrent_id).text(text.conversion_details);
                    $('#download_btnmylistformultiplefiles' + torrent_id).text(text.conversion_details);
                    $('#download_btnslider' + torrent_id).text(text.conversion_details);


                }
                else{
                     $('#checkingmylist' + torrent_id).hide()
                     $('#checkingmylistformultiplefiles' + torrent_id).hide()
                     $('#checkingslider' + torrent_id).hide()

                    $('#download_progressmylist' + torrent_id).css({'width': '0px'})
                    $('#download_progressmylistformultiplefiles' + torrent_id).css({'width': '0px'})
                    $('#download_progressslider' + torrent_id).css({'width': '0px'})
                    $('#download_progressmylist' + torrent_id).hide()
                    $('#download_progressmylistformultiplefiles' + torrent_id).hide()
                    $('#download_progressslider' + torrent_id).hide()
                    $('#download_btn_divmylist' + torrent_id).hide()
                    $('#download_btn_divmylistformultiplefiles' + torrent_id).hide()
                    $('#download_btn_divslider' + torrent_id).hide()
                    $('#watch_btnmylist' + torrent_id).show()
                    $('#watch_btnslider' + torrent_id).show()


                    $('#downloadmylist' + torrent_id).show()
                    $('#downloadmylistformultiplefiles' + torrent_id).show()
                    $('#downloadslider' + torrent_id).show()
                    $('#delete_btnmylist' + torrent_id).show()
                    $('#delete_btnmylistformultiplefiles' + torrent_id).show()
                    $('#delete_btnslider' + torrent_id).show()

                    clearInterval(intervalId);
                }
            });
    }, 4000);
}



function checkifexists(torrent_id, magnet_link){

        console.log('enter')
        $('#convertindex' + torrent_id).hide()
        $('#downloadindex' + torrent_id).hide()
        $('#delete_btnindex' + torrent_id).hide()
        $('#checkingindex' + torrent_id).show()
        $('#download_btn_divindex' + torrent_id).hide()
        $('#watch_btnindex' + torrent_id).hide()
        $('#cancel_btn_divindex' + torrent_id).hide()
        $('#download_progressindex' + torrent_id).hide()

        $('#convertslider' + torrent_id).hide()
        $('#downloadslider' + torrent_id).hide()
        $('#delete_btnslider' + torrent_id).hide()
        $('#checkingslider' + torrent_id).show()
        $('#download_btn_divslider' + torrent_id).hide()
        $('#watch_btnslider' + torrent_id).hide()
        $('#cancel_btn_divslider' + torrent_id).hide()
        $('#download_progressslider' + torrent_id).hide()

        $('#convertdslider' + torrent_id).hide()
        $('#downloaddslider' + torrent_id).hide()
        $('#delete_btndslider' + torrent_id).hide()
        $('#checkingdslider' + torrent_id).show()
        $('#download_btn_divdslider' + torrent_id).hide()
        $('#watch_btndslider' + torrent_id).hide()
        $('#cancel_btn_divdslider' + torrent_id).hide()
        $('#download_progressdslider' + torrent_id).hide()

        $('#convertmylist' + torrent_id).hide()
        $('#convertmylistformultiplefiles' + torrent_id).hide()
        $('#downloadmylist' + torrent_id).hide()
        $('#downloadmylistformultiplefiles' + torrent_id).hide()
        $('#delete_btnmylist' + torrent_id).hide()
        $('#delete_btnmylistformultiplefiles' + torrent_id).hide()
        $('#checkingmylist' + torrent_id).show()
        $('#checkingmylistformultiplefiles' + torrent_id).show()
        $('#download_btn_divmylist' + torrent_id).hide()
        $('#download_btn_divmylistformultiplefiles' + torrent_id).hide()
        $('#watch_btnmylist' + torrent_id).hide()
        $('#cancel_btn_divmylist' + torrent_id).hide()
        $('#download_progressmylist' + torrent_id).hide()
        $('#download_progressmylistformultiplefiles' + torrent_id).hide()

        $('#convertspinnermylist' + torrent_id).css({'display':'none'})
        $('#convertspinnermylistformultiplefiles' + torrent_id).css({'display':'none'})
        $('#convertspinnerslider' + torrent_id).css({'display':'none'})

        console.log('yo')
        fetch('/check_if_exists'+'/'+ torrent_id)
    .then(function (response) {
          return response.json();
      }).then(function (text) {
            console.log(text)
        if (text.condition == true){

            if (text.conversion_flag == true){
                console.log("yeso")
                return get_conversion_status(torrent_id)
            }

            console.log('inside')
            $('#checkingindex' + torrent_id).hide()
            $('#download_btn_divindex' + torrent_id).hide()
            $('#watch_btnindex' + torrent_id).show()
            $("#operationsindex" + torrent_id).addClass("d-flex w-100");
            $('#convertindex' + torrent_id).show()
            $('#downloadindex' + torrent_id).show()
            $('#delete_btnindex' + torrent_id).show()


            $('#checkingslider' + torrent_id).hide()
            $('#download_btn_divslider' + torrent_id).hide()
            $('#watch_btnslider' + torrent_id).show()
            $("#operationsslider" + torrent_id).addClass("d-flex w-100");
            $('#convertslider' + torrent_id).show()
            $('#downloadslider' + torrent_id).show()
            $('#delete_btnslider' + torrent_id).show()

            $('#checkingdslider' + torrent_id).hide()
            $('#download_btn_divdslider' + torrent_id).hide()
            $('#watch_btndslider' + torrent_id).show()
            $("#operationsdslider" + torrent_id).addClass("d-flex w-100");
            $('#convertdslider' + torrent_id).show()
            $('#downloaddslider' + torrent_id).show()
            $('#delete_btndslider' + torrent_id).show()


            $("#operationsmylistformultiplefiles" + torrent_id).addClass("d-flex w-100");

            $('#convertmylist' + torrent_id).show()
            $('#convertmylistformultiplefiles' + torrent_id).show()
            $('#downloadmylist' + torrent_id).show()
            $('#downloadmylistformultiplefiles' + torrent_id).show()
            $('#delete_btnmylist' + torrent_id).show()
            $('#delete_btnmylistformultiplefiles' + torrent_id).show()
            $('#checkingmylist' + torrent_id).hide()
            $('#checkingmylistformultiplefiles' + torrent_id).hide()
            $('#download_btn_divmylist' + torrent_id).hide()
            $('#download_btn_divmylistformultiplefiles' + torrent_id).hide()
            $('#watch_btnmylist' + torrent_id).show()
            $('#cancel_btn_divmylist' + torrent_id).hide()
            $('#download_progressmylist' + torrent_id).hide()
            $('#download_progressmylistformultiplefiles' + torrent_id).hide()
        }

         if (text.condition == false){


            $('#watch_btnindex' + torrent_id).hide()
            $('#watch_btnslider' + torrent_id).hide()
            $('#watch_btndslider' + torrent_id).hide()
            $('#watch_btnmylist' + torrent_id).hide()

            $('#checkingindex' + torrent_id).hide()
            $('#checkingslider' + torrent_id).hide()
            $('#checkingdslider' + torrent_id).hide()
            $('#checkingmylist' + torrent_id).hide()
            $('#checkingmylistformultiplefiles' + torrent_id).hide()

            $('#checkingindex' + torrent_id).show()
            $('#checkingslider' + torrent_id).show()
            $('#checkingdslider' + torrent_id).show()
            $('#checkingmylist' + torrent_id).show()
            $('#checkingmylistformultiplefiles' + torrent_id).show()

            if(text.percentage != 100){



                   const intervalId = setInterval(function call() {


                   $('#checkingindex' + torrent_id).hide()
                   $('#checkingslider' + torrent_id).hide()
                   $('#checkingdslider' + torrent_id).hide()
                   $('#checkingmylist' + torrent_id).hide()
                   $('#checkingmylistformultiplefiles' + torrent_id).hide()
                fetch('/get_download_status'+'/'+ torrent_id)
                .then(function (response) {
                    return response.json();
                    }).then(function (text) {
                    $('#download_progressindex' + torrent_id).show()
                    $('#download_progressslider' + torrent_id).show()
                    $('#download_progressdslider' + torrent_id).show()
                    $('#download_progressmylist' + torrent_id).show()
                    $('#download_progressmylistformultiplefiles' + torrent_id).show()

                    $('#download_progressindex' + torrent_id).css({'width': text.percentage * 0.8 +'%', 'max-width':'80%'})
                    $('#download_progressslider' + torrent_id).css({'width': text.percentage * 0.8 +'%', 'max-width':'80%'})
                    $('#download_progressdslider' + torrent_id).css({'width': text.percentage * 0.8 +'%', 'max-width':'80%'})
                    $('#download_progressmylist' + torrent_id).css({'width': text.percentage * 0.8 +'%', 'max-width':'80%'})
                    $('#download_progressmylistformultiplefiles' + torrent_id).css({'width': text.percentage * 0.8 +'%', 'max-width':'80%'})

                    if(text.percentage > 0.0){
                    $('#download_btn_divindex' + torrent_id).prop('disabled', true);
                    $('#download_btn_divslider' + torrent_id).prop('disabled', true);
                    $('#download_btn_divdslider' + torrent_id).prop('disabled', true);
                    $('#download_btn_divmylist' + torrent_id).prop('disabled', true);
                    $('#download_btn_divmylistformultiplefiles' + torrent_id).prop('disabled', true);


                    $('#download_btn_divindex' + torrent_id).css({'background-color': '#28a745', 'color': 'white', 'cursor':' not-allowed', 'opacity': '1'})
                    $('#download_btn_divslider' + torrent_id).css({'background-color': '#28a745', 'color': 'white', 'cursor':' not-allowed', 'opacity': '1'})
                    $('#download_btn_divdslider' + torrent_id).css({'background-color': '#28a745', 'color': 'white', 'cursor':' not-allowed', 'opacity': '1'})
                    $('#download_btn_divmylist' + torrent_id).css({'background-color': '#28a745', 'color': 'white', 'cursor':' not-allowed', 'opacity': '1'})
                    $('#download_btn_divmylistformultiplefiles' + torrent_id).css({'background-color': '#28a745', 'color': 'white', 'cursor':' not-allowed', 'opacity': '1'})


                    $('#download_progressmylist' + torrent_id).css({"border-left": "2px solid #28a745"})
                    $('#download_progressmylistformultiplefiles' + torrent_id).css({"border-left": "2px solid #28a745"})
                    $('#download_progressindex' + torrent_id).css({"border-left": "2px solid #28a745"})
                    $('#download_progressslider' + torrent_id).css({"border-left": "2px solid #28a745"})
                    $('#download_progressdslider' + torrent_id).css({"border-left": "2px solid #28a745"})

                }

                    $('#download_btn_divindex' + torrent_id).show()
                    $('#download_btn_divslider' + torrent_id).show()
                    $('#download_btn_divdslider' + torrent_id).show()
                    $('#download_btn_divmylist' + torrent_id).show()
                    $('#download_btn_divmylistformultiplefiles' + torrent_id).show()

                    $('#download_btnindex' + torrent_id).text(text.download_details)
                    $('#download_btnslider' + torrent_id).text(text.download_details)
                    $('#download_btndslider' + torrent_id).text(text.download_details)
                    $('#download_btnmylist' + torrent_id).text(text.download_details)
                    $('#download_btnmylistformultiplefiles' + torrent_id).text(text.download_details)

                    if(text.status == "Downloading"){


                        if(text.user_id == text.session_id){

                        $('#cancel_btn_divindex' + torrent_id).show()
                        $('#cancel_btn_divslider' + torrent_id).show()
                        $('#cancel_btn_divdslider' + torrent_id).show()
                        $('#cancel_btn_divmylist' + torrent_id).show()
                        $('#cancel_btn_divmylistformultiplefiles' + torrent_id).show()
                        console.log("in")
                        }
                    }


                    if(text.percentage == 100){

                        $('#download_btn_divindex' + torrent_id).hide()
                        $('#download_btn_divslider' + torrent_id).hide()
                        $('#download_btn_divdslider' + torrent_id).hide()
                        $('#download_btn_divmylist' + torrent_id).hide()
                        $('#download_btn_divmylistformultiplefiles' + torrent_id).hide()

                        $('#download_progressindex' + torrent_id).hide()
                        $('#download_progressslider' + torrent_id).hide()
                        $('#download_progressdslider' + torrent_id).hide()
                        $('#download_progressmylist' + torrent_id).hide()
                        $('#download_progressmylistformultiplefiles' + torrent_id).hide()

                        $('#cancel_btn_divindex' + torrent_id).hide()
                        $('#cancel_btn_divslider' + torrent_id).hide()
                        $('#cancel_btn_divdslider' + torrent_id).hide()
                        $('#cancel_btn_divmylist' + torrent_id).hide()
                        $('#cancel_btn_divmylistformultiplefiles' + torrent_id).hide()

                        $('#download_progressindex' + torrent_id).css({'width': '0px'})
                        $('#download_progressslider' + torrent_id).css({'width': '0px'})
                        $('#download_progressdslider' + torrent_id).css({'width': '0px'})
                        $('#download_progressmylist' + torrent_id).css({'width': '0px'})
                        $('#download_progressmylistformultiplefiles' + torrent_id).css({'width': '0px'})

                        $("#operationsindex" + torrent_id).addClass("d-flex w-100");
                        $("#operationsslider" + torrent_id).addClass("d-flex w-100");
                        $("#operationsdslider" + torrent_id).addClass("d-flex w-100");
                        $("#operationsmylist" + torrent_id).addClass("d-flex w-100");
                        $("#operationsmylistformultiplefiles" + torrent_id).addClass("d-flex w-100");

                        $('#convertindex' + torrent_id).show()
                        $('#convertslider' + torrent_id).show()
                        $('#convertdslider' + torrent_id).show()
                        $('#convertmylist' + torrent_id).show()
                        $('#convertmylistformultiplefiles' + torrent_id).show()

                        $('#downloadindex' + torrent_id).show()
                        $('#downloadslider' + torrent_id).show()
                        $('#downloaddslider' + torrent_id).show()
                        $('#downloadmylist' + torrent_id).show()
                        $('#downloadmylistformultiplefiles' + torrent_id).show()

                        $('#watch_btnindex' + torrent_id).show()
                        $('#watch_btnslider' + torrent_id).show()
                        $('#watch_btndslider' + torrent_id).show()
                        $('#watch_btnmylist' + torrent_id).show()

                        if(text.user_id == text.session_id){

                        $('#delete_btnindex' + torrent_id).show()
                        $('#delete_btnslider' + torrent_id).show()
                        $('#delete_btndslider' + torrent_id).show()
                        $('#delete_btnmylist' + torrent_id).show()
                        $('#delete_btnmylistformultiplefiles' + torrent_id).show()
                        }

                    }

                })
             }, 4000);

            }
            else{
                clearInterval(intervalId);

            }




         }
      })
}







// download history slider
const openSliderButton_for_mobile = document.getElementById('openSlider_for_mobile');
const closeSliderButton_for_mobile = document.getElementById('closeSlider_for_mobile');
const slider_for_mobile = document.getElementById('slider_for_mobile');

if(openSliderButton_for_mobile){

openSliderButton_for_mobile.addEventListener('click', () => {
  slider_for_mobile.style.right = '0';
});
}

if(closeSliderButton_for_mobile){
closeSliderButton_for_mobile.addEventListener('click', () => {
  slider_for_mobile.style.right = '-100%';
});
}
// Add a click event listener to the document
document.addEventListener('click', (event) => {
  if (!slider_for_mobile.contains(event.target) && event.target !== openSliderButton_for_mobile) {
    // Close the slider if the click is outside the slider and not on the openSliderButton
    slider_for_mobile.style.right = '-100%';
  }
});


// download history slider
const openSliderButton_for_pc = document.getElementById('openSlider_for_pc');
const closeSliderButton_for_pc = document.getElementById('closeSlider_for_pc');
const slider_for_pc = document.getElementById('slider_for_pc');

if(openSliderButton_for_pc){

openSliderButton_for_pc.addEventListener('click', () => {
  slider_for_pc.style.right = '0';
});
}

if(closeSliderButton_for_pc){
closeSliderButton_for_pc.addEventListener('click', () => {
  slider_for_pc.style.right = '-100%';
});
}
// Add a click event listener to the document
document.addEventListener('click', (event) => {
  if (!slider_for_pc.contains(event.target) && event.target !== openSliderButton_for_pc) {
    // Close the slider if the click is outside the slider and not on the openSliderButton
    slider_for_pc.style.right = '-100%';
  }
});



//download in progress slider

const dopenSliderButton_for_mobile = document.getElementById('currentlyDownloading_for_mobile');
const dcloseSliderButton_for_mobile = document.getElementById('dcloseSlider_for_mobile');
const dslider_for_mobile = document.getElementById('dslider_for_mobile');

if(dopenSliderButton_for_mobile){
dopenSliderButton_for_mobile.addEventListener('click', () => {
  dslider_for_mobile.style.right = '0';
});
}
if(dcloseSliderButton_for_mobile){
dcloseSliderButton_for_mobile.addEventListener('click', () => {
  dslider_for_mobile.style.right = '-100%';
});
}

// Add a click event listener to the document
document.addEventListener('click', (event) => {
  if (!dslider_for_mobile.contains(event.target) && event.target !== dopenSliderButton_for_mobile) {
    // Close the slider if the click is outside the slider and not on the openSliderButton
    dslider_for_mobile.style.right = '-100%';
  }
});


//download in progress slider

const dopenSliderButton_for_pc = document.getElementById('currentlyDownloading_for_pc');
const dcloseSliderButton_for_pc = document.getElementById('dcloseSlider_for_pc');
const dslider_for_pc = document.getElementById('dslider_for_pc');

if(dopenSliderButton_for_pc){
dopenSliderButton_for_pc.addEventListener('click', () => {
  dslider_for_pc.style.right = '0';
});
}
if(dcloseSliderButton_for_pc){
dcloseSliderButton_for_pc.addEventListener('click', () => {
  dslider_for_pc.style.right = '-100%';
});
}

// Add a click event listener to the document
document.addEventListener('click', (event) => {
  if (!dslider_for_pc.contains(event.target) && event.target !== dopenSliderButton_for_pc) {
    // Close the slider if the click is outside the slider and not on the openSliderButton
    dslider_for_pc.style.right = '-100%';
  }
});





jQuery(function($) {
  var path = window.location.href;
  // because the 'href' property of the DOM element is the absolute path
  $('li a').each(function() {
    if (this.href === path) {
      $(this).addClass('active link-dark bg-info p-2 rounded');

    }
  });
  let url = path.split("/");
  $('#title').text(url[url.length - 1]);
});





