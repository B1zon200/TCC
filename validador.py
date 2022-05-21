import math
import xlrd, xlwt

linha=0
opcao1=input("Qual das seguintes opções será validado:\n1 - Semana\n2 - Mês\n:")

if int(opcao1) == 1:
    linha=169    
elif int(opcao1) == 2:
    linha=745
else:
    input("Opção invalida, comece de novo!!")
    quit()

opcao2=input("Será considerado a vazão fictícia:\n1 - Sim\n2 - Não\n:")

if int(opcao2) == 1:
    print("Você escolheu para considerar a vazão fictícia\n")    
elif int(opcao2) == 2:
    print("Você escolheu para não considerar a vazão fictícia\n")    
else:
    input("Opção invalida, comece de novo!!")
    quit()

###########################################################
##------------------DADOS DA PLANILHA--------------------## 
###########################################################
path='Dados2.xlsx'

newworkbook = xlwt.Workbook()
planilha = xlrd.open_workbook(path)


if int(opcao1) == int(1):
    sheet = planilha.sheet_by_name("Resultado1")
    sheet1 = planilha.sheet_by_name("Dados")

else:
    sheet = planilha.sheet_by_name("Resultado2")
    sheet1 = planilha.sheet_by_name("Dados2")


sh1 = newworkbook.add_sheet('Tanque 1')
sh2 = newworkbook.add_sheet('Tanque 2')
sh3 = newworkbook.add_sheet('Tanque 3')
sh4 = newworkbook.add_sheet('Tanque 4')

header1 = sheet.row_values(1, start_colx=1, end_colx=int(linha))
header2 = sheet.row_values(2, start_colx=1, end_colx=int(linha))
header3 = sheet.row_values(3, start_colx=1, end_colx=int(linha))
header4 = sheet.row_values(4, start_colx=1, end_colx=int(linha))
header5 = sheet1.col_values(6,start_rowx=1, end_rowx=int(linha))
header6 = sheet1.col_values(7,start_rowx=1, end_rowx=int(linha))
header7 = sheet1.col_values(8,start_rowx=1, end_rowx=int(linha))
header8 = sheet1.col_values(9,start_rowx=1, end_rowx=int(linha))
    
###########################################################
##------------------DADOS DOS TANQUES--------------------## 
###########################################################
raio1 = float(24.5325170933749)
raio2 = float(29.2509306222257)
raio3 = float(19.9471136494421)
raio4 = float(13.81976572207375)

###########################################################
##--------------------CRIA PLANILHA----------------------## 
###########################################################

for i in range(0,17):
    if i<8:
       sh1.write(0,i,"Pj%s" %(i+1))
       sh2.write(0,i,"Pj%s" %(i+1))
       sh3.write(0,i,"Pj%s" %(i+1))
       sh4.write(0,i,"Pj%s" %(i+1))
    elif i>8: 
       sh1.write(0,i,"Pm%s" %(i-8))
       sh2.write(0,i,"Pm%s" %(i-8))
       sh3.write(0,i,"Pm%s" %(i-8))
       sh4.write(0,i,"Pm%s" %(i-8)) 
###########################################################
## Calcula a altura da água no horizonte de tempo e cal- ##
## cula a vazão por hora ------------------------------- ## 
###########################################################
for j in range(0,4):
    for i in range(0,int(linha)-1):
        if j == 0:
            #print("DADOS PARA TANQUE 1\n\n")
            h = float(header1[i])/(math.pi*raio1**2)
            q = (float(header5[i])*1000)/(60*60)
        elif j == 1:
            #print("DADOS PARA TANQUE 2\n\n")
            h = float(header2[i])/(math.pi*raio1**2)
            q = (float(header6[i])*1000)/(60*60)    
        elif j == 2:
            #print("DADOS PARA TANQUE 3\n\n")
            h = float(header3[i])/(math.pi*raio1**2)
            q = (float(header7[i])*1000)/(60*60)
        elif j == 3:
            #print("DADOS PARA TANQUE 4\n\n")
            h = float(header4[i])/(math.pi*raio1**2)
            q = (float(header8[i])*1000)/(60*60) 

        Hc = int(85+h) # Altura do reservátorio + altura da água    
