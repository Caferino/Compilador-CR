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

~Óscar Antonio Hinojosa Salum A00821930
