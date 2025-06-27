🏆 أفضل 5 قواعد حسب الأداء (وفق نتائج التجربة):
في التوزيع التسلسلي (Serial Allocation):

| الترتيب | القاعدة    | الأداء (أقل زيادة في مدة المشروع) |
| ------- | ---------- | --------------------------------- |
| 🥇 1    | **LST**    | الأفضل في معظم الحالات            |
| 🥈 2    | **HRPW\*** | قوية عند موارد متعددة             |
| 🥉 3    | **LFT**    | فعالة جدًا أيضًا                  |
| 🏅 4    | **MTS**    | متقدمة في بعض الحالات             |
| 🏅 5    | **MIS**    | أداء جيد في بعض السيناريوهات      |


في التوزيع المتوازي (Parallel Allocation):

| الترتيب | القاعدة         | الأداء                     |
| ------- | --------------- | -------------------------- |
| 🥇 1    | **LFT**         | الأفضل عمومًا              |
| 🥈 2    | **LST**         | أداء ممتاز                 |
| 🥉 3    | **HRPW\***      | ضمن الثلاثة الأوائل غالبًا |
| 🏅 4    | **MTS**         | قوية مع تعدد الموارد       |
| 🏅 5    | **HRU1 / HRU2** | جيدة في الشبكات المعقدة    |



🏆 TOP 10 – Moyenne des performances sur tous les cas :

| 🥇 Rang | Règle      | Code     | Pourquoi elle est dans le top                                                       |
| ------- | ---------- | -------- | ----------------------------------------------------------------------------------- |
| 1       | **HRPW\*** | `HRPW*`  | La **meilleure performance globale**, surtout avec ressources limitées et 10 types. |
| 2       | **LST**    | `LST`    | Très robuste, surtout en allocation sérielle.                                       |
| 3       | **LFT**    | `LFT`    | Excellente en allouation parallèle, souvent n°1.                                    |
| 4       | **MTS**    | `MTS`    | Performante dans presque tous les scénarios.                                        |
| 5       | **TIMROS** | `TIMROS` | Très bonne dans les cas complexes, équilibre temps/ressources.                      |
| 6       | **HRU1**   | `HRU1`   | Très efficace avec plusieurs types de ressources.                                   |
| 7       | **TIMRES** | `TIMRES` | Variante de TIMROS, aussi performante.                                              |
| 8       | **HRU2**   | `HRU2`   | Robuste dans la plupart des scénarios.                                              |
| 9       | **STFD**   | `STFD`   | Performante dans des cas spécifiques.                                               |
| 10      | **EFT**    | `EFT`    | Simple et efficace dans les scénarios moyens.                                       |


🏆 Top 10 des règles de priorité (ordonnées par performance globale)


| 🔢 Rang | Nom de la règle                      | Abréviation | Description simplifiée                                                          |
| ------- | ------------------------------------ | ----------- | ------------------------------------------------------------------------------- |
| 1️⃣     | **Highest Rank Positional Weight 2** | `HRPW*`     | Tient compte du poids des successeurs totaux (plus performant globalement).     |
| 2️⃣     | **Late Start Time**                  | `LST`       | Priorise les activités avec le début tardif le plus bas.                        |
| 3️⃣     | **Late Finish Time**                 | `LFT`       | Choisit l'activité avec la fin la plus tôt possible sans retarder le projet.    |
| 4️⃣     | **Maximum Total Successors**         | `MTS`       | Priorise les tâches avec le plus de successeurs au total.                       |
| 5️⃣     | **TIMROS**                           | `TIMROS`    | Heuristique basée sur le ratio du temps et de la disponibilité des ressources.  |
| 6️⃣     | **Highest Resource Utilization 1**   | `HRU1`      | Tient compte de l'utilisation cumulée des ressources sur les chemins critiques. |
| 7️⃣     | **TIMRES**                           | `TIMRES`    | Variante de TIMROS avec une formule de pondération différente.                  |
| 8️⃣     | **Highest Resource Utilization 2**   | `HRU2`      | Similaire à HRU1 mais pondéré par la durée des tâches.                          |
| 9️⃣     | **Smallest Dynamic Total Float**     | `STFD`      | Priorise les tâches avec le moins de marge dynamique.                           |
| 🔟      | **Early Finish Time**                | `EFT`       | Choisit les tâches qui finissent le plus tôt (simple mais efficace).            |



