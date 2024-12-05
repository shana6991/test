import streamlit as st
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d

# Données pour une prime de 300 CHF
values_4_percent_300 = np.array([
    1112, 2318, 3588, 4928, 6339, 10268, 14400, 18755, 23344, 28179,
    33272, 38636, 44285, 50231, 56491, 63079, 70013, 77308, 84983, 93056,
    101546, 110473, 119859, 129726, 140096, 150994, 162445, 174477, 187116, 200393,
    214338, 228985, 244367, 260520, 280523
])

values_7_percent_300 = np.array([
    1130, 2388, 3752, 5232, 6835, 11053, 15617, 20565, 25928, 31740,
    38037, 44860, 52250, 60254, 68921, 78306, 88466, 99463, 111366, 124246,
    138183, 153260, 169569, 187209, 206286, 226914, 249217, 273330, 299395, 327568,
    358018, 390926, 426487, 464912, 511869
])

values_9_percent_300 = np.array([
    1141, 2435, 3865, 5443, 7186, 11615, 16497, 21887, 27838, 34407,
    41657, 49657, 58484, 68222, 78962, 90808, 103871, 118275, 134154, 151657,
    170949, 192209, 215635, 241445, 269879, 301200, 335697, 373690, 415526, 461592,
    512310, 568146, 629611, 697266, 779919
])

# Données pour une prime de 588 CHF
values_4_percent_588 = np.array([
    2286, 4723, 7294, 10003, 12857, 20651, 28849, 37488, 46593, 56184,
    66287, 76928, 88133, 99930, 112348, 125418, 139173, 153645, 168870, 184885,
    201727, 219436, 238054, 257626, 278196, 299815, 322531, 346397, 371469, 397805,
    425467, 454520, 485032, 517073, 556753
])

values_7_percent_588 = np.array([
    2321, 4867, 7628, 10622, 13867, 22245, 31310, 41138, 51790, 63334,
    75842, 89393, 104072, 119969, 137185, 155825, 176005, 197848, 221489, 247071,
    274751, 304697, 337090, 372124, 410013, 450984, 495281, 543171, 594938, 650893,
    711369, 776726, 847353, 923668, 1016927
])

values_9_percent_588 = np.array([
    2345, 4964, 7857, 11052, 14579, 23384, 33088, 43804, 55634, 68692,
    83104, 99008, 116554, 135912, 157263, 180811, 206778, 235409, 266974, 301767,
    340115, 382376, 428942, 480247, 536767, 599026, 667598, 743116, 826276, 917841,
    1018654, 1129639, 1251813, 1386290, 1550576
])

# Fonction pour interpoler et ajuster les données en fonction de la prime
def calculate_values(prime, interest_rate, years):
    # Taux de base et données correspondantes
    base_rates = [4, 7, 9]
    data_300 = np.vstack([values_4_percent_300, values_7_percent_300, values_9_percent_300]).T
    data_588 = np.vstack([values_4_percent_588, values_7_percent_588, values_9_percent_588]).T

    # Interpolateurs
    interpolator_300 = interp1d(base_rates, data_300, axis=1, kind='linear', fill_value="extrapolate")
    interpolator_588 = interp1d(base_rates, data_588, axis=1, kind='linear', fill_value="extrapolate")

    # Interpolation pour le taux donné
    values_300 = interpolator_300(interest_rate)[:years]
    values_588 = interpolator_588(interest_rate)[:years]

    # Ajustement des valeurs en fonction de la prime modulable
    ratio = (prime - 300) / (588 - 300)  # Calcul du ratio entre 300 et 588
    estimated_values = values_300 + ratio * (values_588 - values_300)
    return estimated_values

# Application Streamlit
st.title("Prédictions des Valeurs de Rachat pour N'importe Quel Taux et Prime Modulable")
st.write("Calculez les valeurs de rachat pour une prime et un taux de rendement donnés, avec des estimations précises basées sur les données existantes.")

# Entrées utilisateur
prime = st.number_input("Saisissez le montant de la prime mensuelle (CHF)", min_value=100, max_value=1000, step=1, value=350)
interest_rate = st.number_input("Saisissez le taux de rendement (%)", min_value=1.0, max_value=15.0, step=0.1, value=7.0)
years = st.number_input("Nombre d'années de contrat", min_value=1, max_value=35, step=1, value=35)

# Calcul des valeurs
values = calculate_values(prime, interest_rate, years)

if values is not None:
    # Affichage des résultats
    years_display = np.arange(1, years + 1)
    results_df = pd.DataFrame({"Année": years_display, "Valeur estimée (CHF)": values})

    st.write("### Résultats des Prédictions")
    st.dataframe(results_df)

    # Option de téléchargement
    csv = results_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Télécharger les résultats (CSV)",
        data=csv,
        file_name=f"predictions_prime_{prime}_taux_{interest_rate}.csv",
        mime="text/csv"
    )
else:
    st.error("Impossible de calculer les valeurs pour cette combinaison de prime et de taux.")
