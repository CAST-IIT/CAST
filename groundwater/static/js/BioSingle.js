function plotScatterData(top, concentration, width, longitudinal, la) {
 $.ajax({
    data : {
				Threshold_Concentration :  $('#Threshold_Concentration').val(),
				Time :  $('#Time').val(),
                Top_Of_Source : top,
                Input_Concentration : concentration,
                Width : width,
                Velocity : $('#Velocity').val(),
                Longitudinal : longitudinal,
                Horizontal : $('#Horizontal').val(),
                Vertical : $('#Vertical').val(),
                Diffusion : $('#Diffusion').val(),
                R : $('#R').val(),
                Ga : $('#Ga').val(),
                La : la,
                M : $('#M').val(),
				Result : $('#Thickness').val()
			},
            url: '/BioSinglePlot',
            type: "POST",
        success: function(resp,data){
            $('#successAlert').text("Maximum Plume Length(LMax): "+resp.Result).show();
            $('div#response').html(resp.data);
        }
    });
   }

function fetchValuesAndPlotData() {
    let top = $('#scatterplot_fits').val();
    let concentration = $('#parameters').val();
    let width = $('#parameters2').val();
    let longitudinal = $('#parameters3').val();
    let la = $('#parameters4').val();
    console.log($('#parameters2').val())
    console.log($('#parameters3').val())
    $("#Top_Of_Source").val(top);
    $("#Input_Concentration").val(concentration);
    $("#Width").val(width);
    $("#Longitudinal").val(longitudinal);
    $("#La").val(la);
    plotScatterData(top, concentration, width, longitudinal, la);
}

$('form').on("submit",function(event){
    event.preventDefault();
   $("#scatterplot_fits").val($('#Top_Of_Source').val());
   $("#thicknessVal").text($('#Top_Of_Source').val());
   $("#parameters").val($('#Input_Concentration').val());
   $("#dispersivityVal").text($('#Input_Concentration').val());
   $("#parameters2").val($('#Width').val());
   $("#widthVal").text($('#Width').val());
   $("#parameters3").val($('#Longitudinal').val());
   $("#longitudinalVal").text($('#Longitudinal').val());
   $("#parameters4").val($('#La').val());
   $("#laVal").text($('#La').val());

   $('#sliderTop').css('display', '');
   $('#sliderConcentration').css('display', '');
   $('#sliderWidth').css('display', '');
   $('#sliderLongitudinal').css('display', '');
   $('#sliderLa').css('display', '');
   plotScatterData($('#Top_Of_Source').val(), $('#Input_Concentration').val(), $('#Width').val(),$('#Longitudinal').val(),$('#La').val());
});

$('#sliderTop').on('change', () => fetchValuesAndPlotData())
$('#sliderConcentration').on('change', () => fetchValuesAndPlotData())
$('#sliderWidth').on('change', () => fetchValuesAndPlotData())
$('#sliderLongitudinal').on('change', () => fetchValuesAndPlotData())
$('#sliderLa').on('change', () => fetchValuesAndPlotData())

