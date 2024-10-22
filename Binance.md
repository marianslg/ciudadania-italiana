# rambot
Es el nombre del programa/bot que quiero hacer para estudiar criptomonedas. Mi objetivo principal es poder 

# Objetivos:
* Predecir el precio de criptomonedas en tiempo real.

Para empezar, trabajé con BTCUSDT, pero tengo que poder escalar a consultar y predecir sobre cualquier moneda. Tambien la idea es que rambot pueda estudiar todas las monedas y encontrar oportunidades.

Tengo dos enfoques, uno historico y otro temporal (del ultimo periodo).
El primer enfoque me servira mas que nada para entender como se fue moviendo el precio por el tiempo. Saber como se comporto, cuanto es lo promedio que suba que baje, cual es el volumen promedio, etc.
El otro enfoque lo quiero para calcular indicadores, soportes y resistencias.

Para 


Quiero trabajar con el primer objetivo y tengo varias preguntas:
1. Es necesario descargar todo el historial de de velas de una criptomoneda?

Para ello debo resolver varias cosas:
* Descargar velas historicas de criptomonedas 

# Etapas del proceso:
1. Recopilación de datos.
2. Limpieza de datos.
3. Calculo de indicadores.
4. Mas etapas a definir.

## 1. Recopilación de datos:

### 1.1 Descarga de datos:
Los datos van a ser descargados de la API de binance y seran almacenados en un archivo en la base de datos sqlite.

[] 

La idea es crear un programa que descargue la informacion de velas de distintas criptomonedas y las guarde en un archivo csv. Hay dos tipos de descarga: historica o por rango.
La historica es la que se descarga la informacion de todas las velas de una criptomoneda. Esto sucede cuando no tenemos ya descargada la informacion de la criptomoneda.
La descarga por rango sucede cuando ya tenemos data historica de la criptomoneda y queremos completar las velas al dia de hoy.
Quizas hay una tercera descarga que es la de la ultima vela.

