function plotScatterData(thickness, dispersivity) {
 $.ajax({
    data : {
				Thickness : thickness,
				Dispersivity : dispersivity,
                Stoichiometric : $('#Stoichiometric').val(),
                Acceptor : $('#Acceptor').val(),
                Donor : $('#Donor').val(),
				Result : $('#Thickness').val()
			},
            url: '/MaierAndGrathwohlSinglePlot',
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
    console.log(thickness);
    plotScatterData(thickness, dispersivity);
}

$('form').on("submit",function(event){
    event.preventDefault();
   $('#sliderThickness').css('display', '');
   $('#sliderDispersivity').css('display', '');
   plotScatterData($('#Thickness').val(), $('#Dispersivity').val());
 });

$('#sliderThickness').on('change', () => fetchValuesAndPlotData())
$('#sliderDispersivity').on('change', () => fetchValuesAndPlotData())