###########################################################
##------------------DADOS DO EXERCÍCIO-------------------## 
###########################################################
# Extensão dos canos em metros
        L1 = int(100)
        L2 = int(100)
        L3 = int(150)
        L4 = int(150)
        L5 = int(80)
        L6 = int(120)
        L7 = int(200)
        L8 = int(450)
        LT = L1+L2+L3+L4+L5+L6+L7+L8

# Coeficiente de perda de cargas Hazen-Williams
        C = 130 

        Qx = q/LT
# Diametro inicial em mm
        D1 = 50
        D2 = 50
        D3 = 50
        D4 = 50
        D5 = 50
        D6 = 50
        D7 = 50
        D8 = 50
# Alturas dos pontos a montante - metros
        Hm1 = int(70)
        Hm2 = int(72)
        Hm3 = int(72)
        Hm4 = float(78.20)
        Hm5 = int(74)
        Hm6 = int(74)
        Hm7 = float(78.20)
        Hm8 = int(85) 
# Alturas dos pontos a jusante - metros
        Hj1 = int(81)
        Hj2 = int(70)
        Hj3 = int(76)
        Hj4 = int(72)
        Hj5 = float(72.50)
        Hj6 = float(60.20)
        Hj7 = int(74)
        Hj8 = float(78.2)                        
###########################################################
##----------------CALCULO VAZÃO EM MARCHA----------------## 
###########################################################
# Vazão consumida em cada um dos trechos
        VM1 = (L1*q)/LT
        VM2 = (L2*q)/LT
        VM3 = (L3*q)/LT
        VM4 = (L4*q)/LT
        VM5 = (L5*q)/LT
        VM6 = (L6*q)/LT
        VM7 = (L7*q)/LT
        VM8 = (L8*q)/LT
###########################################################
##---------------CALCULO VAZÃO A MONTANTE----------------## 
###########################################################
#Vazão no início - fazer a análise do último trecho até o trecho que esta no reservatório - soma da vazão de jusante com a vazão de marcha
        Vm1 = VM1
        Vm2 = VM2 + Vm1
        Vm3 = VM3
        Vm4 = VM4 + Vm3 + Vm2
        Vm5 = VM5
        Vm6 = VM6
        Vm7 = VM7 + Vm6 + Vm5 + Vm4
        Vm8 = VM8 
###########################################################
##---------------CALCULO VAZÃO A JUSANTE-----------------## 
###########################################################        
#Vazão no final - Quando igual a zero quer dizer que não abastece nenhum outro trecho 
        Vj1 = Vm1 - VM1
        Vj2 = Vm2 - VM2
        Vj3 = Vm3 - VM3
        Vj4 = Vm4 - VM4
        Vj5 = Vm5 - VM5
        Vj6 = Vm6 - VM6
        Vj7 = Vm7 - VM7
        Vj8 = Vm8 - VM8
###########################################################
##---------------CALCULO VAZÃO FICTÍCIA------------------## 
###########################################################        
#A média da vazão de jusante e montante
        if int(opcao2) == int(1):
            Vf1 = (Vj1+Vm1)/2
            Vf2 = (Vj2+Vm2)/2
            Vf3 = (Vj3+Vm3)/2
            Vf4 = (Vj4+Vm4)/2
            Vf5 = (Vj5+Vm5)/2
            Vf6 = (Vj6+Vm6)/2
            Vf7 = (Vj7+Vm7)/2
            Vf8 = (Vj8+Vm8)/2
        else:
            Vf1 = 0
            Vf2 = 0
            Vf3 = 0
            Vf4 = 0
            Vf5 = 0
            Vf6 = 0
            Vf7 = 0
            Vf8 = 0   
