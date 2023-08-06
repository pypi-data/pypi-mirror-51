# DéclaTravaux

DéclaTravaux est un utilitaire de télétransmission des déclarations de projet de travaux (DT), des déclarations d'intention de commencement de travaux (DICT) et des avis de travaux urgents (ATU).

Le logiciel, développé dans le langage Python, est disponible sous la licence libre CeCILL (http://www.cecill.info/).

## Contexte

Lorsque des travaux sont envisagés à proximité de réseaux ou canalisations, le maître d'ouvrage et/ou l'exécutant des travaux doit déclarer ce projet de travaux aux exploitants des réseaux concernés.

Pour ce faire, il doit obligatoirement consulter la plateforme http://www.reseaux-et-canalisations.ineris.fr/ : le déclarant y indique l'emprise géographique des travaux prévus, et, en retour, le téléservice lui propose de télécharger une archive contenant les déclarations à souscrire auprès des différents exploitants concernés.

Il appartient ensuite au déclarant d'envoyer par courriel les différentes déclarations ainsi téléchargées aux exploitants identifiés.

## Objet du logiciel

Le présent logiciel a pour objet d'automatiser l'envoi par courriel des différentes déclarations.

Par un traitement de l'archive issue du téléservice, il extrait les informations relatives aux exploitants concernés et à leurs coordonnées, et procède à l'envoi des déclarations correspondant à chacun d'eux.

## Utilisation

Lors du premier lancement du logiciel, il convient de renseigner les informations suivantes (bouton `Paramètres`) :
* Configuration :
    * Répertoire de recherche : répertoire dans lequel le logiciel va automatiquement rechercher les archives issues du téléservice ;
    * Repertoire de traitement : répertoire dans lequel les archives sont conservées après avoir été traitées.
* Courriels :
    * Adresse électronique : adresse éléectronique utilisée pour envoyer les déclarations aux exploitants ;
    * Mot de passe : mot de passe de connexion au serveur SMTP correspondant à l'adresse électronique ;
    * Adresse du serveur SMTP ;
    * Port du serveur SMTP ;
    * Nom de l'expéditeur : identité utilisée en signature des courriels.

Une fois ces informations renseignées, le logiciel va automatiquement rechercher des archives ZIP téléchargées sur le téléservice ; s'il n'en détecte aucune, il propose à l'utilisateur de sélectionner manuellement une archive.

Une fois le choix de l'archive confirmé par l"utilisateur, le logiciel :
1. extrait les informations relatives aux exploitants contenues dans l'archive (notamment dans le fichier « *_description.xml ») ;
2. associe à chaque exploitant la déclaration correspondante (au format PDF) ;
3. se connecte au serveur de messagerie de l'utilisateur ;
4. envoie un courriel à chaque exploitant, contenant en pièce jointe les fichiers requis ;
5. envoie un courriel récapitulatif à l'utilisateur, confirmant l'envoi des différents courriels.

## Bibliothèques tierces / Dépendances

Le logiciel utilise les bibliothèques tierces suivantes :
* keyring, disponible sous les licences MIT et PSF (https://github.com/jaraco/keyring) ;
* PyPDF2, écrite par la société [Phaseit](http://phaseit.net/), disponible sous la licence BSD modifiée (http://mstamy2.github.io/PyPDF2/) ;
* PyQt5, disponible sous la licence GPL (https://www.riverbankcomputing.com/software/pyqt/).