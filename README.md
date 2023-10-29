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

> Durante la Semana i logré acabar toda la lógica de los prints, strings y la mitad de funciones. Me falta asegurarme de que no se impriman variables locales estando afuera de la función, arreglar la asignación de parámetros en las function_calls, y finalmente, lo último de todo el proyecto: el return y la recursión; ya están en el Parser, solo faltan sus cuádruplos y testing final.

~Óscar Antonio Hinojosa Salum A00821930
