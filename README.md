# Points
Всё работает на библиотеке pygame.\
Это основные сочетания кнопок для программ:
* <kbd>LMB</kbd> - создание активной точки
* <kbd>RMB</kbd> - создание пассивной точки
* Колёсико мыши - используется если <kbd>LMB</kbd> и <kbd>RMB</kbd> заняты
* <kbd>Space</kbd> - пауза или пуск времени
* <kbd>Esc</kbd> или крестик окна - закрытие программы
# Оглавление
* v1 - залипалка
* v2 - остановка от расстояния
* v3 - замена от расстояния
* v4 - неконтролируемая цепная реакция
* v5 - митоз клетки
* v6 - порталы
* v7 - стены
* v8 - гравитация
## Первая версия
Обычная залипаловка. При приближении точек на расстояние `dist` между ними образуется "связь" в виде линии. Если точка движется - она коричневая, а если нет то зелёная.
## Вторая версия
На поле расположены движущиеся коричневые точки. Когда к зелёной стоячей точке приближается коричневая на растояние `dist` коричнеая точка превращается в зелёную и останавливается. На внешний вид получается корни какого-то дерева.
## Третья версия
Тоже поле как из второй версии. Когда к синий точке прибижается коричневая на растояние `dist` помеченное окружностью коричневая точка превращается в синию, а синия просто исчезает. Спустя время останутся только синии.
## Четвёртая версия
Мини модель распада урана после столкновения с нейтроном. При столкновении синей точки с зелёной (очень близкое приближение) эти две точки удаляются и на их месте создаются две точки коричного цвета которые летят некоторое время, а потом останавливаются, также появляется 2-3 синих точки летящие кто куда.
## Пятая версия
Мини модель митоза клетки. Точка растёт до определённого момента и исчезает и в противоположные стороны разлетаются две точки, которые после тоже делятся. Меняя параметр `stage` в классе можно ускорять до раза в секунду или замедлять хоть до бесконечности.
## Шестая версия
Одно слово - порталы. В этой версии есть синий и оранжевый порталы. Когда портал не имеет своей пары он серый, но когда у него появляется пара он становится белым. Кроме порталов в этой версии нет ничего особенного, но код порталов легко интегрировать в другие версии.
## Седьмая версия
скоро будет. Там будет стены
## Восьмая версия
Похожа на первую версию т.е. похожа на залипалку. Обычные точки смотрят на большие точки и ищут расстояние между ей и собой. Находя самую ближнюю она окрашевается в тот же цвет как и большая и соединяется с ней линией того же цвета. Нажимая на клавиши <kbd>G</kbd> или <kbd>A</kbd> можно притягивать или отталкивать маленькие точки относительно большей ближайщей.
