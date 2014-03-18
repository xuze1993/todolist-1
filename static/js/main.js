var log={
	debug:function(str){
		console.log(str);
	},
}

Date.prototype.addDays = function(days){
    return new Date(this.getTime() + 24*60*60*1000*days);
};

var Util = {
	format_date:function(date){
		var month = date.getMonth() + 1;
		month = month<10 ? "0"+month : month;
        return date.getFullYear() + "" + month + '' + date.getDate();
	},
};

var Index = {
	last_content: '',
	show_dates:[],

	render_list:function(date){
		var loaded_days = Index.get_loaded_days(true);
		if(loaded_days.indexOf(date)<0){
			$("#container").append('<div id="day_tasks_'+ date +'"/>');
		}

		$.getJSON('/datelist', {'date':date,'r':Math.random()}, function(data){
			//if(data.list.length==0){ return ;} 数据为空的情况下也保留占位div						 
			$("#day_tasks_" + date).html(juicer($("#tpl_date_tasklist").html(), data)); 
		}); 
	},

	set_head_nav:function(day){
		var tmp = $("#day_tasks_" + day).find("h2").html()
		$("#hNavHeader").html(tmp); 
	},

	get_loaded_days: function(dayOnly){  //获得已加载的日期
		var days=[];
		$("div[id^=day_tasks_").each(function(){ 
			var x = {'elementId':this.id,
				'offset_top':$(this).offset().top,
				'height': $(this).height(),
				'day':this.id.split('_')[2],
				'item_length':$(this).find('li').length } ;

			if(dayOnly){
				days.push(this.id.split('_')[2]);
			}else{
				days.push( x  );
			} 
		});
		days.sort();		 
		return days;
	},
	
};

$(function(){
	var today = Util.format_date(new Date());
	var yestoday = Util.format_date((new Date()).addDays(-1)); 

	//init
	Index.render_list(today);
	Index.render_list(yestoday);
	Index.render_list(Util.format_date((new Date()).addDays(-2)));
	Index.render_list(Util.format_date((new Date()).addDays(-3)));
	Index.render_list(Util.format_date((new Date()).addDays(-4)));

	var last_scrollTop = 0 ;
	$(window).scroll(function(e){
		var document_scrollTop = $(document).scrollTop();
		var loaded_days = Index.get_loaded_days(false);
		
		var last_index = 0;
		for(var i in loaded_days){
			if(loaded_days[i].item_length==0){continue;}

			if((loaded_days[i].offset_top + loaded_days[i].height) >document_scrollTop){
				Index.set_head_nav(loaded_days[i].day);				 
				//var tmp = $("#day_tasks_" + loaded_days[i].day).find("h2").html()
				//$("#hNavHeader").html(tmp); 
				break;
			}
			last_index = i;
		} 
		//last_scrollTop = $(document).scrollTop();		 
	});

	//form
	$("#txtContent").keydown(function(){
		var content = $('#txtContent').val().trim(); 
		if(content!=''){
			$('#newPostForm').removeClass('alert-danger');	
			$('#btnSubmit').removeClass('btn-danger').addClass('btn-default');	
		}
	});

	//bindding
	$('#newPostForm').submit(function(){
		//alert($.now());
		var content = $('#txtContent').val().trim(); 

		if(content=='' || Index.last_content==content){
			$('#newPostForm').addClass('alert-danger');	
			$('#btnSubmit').removeClass('btn-default').addClass('btn-danger');	
			return false; 
		}

		if(Index.last_content==content){
			//?
			return false;
		} 

		$.post('/new', {'content':content}, function(result){
			var data = 	$.parseJSON(result);		 
			$("#list_"+today).append(juicer($("#tpl_newtask_form").html(), data)); 			 
			$("html,body").animate({				
            	scrollTop: $("#day_tasks_" + today).height() - $(window).height() + 76  //计算定位比较陌生
            },300);

            Index.set_head_nav(today);	

			Index.last_content = content;
			$('#txtContent').val('');
		})		 
		return false; //禁止提交后页面刷新
	});  

});