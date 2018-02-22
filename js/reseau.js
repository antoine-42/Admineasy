var Machine= {
	 estCo: true,

	setConnecter: function(co){
		this.estCo=co;
	},

	afficherMachine: function(){
		machine=document.getElementById("machine");
		if(this.estCo==true){
			machine.style.color="green";
			
		}else if(this.estCo==false){
			machine.style.color="grey";
		}

	},

};
