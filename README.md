# Plateforme SaaS pour les Agents de Sourcing

## Description

Cette plateforme SaaS permet aux agents de sourcing freelance de gérer leurs contacts fournisseurs, de créer et gérer des documents RFI/RFQ, et de suivre des indicateurs clés de performance (KPI) via un tableau de bord. Le MVP utilise Streamlit pour l'interface utilisateur et Firebase pour la gestion des données.

## Fonctionnalités

1. **Gestion des Contacts Fournisseurs**
   - Ajouter, modifier, supprimer et afficher les fournisseurs.
2. **Gestion des Documents RFI/RFQ**
   - Créer, modifier, supprimer et afficher des documents RFI (Request for Information) et RFQ (Request for Quotation).
3. **Tableau de Bord - KPI**
   - Afficher des KPI clés comme le nombre total de fournisseurs, RFIs, et RFQs.

## Technologies Utilisées

- [Streamlit](https://streamlit.io/) : Pour la création de l'interface utilisateur.
- [Firebase](https://firebase.google.com/) : Pour la gestion de la base de données.
- [Python](https://www.python.org/) : Langage de programmation principal.

## Prérequis

- Python 3.x installé sur votre machine.
- Un compte Firebase et un projet configuré avec l'Admin SDK.
- Les bibliothèques Python requises (voir ci-dessous).

## Installation

1. Clonez le dépôt :

    ```bash
    git clone https://github.com/votre-utilisateur/votre-repo.git
    cd votre-repo
    ```

2. Installez les dépendances requises :

    ```bash
    pip install -r requirements.txt
    ```

3. Configurez Firebase :

    - Ajoutez votre fichier de configuration `firebase_config.json` dans le répertoire du projet.

4. Exécutez l'application Streamlit :

    ```bash
    streamlit run app.py
    ```

## Utilisation

### Accueil

Sur la page d'accueil, vous trouverez une brève introduction et description de la plateforme.

### Gestion des Contacts

- Accédez à la section "Gestion des Contacts" dans le menu de navigation.
- Utilisez le formulaire pour ajouter de nouveaux fournisseurs.
- Affichez la liste des fournisseurs enregistrés.

### Documents RFI/RFQ

- Accédez à la section "Documents RFI/RFQ" dans le menu de navigation.
- Sélectionnez le type de document (RFI ou RFQ).
- Utilisez le formulaire pour ajouter de nouveaux documents.
- Affichez la liste des documents enregistrés.

### Tableau de Bord - KPI

- Accédez à la section "Tableau de Bord" dans le menu de navigation.
- Consultez les KPI clés pour suivre la performance des activités de sourcing.

## Contribuer

Les contributions sont les bienvenues ! Veuillez soumettre une pull request ou ouvrir une issue pour toute suggestion ou amélioration.

## License

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## Auteurs

- **Votre Nom** - *Développeur Principal* - [Votre Profil](https://github.com/votre-utilisateur)

## Remerciements

- Merci à la communauté Streamlit et Firebase pour leurs excellentes documentations et supports.
