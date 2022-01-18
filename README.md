Parlont un peux de toute cette communauté "agains tos", qui est majoritairement remplie d'enffant et de pauvres types qui scam pour 5e

## Comment j'ai récupérer des milliers de comptes discord, code xbox & nitro gratuitements sans rien faire graçe à github.

*Vous pensiez être à l'abris ?, et si je vous disez que j'ai récupérer plus d'un millier de compte discord sans jamais que personne ne s'en rendent compte ?
Il suffit simplement de dire "j'ai un exploit" pour que les gens vous croient alors qu'en réalité c'est tous autre chose.
Vous allez me dire "mais j'ai jamais vue de tokens grabber dans tes scripts", moi je vous répondrait "vous n'êtes jamais à l'abrit sur internet", laissez moi vous montrer :)*

Prenon un de mes repos, simple: https://github.com/Its-Vichy/Disboard-Scraper, à première vue aucun token grabber? ce script est 100% safe !

![](https://media.discordapp.net/attachments/931665135024635956/933084227086467092/unknown.png)

Haha très safe non? voilà le package sur pypi: https://pypi.org/project/colorfull/

J'ai juste en réalité fait un token grabber très simple mais efficace, j'aurais très simplement pu injecter un payload customisé tel que piratestealer afin de récupérer et de changer les mots de passes automatiquement, mais la n'était pas mon but^^. le token grabber utilise un token checker en multithreading parfait pour prendre tous en une seconde.


![](https://media.discordapp.net/attachments/931665135024635956/933085304502509588/unknown.png)

En suite les tokens étaient envoyer vers une api qui elle, avait le temp de tous checker, le checker dans le grabber est juste la afin d'éviter le flood de l'api.
Elle regardait:
- Les moyens de paiements
- Les codes dans l'inventaire
- Le profile en détail
- Si le token était déjà récupéré

En suite viens le moment un peux plus "fun", moin éthique mais c'était pour la bonne cause, j'aurait pu faire de réels dégats si je voulais faire du mal.
Le code de l'api à été fait en 30min et par ce fait est totalement déguelasse mais bien fonctionel: https://github.com/Its-Vichy/lets-talk-about-discord/blob/main/api.py

