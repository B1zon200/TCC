/*********************************************
 * OPL 20.1.0.0 Data
 * Author: Gabriel Garcia
 * Creation Date: 29/04/2021 at 21:00:00
 *********************************************/

 //using CP;

int NH = ...;			//Numero de Horas
int NB = ...;			//Numero de Bombas
int NT = ...;			//Numero de Tanque

range H = 1..NH;		//Conjunto de horas   -- mudar Conjunto para maiusculo e manter os indices
range B = 1..NB;		//Conjunto de bombas
range T = 1..NT;		//Conjunto de tanques

float Et[T][H] =...;	//Parametro entrada dos tanques [m3/h]
float Fb[B] = ...;		//Parametro fluxo das bombas [m3/h]
float Nit[T] = ...;		//Parametro nivel inicial dos tanques[m3]
float Ntmin[T] = ...;	//Parametro niveis minimos dos tanques[R+]
float Ntmax[T] = ...;	//Parametro niveis maximos dos tanques[R+]
float Ct [T] = ...;		//Parametro capacidade maxima dos tanques[m3]
float Vt[T][H] = ...;	//Parametro vazao dos tanques[m3/h]
float Ceh[H] = ...;		//Parametro custo da energia por horas[Z+]
float Cbh[B][H] = ...;	//Parametro consumo de energia das bombas por hora[Z+]
float k = ...;			//Parametro para evitar viola��es do nivel do tanque ao final do horizonte de analise
float alfa = ...;		//Parametro para porcentagem do n�vel m�nimo final 
float beta = ...;		//Parametro para porcentagem do n�vel m�ximo final

int Bat[B][T] = ...;	//Parametro matriz das ligacoes das bombas que abastecem os tanques{0,1}
int But[B][T] = ...;	//Parametro matriz das bombas que os tanques estao utilizando {0,1}

dvar boolean Hb[B][H]; 	//Variavel horario que as bombas ficam ligadas{0,1}
dvar float+ Nt[T][H];	//Variavel dos niveis dos tanques[m3]
dvar float+ Pfd[T][B][H] in 0..1; 	//Variavel da porcentagem do fluxo que chegara ao seu destino[R+]
dvar float+ Vmint[T];   //Variavel de viola��o de nivel minimo do tanque ao final do horizonte
dvar float+ Vmaxt[T];	//Variavel de viola��o de nivel maximo do tanque ao final do horizonte

// Obs_LM: Acredito que possa ser limitada entre zero e 1 j� na defini��o.
// Obs_GG: Deu certo, at� mesmo para 1 mes de dados
 
dvar float+ Lnt[T][B][H] in 0..1;	//Variavel para a linearizacao do nivel dos tanques[R+] 

//execute Model_Parameters {
//	cplex.tilim = 30;
//} 

minimize
  sum(b in B, h in H) Ceh[h] * Cbh[b][h] * Hb[b][h] + k*sum(t in T)(Vmint[t] +Vmaxt[t]); 

subject to{
  //Restri��es de limites operacionais de capacidade de tancagem
  forall (h in H, t in T ) {
    	//Restri��o de nivel m�ximo do tanque
   		HT1: Nt[t][h] <= Ntmax[t] * Ct[t];
   		//Restri��o de nivel m�nimo do tanque	 
    	HT2: Nt[t][h] >= Ntmin[t] * Ct[t];	
    	//Restri��es de balan�o de massa, calculo de n�vel dos tanques
    	HT3: if(h == 1){
    		Nt[t][h] == Nit[t] + (sum(b in B)Fb[b]*Bat[b][t]*Lnt[t][b][h]) + Et[t][h] - Vt[t][h] - (sum(b in B)Fb[b]*But[b][t]*Hb[b][h]);        
  		} 
  	 	else{
  	 	    Nt[t][h] == Nt[t][h-1] + (sum(b in B)Fb[b]*Bat[b][t]*Lnt[t][b][h]) + Et[t][h] - Vt[t][h] - (sum(b in B)Fb[b]*But[b][t]*Hb[b][h]);          	 	
  	 	}	    	
  }
  //Restri��o de balan�o de massa. Garante que o fluxo de sa�da de cada bomba em cada intervalo, em todos os tanques por ela atendidos, deve igualar o fluxo de entrada.
  forall (b in B, h in H){
  		BH1: sum(t in T) Pfd[t][b][h] == 1;   
  }  
// Obs_LM: Farei coment�rios na sequ�ncia em cada grupo de restri��es.
// 1) Notar que a vari�vel que cont�m o valor da lineariza��o � empregada nas restri��es de n�vel de tanque acima   
  forall (b in B, t in T, h in H){
		// Se par�metro = 0, ent�o vari�vel base = 0. Ok.
  		BTH1: if(Bat[b][t] == 0){ 
  			  Pfd[t][b][h] == 0;   		
  		}
		// Ok. Vari�vel do produto menor que a bin�ria. 
		// Notar que quando bin�ria � zero, produto necessariamente zera; quando bin=1, produto � limitado pelo percentual	
  		LNT2: Lnt[t][b][h] <= Hb[b][h]; 
  		// O termo final n�o tinha fun��o ativa, mas a parte inicial � importante. Comentei a parte inoperante.
  		LNT3: Lnt[t][b][h] <= Pfd[t][b][h]; 
		// Se var.bin�ria igual a 1, est� Ok; se bin�ria for zero, n�o necessariamente zera conte�do do produto.
		// Atua��o conjunta com a Dest1 imp�e que produto igual a zero.
  		LNT4: Lnt[t][b][h] >= Pfd[t][b][h] - 1*(1 - Hb[b][h]);  		       
  }
 // Obs_LM: Avaliar possibilidade de altera��es nos n�veis recomendados, em caso de viola��es (infactibilidades)
 // Obs_LM: Na formaliza��o do modelo, n�o colocar par�metros adhoc dentro do modelo; definir par�metros que multiplicam as vari�veis.
 //         Neste caso, os par�metros assumem os valores de acordo com o estudo de caso.
 
 // A restri��o faz com que o n�vel de cada tanque ao final do horizonte de tempo NH esteja entre 0,75 ah 1,25 do nivel inicial 
  forall (t in T){
  		//T1: Nt[t][NH] >= 0.75*Nit[t]; //Restri��o para n�vel final dos tanques
  		//T2: Nt[t][NH] <= 1.25*Nit[t]; //Restri��o para n�vel final dos tanques
  		T1: Nt[t][NH] >= alfa*Ct[t] - Vmint[t]; //Restri��o para n�vel final dos tanques // alfa < beta
  		T2: Nt[t][NH] <= beta*Ct[t] + Vmaxt[t]; //Restri��o para n�vel final dos tanques // beta
  		T3: Vmint[t] <= alfa*Ct[t];  //  alfa
  		T4: Vmaxt[t] <= (1-beta)*Ct[t];  //  1 - beta
  }
}