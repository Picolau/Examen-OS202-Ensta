import matplotlib.pyplot as plt

# Données pour la première courbe
x1 = [1, 2, 3, 4, 5, 6, 7, 8]  # Numéros de ligne
y1 = [0.710884, 0.524305, 0.339403, 0.218295, 0.290413, 0.247893, 0.226295, 0.160463]  # Temps de la première colonne

# Données pour la deuxième courbe
x2 = [1, 2, 3, 4, 5, 6, 7, 8]  # Numéros de ligne
y2 = [8.64069, 4.9916, 3.76827, 3.51655, 3.21293, 3.1036, 3.2686, 3.30863]  # Temps de la deuxième colonne

# Tracer les courbes
plt.plot(x1, y1, label='Generation de cellules')
plt.plot(x2, y2, label="Affichage des résultats")

# Ajouter un titre et des étiquettes d'axe
plt.title('Comparaison des temps')
plt.xlabel('Numéro de coeurs physiques')
plt.ylabel('Temps (s)')

# Ajouter une légende
plt.legend()

# Afficher le graphique
plt.show()