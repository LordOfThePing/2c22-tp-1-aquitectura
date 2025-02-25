<details>
   <summary>Enunciado</summary>
   <br>

# Punto de partida para el TP 1 de Arquitectura del Software (75.73) del 2do cuatrimestre de 2022

> **La fecha de entrega para el informe y el código es el jueves 13/10** :bangbang:

La forma de entrega será crear un canal **privado** en Slack (llamado como el grupo) con todos los miembros del grupo y todos los docentes, y poner ahí un link al repositorio con el código (en caso de ser privado, invitar también a todos los docentes) y el informe (o avisar si está en el repositorio).

El informe puede ser un PDF, Google Doc o Markdown/Wiki en el mismo repositorio del código. **Debe** incluir screenshots del dashboard de métricas para cada caso analizado que permitan observar los resultados obtenidos.

## Objetivos

El objetivo principal es comparar algunas tecnologías, ver cómo diversos aspectos impactan en los atributos de calidad y probar, o al menos sugerir, qué cambios se podrían hacer para mejorarlos.
El objetivo menor es que aprendan a usar una variedad de tecnologías útiles y muy usadas hoy en día, incluyendo:

- Node.js (+ Express)
- Docker
- Docker Compose
- Nginx
- Algún generador de carga (la propuesta es usar Artillery, pero pueden cambiarlo)
- Alguna forma de tomar mediciones varias y visualizarlas, preferentemente en tiempo real, con persistencia, y en un dashboard unificado (la propuesta es usar el plugin de Artillery + cAdvisor + StatsD + Graphite + Grafana, pero pueden cambiarlo).

## Consigna

### Sección 1

Implementar un servicio HTTP en Node.js-Express. Someter distintos tipos de endpoints a diversas intensidades/escenarios de carga en algunas configuraciones de deployment, tomar mediciones y analizar resultados.

A partir de este repositorio como punto inicial, van a tener que implementar el webserver y dockerizarlo (completar la carpeta `app/`), agregar los servicios con el webserver y una imagen provista por la cátedra al `docker-compose.yml`, y configurar las locations y upstreams de nginx en `nginx_reverse_proxy.conf`.

La imagen provista por la cátedra es `arqsoft/bbox:202202.1`. Se trata de una aplicación ("bbox") que provee 2 servicios, uno con comportamiento sincrónico y otro con comportamiento asincrónico. Se configura a través del archivo `/opt/bbox/config.properties`, que ustedes deberán mapear vía un volumen a un archivo en el equipo host (caso similar a la configuración de nginx que les da la cátedra).

Este archivo tiene 2 parámetros:

```INI
server.basePort=9090
group.key=
```

- **server.basePort**: Puerto base para que escuchen los servicios *en el container*. En el ejemplo, el 1er servicio escuchará en 9090 y el 2do en 9091.
- **group.key**: Cadena alfanumérica que identifica al grupo. Se recomienda que utilicen el nombre del grupo, aunque pueden usar cualquier cadena.

El archivo que utilicen **debe ser subido al repositorio**.

Para _probar manualmente_ la interacción con los servicios, tienen 2 opciones:

- Mapear los puertos al host: Deben asignar un puerto del host a cada puerto del container
- Pasar a través de nginx: Deben agregar los upstreams en la configuración de nginx

Luego, pueden enviar un GET a cualquier endpoint de cada servicio. Por ejemplo, si mapearon los puertos al host con la misma numeración que el archivo de configuración:

- `curl http://localhost:9090/` accederá al 1er servicio
- `curl http://localhost:9091/` accederá al 2do servicio

Si, en cambio, eligieron pasar a través de nginx, entonces deberán enviar un GET a las locations que hayan configurado.

Ambos servicios devuelven la cadena "Hello, world!".

Para generar carga y ver las mediciones obtenidas, en la carpeta `perf/` tienen un dashboard de Grafana ya armado (`dashboard.json`) y un ejemplo de un escenario básico de artillery (**deben** crear sus propios escenarios de manera apropiada para lo que estén probando). También hay un script y una configuración en el `package.json` para que puedan ejecutar los escenarios que hagan corriendo:

```npm run scenario <filename> <env>```

donde `<filename>` es el nombre del archivo con el escenario (sin la extensión `.yaml`) y `<env>` es el entorno en el cual correrá la prueba (vean la sección `environments` dentro del yaml del escenario).

