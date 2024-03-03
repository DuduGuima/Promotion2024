# Stratégie

Bon, je vais utiliser 1 processeur pour faire la affichage et le reste va faire les calculs.
La division de calcul parmi plusieurs processeurs ne sera pas un probleme, puisque le calcul de la prochaine iteration (t+1) n'utilise que la grille ancienne (la grid du moment t). Ainsi, le calcul est independant et la communication entre chaque processeur de calcul est limitée(on fait un all gather juste pour mettre a jour la nouvelle grille). 

On crée deux communicators, un qui contient tous les processeurs, le 0 est qui va afficher les resultats, e um nouveau communicator, entre les processeurs de calcul. On pourrait utiliser un seul communicator et partager les calculs parmi tous les processeurs, mais je voulais apprendre un peu commment utiliser la creation d'autre communicator.


On choit alors le paradigm maitre-eclave juste par le fait que c'est une strategie que je n'avais pas compris e plus difficile d'appliquer, alors ç'était une façon de l'apprendre.






