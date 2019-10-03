function plotScatterData(thickness, dispersivity, VDispersivity, Width) {
 $.ajax({
    data : {
				Thickness : thickness,
				Dispersivity : dispersivity,
				VDispersivity : VDispersivity,
				SourceWidth : Width,
                Stoichiometric : $('#Stoichiometric').val(),
                Threshold : $('#Threshold').val(),
                Acceptor : $('#Acceptor').val(),
                Donor : $('#Donor').val(),
				Result : $('#Thickness').val()
			},
            url: '/liedl3DSinglePlot',
            type: "POST",
        success: function(resp,data){
            $('#successAlert').text("Maximum Plume Length(LMax): "+resp.Result).show();
            $('div#response').html(resp.data);
        }
    });
   }

function fetchValuesAndPlotData() {
    let thickness = $('#scatterplot_fits').val();
    let dispersivity = $('#parameters').val();
    let VDispersivity = $('#verticalDispersivity').val();
    let Width = $('#width').val();
    console.log(Width);
    plotScatterData(thickness, dispersivity, VDispersivity, Width);
}

$('form').on("submit",function(event){
    event.preventDefault();
   $('#sliderThickness').css('display', '');
   $('#sliderDispersivity').css('display', '');
   $('#sliderVerticalDispersivity').css('display', '');
   $('#sliderWidth').css('display', '');
   plotScatterData($('#Thickness').val(), $('#Dispersivity').val(), $('#VDispersivity').val(),$('#SourceWidth').val());
 });

$('#sliderThickness').on('change', () => fetchValuesAndPlotData())
$('#sliderDispersivity').on('change', () => fetchValuesAndPlotData())
$('#sliderVerticalDispersivity').on('change', () => fetchValuesAndPlotData())
$('#sliderWidth').on('change', () => fetchValuesAndPlotData())