###########################################################
##-----------CALCULO DA VELOCIDADE REAL INICAL-----------## 
###########################################################         
        Vr1 = 4*(Vf1/1000)/(math.pi*(D1/1000)**2)
        Vr2 = 4*(Vf2/1000)/(math.pi*(D2/1000)**2)
        Vr3 = 4*(Vf3/1000)/(math.pi*(D3/1000)**2)
        Vr4 = 4*(Vf4/1000)/(math.pi*(D4/1000)**2)
        Vr5 = 4*(Vf5/1000)/(math.pi*(D5/1000)**2)
        Vr6 = 4*(Vf6/1000)/(math.pi*(D6/1000)**2)
        Vr7 = 4*(Vf7/1000)/(math.pi*(D7/1000)**2)
        Vr8 = 4*(Vf8/1000)/(math.pi*(D8/1000)**2)
###########################################################
##----------CALCULO DA VELOCIDADE MÁXIMA INICAL----------## 
###########################################################
        Vmax1 = (600+1.5*D1)/1000
        Vmax2 = (600+1.5*D2)/1000
        Vmax3 = (600+1.5*D3)/1000
        Vmax4 = (600+1.5*D4)/1000
        Vmax5 = (600+1.5*D5)/1000
        Vmax6 = (600+1.5*D6)/1000
        Vmax7 = (600+1.5*D7)/1000
        Vmax8 = (600+1.5*D8)/1000
###########################################################
##-------------CALCULO DO DIÂMETRO DOS CANOS-------------## 
###########################################################        
        '''
        # Fórmula para calcular o diametro do cano 
        while True:
            if(D1>=400):
                    D1 = D1 + 100
            if(Vmax1<Vr1):
                if(D1>=100):
                    D1 = D1 + 50
                else:    
                    D1 = D1 + 25
                Vr1 = 4*(Vf1/1000)/(math.pi*(D1/1000)**2)
                Vmax1 = (600+1.5*D1)/1000
            else:
                break    
        while True:
            if(D2>=400):
                    D2 = D2 + 100
            if(Vmax2<Vr2):
                if(D2>=100):
                    D2 = D2 + 50
                else:    
                    D2 = D2 + 25
                Vr2 = 4*(Vf2/1000)/(math.pi*(D2/1000)**2)
                Vmax2 = (600+1.5*D2)/1000            
            else:
                break    
        while True:
            if(Vmax3<Vr3):
                if(D3>=400):
                    D3 = D3 + 100
                if(D3>=100):
                    D3 = D3 + 50
                else:    
                    D3 = D3 + 25
                Vr3 = 4*(Vf3/1000)/(math.pi*(D3/1000)**2)
                Vmax3 = (600+1.5*D3)/1000
            else:
                break    
        while True:
            if(Vmax4<Vr4):
                if(D4>=400):
                    D4 = D4 + 100
                if(D4>=100):
                    D4 = D4 + 50
                else:    
                    D4 = D4 + 25
                Vr4 = 4*(Vf4/1000)/(math.pi*(D4/1000)**2)
                Vmax4 = (600+1.5*D4)/1000            
            else:
                break    
        while True:
            if(Vmax5<Vr5):
                if(D5>=400):
                    D5 = D5 + 100
                if(D5>=100):
                    D5 = D5 + 50
                else:    
                    D5 = D5 + 25
                Vr5 = 4*(Vf5/1000)/(math.pi*(D5/1000)**2)
                Vmax5 = (600+1.5*D5)/1000            
            else:
                break    
        while True:
            if(Vmax6<Vr6):
                if(D6>=400):
                    D6 = D6 + 100
                if(D6>=100):
                    D6 = D6 + 50
                else:    
                    D6 = D6 + 25        
                Vr6 = 4*(Vf6/1000)/(math.pi*(D6/1000)**2)
                Vmax6 = (600+1.5*D6)/1000            
            else:
                break    
        while True:
            if(Vmax7<Vr7):
                if(D7>=400):
                    D7 = D7 + 100
                if(D7>=100):
                    D7 = D7 + 50
                else:    
                    D7 = D7 + 25
                Vr7 = 4*(Vf7/1000)/(math.pi*(D7/1000)**2)
                Vmax7 = (600+1.5*D7)/1000            
            else:
                break    
        while True:
            if(Vmax8<Vr8):
                if(D8>=400):
                    D8 = D8 + 100
                if(D8>=100):
                    D8 = D8 + 50
                else:    
                    D8 = D8 + 25
                Vr8 = 4*(Vf8/1000)/(math.pi*(D8/1000)**2)
                Vmax8 = (600+1.5*D8)/1000
            else: 
                break
        '''    
        D1 = 150
        D2 = 250
        D3 = 200
        D4 = 400
        D5 = 150
        D6 = 200
        D7 = 550
        D8 = 300
