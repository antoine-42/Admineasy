var Machine = {
	 estCo: true,

	setConnecter: function(co){
		this.estCo=co;
	},

	afficherMachine: function(){
		console.log("AFFICHER MACHINE");
		machine=document.getElementById("machine");
		machine.style.display="block";
		image=document.getElementById("image");
		image.style.display="inline";
		if(this.estCo==true){
			machine.style.color="green";
			
		}else if(this.estCo==false){
			machine.style.color="grey";
		}

	},

	effacerMachine: function () {
		machine=document.getElementById("machine");
		machine.style.display="none";
	},

};
