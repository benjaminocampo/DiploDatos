# %%
import numpy as np
import pandas as pd
import statsmodels.stats.api as sms

URL = "https://cs.famaf.unc.edu.ar/~mteruel/datasets/diplodatos/sysarmy_survey_2020_processed.csv"
DB = pd.read_csv(URL)

# random variables
salary_monthly_NETO = "salary_monthly_NETO"
profile_gender = "profile_gender"

df = DB[[salary_monthly_NETO, profile_gender]]

df.groupby(profile_gender).describe()

alpha = 0.05

is_man = df.profile_gender == 'Hombre'

groupA = df[(df[salary_monthly_NETO] > 1000) & is_man][salary_monthly_NETO]
groupB = df[(df[salary_monthly_NETO] > 1000) & ~is_man][salary_monthly_NETO]

# %%
groupA

# %%
groupB

# %% [markdown]
# ## Estimación Puntual
# Consideramos las variables aleatorias $X_A$ y $X_B$, salario neto de los
# hombres (**groupA**), y el salario neto de las mujeres y otros (**groupB**)
# respectivamente. El estimador $\hat{\theta}$ que vamos a utilizar es $\overline{X_A} -
# \overline{X_B}$. Por lo tanto la estimación puntual obtenida es:
# %%
groupA.mean() - groupB.mean()

# %% [markdown]
# Notar que la diferencia de las medias del salario de ambos de grupos es de
# \$23262. A su vez podemos ver de cuanto es esta diferencia relativo al salario
# medio del grupo A:

# %% 
(groupA.mean() - groupB.mean()) / groupA.mean() * 100
# %% [markdown]
# Esto nos dice que el grupo de hombres cobran casi un 23% más del salario neto que el conformado por las mujeres y otros.

# %% [markdown]
# Aparte de reportar la estimación puntual se calculo el error estandar como una
# medida de precisión del estimador, es decir,
# 
# $\sqrt{Var(\hat{\theta})} =
# \sqrt{Var(\overline{X_A} - \overline{X_B})} = \sqrt{Var(\overline{X_A}) +
# Var(\overline{X_B}))} =  \sqrt{\frac{\sigma_A^{2}}{n_A} +
# \frac{\sigma_B^2}{n_B}}$
#
# %%
np.sqrt(groupA.std()**2 / groupA.size + groupB.std()**2 / groupB.size)
# %% [markdown]
# Notar que la diferencia de las medias del salario de ambos de grupos es de
# \$23262 con un error de estimación de alrededor de los \$2400, es decir, que
# la estimación realizada tiene un bajo desvío, lo cual nos indicaría que tiene
# buena precisión probablemente debido al gran tamaño de las muestras.

# %% [markdown]
# ## Intervalo de Confianza para $\mu_A - \mu_B$
# Ahora compararemos la estimación puntual obtenida con la de un intervalo de
# confianza cuyo nivel de significancia es de $1 - \alpha = 0.95$. El
# estadistico utilizado es $\frac{\overline X_A - \overline X_B - \mu_A -
# \mu_B}{\sqrt{{\frac{S_A^2}{n_A} + \frac{S_B^2}{n_B}}}}$
#
# Ahora bien, como el tamaño de la muestra para el grupo A es de 4815 y el del
# grupo B de 891, por el TCL, el estadistico tiene distribución aprox. normal.
# Obteniendo el siguiente intervalo de confianza:
# %%
cm = sms.CompareMeans(sms.DescrStatsW(groupA), sms.DescrStatsW(groupB))
cm.zconfint_diff(alpha=alpha, usevar='unequal')
# %% [markdown]
# Con un 95% de confianza se espera que la diferencia de salarios medios entre
# el grupo A y B este comprendido entre \$18561 y \$27964. Es decir, si
# generamos sucesivos intervalos por medio de este estadistico, el 95% de ellos
# van a contener el parámetro. Entonces hay una chance del 95% de que el
# obtenido sea uno de esos intervalos.

# %% [markdown]
# Similarmente más allá del tamaño de la muestra, nuestro estadistico tiene
# distribución t-student y por ende también podemos realizar un análisis sin
# suponer normalidad. Aún aborando de esta manera obtenemos un resultado
# similar.
cm.tconfint_diff(alpha=alpha, usevar='unequal')
# %% [markdown]
# ## Tests de Hipótesis
# Para este caso querremos ver si podemos afirmar con una cierta significancia
# que el salario medio neto del grupo A es superior al del grupo B. Para ellos
# planteamos el siguiente test de hipótesis.
# 
# $H_0: \mu_A - \mu_B = 0$
#
# $H_a: \mu_A - \mu_B > 0$
#
# Nuestro estadistico a utilizar en este test es el mismo que para los
# intervalos de confianza. Suponemos inicialmente $H_0$, es decir que el salario
# medio de ambos grupos son iguales. Bajo $H_0$ el estadístico tiene:
#
#   - Distribución aprox. normal, considerando el tamaño de la muestra y el TCL.
#   - Distribución t-student.
#
#
# Por lo tanto procederemos a realizar tanto z como t tests para ver que
# para ambos tenemos resultados similares.
# Consideramos un nivel de significancia similar del 95% y suponiendo varianzas
# distintas de ambos grupos.

# %%
ztstat, zpvalue = cm.ztest_ind(alternative="larger", usevar="unequal")
(ztstat, zpvalue)
# %% [markdown]
# `ztstat` es el valor observado del estadistico y `zpvalue` es el p-valor
# obtenido. Luego para concluir con el test solo queda ver que:
#   
#   - Rechazar $H_0$ si $pvalue \leq \alpha$
#   - No rechazar $H_0$ si $pvalue \gt \alpha$
# %%
zpvalue <= alpha

# %% [markdown]
# Claramente el p-valor es menor por una gran diferencia y por ende afirmamos que
# con un 95% de confianza el salario medio del grupo A es mayor que el del B.

# %% [markdown]
# Si ahora realizamos el mismo test de hipotesis bajo la suposición de $H_0$ y
# distribución t-student por parte de nuestro estadistico, obtenemos:
# %%
ttstat, tpvalue, df = cm.ttest_ind(alternative="larger", usevar="unequal")

(ttstat, tpvalue, df)
# %% [markdown]
# Notar que el valor observado `ttstat` es el mismo que el anterior `ztstat`
# pues las expresiones de los estadisticos son las mismas. Lo que cambia es cual
# es la distribución a considerar durante el test y por ende los valores
# criticos para el calculo del pvalor. `df` Nos indica los grados de libertad
# utilizada en el test, recordar que a mayor grados de libertad, nuestro
# estadístico tendrá más similitud a una normal. Finalmente para concluir el
# test, también rechazamos $H_0$.

# %%
tpvalue <= alpha

# %%
