# Buste des modèles féminins — deux boules de 60 cubes, textures repeintes

> Modification « troll » du fork, **2ᵉ version**. Version 1 : le cube de poitrine était
> remplacé par **8 bandes plates** — ça marchait, mais le rendu restait raisonnable. Cette
> version 2 reconstruit le buste en **deux boules** (chaque lobe = 5 bandes × 6 anneaux
> concentriques = 30 cubes), avec un **vrai sillon** au milieu, une **saillie de 10,4 px**
> (contre 3,7 px avant, 1,7 px dans MineColonies) et une **largeur de 12 px pour un torse
> de 8** : les seins débordent du corps. La zone de texture est repeinte en **une seule
> couleur**, pour qu'aucune couture ne soit possible entre les 60 cubes.

![Avant / après](documentation/female_models_bust/avant_apres.png)

---

## 1. Résumé

| | |
|---|---|
| **Ce qui a changé** | La pièce `"breast"` des 40 modèles féminins adultes n'est plus un empilement de 8 bandes : chaque côté est une **boule** construite en 5 bandes × 6 anneaux, les deux lobes étant **séparés par un sillon de 1,1 à 1,35 px** (géométrique, pas dessiné). |
| **Taille** | Saillie **10,37 px** devant la face avant du torse (= 0,65 bloc), largeur **12,0 px** (le torse en fait 8), hauteur **6,85 px**. Soit **×2,8** sur la saillie par rapport à la version 1, **×6** par rapport à MineColonies. |
| **Rond** | Deux profils, pas un : la bande du haut et celle du bas mesurent 57 % de la largeur et de la saillie de celle du milieu (`V(t) = √(1−(t/Rv)²)`) → silhouette arrondie **vue de profil** ; les anneaux se rétrécissent vers la pointe → silhouette arrondie **vue de dessus**. Vu de face, les anneaux concentriques produisent l'anneautage d'une sphère (voir § 2.3). |
| **Séparé en 2** | Les deux lobes ne sont plus deux moitiés d'un même cube : ils sont écartés, et leurs faces intérieures (faces latérales, donc naturellement plus sombres dans le moteur de rendu de Minecraft) forgent l'ombre du sillon. |
| **Textures** | `textures/entity/citizen/<style>/*female*.png`, 1 720 fichiers : le rectangle 22×6 px échantillonné par le buste est uniformisé à **une seule couleur**, calculée depuis le fichier (donc par métier et par carnation). |
| **Le réglage** | Toujours une ligne : `BREAST_DEFORMATION` dans `CitizenModel.java` — mais désormais sur l'axe **z seulement** (0,35 retenu, plage utile 0 → 1,4), parce que c'est le seul axe qui allonge sans étirer la texture. |
| **Non touché** | `FemaleChildModel`, les modèles masculins, les pillards, les animations, tous les autres pixels des textures (**0 pixel modifié hors du rectangle**, vérifié par diff). |

Les trois états du buste :

![Original, version 1, version 2](documentation/female_models_bust/trois_etats.png)

---

## 2. Où changer quoi (3 endroits)

### 2.1 La taille — `CitizenModel.java`

`src/main/java/com/minecolonies/api/client/render/modeltype/CitizenModel.java`, ligne 37 :

```java
public static final CubeDeformation BREAST_DEFORMATION = new CubeDeformation(0.0F, 0.0F, 0.35F);
```

Les 60 cubes des 40 modèles utilisent cette constante : changer ces trois nombres change la
poitrine de tous les métiers d'un coup. Un `CubeDeformation` **gonfle** la boîte sur chaque
face ; grossir `z` n'étire **aucune** texture (la face avant garde sa taille en pixels, elle
est seulement plus loin), alors que grossir `x` ou `y` étire le motif et fait entrer le buste
dans les bras et dans le cou. D'où les deux zéros.

