import streamlit as st
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d

# Données pour une prime de 300 CHF
values_2_percent_300 = np.array([
    1099, 2251, 3419, 4605, 5808, 9440, 13127, 16867, 20661, 24511,
    28417, 32379, 36399, 40477, 44613, 48808, 53063, 57378, 61755, 66193,
    70693, 75255, 79880, 84568, 89320, 94137, 99018, 103964, 108976, 114054,
    119200, 124414, 129699, 135054, 140481
])

values_3_percent_300 = np.array([
    1105, 2274, 3471, 4698, 5955, 9668, 13473, 17371, 21365, 25457,
    29648, 33943, 38343, 42850, 47466, 52195, 57038, 61999, 67081, 72284,
    77613, 83069, 88656, 94376, 100232, 106227, 112364, 118645, 125075, 131656,
    138392, 145289, 152348, 159576, 166973
])

values_4_percent_300 = np.array([
    1112, 2318, 3588, 4928, 6339, 10268, 14400, 18755, 23344, 28179,
    33272, 38636, 44285, 50231, 56491, 63079, 70013, 77308, 84983, 93056,
    101546, 110473, 119859, 129726, 140096, 150994, 162445, 174477, 187116, 200393,
    214338, 228985, 244367, 260520, 280523
])

values_6_percent_300 = np.array([
    1122, 2343, 3630, 4988, 6419, 10391, 14580, 18997, 23655, 28566,
    33743, 39203, 44960, 51030, 57428, 64175, 71288, 78787, 86694, 95028,
    103815, 113077, 122841, 133133, 143982, 155418, 167472, 180178, 193570, 207687,
    222568, 238255, 254792, 272226, 290605
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
values_2_percent_588 = np.array([
    2258, 4586, 6948, 9345, 11776, 18971, 26273, 33681, 41197, 48823,
    56559, 64407, 72369, 80446, 88638, 96948, 105376, 113924, 122593, 131384,
    140298, 149334, 158495, 167782, 177194, 186735, 196403, 206200, 216127, 226185,
    236377, 246706, 257173, 267781, 278529
])

values_3_percent_588 = np.array([
    2270, 4633, 7054, 9534, 12075, 19433, 26972, 34696, 42610, 50718,
    59024, 67534, 76252, 85182, 94330, 103700, 113298, 123129, 133197, 143508,
    154067, 164879, 175949, 187283, 198887, 210766, 222927, 235374, 248114, 261155,
    274503, 288167, 302156, 316477, 331137
])

values_4_percent_588 = np.array([
    2286, 4723, 7294, 10003, 12857, 20651, 28849, 37488, 46593, 56184,
    66287, 76928, 88133, 99930, 112348, 125418, 139173, 153645, 168870, 184885,
    201727, 219436, 238054, 257626, 278196, 299815, 322531, 346397, 371469, 397805,
    425467, 454520, 485032, 517073, 556753
])

values_6_percent_588 = np.array([
    2306, 4775, 7378, 10123, 13018, 20899, 29209, 37972, 47212, 56955,
    67227, 78059, 89479, 101520, 114216, 127600, 141712, 156590, 172275, 188810,
    206242, 224618, 243988, 264407, 285930, 308618, 332532, 357739, 384309, 412316,
    441838, 472960, 505769, 540357, 576819
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

# Fonction pour interpoler et ajuster les données
def calculate_values(prime, interest_rate, years):
    base_rates = [2, 3, 4, 6, 7, 9]
    data_300 = np.vstack([values_2_percent_300, values_3_percent_300, values_4_percent_300, values_6_percent_300, values_7_percent_300, values_9_percent_300]).T
    data_588 = np.vstack([values_2_percent_588, values_3_percent_588, values_4_percent_588, values_6_percent_588, values_7_percent_588, values_9_percent_588]).T

    interpolator_300 = interp1d(base_rates, data_300, axis=1, kind='linear', fill_value="extrapolate")
    interpolator_588 = interp1d(base_rates, data_588, axis=1, kind='linear', fill_value="extrapolate")

    values_300 = interpolator_300(interest_rate)[:years]
    values_588 = interpolator_588(interest_rate)[:years]

    ratio = (prime - 300) / (588 - 300)
    estimated_values = values_300 + ratio * (values_588 - values_300)
    return estimated_values

# Application Streamlit
st.title("Prédictions des Valeurs de Rachat avec Taux Étendus")
st.write("Calculez les valeurs de rachat pour une prime et un taux de rendement donnés, avec des taux de 2 % à 9 %.")

# Entrées utilisateur
prime = st.number_input("Saisissez le montant de la prime mensuelle (CHF)", min_value=100, max_value=1000, step=1, value=350)
interest_rate = st.number_input("Saisissez le taux de rendement (%)", min_value=2.0, max_value=15.0, step=0.1, value=7.0)
years = st.number_input("Nombre d'années de contrat", min_value=1, max_value=35, step=1, value=35)

# Calcul des valeurs
values = calculate_values(prime, interest_rate, years)

if values is not None:
    years_display = np.arange(1, years + 1)
    results_df = pd.DataFrame({"Année": years_display, "Valeur estimée (CHF)": values})

    st.write("### Résultats des Prédictions")
    st.dataframe(results_df)

    csv = results_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Télécharger les résultats (CSV)",
        data=csv,
        file_name=f"predictions_prime_{prime}_taux_{interest_rate}.csv",
        mime="text/csv"
    )
else:
    st.error("Impossible de calculer les valeurs pour cette combinaison de prime et de taux.")
