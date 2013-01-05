
var pageContentOptions = [];

function setPageContent(el) {
	var data  = $(el).val().split('-');
	var model = data[0]
	var name  = data[1];
	var menu  = data[2];
	var changeUrl = data[3] == 'true'
	
	$('.form-row.meta_data').css('display','block');
	$('.form-row.html_title').css('display','block');
	
	if (menu == 'menu') {
		$('.form-row.order').css('display','block');
		$('.form-row.default').css('display','block');
	} else {
		$('.form-row.order').css('display','none');
		$('#id_order').val('');
		$('.form-row.default').css('display','none');
		$('#id_default').attr('checked', false);
	}
	
	if (changeUrl) {
		$('.form-row.relative_url').css('display','block');
	} else {
		$('.form-row.relative_url').css('display','none');
		$('#id_relative_url').val('');
	}
	
	
	if (model == 'none') {
		$('.form-row.content').css('display','none');
		if (name == 'redirects') {
			$('.form-row.meta_data').css('display','none');
			$('.form-row.html_title').css('display','none');
		}
	} else {
		$('#add_id_content').attr('href','/admin/'+model.split('.')[0]+'/'+model.split('.')[1]+'/add/');
		
		$('#id_content option').css('display','block');
		
		select = 'select#id_content';
		
		val = $(select).val();
		$(select).empty();
		$.each(pageContentOptions, function(){
			option = this;
			if (option.value == '' || option.value.split('$')[0] == model) {
				
				$(select).append(
	               $('<option>').text(option.text).val(option.value)
	             );
			}
			
		});
		
		$(select).val(val);
		if ($('#edit_id_content').length) {
			$('#edit_id_content').attr('href','/admin/'+model.split('.')[0]+'/'+model.split('.')[1]+'/'+$('#id_content').val()+'/');
			
		}
		$('.form-row.content').css('display','block');
	}
}




function pageContent() {
	select = 'select#id_content';
    $(select).find('option').each(function() {
    	pageContentOptions.push({value: $(this).val(), text: $(this).text()});
    });
        
	setPageContent($('#id_page_type'));
	$('#id_page_type').change(function() {
		setPageContent(this);
	});
}




$(document).ready(function(){
	pageContent();
});
 
