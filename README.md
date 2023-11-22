**Comandos y archivos utilizados para debugging:**

Dentro de: ~/.../Compilaor-CR

> python3 Parser.py prueba1.txt
>
> python3 Parser.py prueba2.txt
>
> python3 Parser.py prueba3.txt
>
> python3 Parser.py prueba4.txt
>
> python3 Parser.py prueba5.txt

**=== Avances ===**

**Septiembre 20 2023:**

> Reinicio. Se ocupará arreglar primero la semántica. Por usar PLY, Right-To-Left o Bottom-Up, tengo que dividir la construcción de la tabla de variables en pedazos pequeños.

**Octubre 20 2023:**

> Remasterización completada, ahora el parser funciona como Top-Down en vez de Bottom-Up. Este cambio grande fue para poder manejar funcionas recursivas apropiadamente y a la vez hacer el proyecto 100 veces más legible y accesible; antes hacía todo al revés.

**Octubre 22 2023:**

> Ya puede hablar.

**Octubre 28 2023:**

> Llamadas a funciones lista, faltan algunos tweaks, el return y la recursión.

**Noviembre 3 2023:**

> Llamadas a funciones con Returns funcionando, mejor verificación de tipos al imprimir o asignar valores (en estos dos casos no servía para nada el SemanticCube por alguna razón de mal diseño, ahora sí se usa bien) y mejores errores, con menos comillas y comas que salían sobrando (por no saber usar 'f-strings' antes)... Solo queda la recursión, la cual debe caer como un guante, lo más difícil será diseñar el control de los "snapshots" de la SymbolTable y saber cuál leer en el momento; es decir, saber en cuál número de la iteración recursiva debe ejecutarse la función, con cuáles valores, etc.

**Noviembre 10 2023:**

> Durante esta semana desarrollé la recursión simple, entre otros varios tweaks. La mejor bitácora deberían ser el historial de commits, le perdi atención a este README durante este lapso de tiempo doloroso.

**Noviembre 19 2023:**

> El Día de la Independencia: Logré sacar la recursión compleja, es decir, correr códigos como fibonacci o más complejos. Todo lo medité por 8+ horas diarias hecho bolita en la cama, sin papel ni apoyo visual más que el puro código, comiendo sin parar; en 4 o 5 días terminé resolviéndolo, el mayor problema se hallaba en la VirtualMachine con el control de las SymbolTables y después también las registers temporales, cada iteración recursiva debía guardar sus propios valores.

**Noviembre 21 2023:**

> Limpieza de código general e implementación de '>=' y '<=' mas el chequeo de variables globales vs locales (según a la función a la que pertenecen).

~Óscar Antonio Hinojosa Salum A00821930
