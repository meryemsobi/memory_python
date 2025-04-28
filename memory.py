from graphics import *     # Importer graphics pour dessiner
import random              # Pour mélanger les cartes
import os                  # Pour gérer les chemins d'accès aux images

# Créer la fenêtre de jeu
win = GraphWin("Memory Foot", 800, 600)    # Fenêtre de taille 800x600

# Afficher l'image de fond (terrain de foot)
background = Image(Point(400, 300), os.path.join("images", "terrain.gif"))   # Image centrée
background.draw(win)     # Dessiner l'image de fond

# Liste des noms des joueurs (15 joueurs différents, chaque image 2 fois)
joueurs = [
    "messi.gif", "ronaldo.gif", "mbappe.gif", "neymar.gif", "barcola.gif",
    "halaand.gif", "vitinha.gif", "kante.gif", "griezmann.gif", "salah.gif",
    "doue.gif", "yamal.gif", "bellingham.gif", "ronaldinho.gif", "dembele.gif"
]

# Doubler les images pour avoir 30 cartes (2 fois chaque joueur)
images = joueurs * 2

# Mélanger les images pour les répartir au hasard
random.shuffle(images)

# Positions de chaque carte
cards = []            # Liste pour stocker chaque carte (rectangle, image, chemin image, révélé ou pas)
images_drawn = []     # Liste pour stocker les images dessinées

# Créer toutes les cartes
for i in range(30):
    col = i % 5               # Colonne (0 à 4)
    row = i // 5              # Ligne (0 à 5)
    x = 100 + col * 140       # Position x (plus d'espace entre les cartes)
    y = 80 + row * 90         # Position y (espace vertical correct)

    rect = Rectangle(Point(x-50, y-50), Point(x+50, y+50))    # Créer un rectangle 100x100
    rect.setFill("white")                                     # Couleur blanche face cachée
    rect.draw(win)                                            # Dessiner le rectangle

    img_path = os.path.join("images", images[i])    # Construire le chemin vers l'image
    img = Image(Point(x, y), img_path)              # Charger l'image
    images_drawn.append(img)                        # Ajouter l'image à la liste
    cards.append((rect, img, images[i], False))      # Stocker les données de la carte

# Fonction pour récupérer l'indice d'une carte cliquée
def get_clicked_card(x, y):
    for i in range(30):
        rect, img, name, revealed = cards[i]
        p1 = rect.getP1()     # Coin supérieur gauche
        p2 = rect.getP2()     # Coin inférieur droit
        if p1.getX() <= x <= p2.getX() and p1.getY() <= y <= p2.getY():
            return i          # Retourner l'indice si clic dans la carte
    return None               # Sinon rien

# Liste pour mémoriser les cartes sélectionnées
selected = []

# Compteur de paires trouvées
pairs_found = 0

# Boucle principale du jeu
while pairs_found < 15:     # Tant que toutes les paires ne sont pas trouvées
    click = win.getMouse()           # Attendre un clic de la souris
    x = click.getX()                 # Récupérer x du clic
    y = click.getY()                 # Récupérer y du clic

    card_index = get_clicked_card(x, y)    # Chercher quelle carte a été cliquée

    if card_index is not None and not cards[card_index][3]:   # Si carte valide et pas déjà révélée
        rect, img, name, _ = cards[card_index]
        img.draw(win)                 # Afficher l'image du joueur
        cards[card_index] = (rect, img, name, True)    # Marquer la carte comme retournée
        selected.append(card_index)   # Ajouter à la sélection

    if len(selected) == 2:   # Si 2 cartes sont retournées
        idx1, idx2 = selected
        if cards[idx1][2] == cards[idx2][2]:    # Si c'est la même image
            print("Paire trouvée !")            # Message dans la console
            pairs_found += 1                    # Ajouter une paire trouvée
        else:
            print("Pas de paire...")
            time.sleep(1)                       # Pause pour voir l'erreur
            for idx in selected:                # Remettre les cartes face cachée
                rect, img, name, _ = cards[idx]
                cards[idx] = (rect, img, name, False)
                img.undraw()                    # Enlever l'image affichée
        selected = []   # Réinitialiser la sélection

# Partie terminée : afficher un message de victoire
background.undraw()         # Retirer le terrain pour mieux voir les textes
win.setBackground("gold")   # Fond doré

# Afficher message de victoire
congrats = Text(Point(400, 250), "Bravo :)")  # Créer un objet texte avec le message "Bravo :)" au centre de la fenêtre (point (400, 250))
congrats.setSize(24)                          # Définir la taille du texte à 24 pixels
congrats.setTextColor("white")                # Définir la couleur du texte en blanc
congrats.draw(win)                            # Afficher le message dans la fenêtre de jeu

# Fin du jeu : attendre un dernier clic pour fermer
win.getMouse()                                # Attendre que l'utilisateur clique dans la fenêtre avant de fermer
win.close()                                   # Fermer la fenêtre du jeu après le clic

