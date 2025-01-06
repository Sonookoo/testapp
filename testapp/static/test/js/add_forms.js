var numOfFormsElement = $('input#id_numOfForms');
var currentCount = parseInt(numOfFormsElement.val());

$('button#add').on('click', function(){
    var modelNameElement = $('<input>', {
        name: `model_name_${currentCount}`,
        type: "text",
        value: "",
        id: `id_model_name_set_${currentCount}`,
    });
    var fileElement = $('<input>', {
        name: `files_${currentCount}`,
        type: 'file',
        multiple,
        value: "",
        id: `id_file_set_${currentCount}`,
    });
    $('div#form_space').append(modelNameElement);
    $('div#form_space').append(fileElement);
    currentCount++;
    numOfFormsElement.attr('value', currentCount);
});
console.log("add");