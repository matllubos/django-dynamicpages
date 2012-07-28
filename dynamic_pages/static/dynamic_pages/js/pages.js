
var options = [];

function set_page_content(el) {
	var data  = $(el).val().split('-');
	var model = data[0].split('.');
	var app = model[0]
	model = model[1]
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
		$('#add_id_content').attr('href','/admin/'+app+'/'+model+'/add/');
		
		$('#id_content option').css('display','block');
		
		select = 'select#id_content';
		
		val = $(select).val();
		$(select).empty();
		$.each(options, function(){
			option = this;
			if (option.value == '' || option.value.split('$')[0] == model) {
				
				$(select).append(
	               $('<option>').text(option.text).val(option.value)
	             );
			}
			
		});
		
		$(select).val(val);
		if ($('#edit_id_content').length) {
			$('#edit_id_content').attr('href','/admin/'+app+'/'+model+'/'+$('#id_content').val()+'/');
			
		}
		$('.form-row.content').css('display','block');
	}
}




function page_content() {
	select = 'select#id_content';
    $(select).find('option').each(function() {
        options.push({value: $(this).val(), text: $(this).text()});
    });
        
	set_page_content($('#id_page_type'));
	$('#id_page_type').change(function() {
		set_page_content(this);
	});
}
$(document).ready(function(){
	page_content();
        
});
 
