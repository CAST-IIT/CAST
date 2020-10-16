function plotScatterData(top, concentration, longitudinal, width, la) {
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
    let longitudinal = $('#parameters2').val();
    let width = $('#parameters3').val();
    let la = $('#parameters4').val();
    console.log(width);
    plotScatterData(top, concentration, longitudinal, width, la);
}

$('form').on("submit",function(event){
    event.preventDefault();
   $('#sliderTop').css('display', '');
   $('#sliderConcentration').css('display', '');
   $('#sliderLongitudinal').css('display', '');
   $('#sliderWidth').css('display', '');
   $('#sliderLa').css('display', '');
   plotScatterData($('#Top_Of_Source').val(), $('#Input_Concentration').val(), $('#Width').val(),$('#Longitudinal').val(),$('#La').val());
});

$('#sliderTop').on('change', () => fetchValuesAndPlotData())
$('#sliderConcentration').on('change', () => fetchValuesAndPlotData())
$('#sliderLongitudinal').on('change', () => fetchValuesAndPlotData())
$('#sliderWidth').on('change', () => fetchValuesAndPlotData())
$('#sliderLa').on('change', () => fetchValuesAndPlotData())