###########################################################
##-----------CALCULO DA PERDA DE CARGA UNITÁRIA----------## 
###########################################################         
#Fórmula Hazen-Williams
        J1 = (10.65*((Vf1/1000)**1.85))/((C**1.85)*((D1/1000)**4.87))
        J2 = (10.65*((Vf2/1000)**1.85))/((C**1.85)*((D2/1000)**4.87))
        J3 = (10.65*((Vf3/1000)**1.85))/((C**1.85)*((D3/1000)**4.87))
        J4 = (10.65*((Vf4/1000)**1.85))/((C**1.85)*((D4/1000)**4.87))
        J5 = (10.65*((Vf5/1000)**1.85))/((C**1.85)*((D5/1000)**4.87))
        J6 = (10.65*((Vf6/1000)**1.85))/((C**1.85)*((D6/1000)**4.87))
        J7 = (10.65*((Vf7/1000)**1.85))/((C**1.85)*((D7/1000)**4.87))
        J8 = (10.65*((Vf8/1000)**1.85))/((C**1.85)*((D8/1000)**4.87))
###########################################################
##---------------CALCULO DA PERDA DE CARGA---------------## 
########################################################### 
        dH1 = L1*J1
        dH2 = L2*J2
        dH3 = L3*J3
        dH4 = L4*J4
        dH5 = L5*J5
        dH6 = L6*J6
        dH7 = L7*J7
        dH8 = L8*J8
###########################################################
##---------CALCULO COTA PIEZOMETRICA A MONTANTE----------## 
###########################################################         
# Estratégia de cálculo para a pressão - Começar pelo reservatório - pressão dinâmica > 10 mca - pressão estática < 50 mca
# Propor uma pressão para o reservatório - no caso 15 mc
# inicio
        Cm8 = Hc + int(15)
        Cm7 = Cm8 - dH8
        Cm6 = Cm7 - dH7
        Cm5 = Cm7 - dH7
        Cm4 = Cm8 - dH8
        Cm3 = Cm4 - dH4
        Cm2 = Cm4 - dH4
        Cm1 = Cm2 - dH2
###########################################################
##----------CALCULO COTA PIEZOMETRICA A JUSANTE----------## 
###########################################################                
# final
        Cj8 = Cm8 - dH8
        Cj7 = Cm7 - dH7
        Cj6 = Cm6 - dH6
        Cj5 = Cm5 - dH5
        Cj4 = Cm4 - dH4
        Cj3 = Cm3 - dH3
        Cj2 = Cm2 - dH2
        Cj1 = Cm1 - dH1
###########################################################
##--------------CALCULO PRESSÃO A MONTANTE---------------## 
########################################################### 
        Pm1 = Cm1 - Hm1
        Pm2 = Cm2 - Hm2
        Pm3 = Cm3 - Hm3
        Pm4 = Cm4 - Hm4
        Pm5 = Cm5 - Hm5
        Pm6 = Cm6 - Hm6
        Pm7 = Cm7 - Hm7
        Pm8 = Cm8 - Hm8
