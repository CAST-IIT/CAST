function plotScatterData(thickness, dispersivity) {
 $.ajax({
    data : {
				Thickness : thickness,
				Dispersivity : dispersivity,
                Acceptor : $('#Acceptor').val(),
                Donor : $('#Donor').val(),
                Stoichiometric : $('#Stoichiometric').val(),
                Porosity : $('#Porosity').val(),
				Result : $('#Thickness').val()
			},
            url: '/hamEtAlSinglePlot',
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
    $("#Thickness").val(thickness);
    $("#Dispersivity").val(dispersivity);
    plotScatterData(thickness, dispersivity);
}

$('form').on("submit",function(event){
    event.preventDefault();
    $("#scatterplot_fits").val($('#Thickness').val());
   $("#thicknessVal").text($('#Thickness').val());
   $("#parameters").val($('#Dispersivity').val());
   $("#dispersivityVal").text($('#Dispersivity').val());
   $('#sliderThickness').css('display', '');
   $('#sliderDispersivity').css('display', '');
   plotScatterData($('#Thickness').val(), $('#Dispersivity').val());
 });

$('#sliderThickness').on('change', () => fetchValuesAndPlotData())
$('#sliderDispersivity').on('change', () => fetchValuesAndPlotData())

