var tbody = d3.select("tbody");

function updatePregnancy() {
    var sel = document.getElementById('selectGender');
    value = sel.options[sel.selectedIndex].value;

    if (value == '0' && value != null && value != undefined) {
        d3.select('#inputPregnant').property('style', "display:none")
        d3.select('#labelPregnant').property('style', "display:none")
    }
    if (value == '1' || value == 1) {
        console.log(sel.options[sel.selectedIndex].value)
        d3.select('#inputPregnant').property('style', "display:on")
        d3.select('#labelPregnant').property('style', "display:on")
    }

}


d3.select("#selectGender").on('click', updatePregnancy);