| `BREAST_DEFORMATION` | Saillie devant le torse | Largeur | Hauteur | Marge sous le cou | Derrière le dos |
|---|---|---|---|---|---|
| `(0.0F, 0.0F, 0.0F)` | 10,0 px | 12,0 px | 6,75 px | 1,95 px | sorti de 1,4 px |
| **`(0.0F, 0.0F, 0.35F)`** — retenu | **10,37 px** | **12,0 px** | **6,85 px** | **1,90 px** | rentré de 1,1 px |
| `(0.0F, 0.0F, 0.8F)` | 10,8 px | 12,0 px | 7,0 px | 1,83 px | rentré de 0,6 px |
| `(0.0F, 0.0F, 1.4F)` | 11,4 px | 12,0 px | 7,14 px | 1,75 px | **±0** (amorce de traversée) |
| pour rappel : version 1 | 3,70 px | 9,0 px | 7,59 px | 1,01 px | — |
| pour rappel : MineColonies | 1,74 px | 8,5 px | 4,78 px | 1,44 px | — |

Mesures prises sur le rendu réel du modèle (`tools/female_bust/verify_bust.py`, 1 unité =
1 px de texture = 1/16 de bloc ; 16 = un bloc, donc un carré du sol Minecraft). « Marge sous
le cou » = distance du point le plus haut du buste à la ligne du cou (`y = 0` dans le repère
du corps) — elle reste de presque 2 px, le cou et la tête ne sont jamais touchés. « Derrière
le dos » = position de la face la plus en arrière par rapport à la face arrière du torse
(`z = 2`) : au-delà d'environ 1,4, un sein se met à se voir **dans le dos**, ce qui serait un
vrai bug.

![Échelle des tailles](documentation/female_models_bust/comparatif_tailles.png)

Pour revenir à un buste raisonnable sur **un seul** métier, on remet
`new CubeDeformation(0.0F)` dans les `addBox` de ce fichier ; pour le faire disparaître
complètement, on supprime l'instruction `breast`.

### 2.2 La forme — les 40 `Female*Model.java`

`src/main/java/com/minecolonies/core/client/model/`. Dans MineColonies (révision importée
`75a3c0a`), l'instruction est un cube plat et son double « couche vêtement » :

```java
PartDefinition breast = bipedBody.addOrReplaceChild("breast", CubeListBuilder.create()
    .texOffs(64, 49).addBox(-3.0F, 1.8938F, -5.716F, 8.0F, 3.0F, 3.0F, new CubeDeformation(0.0F))
    .texOffs(64, 55).addBox(-3.0F, 1.8938F, -5.716F, 8.0F, 3.0F, 3.0F, new CubeDeformation(0.25F)),
    PartPose.offsetAndRotation(-1.0F, 3.0F, 4.0F, -0.5236F, 0.0F, 0.0F));
```

