Az events.py modul segítségével speciális körülmények közt létrejövő eseménykere reagálhatunk egy-egy funkcióval.


## Főbb funkciók:

*	Feliratkozás eseményekre annak körülményei meghatározásával
*	Leiratkozás eseménykről
*	Összes eseményre való feliratkozás törlése
*	Az eseménykre való feliratkozások kikérése
*	Események integrált vizsgálata
*	Előre regisztrált eseményfeliratkozó function-ok a paraméterek esetében típus ellenőrzéssel

---

## Használat

*	A használathoz másoljuk be az events.py-t a projektünk gyökérkönyvtárába
*	Iratkozzunk fel egy eseményre, megadva azokat a körülményeket amikre szeretnék ha az általunk meghatározott reakció(reagáló function) működésbe lépjen
```
	EventHandlerContext.addKeyDownEventHandler(key=115, mod=64, handlerFunction=lambda event: print("save..."))
```
*	Hozzunk létre egy "main" loop-ot(végtelen while ciklus)
*	Itt hívjuk meg az eventObservert, ami folyamatosan monitorozza a pygame által létrehozott eseményeket, és kikeresi azokat az általunk regisztrált handlereket amiknek az adott körlményekben teljeseülniük kéne
```python
	while eng_screen.run:
		events.observeEvents()
```	

## Érdemes tudni

*	A reakciók(reagáló function) paraméterben egy dict-et kell hogy várjon(ez az "elkapott" esemény körülményeit tartalmazza, hogy a reakcióban felhasználhassuk azokat) és nem lehet visszatérési értéket
*	Eseményre az előre meghatározott esemény hozzáadó funkcióval reisztrálhatunk(EventhandlerContext.add[eseménynév]EventHandler) vagy egy általános eseményhozzáadó function-el ami paraméterben várja a kondíciókat dict típusként, amik esetén szeretnénk a reakciónkat végrehajtani
*	Az előre meghatározott eseménykezelő hozáadó function-nél ha egy paramétert nem adunk meg az ha egy esemény ugyan ilyen nevű paraméterével kerül összehasonlításra mindig teljesülni fog
```python
	EventHandlerContext.addKeyDownEventHandler(handlerFunction=lambda event: print("save..."))
```
Mivel a fenti eseménykezlő hozzáadó function-nél nem határoztuk meg hogy a gomblenyomás esetén milyen gomb értékre reagáljon így bármilyen gombot nyomunk le a reakciót végre fogja hajtani



 
