# Core Pkgs
import streamlit as st 
import os
import numpy as np
import matplotlib.pyplot as plt
import cmath as cm

def filtro_sintonizado(R_filtro, L_filtro, C_filtro, w):
     Zsint = R_filtro + 1j*w*L_filtro + 1/(1j*w*C_filtro)
     return Zsint

def filtro_amortecido(R_filtro, L_filtro, C_filtro, w):
     Zamort = 1/((1/R_filtro)+1/(1j*w*L_filtro)) + 1/(1j*w*C_filtro)
     return Zamort  

def grafico_impedancia(hh, ZZ):
     fig, ax = plt.subplots()
     ax.plot(hh, abs(ZZ))
     ind_z_fund = np.where( hh == 1)
     lim = abs(ZZ[ind_z_fund])
     ax.set_ylim(-0.1*lim, 1.1*lim)
     ax.grid()
     st.pyplot(fig)


h = np.arange(0.1, 11, 0.1)
f = 60 * h
w = 2*np.pi*f


tipo_de_filtro = st.sidebar.selectbox(
                              "Selecione o tipo de filtro",
                              ("Sintonizado", "Amortecido")
)



L_filtro = st.slider('Indutância [mH]', 0, 130, 25)
C_filtro = st.slider('Indutância [μF]', 0, 130, 25)
L_filtro = L_filtro*1e-3
C_filtro = C_filtro*1e-6
if tipo_de_filtro=="Sintonizado":
     R_filtro = st.slider('Resistência [mΩ]', 0, 10000, 100)
     R_filtro = R_filtro*1e-3
     impedancia_filtro = filtro_sintonizado(R_filtro, L_filtro, C_filtro, w)
elif tipo_de_filtro=="Amortecido":
     R_filtro = st.slider('Resistência [Ω]', 10, 10000, 1000)
     R_filtro = R_filtro*1
     impedancia_filtro = filtro_amortecido(R_filtro, L_filtro, C_filtro, w)     
else:
     pass

grafico_impedancia(h, impedancia_filtro)