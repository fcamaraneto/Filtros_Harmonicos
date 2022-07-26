import streamlit as st 
import os
import matplotlib.pyplot as plt
import cmath as cm
from engineering_notation import EngNumber
from PIL import Image
import numpy

class funcoes:

    def filtro_sintonizado(R_filtro, L_filtro, C_filtro, w):
        Zsint = R_filtro + 1j*w*L_filtro + 1/(1j*w*C_filtro)
        w0 = 1 / numpy.sqrt(L_filtro*C_filtro)
        return [Zsint, w0]

    def filtro_amortecido(R_filtro, L_filtro, C_filtro, w):
        Zamort = 1/((1/R_filtro)+1/(1j*w*L_filtro)) + 1/(1j*w*C_filtro)
        num = numpy.sqrt(L_filtro*R_filtro**2)
        w0 = R_filtro / numpy.sqrt(L_filtro*(C_filtro*R_filtro**2-L_filtro))
        return [Zamort, w0]  

    def grafico_impedancia(hh, ZZ_filtro, ZZ_equivalente, ZZ_trafo, hh_filtrar, Z_base_trafo):
        fig, ax = plt.subplots(figsize=(5, 2.5))
        ax.plot(hh, abs(ZZ_filtro/Z_base_trafo), label='filtro')
        ax.plot(hh, abs(ZZ_equivalente/Z_base_trafo), label='equivalente')
        ax.plot(hh, abs(ZZ_trafo/Z_base_trafo), label='trafo')
        ind_harmonico_a_filtrar = numpy.where( hh == hh_filtrar)
        limY = abs(ZZ_equivalente[ind_harmonico_a_filtrar])
        ax.set_ylim(-0.1, 3.1)
        ax.set_xlabel(r'Harmônico $[f/f_1]$')
        ax.set_ylabel(r'Impedância $\left[ \frac{Z}{Z_{base}} \right]$')
        ax.legend(fontsize=6)
        ax.grid(ls='dashed', lw=0.5)
        st.pyplot(fig)

    def grafico_corrente(hh, ii_trafo, ii_filtro, ii_fonte):
        fig, ax = plt.subplots(figsize=(5, 2.5))
        ax.bar(hh-0.5, abs(ii_fonte/ ii_trafo[1]), label='total', width=0.5)
        ax.bar(hh,     abs(ii_filtro/ii_trafo[1]), label='filtro', width=0.5)
        ax.bar(hh+0.5, abs(ii_trafo/ ii_trafo[1]), label='trafo', width=0.5)
        ax.set_xlabel(r'Harmônico $\left[\frac{f}{f_1}\right]$')
        ax.set_ylabel(r'Corrente $\left[\frac{i}{i_1}\right]$')
        ax.legend(fontsize=6)
        ax.grid(ls='dashed', lw=0.5)
        st.pyplot(fig)


    def grafico_corrente_filtro(hh, i_resistor_inteiros, i_indutor_inteiros, i_capacitor_inteiros, i_fund):
        fig, ax = plt.subplots(figsize=(5, 2.5))
        ax.bar(hh-0.5, abs(i_resistor_inteiros/ i_fund), label='$i_R$', width=0.5)
        ax.bar(hh,     abs(i_indutor_inteiros/  i_fund), label='$i_L$', width=0.5)
        ax.bar(hh+0.5, abs(i_capacitor_inteiros/i_fund), label='$i_C$', width=0.5)
        ax.set_xlabel(r'Harmônico $\left[\frac{f}{f_1}\right]$')
        ax.set_ylabel(r'Corrente $\left[\frac{i}{i_1}\right]$')
        ax.legend(fontsize=6)
        ax.grid(ls='dashed', lw=0.5)
        st.pyplot(fig)

    def grafico_tensao_filtro(hh, v_resistor_inteiros, v_indutor_inteiros, v_capacitor_inteiros, V_fund):
        fig, ax = plt.subplots(figsize=(5, 2.5))
        ax.bar(hh-0.5, numpy.sqrt(3)*abs(v_resistor_inteiros/V_fund), label='$v_R$', width=0.5)
        ax.bar(hh,     numpy.sqrt(3)*abs(v_indutor_inteiros/ V_fund), label='$v_L$', width=0.5)
        ax.bar(hh+0.5, numpy.sqrt(3)*abs(v_capacitor_inteiros/V_fund), label='$v_C$', width=0.5)
        ax.set_xlabel(r'Harmônico $\left[\frac{f}{f_1}\right]$')
        ax.set_ylabel(r'Tensão $\left[\frac{v}{v_1}\right]$')
        ax.legend(fontsize=6)
        ax.grid(ls='dashed', lw=0.5)
        st.pyplot(fig)



    #grafico_tensao(h_inteiros, v_resistor_inteiros, v_capacitor_inteiros, v_indutor_inteiros)
    def grafico_tensao(hh, vv_resistor, vv_indutor, vv_capacitor):
        fig, ax = plt.subplots(figsize=(5, 2.5))
        ax.bar(hh-0.33, numpy.abs(vv_resistor), label='resistor', width=0.30)
        ax.bar(hh, numpy.abs(vv_indutor), label='indutor', width=0.30)
        ax.bar(hh+0.33, numpy.abs(vv_capacitor), label='capacitor', width=0.30)
        ax.set_xlabel(r'Harmônico $\left[\frac{f}{f_1}\right]$')
        ax.set_ylabel(r'Tensão $\left[\frac{v}{v_1}\right]$')
        ax.legend(fontsize=6)
        ax.grid(ls='dashed', lw=0.5)
        st.pyplot(fig)

    def grafico_potencia_filtro(hh, p_resistor_inteiros, p_indutor_inteiros, p_capacitor_inteiros):
        fig, ax = plt.subplots(figsize=(5, 2.5))
        ax.bar(hh-0.5, numpy.real(3*p_resistor_inteiros/1e6),  label='resistor',  width=0.5)
        ax.bar(hh,     numpy.imag(3*p_indutor_inteiros/1e6),   label='indutor',   width=0.5)
        ax.bar(hh+0.5, numpy.imag(3*p_capacitor_inteiros/1e6), label='capacitor', width=0.5)
        ax.set_xlabel(r'Harmônico $\left[\frac{f}{f_1}\right]$')
        ax.set_ylabel(r'Potência [MW] ou [MVAr]')
        ax.legend(fontsize=6)
        ax.grid(ls='dashed', lw=0.5)
        st.pyplot(fig)



    def dados_transformador_freq_fundamental(Snom, V1, Rperc, Xperc):
        I_trafo_fund   = Snom / (numpy.sqrt(3)*V1)
        Z_base_trafo   =  V1/numpy.sqrt(3) / I_trafo_fund
        Z_trafo_fund   = 1e-2 * ( Rperc + 1j*Xperc ) * Z_base_trafo
        return [I_trafo_fund, Z_base_trafo, Z_trafo_fund]

    def definicoes_iniciais(ff_fund_, VV_fund_, hh):
        V_fund = 1e3 * VV_fund_
        if ff_fund_=="60 Hz":
            f_fund = 60
        elif ff_fund_=="50 Hz":
            f_fund = 50
        else:
            pass
        w_fund = 2 * numpy.pi*f_fund
        f = f_fund * hh
        w = 2*numpy.pi*f
        return [V_fund, f_fund, w_fund, f, w]


    def fundamentais_filtro(reativos_ou_capacitancia, h_principal, V_fund, w_fund, tipo_de_filtro):
        if reativos_ou_capacitancia=="μF":
            L_filtro = st.number_input('Indutância do filtro em mH',   min_value=0.0, max_value=80.0, value=26.31, step=1.0)
            C_filtro = st.number_input('Capacitância do Filtro em μF', min_value=0.0, max_value=30.0, value=10.70, step=1.0)
            L_filtro = L_filtro*1e-3
            C_filtro = C_filtro*1e-6
        elif reativos_ou_capacitancia=="kVAr":
            dessintonia        = st.number_input('Dessintonia %:'               , min_value=0.0, max_value=5.0, value=2.0, step=0.1)
            Q_reat_fund_filtro = st.number_input('MVAr Capacitivos Fundamental:', min_value=0.0, max_value=100.0, value=5.0, step=1.0)
            dessintonia = 1e-2 * dessintonia
            Q_reat_fund_filtro = 1e6 * Q_reat_fund_filtro
            XFILTRO_fund = V_fund**2 / Q_reat_fund_filtro
            h_dessintonia_quadrado = ( h_principal * (1 - dessintonia) )**2
            XC_sobre_XL = h_dessintonia_quadrado
            XC_fund = V_fund**2 / ( Q_reat_fund_filtro*(1-1/XC_sobre_XL) )
            XL_fund = XC_fund - XFILTRO_fund
            C_filtro = 1 / (w_fund*XC_fund)
            L_filtro = XL_fund / w_fund
        else:
            pass
        if tipo_de_filtro=="Sintonizado":
            R_filtro = st.number_input('Resistência do filtro em mΩ', min_value=0.0, max_value=1000.0, value=100.,   step=1.0)
            R_filtro = R_filtro*1e-3
        elif tipo_de_filtro=="Amortecido":
            R_filtro = st.number_input('Resistência do filtro em Ω', min_value=10.0, max_value=5000.0, value=100.0,   step=100.0)
        else:
            pass

        return [R_filtro, L_filtro, C_filtro]

    def selecao_da_imagem(tipo_de_filtro):
        if tipo_de_filtro=="Sintonizado":
            imagem = Image.open('./figs/Sintonizado.png')
        elif tipo_de_filtro=="Amortecido":
            imagem = Image.open('./figs/Amortecido.png')
        else:
            pass
        return imagem


    def impedancias(tipo_de_filtro, R_filtro, L_filtro, C_filtro, w, h, Z_trafo_fund):
        if tipo_de_filtro=="Sintonizado":
            Z_filtro, w_ressonancia = funcoes.filtro_sintonizado(R_filtro, L_filtro, C_filtro, w)
            w_min_lactec = w_ressonancia
        elif tipo_de_filtro=="Amortecido":
            Z_filtro, w_ressonancia = funcoes.filtro_amortecido(R_filtro, L_filtro, C_filtro, w)
            # essas próximas linhas até o final do elif foi só para conferir com dados do lactec
            aa = C_filtro**2 * R_filtro**4 + 2 * C_filtro * L_filtro *R_filtro**2 - L_filtro**2
            bb_num = C_filtro**2 * R_filtro**8 + 2 * C_filtro * L_filtro * R_filtro**6
            bb_den = L_filtro**2 * (C_filtro**2 * R_filtro**4 + 2 * C_filtro * L_filtro * R_filtro**2 - L_filtro**2)**2
            num_grande = aa * numpy.sqrt(bb_num/bb_den) + R_filtro**2
            den_grande = C_filtro**2 * R_filtro**4 + 2 * C_filtro * L_filtro * R_filtro**2 - L_filtro**2
            w_min_lactec = numpy.sqrt(num_grande / den_grande)
        else:
            pass
        Z_trafo = numpy.real(Z_trafo_fund) + 1j*h*numpy.imag(Z_trafo_fund)
        Z_equivalente = 1 / (1/Z_trafo + 1/Z_filtro)
        # indice limite para maior frequencia de ressonancia de maxima impedancia
        idx_limite = numpy.where(w < w_ressonancia)
        ind_max_impedancia = numpy.where( numpy.imag(Z_equivalente) == numpy.max(numpy.imag(Z_equivalente[idx_limite])))
        
        return [Z_filtro, Z_trafo, Z_equivalente, w_ressonancia, w_min_lactec, ind_max_impedancia]



    def grandezas_inteiras(h, w, Z_trafo, Z_equivalente, Z_filtro, Z_base_trafo, h_principal, ih_principal, tipo_de_filtro, R_filtro, L_filtro, C_filtro, V_fund, S_trafo_fund):
        # --- somente os harmônicos inteiros
        temp =  numpy.where(numpy.mod(h,1) == 0)[0]
        indices_h_inteiro = numpy.zeros(len(temp)+1, dtype=int)
        indices_h_inteiro[1:len(indices_h_inteiro)] = temp
        h_inteiros = h[indices_h_inteiro]
        w_inteiros = w[indices_h_inteiro]
        # --- todas as impedâncias inteiras
        Z_trafo_inteiros       = Z_trafo[indices_h_inteiro] 
        Z_filtro_inteiros      = Z_filtro[indices_h_inteiro] 
        Z_equivalente_inteiros = Z_equivalente[indices_h_inteiro]
        # --- todas as correntes inteiras da carga ou fonte no caso de gerador
        i_carga_inteiros = numpy.random.randint(0 , 3, len(h_inteiros)) +1j*numpy.random.randint(0 , 2, len(h_inteiros))
        i_carga_inteiros = i_carga_inteiros * 0 # maneira elegante de zerar
        i_base_trafo     = S_trafo_fund / (numpy.sqrt(3)*V_fund)
        i_carga_inteiros[h_principal] = ih_principal/100 * i_base_trafo
        i_carga_inteiros[1] =  i_base_trafo
        # --- tensão na barra comum já com o filtro instalado
        v_queda_trafo_paralelo_com_filtro = i_carga_inteiros * Z_equivalente_inteiros
        v_barra_inteiros = v_queda_trafo_paralelo_com_filtro
        v_barra_inteiros[1] = V_fund/(numpy.sqrt(3)) - v_queda_trafo_paralelo_com_filtro[1]
        # --- corrente do filtro e do transformador
        i_filtro_inteiros =  v_barra_inteiros / Z_filtro_inteiros
        i_trafo_inteiros  = i_carga_inteiros - i_filtro_inteiros
        # --- tensões e correntes nos elementos do filtro
        v_capacitor_inteiros = i_filtro_inteiros *  1/(1j*w_inteiros*C_filtro) 
        i_capacitor_inteiros = i_filtro_inteiros
        if tipo_de_filtro=='Sintonizado':
            v_resistor_inteiros  = i_filtro_inteiros * R_filtro
            v_indutor_inteiros   = i_filtro_inteiros * 1j*w_inteiros*L_filtro
            i_indutor_inteiros   = i_filtro_inteiros
            i_resistor_inteiros  = i_filtro_inteiros
            
        elif tipo_de_filtro=='Amortecido':
            z_paralelo_RL_inteiros = 1/( 1/R_filtro + 1/(1j*w_inteiros*L_filtro) )
            v_paralelo_RL_inteiros = i_filtro_inteiros * z_paralelo_RL_inteiros
            i_resistor_inteiros    = v_paralelo_RL_inteiros / R_filtro
            i_indutor_inteiros     = v_paralelo_RL_inteiros / (1j*w_inteiros*L_filtro) 
            v_indutor_inteiros     = v_paralelo_RL_inteiros
            v_resistor_inteiros    = v_paralelo_RL_inteiros    

        return [h_inteiros, i_trafo_inteiros, i_filtro_inteiros, i_carga_inteiros, v_barra_inteiros, i_resistor_inteiros, i_indutor_inteiros, i_capacitor_inteiros, v_resistor_inteiros, v_indutor_inteiros, v_capacitor_inteiros]


    def tensoes_eficazes_nos_elementos_do_filtro(v_resistor_inteiros, v_indutor_inteiros, v_capacitor_inteiros):
        temp = numpy.abs(v_indutor_inteiros)
        tensao_eficaz_indutor = numpy.sqrt(numpy.dot(temp, temp))
        temp = numpy.abs(v_capacitor_inteiros)
        tensao_eficaz_capacitor = numpy.sqrt(numpy.dot(temp, temp))
        temp = numpy.abs(v_resistor_inteiros)
        tensao_eficaz_resistor = numpy.sqrt(numpy.dot(temp, temp))
        return [tensao_eficaz_resistor, tensao_eficaz_indutor, tensao_eficaz_capacitor]


    def correntes_eficazes_nos_elementos_do_filtro(i_resistor_inteiros, i_indutor_inteiros, i_capacitor_inteiros):
        temp = numpy.abs(i_indutor_inteiros)
        corrente_eficaz_indutor = numpy.sqrt(numpy.dot(temp, temp))
        temp = numpy.abs(i_capacitor_inteiros)
        corrente_eficaz_capacitor = numpy.sqrt(numpy.dot(temp, temp))
        temp = numpy.abs(i_resistor_inteiros)
        corrente_eficaz_resistor = numpy.sqrt(numpy.dot(temp, temp))
        return [corrente_eficaz_resistor, corrente_eficaz_indutor, corrente_eficaz_capacitor]


    def potencias_eficazes(v_resistor_inteiros, v_indutor_inteiros, v_capacitor_inteiros, i_resistor_inteiros, i_indutor_inteiros, i_filtro_inteiros):
        potencia_eficaz_resistor  = numpy.dot(v_resistor_inteiros,  numpy.conjugate(i_resistor_inteiros))
        potencia_eficaz_indutor   = numpy.dot(v_indutor_inteiros,   numpy.conjugate(i_indutor_inteiros))
        potencia_eficaz_capacitor = numpy.dot(v_capacitor_inteiros, numpy.conjugate(i_filtro_inteiros))
        potencia_eficaz_resistor  = numpy.sqrt(potencia_eficaz_resistor)
        potencia_eficaz_indutor   = numpy.sqrt(potencia_eficaz_indutor)
        potencia_eficaz_capacitor = numpy.sqrt(potencia_eficaz_capacitor)
        return [potencia_eficaz_resistor, potencia_eficaz_indutor, potencia_eficaz_capacitor]

    def potencias_inteiras(v_resistor_inteiros, v_indutor_inteiros, v_capacitor_inteiros, i_resistor_inteiros, i_indutor_inteiros, i_capacitor_inteiros):
        p_capacitor_inteiros = v_capacitor_inteiros * numpy.conjugate(i_capacitor_inteiros)
        p_indutor_inteiros   = v_indutor_inteiros   * numpy.conjugate(i_indutor_inteiros)
        p_resistor_inteiros  = v_resistor_inteiros  * numpy.conjugate(i_resistor_inteiros)
        return [p_resistor_inteiros, p_indutor_inteiros, p_capacitor_inteiros]