###########################################################
##--------------CALCULO PRESSÃO A JUSANTE----------------## 
###########################################################
        Pj1 = Cj1 - Hj1
        Pj2 = Cj2 - Hj2
        Pj3 = Cj3 - Hj3
        Pj4 = Cj4 - Hj4
        Pj5 = Cj5 - Hj5
        Pj6 = Cj6 - Hj6
        Pj7 = Cj7 - Hj7
        Pj8 = Cj8 - Hj8
###########################################################
##------------INCLUI DADOS NA NOVA PLANILHA--------------## 
###########################################################        
        if j == 0:
            if (Pj1 < 9 or Pj2 <9 or Pj3 <9 or Pj4 <9 or Pj5 <9 or Pj6 <9 or Pj7 <9 or Pj8 <9 or Pm1 <9 or Pm2 <9 or Pm3 <9 or Pm4 <9 or Pm5 <9 or Pm6 <9 or Pm7 <9 or Pm8 <9):
                print("ALGUMA DAS PRESSOES ESTA ABAIXO TANQUE 1")
            if (Pj1 > 50 or Pj2 > 50 or Pj3 > 50 or Pj4 > 50 or Pj5 > 50 or Pj6 > 50 or Pj7 > 50 or Pj8 > 50 or Pm1 > 50 or Pm2 > 50 or Pm3 > 50 or Pm4 > 50 or Pm5 > 50 or Pm6 > 50 or Pm7 > 50 or Pm8 > 50):
                print("ALGUMA DAS PRESSOES ESTA ACIMA TANQUE 1")    
            sh1.write(i+1,0,Pj1)
            sh1.write(i+1,1,Pj2)
            sh1.write(i+1,2,Pj3)
            sh1.write(i+1,3,Pj4)
            sh1.write(i+1,4,Pj5)
            sh1.write(i+1,5,Pj6)
            sh1.write(i+1,6,Pj7)
            sh1.write(i+1,7,Pj8)
            sh1.write(i+1,9,Pm1)
            sh1.write(i+1,10,Pm2)
            sh1.write(i+1,11,Pm3)
            sh1.write(i+1,12,Pm4)
            sh1.write(i+1,13,Pm5)
            sh1.write(i+1,14,Pm6)
            sh1.write(i+1,15,Pm7)
            sh1.write(i+1,16,Pm8)

        if j == 1:
            if (Pj1 < 9 or Pj2 <9 or Pj3 <9 or Pj4 <9 or Pj5 <9 or Pj6 <9 or Pj7 <9 or Pj8 <9 or Pm1 <9 or Pm2 <9 or Pm3 <9 or Pm4 <9 or Pm5 <9 or Pm6 <9 or Pm7 <9 or Pm8 <9):
                print("ALGUMA DAS PRESSOES ESTA ABAIXO TANQUE 2")
            if (Pj1 > 50 or Pj2 > 50 or Pj3 > 50 or Pj4 > 50 or Pj5 > 50 or Pj6 > 50 or Pj7 > 50 or Pj8 > 50 or Pm1 > 50 or Pm2 > 50 or Pm3 > 50 or Pm4 > 50 or Pm5 > 50 or Pm6 > 50 or Pm7 > 50 or Pm8 > 50):
                print("ALGUMA DAS PRESSOES ESTA ACIMA TANQUE 2")    
            sh2.write(i+1,0,Pj1)
            sh2.write(i+1,1,Pj2)
            sh2.write(i+1,2,Pj3)
            sh2.write(i+1,3,Pj4)
            sh2.write(i+1,4,Pj5)
            sh2.write(i+1,5,Pj6)
            sh2.write(i+1,6,Pj7)
            sh2.write(i+1,7,Pj8)
            sh2.write(i+1,9,Pm1)
            sh2.write(i+1,10,Pm2)
            sh2.write(i+1,11,Pm3)
            sh2.write(i+1,12,Pm4)
            sh2.write(i+1,13,Pm5)
            sh2.write(i+1,14,Pm6)
            sh2.write(i+1,15,Pm7)
            sh2.write(i+1,16,Pm8)
        if j == 2:
            if (Pj1 < 9 or Pj2 <9 or Pj3 <9 or Pj4 <9 or Pj5 <9 or Pj6 <9 or Pj7 <9 or Pj8 <9 or Pm1 <9 or Pm2 <9 or Pm3 <9 or Pm4 <9 or Pm5 <9 or Pm6 <9 or Pm7 <9 or Pm8 <9):
                print("ALGUMA DAS PRESSOES ESTA ABAIXO TANQUE 3")
            if (Pj1 > 50 or Pj2 > 50 or Pj3 > 50 or Pj4 > 50 or Pj5 > 50 or Pj6 > 50 or Pj7 > 50 or Pj8 > 50 or Pm1 > 50 or Pm2 > 50 or Pm3 > 50 or Pm4 > 50 or Pm5 > 50 or Pm6 > 50 or Pm7 > 50 or Pm8 > 50):
                print("ALGUMA DAS PRESSOES ESTA ACIMA TANQUE 3")    
            sh3.write(i+1,0,Pj1)
            sh3.write(i+1,1,Pj2)
            sh3.write(i+1,2,Pj3)
            sh3.write(i+1,3,Pj4)
            sh3.write(i+1,4,Pj5)
            sh3.write(i+1,5,Pj6)
            sh3.write(i+1,6,Pj7)
            sh3.write(i+1,7,Pj8)
            sh3.write(i+1,9,Pm1)
            sh3.write(i+1,10,Pm2)
            sh3.write(i+1,11,Pm3)
            sh3.write(i+1,12,Pm4)
            sh3.write(i+1,13,Pm5)
            sh3.write(i+1,14,Pm6)
            sh3.write(i+1,15,Pm7)
            sh3.write(i+1,16,Pm8)
        if j == 3:
            if (Pj1 < 9 or Pj2 <9 or Pj3 <9 or Pj4 <9 or Pj5 <9 or Pj6 <9 or Pj7 <9 or Pj8 <9 or Pm1 <9 or Pm2 <9 or Pm3 <9 or Pm4 <9 or Pm5 <9 or Pm6 <9 or Pm7 <9 or Pm8 <9):
                print("ALGUMA DAS PRESSOES ESTA ABAIXO TANQUE 4")
            if (Pj1 > 50 or Pj2 > 50 or Pj3 > 50 or Pj4 > 50 or Pj5 > 50 or Pj6 > 50 or Pj7 > 50 or Pj8 > 50 or Pm1 > 50 or Pm2 > 50 or Pm3 > 50 or Pm4 > 50 or Pm5 > 50 or Pm6 > 50 or Pm7 > 50 or Pm8 > 50):
                print("ALGUMA DAS PRESSOES ESTA ACIMA TANQUE 4")    
            sh4.write(i+1,0,Pj1)
            sh4.write(i+1,1,Pj2)
            sh4.write(i+1,2,Pj3)
            sh4.write(i+1,3,Pj4)
            sh4.write(i+1,4,Pj5)
            sh4.write(i+1,5,Pj6)
            sh4.write(i+1,6,Pj7)
            sh4.write(i+1,7,Pj8)
            sh4.write(i+1,9,Pm1)
            sh4.write(i+1,10,Pm2)
            sh4.write(i+1,11,Pm3)
            sh4.write(i+1,12,Pm4)
            sh4.write(i+1,13,Pm5)
            sh4.write(i+1,14,Pm6)
            sh4.write(i+1,15,Pm7)
            sh4.write(i+1,16,Pm8)
# Salva nova planilha
if int(opcao1) == 1 and int(opcao2) == 1:            
    newworkbook.save("Resultados.xls")
elif int(opcao1) == 2 and int(opcao2) == 1:
    newworkbook.save("Resultados2.xls")
elif int(opcao1) == 1 and int(opcao2) == 2:
    newworkbook.save("Resultados3.xls")
elif int(opcao1) == 2 and int(opcao2) == 2:
    newworkbook.save("Resultados4.xls")        