et après cette modification (début de l'instruction dans `FemaleCitizenModel.java`, sur 60 lignes) :

```java
PartDefinition breast = bipedBody.addOrReplaceChild("breast", CubeListBuilder.create()
  .texOffs(64, 49).addBox(-2.099F, 0.0313F, -7.156F, 1.767F, 1.2F, 3.164F, BREAST_DEFORMATION)
  .texOffs(64, 49).addBox(4.132F, 0.0313F, -7.156F, 1.767F, 1.2F, 3.164F, BREAST_DEFORMATION)
  .texOffs(64, 49).addBox(-2.824F, 0.0313F, -8.556F, 2.616F, 1.2F, 1.384F, BREAST_DEFORMATION)
  .texOffs(64, 49).addBox(5.208F, 0.0313F, -8.556F, 2.616F, 1.2F, 1.384F, BREAST_DEFORMATION)
  ... 56 lignes de plus ...
  PartPose.offsetAndRotation(-1.0F, 3.0F, 4.0F, -0.14F, 0.0F, 0.0F));
```

Comment ces 60 nombres sont produits — c'est **un seul tableau de paramètres**, dans
`tools/female_bust/bust_shape.py` (et c'est là qu'on change la **forme**, pas dans les 40
fichiers Java) :

```python
rings      = ((3.10, 1.50), (4.60, 2.90), (5.40, 4.90),
              (5.20, 6.90), (4.10, 8.60), (2.20, 9.90))   # (largeur, saillie) par anneau, du torse vers la pointe
nbands     = 5 ; band_h = 1.20 ; band_step = 1.12          # hauteur d'une bande, et son pas
radius_v   = 2.75                                          # rayon vertical d'un lobe
cleavage   = 1.10 ; cleavage_step = 0.05                    # le sillon, ouvert anneau par anneau
back       = 2.2                                            # ancrage de l'anneau de base dans le torse
ring_eps   = 0.14 ; tilt = -0.14 rad (-8°)
```

Les règles qui fabriquent les boîtes, et pourquoi :

* **un anneau = une boîte** posée devant le précédent, centrée sur le lobe : la largeur suit
  une ellipse (`rangs de 3,1 → 5,4 → 2,2 px`), donc la vue de dessus est ronde. L'anneau
  suivant commence 0,14 px **avant** la face arrière du précédent : deux faces parfaitement
  coplanaires clignoteraient (z-fighting) — c'est la règle n° 1 de ce modèle.
* **une bande = une hauteur de 1,20 px pour un pas de 1,12**, donc 0,08 px de recouvrement
  vertical : encore une fois jamais deux faces coplanaires, et aucune fente entre les bandes.
* **`V(t) = √(1 − (t/2,75)²)` multiplie à la fois la largeur et la saillie** de la bande : les
  deux bandes extrêmes font 57 % de celle du milieu, ce qui donne la boule vue de profil.
  Comme la saillie suit la largeur, l'anneautage vu de face reste des cercles concentriques.
* **seul l'anneau de base est confiné dans la largeur du torse** (3,10 + 1,10/2 → bord à
  `|x| = 3,65`, alors que les bras commencent à 3,75) : c'est le seul dont la boîte rentre dans
  le torse, donc le seul qui pourrait traverser un bras et y laisser paraître une bande de
  texture. Les 24 anneaux suivants (`verify_bust.py` les compte, colonne `wide`) sortent
  jusqu'à `|x| = 6,0` **sans bug** : leur `z` reste ≤ −2,9, très devant les bras (qui occupent
  `z −2,25..2,25`) → ils les masquent, au lieu de les découper. C'est ce qui permet un buste
  plus large que le corps ; élargir l'anneau de base, même de 1,5 px, fait immédiatement
  apparaître 6 boîtes dans le volume des bras.
