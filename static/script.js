$(document).ready(function () {
  var coordValid = false;
  var cityValid = false;
  var road = false;
  if ($(".niewiadomo").children(".card-localisation").length >= 3) {
    $(".button-road-2").prop("disabled", false);
    road = true;
  } else {
    $(".button-road-2").prop("disabled", true);
    road = false;
  }
  $(".nawetnieiwem").click(function () {
    console.log("dizenki dziaśa");
    if (road) {
      window.location.href = "/road";
    }
  });
  console.log("nie");
  $(".input-form").focus(function () {
    var border_id = ".br-" + $(this)[0].id;
    $(border_id).css("width", "100%");
  });
  $(".input-form").focusout(function () {
    checkLength(this);
    var border_id = ".br-" + $(this)[0].id;
    $(border_id).css("width", "0px");
  });

  function checkLength(input) {
    inputLength = $(input).val().length;
    if ($(input)[0].id == "1") {
      if (inputLength >= 34) {
        coordValid = true;
      } else {
        coordValid = false;
      }
    }
    if ($(input)[0].id == "2") {
      if (inputLength >= 2) {
        cityValid = true;
      } else {
        cityValid = false;
      }
    }
    if (cityValid == true && coordValid == true) {
      $(".button-form-submit").prop("disabled", false);
    } else {
      $(".button-form-submit").prop("disabled", true);
    }
  }
});
