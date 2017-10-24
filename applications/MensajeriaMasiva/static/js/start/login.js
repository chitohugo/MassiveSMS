login = {
	init:function(){
		this.Form();

	},

	Form:function(){


		$('#formLogin').submit(function(e){
        	e.preventDefault();
        	return false;
         });
		$('#entrar').click(function(){
			if($('#formLogin')[0].checkValidity()){
				alert("Hola")
			}
		});
	}
}