* **`PartPose.offsetAndRotation(-1.0F, 3.0F, 4.0F, -0.14F, 0, 0)`** — l'inclinaison passe de
  −30° (la version 1 utilisait −25°) à **−8°**. Une grosse poitrine pointe vers l'avant, pas
  vers le plafond ; et surtout la rotation fait **remonter** tout point éloigné (à −25°, une
  face avant à 10 px d'ici se retrouve ~4 px plus haut) : mesuré, avec la forme actuelle et
  l'ancienne inclinaison, le haut du lobe finirait à `y = −1,87`, c'est-à-dire **dans la tête**.
  Un `tilt` positif (pendouillant) est aussi testé et écarté : il repousse l'ancrage vers
  l'arrière (`arm` passe à 2) et fait frôler la ceinture.
* **le pivot et le centre viennent du fichier lu**, pas d'une constante : `FemaleCourierModel`
  a son cube à `y = 2.2938F` avec un pivot à `−9.0F`, `FemaleAlchemistModel` écrit son
  instruction sur trois lignes. Le script relit l'ancienne géométrie et retrouve le repère du
  cube d'origine (`cx = 1,0`, `cy = 3,3938`, `front0 = −5,716`) — c'est ce qui rend l'outil
  **idempotent** et capable d'enchérir sur la version 1 (`LAY_V1` dans `rework_bust.py`).

Il n'y a **aucune limite de Minecraft** sur la taille d'une boîte d'entité (les 16 px maxi
concernent les blocs, pas les cubes d'un `ModelPart`) : la seule borne est celle de la texture
du § 2.3, et elle est vérifiée modèle par modèle.

### 2.3 Les textures — `tools/female_bust/paint_textures.py`

Le rectangle échantillonné par les 60 cubes est `x 64..85, y 49..54` (22×6 px sur les textures
128×64, 44×12 sur les 256×128 de certains styles). Il faut **15,1 × 5,0 px** au total
(`Bust.uv_need()`), donc tout tient dans ce rectangle : **aucune face d'aucun modèle ne peut
regarder un pixel d'un autre morceau du corps**, ce qui était la source des pixels parasites de
la version d'origine.

Sur les 1 720 textures féminines des 8 styles (`default`, `modern`, `medieval`, `hellenic`,
`eastasian`, `nordic`, `nether`, `undead`), pour chaque fichier :

1. le contenu de l'ancienne couche « vêtement » (`y 55..60`) est **recombiné** dans le
   rectangle quand il est réellement peint (583 fichiers sur 1 720 : tabliers, gilets,
   plastrons) — c'est lui qui donnait la couleur visible sur la poitrine ;
2. les 6 lignes sont remplacées par **la même couleur** : la médiane des couleurs que le
   fichier avait déjà sur la fenêtre de la face avant, étalée sur toute la largeur ;
3. par-dessus, la rampe `RAMP` (`1,10 / 1,05 / 1,00 / 0,94 / 0,88 / 0,80` sur les lignes
   49 → 54) — légère, pour ne pas redessiner ce que la géométrie dit déjà.

Le point important : une boîte à `texOffs(64, 49)` échantillonne sa face avant à la
`ligne 49 + profondeur`. Or la profondeur d'un anneau = l'épaisseur qu'il reste entre sa face
avant et l'anneau précédent : l'anneau **collé au torse** est le plus épais (4,2 px → lignes
basses, sombres), celui **au sommet de la boule** le plus fin (1,1 px → lignes hautes,
claires). Un aplat de boule, avec un éclairage qui décroît du centre vers le bord, **sans
qu'aucun pixel ne dépende d'un étirement** — la rampe ne fait qu'accentuer ce que l'index de
ligne fournit déjà.

C'est aussi pour ça que la couleur est passée de « une par ligne » (v1) à « une seule » : avec
une vraie volumétrie, les nuances du vêtement dans le rectangle ne faisaient plus que souligner
les marches entre les anneaux.

![Zone de texture avant / après](documentation/female_models_bust/textures.png)

Les fichiers en mode palette (`P`, 692 d'entre eux) sont écrits en `RGBA`, leur palette ne
contenant pas les nuances de la rampe. Minecraft charge les deux de la même façon.

---

## 3. Outils ajoutés (`tools/female_bust/`)

| Script | Rôle |
|---|---|
| `bust_shape.py` | **Les paramètres de la forme** : `Bust(rings, nbands, radius_v, cleavage, tilt, …)`, le calcul des 60 boîtes (`cells()`), l'empreinte de texture (`uv_need()`). C'est le seul fichier à éditer pour changer la silhouette. |
| `rework_bust.py` | Applique `Bust` aux 40 modèles (réécrit l'instruction `"breast"`, met à jour la constante et son javadoc). Idempotent ; `--check-only` affiche le repère lu dans chaque fichier. |
| `bust_paint.py` + `paint_textures.py` | Les couleurs, la rampe, `flat=True`/`--ramp`, et l'application aux 1 720 textures (`--only default`, `--dry-run`). C'est là qu'on change l'**ombrage**. |
| `verify_bust.py` | Le contrôle qualité (§ 4) : cou, ceinture, dos, bras, UV, intersections avec les autres pièces — sur les 40 modèles. `--syntax` parse les 41 fichiers avec `javalang`. |
| `sheet.py` | Planche d'essais : rend une liste de `Bust` candidats (front / profil / 3-4) avec la texture repeinte, et mesure chaque candidate. C'est comme ça que la forme a été choisie. |
| `chest_closeup.py` | Zoom sur la poitrine de quelques métiers, pour l' chasse aux artefacts avec les accessoires (tabliers, lanières, potions). |
| `proto.py`, `render_compare.py`, `make_docs.py` | Atelier de conception v1, rendus avant/après depuis une révision git, et régénération des PNG de ce dossier. |

Pour tout refaire de zéro après avoir changé un paramètre :

```bash
python3 tools/female_bust/rework_bust.py          # les 40 modèles  (numpy + pillow seulement)
python3 tools/female_bust/paint_textures.py       # les 1 720 textures
python3 tools/female_bust/verify_bust.py          # les contrôles du § 4
python3 tools/female_bust/make_docs.py             # les images de ce dossier
```

Le rendu passe par `tools/model_preview/render_citizen_model.py` (petit moteur logiciel écrit
pour ce fork) ; il comprend les `CubeDeformation` à trois axes et lit les constantes d'un autre
fichier avec `--constants-from`.

---

## 4. Vérifications

* **Syntaxe** : les 40 `Female*Model.java` + `CitizenModel.java` passés au parseur Java
  `javalang` → **41 fichiers, 0 erreur**. Le mécanisme (une constante `public static final` de
  la classe de base, référencée dans les `addBox`) est exactement celui de la version 1, qui
  compile chez vous.
* **Géométrie, les 40 modèles** (`verify_bust.py`) : `40 models: 0 with a geometry/UV problem` —
  marge sous le cou ≥ 0,5 px (réel : 1,90), bas du buste ≤ 10,5 (réel : 8,75), aucune boîte
  derrière le torse (`backz = −1,07`, c'est-à-dire 1,07 px de marge), **0 boîte dans le volume
  des bras**, et **0 hors-limites UV** sur les 60 cubes de chaque modèle. Les 40 affichent les
  mêmes nombres (`tip=10.37 halfx=6.0 wide=24 arm=0 uv=0 ok`), sauf la coursière
  (`top_y=2.3`) décalée de 0,4 px comme son modèle.
* **Test négatif** (pour que ces zéros veuillent dire quelque chose) : élargir l'anneau de base
  à 4,6 px fait immédiatement passer `arm` à 6 ; 8 bandes au lieu de 5 font passer la marge
  sous le cou à 0,79. Les compteurs réagissent donc bien aux vrais problèmes.
* **Intersections assumées** : 20 modèles voient une autre de leurs pièces (tablier, lanière,
  sac, potions, faux, carte) entrer dans le volume d'un lobe. C'est le vêtement qui traverse le
  sein, pas l'inverse : le moteur de rendu dessine la face la plus proche, donc la lanière passe
  **devant** ou **derrière** selon son `z`, sans couture qui clignote. C'est le seul type
  d'artefact visible sur les rendus agrandis (`chest_closeup.py`), et il est voulu.
* **Périmètre des textures** : diff pixel par pixel contre la révision précédente sur les
  1 720 fichiers → **218 064 pixels modifiés, 0 en dehors du rectangle du buste**
  (`x 64..85, y 49..54` × l'échelle du fichier).
* **Idempotence** : `rework_bust.py` relancé deux fois produit un fichier strictly identique
  (`--check-only` affiche `[deja reecrit]` sur les 40).

Ce qui est connu et assumé, en plus des intersections ci-dessus :

* quand un citoyen **marche**, ses bras balancent de ±43° et traversent le volume des lobes :
  à cette saillie c'est inévitable (le bras balaie `z = −4,9` au niveau du buste), et c'est le
  comportement habituel de tout modèle à poitrine proéminente dans Minecraft ;
* la **chevalière** garde le comportement d'origine : son buste est masqué quand elle porte un
  plastron (`body.getChild("breast").visible = !entity.hasItemInSlot(CHEST)`) — avec la
  géométrie v2, cela fait le torse *entièrement* lisse, ce qui contraste beaucoup plus ;
* les textures « skin joueur » personnalisées (`customTextureUUID`) ne contiennent rien
  d'exploitable à ces coordonnées UV — c'était déjà le cas avant cette modif ;
* les fichiers palette sont réécrits en `RGBA` et recompressés au passage : le poids total des
  1 720 textures passe de 12,0 MiB (MineColonies) à 8,1 MiB (version 1) puis **8,0 MiB** ici —
  un aplat d'une seule couleur se comprime très bien ; aucun fichier ne dépasse 13,2 Ko.

---

## 5. Passer du code au jar Minecraft

**Attention au piège du zip** : le bouton « Code → Download ZIP » de la page du dépôt
télécharge la branche par défaut `main`, qui ne contient que le README. Le code est sur
`arena/f86d8630-minecolo` :

```bash
git clone -b arena/f86d8630-minecolo https://github.com/YannisSchmidt/minecolo.git
# ou, sans git :
curl -LO https://github.com/YannisSchmidt/minecolo/archive/refs/heads/arena/f86d8630-minecolo.zip
```

Prérequis : **un JDK 21** (par ex. Temurin 21, `java -version` doit répondre `21.x`),
4 Go de RAM dispo et une connexion internet — Gradle 8.13 est fourni par `gradlew`,
rien d'autre à installer. Le build n'a pas besoin du dépôt git (la fonction
`GitInformation` n'est pas activée dans ce projet), les traductions/datagen sont déjà
dans l'arbre, et aucun jeton Crowdin n'est requis (les tâches correspondantes ne sont
câblées que si la propriété est définie).

```bash
cd minecolo
./gradlew build            # Windows : gradlew.bat build
```

La première exécution télécharge NeoForge, les mappings et les dépendances (5 à 15 min).
Le mod installable est :

```
build/libs/minecolonies-0.0.11-1.21.1.jar
```

(le nom vient de `modId` + `modVersion` + version MC du `gradle.properties` ; ignorer les
fichiers `-sources`, `-dev`, `-javadoc`). Pour un nom plus parlant dans la liste des mods
de Minecraft :

```bash
./gradlew build -PmodVersion=1.1.1399 -PmodVersionSuffix=troll
# -> build/libs/minecolonies-1.1.1399-1.21.1-troll.jar
```

Installation : ce jar dans `.minecraft/mods/` (Windows : `%appdata%\.minecraft\mods`),
avec **NeoForge 21.1.x pour Minecraft 1.21.1** et les mods dont dépend MineColonies
(pour 1.21.1 : Structurize, BlockUI, MultiPiston, Domum Ornamentum, TownTalk). Sans ces
dépendances le jeu refuse de démarrer le mod. En cas d'erreur mémoire, augmenter
`org.gradle.jvmargs` dans `gradle.properties` (`-Xmx6G`) ; en cas de plainte des tests,
`./gradlew build -x test`.

Le rendu des citoyens est **côté client** : c'est le jar du client qui dessine les modèles
(et qui filme). En solo, le dossier `mods` de ce client suffit. Si le monde tourne sur un
serveur, le serveur doit avoir MineColonies aussi — le plus simple est d'y mettre le même
jar modifié ; la version n'ayant pas changé, un client avec le fork et un serveur avec le
mod officiel se reconnaissent quand même (le `serverSideVersionCheck` compare la chaîne de
version, inchangée ici).

### Réutiliser les outils de ce fork

Les scripts de `tools/female_bust/` (régénération des 40 modèles, repeinte des textures,
contrôles, rendus de comparaison) tournent hors de Gradle, avec juste Python + Pillow + NumPy :

```bash
pip install pillow numpy javalang
python3 tools/female_bust/rework_bust.py       # applique bust_shape.Bust aux 40 modèles
python3 tools/female_bust/paint_textures.py    # repeint la zone du buste (1 720 textures)
python3 tools/female_bust/verify_bust.py       # cou / dos / bras / UV / intersections + --syntax
python3 tools/female_bust/sheet.py             # compare des formes avant de décider
python3 tools/female_bust/chest_closeup.py     # zoom métier par métier
python3 tools/female_bust/make_docs.py         # régénère les PNG de documentation
```