#### Tipos de endpoints para comparar los servidores

| Caso | Implementado como | Representa |
| ---- | ----------------- | ---------- |
| Ping | Respuesta de un valor constante (rápido y de procesamiento mínimo) | Healthcheck básico ||
| Proxy sincrónico | Invocación a servicio sincrónico provisto por la cátedra. | Aproximación a consumo de servicio real sincrónico. |
| Proxy asincrónico | Invocación a servicio asincrónico provisto por la cátedra. | Aproximación a consumo de servicio real asincrónico. |
| Intensivo | Loop de cierto tiempo (lento y de alto procesamiento) | Cálculos pesados sobre los datos (ej: algoritmos pesados, o simplemente muchos cálculos). |

#### Configuraciones de deployment

> **El tráfico entre cliente y servidor debe pasar por el nginx, para que tenga la latencia del salto "extra". No es necesario (aunque es posible) que bbox esté detrás del nginx cuando es accedido por la app Node.js**

##### Obligatorias

| Caso | Explicación |
| ---- | ----------- |
| Un nodo | Un solo proceso, un solo container. |
| Replicado | Replicado en múltiples containers, con load balancing a nivel de nginx |

##### Opcionales

| Caso | Explicación |
| ---- | ----------- |
| Multi-worker | Para una o varias de las configuraciones obligatorias, pueden probar manejar más de un worker en cada container (usar siempre la misma cantidad). Vean el módulo `cluster` ([v14.x](https://nodejs.org/docs/latest-v14.x/api/cluster.html) o [v16.x](https://nodejs.org/docs/latest-v16.x/api/cluster.html)) |
| Servidor remoto | Todos los casos anteriores suponen que el servidor corre en la misma computadora física que el cliente (generador de carga). Pueden probar montar uno o varios de ellos en otra computadora (otra en la misma casa, o un servidor en algún proveedor cloud) y comparar las métricas al "alejar" cliente de servidor. Consideren en el análisis también que las características de la computadora corriendo el servidor o el cliente pueden cambiar en esos casos. |
| ... | ... pueden agregar otros casos que se les ocurran |

> Queda a cargo de cada grupo elegir qué configuraciones de deployment prueba bajo qué escenarios de carga.
> **Es preferible armar pocos casos y analizarlos lo más posible que juntar muchísima información y estudiar poco los
> resultados.** :warning:

#### Generación de carga para las pruebas

Hay muchos tipos de escenarios de carga y pruebas de performance en general. Pueden leer por ejemplo [acá](https://www.softwaretestingclass.com/what-is-performance-testing/) (o en cualquiera de los miles de links al googlear sobre el tema) sobre algunos tipos de escenarios que pueden implementar. Queda a decisión de cada grupo elegir cuáles implementar, considerando siempre cuál es el que más útil les resulta para analizar lo que quieran estudiar.

#### Adicionales obligatorios

1. Deberán incorporar al informe una **vista Components & Connectors** para los distintos casos estudiados.
2. Deberán generar *sus propias métricas* desde la app Node para ser enviadas al daemon de statsd. Como mínimo, deberán generar una métrica con la demora en responder de cada endpoint (vista desde Node). Este métrica deberá ser visualizada en un gráfico **adicional**, que estará correlacionado con los demás gráficos en el tiempo.

## Sección 2

### Aplicación

La aplicación utilizada en la sección 1, "bbox", posee ciertas características que deberán determinar. El trabajo realizado en la sección 1 debe despejar algunas de ellas, que podrán ser verificadas aquí, y se deberán determinar otras.

### Análisis y caracterización

Deberán caracterizar cada servicio mirando tres propiedades:

1. **Sincrónico / Asincrónico**: Uno de los servicios se comportará de manera sincrónica, y el otro de manera asincrónica. Deberán detectar de qué tipo es cada uno.
2. **Cantidad de workers (en el caso sincrónico)**: El servicio sincrónico está implementado con una cantidad de workers. Deberán buscar algún indicio sobre cuál es esta cantidad.
3. **Demora en responder**: Cada servicio demora un tiempo en responder, que puede ser igual o distinto entre ellos. Deberán obtener este valor para cada uno.

Las herramientas para este análisis son las mismas que usaron en la Sección 1. Deben generar carga que ponga en relieve las características de cada servicio, haciendo uso de gráficos para mostrar puntos interesantes de la prueba. Incluyan en el informe una descripción de la/s estrategia/s utilizada/s. Recomendamos, por claridad, agregar una tabla al final de la sección con los resultados para cada uno.

## Sección 3

### Caso de estudio - Sistema de Inscripciones

Utilizando las herramientas y procedimientos de las secciones anteriores, deberán simular el comportamiento bajo carga de un sistema de inscripciones a materias (similar al SIU Guaraní).

Nos concentraremos en simular la inscripción a una o más materias. Desde el punto de vista del usuario, implica:

1. Iniciar sesión
2. Seleccionar una carrera
3. Inscribirse (_n_ veces)
   1. Ver la lista de materias en las que está inscripto
   2. Ver la lista de materias disponibles
   3. Inscribirse en una materia
4. Cerrar sesión

Para implementar este flujo, herramientas como Artillery (usando [scenarios](https://artillery.io/docs/script-reference/#scenarios)) o JMeter nos permiten simularlo.

Deberán establecer ciertas hipótesis respecto de las dimensiones del problema. Por ejemplo, cantidad de alumnos, cantidad de prioridades y su segmentación en franjas horarias, etc. También deberán modelar el tipo de comportamiento de cada endpoint, y jugar con los tiempos de demora que cada uno debería (razonablemente) tener.

Con el escenario planteado, generar la carga, graficar puntos interesantes y luego analizar el comportamiento que el sistema debería exhibir.

## Aclaraciones sobre la entrega

1. El trabajo debe entregarse **completo**. No se aceptan entregas parciales.
2. Asumimos que todo el grupo participa en la resolución del trabajo. De ocurrir problemas o surgir contratiempos, es el grupo quien debe responder y solucionarlos. Pueden consultar a los docentes pero deben demostrar primero que intentaron solucionarlos internamente.
3. De haber defectos graves en el desarrollo o en el informe del TP, se solicitará una re-entrega. Esto tiene un impacto considerable en la nota final, por lo que les recomendamos que controlen entre todo el grupo las conclusiones y justificaciones antes de entregar el trabajo.

-----------

## Links útiles

- Node.js:
  - https://nodejs.org/
  - https://github.com/creationix/nvm
  - https://nodejs.org/dist/latest-v14.x/docs/api/ o https://nodejs.org/dist/latest-v16.x/docs/api/
- Express:
  - https://expressjs.com/en/starter/hello-world.html
- Nginx:
  - https://nginx.org/
- Docker:
  - https://docker-k8s-lab.readthedocs.io/en/latest/docker/docker-engine.html
  - https://www.docker.com/
- Docker-compose:
  - https://docs.docker.com/compose/
- StatsD:
  - https://github.com/etsy/statsd
  - https://github.com/etsy/statsd/blob/master/docs/graphite.md
- Graphite:
  - https://graphiteapp.org/
  - https://graphite.readthedocs.io/en/latest/
- Grafana:
  - https://grafana.com/
  - https://docs.grafana.org/guides/getting_started/
- Imagen usada (statsd + graphite):
  - https://hub.docker.com/r/graphiteapp/graphite-statsd/
  - https://github.com/graphite-project/docker-graphite-statsd
- Gotchas:
  - http://dieter.plaetinck.be/post/25-graphite-grafana-statsd-gotchas/
- Artillery:
  - https://artillery.io/docs/
  - https://www.npmjs.com/package/artillery
  - https://www.npmjs.com/package/artillery-plugin-statsd
- JMeter:
  - https://jmeter.apache.org/

## Pequeño cheatsheet de docker

Es posible que necesiten ejecutar los comandos con `sudo`, según el sistema que usen y cómo lo hayan instalado.

```sh
# Ver qué containers existen
docker ps [-a]

# Ver qué imagenes hay en mi máquina
docker images

# Ver uso de recursos de containers (como "top" en linux)
# Ejemplo con formato específico: docker stats --format '{{.Name}}\t{{.ID}}\t{{.CPUPerc}}\t{{.MemUsage}}'
docker stats [--format <format_string>]

# Descargar una imagen
docker pull <image>[:<tag>]

# Eliminar un container
docker rm <container_id> [-f]

# Eliminar una imagen
docker rmi <image_id> [-f]

# Eliminar imágenes "colgadas" (dangling)
docker rmi $(docker images -q -f dangling=true)

# Versión instalada
docker version
```

## Pequeño cheatsheet de docker-compose

Todos los siguientes comandos deben ejecutarse desde la carpeta en donde está el archivo `docker-compose.yml` del proyecto.

Es posible que necesiten ejecutar los comandos con `sudo`, según el sistema que usen y cómo lo hayan instalado.

```sh
# ALIAS para escribir menos
alias docc='docker-compose'

# Ayuda general
docc --help

# Ayuda genral para cualquier comando
docc [COMMAND] --help

# Levantar servicios.
# Sugerencia: Usar la opción -d para levantar en background, y poder seguir usando la terminal
# También sirve para escalar horizontalmente un servicio que ya se esté ejecutando [buscar opción --scale].
# Si no se especifica al menos un servicio, se levantan todos
docc up [options] [SERVICE...]

# Ver logs de un servicio ejecutándose en background
docc logs [options] [SERVICE]

# Listar containers y sus estados
docc ps

# Restartear servicios
# Si no se indica al menos un servicio, se restartean todos
docc restart [SERVICE...]

# Frenar servicios corriendo en background (con la opción --detach del `up`)
# Si no se lista ningún servicio, se frenan todos.
# Esto solo frena servicio, no borra el container ni los datos que hayan en el mismo
docc stop [SERVICE...]

# Frenar containers y borrar tanto los containers como las imágenes y los volúmenes de almacenamiento
# (se pierden todos los datos que hubiera en el container).
# Esto aplica a TODOS los levantados con `up`, no filtra por servicio
docc down

# Levantar un nuevo container de un servicio y ejecutar un comando adentro
# (util para tener por ejemplo una terminal dentro de un container e inspeccionarlo o hacer pruebas manuales).
# Como es siempre sobre un container nuevo, lo que ven es el resultado de su docker-compose.yml y sus dockerfiles
# Ejemplo: docc run graphite bash
docc run SERVICE COMMAND

# Correr un comando en un container que ya existe y ya está corriendo.
# Parecido a `run` pero sobre un container en ejecución.
# Útil para alterar o inspeccionar algo que se está ejecutando.
#Lo que ven adentro puede no ser el resultado directo del docker-compose.yml + dockerfiles, así que mucho cuidado
# si van a modificar sus containers así, porque puede ser difícil de reproducir luego.
# Ejemplo: docc exec graphite bash
docc exec SERVICE COMMAND

# Versión instalada
docc version
```
</details>

# TRABAJO PRÁCTICO N°1
## Arquitectura del Software

**2C2022**

### Integrantes:
| Nombre               | Padrón  | Email                 |
|----------------------|--------|-----------------------|
| Pedro Andrés Flynn  | 105742 | pflynn@fi.uba.ar     |
| Juan Cruz Caserío   | 104927 | jcaserio@fi.uba.ar   |
| Franco Papa         | 106249 | fpapa@fi.uba.ar      |
| Luciano Jadur       | 101284 | ljadur@fi.uba.ar     |

---

## Índice
1. [Introducción](#introducción)
2. [PING](#ping)
   - Stress
   - Spike
   - Endurance
3. [SYNC](#sync)
   - Stress
   - Spike
   - Endurance
4. [ASYNC](#async)
   - Stress
   - Spike
   - Endurance
5. [HEAVY](#heavy)
   - Stress
   - Spike
   - Endurance
6. [Métricas desde la App](#métricas-desde-la-app)
7. [Análisis y Caracterización](#análisis-y-caracterización)
8. [Sistema de Inscripción](#sistema-de-inscripción)

---

## Introducción
El presente informe detalla los resultados obtenidos en distintas pruebas realizadas sobre los endpoints de un sistema.

### Components & Connectors
#### Single Node vs Multi Node
Se llevaron a cabo pruebas en ambas configuraciones para evaluar el rendimiento del sistema bajo distintas cargas.

---

## PING
Este endpoint devuelve la cadena `Pong` ante cada request recibido, sin requerir comunicación con servicios externos.

### PING - Stress
#### Fases:
```yaml
  - name: Subida
    duration: 30
    arrivalRate: 1
    rampTo: 275
  - name: Constante
    duration: 170
    arrivalRate: 275
  - name: Reset
    arrivalRate: 1
    duration: 20
```

#### Stress - Un Nodo
El sistema responde correctamente hasta 250 RPS. Al superarlo, comienzan errores de TIMEOUT y CONNRESET.

#### Stress - Multi Nodo
La configuración de múltiples nodos presenta una tasa de errores mayor durante la fase constante.

---

### PING - Spike
#### Fases:
```yaml
  - name: Constante
    duration: 30
    arrivalRate: 100
  - name: Pico
    duration: 10
    arrivalRate: 350
  - name: Constante
    duration: 30
    arrivalRate: 100
  - name: Pico
    duration: 10
    arrivalRate: 400
  - name: Reset
    arrivalRate: 1
    duration: 20
```

#### Spike - Un Nodo / Multi Nodo
- El sistema responde bien hasta 100 RPS.
- La latencia aumenta con los picos de carga.
- Multi Nodo logra reducir algunos errores.

---

### PING - Endurance
#### Fases:
```yaml
  - name: Subida
    duration: 30
    arrivalRate: 20
    rampTo: 200
  - name: Constante
    duration: 200
    arrivalRate: 200
  - name: Reset
    arrivalRate: 1
    duration: 20
```

#### Endurance - Un Nodo
Respuesta aceptable, con latencias máximas de 6000 ms.

#### Endurance - Multi Nodo
La latencia fluctúa entre 10000 y 6000 ms durante la fase constante.

---

## SYNC
Este endpoint devuelve la cadena `Sync: Hello world` tras realizar una petición a `https://bbox:9091`.

### SYNC - Stress
#### Fases:
```yaml
  - name: Subida
    duration: 30
    arrivalRate: 1
    rampTo: 12
  - name: Constante
    duration: 170
    arrivalRate: 12
  - name: Reset
    arrivalRate: 1
    duration: 20
```

#### Stress - Un Nodo / Multi Nodo
- El sistema colapsa al alcanzar los 12 RPS.
- La latencia crece hasta el punto de quiebre.

---

## ASYNC
Este endpoint devuelve la cadena `Async: Hello world` tras una petición a `https://bbox:9090`.

### ASYNC - Stress
#### Fases:
```yaml
  - name: Subida
    duration: 30
    arrivalRate: 1
    rampTo: 65
  - name: Constante
    duration: 170
    arrivalRate: 65
  - name: Reset
    arrivalRate: 1
    duration: 20
```

#### Resultados
- Latencia fluctuante, pero sin errores en ambos escenarios.
- Multi Nodo mantiene estabilidad en latencia y errores.

---

## HEAVY
Este endpoint realiza cálculos intensivos, aumentando la latencia.

### HEAVY - Stress
#### Fases:
```yaml
  - name: Subida
    duration: 30
    arrivalRate: 1
    rampTo: 2
  - name: Constante
    duration: 170
    arrivalRate: 2
  - name: Reset
    arrivalRate: 1
    duration: 20
```

#### Resultados
- Resistencia baja en ambas configuraciones.
- Fallos predominantes tras menos de un minuto de carga.

---

## Métricas desde la App
Se midieron métricas usando `lynx` y `statsd`.

- **PING:** Multi Nodo llega a 500 RPS con `2000ms` response time.
- **ASYNC:** Multi Nodo tiene una performance similar a Single Node.
- **SYNC:** La diferencia entre ambos escenarios es mínima.
- **HEAVY:** Multi Nodo mejora en endurance pero sigue presentando fallos.

---

## Análisis y Caracterización

### Sincrónico vs Asincrónico
- `/async` (puerto 9090) tiene mejor response time y maneja mayor carga.
- `/sync` (puerto 9091) se bloquea y presenta mayor latencia.

### Workers en `sync`
El sistema empieza a fallar alrededor de 10-15 RPS, lo que sugiere esa cantidad de workers.

### Tiempos de Respuesta
- `/async`: 1500 ms.
- `/sync`: 1800-2000 ms.

---

## Sistema de Inscripción

Se simula un sistema de inscripción con los siguientes endpoints:

- `/login` (100ms)
- `/select_grade` (50ms)
- `/list_all` (500ms)
- `/list_courses` (300ms)
- `/enroll` (100ms)
- `/logout` (50ms)

### Caso 1
- 4 usuarios/seg durante 5 minutos.
- Picos de carga afectan el response time.

### Caso 2
- 10 usuarios/seg.
- Se simulan distintos escenarios.
- **Resultados:** Mejor distribución de carga y menor tiempo de respuesta.

---

Fin del Informe.
