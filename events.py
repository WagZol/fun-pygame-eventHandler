import pygame
from typing import Callable
from typing import Tuple
from collections import defaultdict


def observeEvents():
    """
    **Leiras:**
        A pygame esemenyit hozzarendeli az esemenykezelo tarolohoz. Amennyiben talal olyan esemenykezelot ami megfelel az esemeny korulmenyinek ugy aakitvalja az esemenykezelo reakciometodusat
    """
    eventList = pygame.event.get()
    if len(eventList) > 0:
        for event in eventList:
            EventHandlerContext.handleEvent(event)


class HandlerProperties(object):
    def __init__(self, handlerConditions: dict, eventhandler: Callable):
        self.__handlerConditions = handlerConditions
        self.__eventHandler = eventhandler

    def handleEvent(self, conditionsFromTriggeredEvent: dict):
        """
        **Leiras:**
            Az esemenykezelo reakcio metodusanak aktivatora

        **Parameterek:**
            ``conditionsFromTriggeredEvent(dict)`` -- Az aktivalodott esemeny kondicioi, ahhoz kell, hogy maga a reakcio metodus tudjon kalkulalni az esemeny parameterevel is

        **Pelda:**
            >>>EventHandlerContext.addKeyDownEventHandler(lambda event: print(event.key), key=pygame.K_f)

            *A fenti pelda az 'f' billentyulenyomasra aktivalja a regisztralt esemenykezelot, es megkapva az esemeny parameteriet, kiiratja belole a 'key' parametert, azaz melyik gomb aktivalta az esemenyt*

        """
        self.__eventHandler(conditionsFromTriggeredEvent)

    def getConditions(self):
        """
        **Leiras:**
            Az esemenykezelo parameteriet kerhetjuk ki vele, pontosabban azokat a parametereket amikre aktivalodni fog a reakcio metodus
        """
        return self.__handlerConditions

    def setConditions(self, newConditions: dict):
        """
        **Leiras:**
            Az esemenykezelo parameteriet allithajuk be vele, pontosabban azokat a parametereket amikre aktivalodni fog a reakcio metodus
        """
        self.__handlerConditions = newConditions


class EventHandlerContext(object):
    __eventHandlers = defaultdict(list)

    @classmethod
    def __findEventHandlers(cls, conditions: dict, eventId):
        if (cls.__eventHandlers[eventId]):
            return filter(lambda properties: properties.getConditions().items() <= conditions.items(),
                          cls.__eventHandlers[eventId])

    @classmethod
    def addHandlerPropertyToEventHadnlers(cls, newHandlerProperties: HandlerProperties, eventId: int):
        """
        **Leiras:**
            Egy esemenykezelo-t adhatunk hozza ezzel a metodussal a megfelelo esemenykategoriba. Ezt a metodust hasznaéljak az elore megirt esemenykezelo form-ok(pl.:addKeydownEventHandler) ahol az ID adtt, de ha olyan esemenyt szeretnénk hozzaadni az esemenykezelo listahoz amire nincs elore megirt form ez a metodus lehetoseg ad arra is

        **Parameterek:**
            ``newHandlerProperties(HandlerProperties)`` -- Maga az esemenykezelo ami tartalmazza az esemenykezelo kondicioit, es a reakciometodust

            ``eventId(int)`` -- Az az esemenykategoria ahova az esemenykezelonket tenni szeretnenk. Ugyeljunk hogy mindig a megfelelo esemenykategoriab tegyunk az esemenykezelonket, mert az osszehasnlito metodus sesse fog maskulonben egyezest talalani es az esemenykezelonk sose lesz aktivalva

        **Pelda:**
            >>>EventHandlerContext.addHandlerPropertyToEventHadnlers(newHandlerProperties=HandlerProperties({"key": pygame.K_f}, lambda event: print(event.key)), eventId=pygame.KEYDOWN)

            *Az elore megirt esemenykezelo hozzadas metodus helyett, manualisan keszitettuk el az esemenykezelo aktivator kondicioit es rendeltuk hozza a reakciometodust. Egesz pontosan azt csinalja a fenti pelda, hogyha lenyomjuk az f billentyut akkor kiirja hogy melyik billentyu lenyomasa aktivalta az esemeny-t*
        """
        cls.__eventHandlers[eventId].append(newHandlerProperties)

    @classmethod
    def __getNotNoneConditionProperties(cls, conditionProperties: dict):
        return {propertyName: propertyValue for propertyName, propertyValue in conditionProperties.items() if
                propertyValue is not None}

    @classmethod
    def getEventHandlers(cls):
        """
        **Leiras:**
            Az osszes esemenykezelo kikerese

        **Visszateresi ertek:**
            ``cls.__eventHandlers(defaultdict(list))`` -- Az EventHandlerContext-ben  tarolt esemenykezelok az esemeny azonositoja szerint kategorizalva
        """
        return cls.__eventHandlers

    @classmethod
    def removeEventHandlers(cls, handlerConditions: dict = None, eventId: int = None):
        """
        **Leiras:**
            A parameterben megadott esemeny azonosito alatt regisztralt, szinten parameterben megadot korulmenyeknek megfelelo esemenykezelok torlese. Amennyiben a korulmenyek parametert és az eventId parametert uresen hagyjuk ugy a regisztralt osszes esemeny torlesre kerul. Amennyiben az esemenyazonosítot megadjuk, de a kondiciokat nem ugy az adott esemenytipusra feliratkozott osszes esemenykezelo torlesre kerul

        **Paramaeterek:**
            ``handlerConditions(dict=None)`` -- A kondiciok amik alapjan szukiteni szeretnenk a keresest a regisztralt
        esemenykezelok kozott.
            ``eventId(int=None)`` -- Az esemeny egesz szamban meghatorzott azonositoja

        **Pelda:**
            >>>EventHandlerContext.removeEventHandlers({"key": 27}, pygame.KEYDOWN)

            *Torli az escape billentyu lenyomasaval kapcsolatos osszes esemenykezelot*
        """

        if (handlerConditions and eventId):
            handlerSearchResults = cls.__findEventHandlers(conditions=handlerConditions, eventId=eventId)
            if (handlerSearchResults):
                for handlerSearchResult in handlerSearchResults:
                    cls.__eventHandlers[eventId].remove(handlerSearchResult)
            return
        if (eventId):
            cls.__eventHandlers[eventId].clear()
            return
        cls.__eventHandlers.clear()

    @classmethod
    def handleEvent(cls, event: pygame.event):
        """
        **Leiras:**
            A triggerelt esemenyek korulmenyinek megfelelo handlerek aktivatora

        **Paramaeterek**
            ``event(pygame.event)`` -- A pygame modulban meghatarozott esemeny class-t megvalosíto, aktivalt esemeny objektum
        """

        filteredHandlersOfSameEventType = cls.__findEventHandlers(event.dict, event.type)
        if (filteredHandlersOfSameEventType):
            for eventHandler in filteredHandlersOfSameEventType:

                eventHandler.handleEvent(event.dict)

    @classmethod
    def addQuitEventHandler(cls, handlerFunction: Callable[[dict], None]):
        """
        **Leiras:**
            Kilepes esemenyhez(kilepes a pygame-bol) reakcio metodust hozzaado funkcio.

        **Paramaeterek:**
            ``handlerFunction(Callable[[dict], None])`` -- reakciometodus, ami ha az esemeny a parameterben meghatarozott feltetelekkel
            valosul meg vegrehajtasra kerul

        **Pelda:**
            >>>EventHandlerContext.addQuitEventHandler(handlerFunction=lambda event: print("Bye, bye!"))

            *Amennyiben a QUIT esemeny aktivalodik kiiratjuk a konzolba hogy "Bye, bye!"
        """
        conditions = {}
        handlerProperties = HandlerProperties(conditions, handlerFunction)
        cls.addHandlerPropertyToEventHadnlers(handlerProperties, pygame.QUIT)

    @classmethod
    def addActiveEventHandler(cls, handlerFunction: Callable[[dict], None], state: int = None, gain: int = None):
        """
        **Leiras:**
            Ablak aktivitas esemenyhez reakcio metodust hozzaado funkcio.

        **Paramaeterek:**
            ``state(int=None)`` -- az ablak allapotanak kulcsszavai.
                1 - eger a pygame ablakban van

                2 - pygame ablak ki van jelolve

                4 - pygame ablak minimalizalva van
            ``gain(int=None)`` -- az ablak allapotanak ertekei.
                0 - hamis

                1 - igaz
            ``handlerFunction(Callable[[dict], None])`` -- reakciometodus, ami ha az esemeny a parameterben meghatarozott feltetelekkel
                valosul meg vegrehajtasra kerul

        **Pelda:**
            >>>EventHandlerContext.addActiveEventHandler(handlerFunction=lambda event: playSound("minimazed"), state=4, gain=1)

            *Amennyiben az ablakot letesszük talcara egy fiktiv playSound metodussal egy minimazied hangeffektust jatszunk le*
        """
        conditions = {
            'gain': gain,
            'state': state
        }
        handlerProperties = HandlerProperties(cls.__getNotNoneConditionProperties(conditions), handlerFunction)
        cls.addHandlerPropertyToEventHadnlers(handlerProperties, pygame.ACTIVEEVENT)

    @classmethod
    def addKeyDownEventHandler(cls, handlerFunction: Callable[[dict], None], key: int = None,
                               unicode: str = None, mod: int = None,
                               scancode: int = None, window: str = None):
        """
        **Leiras:**
            Billentyuzetgomb lenyomas esemenyhez reakcio metodust hozzaado funkcio.

        **Paramaeterek:**
            ``key(int=None)`` -- a lenyomott gomb ASCII erteke

            ``unicode(str=None)`` -- a lenyomott gomb unicode-ja

            ``mod(int=None)`` -- specialis gombok(RSHIFT, LSHIFT, RCTRL, LCTRL stb...)  erteket adja vissza
            amennyiben azok meg lettek nyomva.

            ``scancode(int=None)`` -- periferiaspecifikus erteket adja a gombnak vissza, ami billentyuzetenkent valtozhat.

            Olyan specialis gombok eseten van haszna mint pl egy multimedia gomb a billentyuzeten

            ``window(str=None)`` -- ?Az ablak ID-ját adja vissza ahol történt a gombnyomás?
                None - Nem beazonosítható ablak

            ``handlerFunction(Callable[[dict], None])`` -- reakciometodus, ami ha az esemeny a parameterben meghatarozott feltetelekkel
            valosul meg vegrehajtasra kerul

        **Pelda:**
            >>>EventHandlerContext.addKeyDownEventHandler(key=pygame.K_s, mod=pygame.K_RCTRL, handlerFunction=lambda event: save())

            *A jobb CTRL+S gomb lenyomasakor meghivunk az esemenykezelovel egy fikiv 'save' funkciot*


        """

        conditions = {
            'unicode': unicode,
            'key': key,
            'mod': mod,
            'scancode': scancode,
            'window': window
        }
        handlerProperties = HandlerProperties(cls.__getNotNoneConditionProperties(conditions), handlerFunction)
        cls.addHandlerPropertyToEventHadnlers(handlerProperties, pygame.KEYDOWN)

    @classmethod
    def addKeyUpEventHandler(cls, handlerFunction: Callable[[dict], None], key: int = None, mod: int = None,
                             scancode: int = None, window: str = None):
        """
        **Leiras:**
            Billentyuzetgomb felengedes esemenyhez reakcio metodust hozzaado funkcio.

        **Paramaeterek:**
            ``key(int=None)`` -- a lenyomott gomb ASCII erteke

            ``mod(int=None)`` -- specialis gombok(RSHIFT, LSHIFT, RCTRL, LCTRL stb...)  erteket adja vissza
            amennyiben azok meg lettek nyomva.

            ``scancode(int=None)`` -- periferiaspecifikus erteket adja a gombnak vissza, ami billentyuzetenkent valtozhat.
            Olyan specialis gombok eseten van haszna mint pl egy multimedia gomb a billentyuzeten

            ``window(str=None)`` -- ?Az ablak ID-ját adja vissza ahol történt a gombnyomás?
                None - Nem beazonosítható ablak

            ``handlerFunction(Callable[[dict], None]`` -- reakciometodus, ami ha az esemeny a parameterben meghatarozott feltetelekkel
            valosul meg vegrehajtasra kerul

        **Pelda:**
            >>>EventHandlerContext.addKeyUpEventHandler(handlerFunction=lambda event: print(event.key))

            *Egy billentyuzetgomb felengedese utan kiirja melyik gomb aktivalta az esemenyt*

        """
        conditions = {
            'key': key,
            'mod': mod,
            'scancode': scancode,
            'window': window
        }
        handlerProperties = HandlerProperties(cls.__getNotNoneConditionProperties(conditions), handlerFunction)
        cls.addHandlerPropertyToEventHadnlers(handlerProperties, pygame.KEYUP)

    @classmethod
    def addMouseMotionEventHandler(cls, handlerFunction: Callable[[dict], None], pos: Tuple[int, int] = None,
                                   rel: Tuple[int, int] = None, buttons: Tuple[int, int, int] = None,
                                   window: str = None):
        """
        **Leiras:**
            Eger mozgas esemenyhez reakcio metodust hozzaado funkcio.

        **Paramaeterek:**
            ``pos(Tuple[int,int]=None)`` -- Az eger aktualis pozicioja az event aktivalasank pillanataban

            ``rel(Tuple[int,int]=None)`` -- Az eger elozo event aktivalashoz kepest megtett relativ tavolsaga

            ``buttons(Tuple[int, int, int]=None)`` -- Az eger gombjainak allapota(bal gomb, kozepso gomb, jobb gomb) az event aktivalasnak pillanataban

            ``window(str=None)`` -- ?Az ablak ID-ját adja vissza ahol történt a gombnyomás?
                None - Nem beazonosítható ablak

            ``handlerFunction(Callable[[dict], None])`` -- reakciometodus, ami ha az esemeny a parameterben meghatarozott feltetelekkel valosul meg vegrehajtasra kerul (alapertelmezett: nincs)

        **Pelda:**
            >>>EventHandlerContext.addMouseMotionEventHandler(handlerFunction=lambda event: mouseCursor.pos(event.pos))

            *Az eger poziciojat egy fiktiv mouseCursor sprite-nak átadjuk igy az jelenhet meg az eger cursor helyett amennyiben azt letiltjuk a pygame ablakon belül*

        """

        conditions = {
            'pos': pos,
            'rel': rel,
            'buttons': buttons,
            'window': window
        }
        handlerProperties = HandlerProperties(cls.__getNotNoneConditionProperties(conditions), handlerFunction)
        cls.addHandlerPropertyToEventHadnlers(handlerProperties, pygame.MOUSEMOTION)

    @classmethod
    def addMouseButtonUpEventHandler(cls, handlerFunction: Callable[[dict], None], button: int = None,
                                     pos: Tuple[int, int] = None, window: str = None):
        """
        **Leiras:**
            Egergomb felengedes esemenyhez reakcio metodust hozzaado funkcio.

        **Paramaeterek:**
            ``button(int=None)`` -- Az eger melyik gombja lett lenyomva az event aktivalasank idopontjaban
                1 - bal gomb

                2 - kozepso gomb

                3 - jobb gomb

                4 - gorgetes fel

                5 - gorgetes le

            ``pos(Tuple[int,int]=None)`` -- Az eger aktualis pozicioja az event aktivalasank pillanataban

            ``window(str=None)`` -- ?Az ablak ID-ját adja vissza ahol történt a gombnyomás?
                None - Nem beazonosítható ablak

            ``handlerFunction(Callable[[dict], None])`` -- reakciometodus, ami ha az esemeny a parameterben meghatarozott feltetelekkel
            valosul meg vegrehajtasra kerul

        **Pelda:**
            >>>EventHandlerContext.addMouseButtonUpEventHandler(handlerFunction=lambda event: draggedObject.pos(event.pos), button=1)

            *Ha a bal gombot elengedjuk akkor egy fiktiv funkcio a "vonszolt" objektumnak atadja az eger poziciojat(esetleges drag&drop vege)*

        """

        conditions = {
            'pos': pos,
            'button': button,
            'window': window
        }
        handlerProperties = HandlerProperties(cls.__getNotNoneConditionProperties(conditions), handlerFunction)
        cls.addHandlerPropertyToEventHadnlers(handlerProperties, pygame.MOUSEBUTTONUP)

    @classmethod
    def addMouseButtonDownEventHandler(cls, handlerFunction: Callable[[dict], None], button: int = None,
                                       pos: Tuple[int, int] = None, window: str = None):
        """
        **Leiras:**
            Egergomb lenyomas esemenyhez reakcio metodust hozzaado funkcio.

        **Paramaeterek:**
            ``button(int=None)`` -- Az eger melyik gombja lett lenyomva az event aktivalasank idopontjaban
                1 - bal gomb

                2 - kozepso gomb

                3 - jobb gomb

                4 - gorgetes fel

                5 - gorgetes le

            ``pos(Tuple[int,int]=None)`` -- Az eger aktualis pozicioja az event aktivalasank pillanataban

            ``window(str=None)`` -- ?Az ablak ID-ját adja vissza ahol történt a gombnyomás?
                None - Nem beazonosítható ablak

            ``handlerFunction(Callable[[dict], None])`` -- reakciometodus, ami ha az esemeny
                a parameterben meghatarozott feltetelekkel valosul meg vegrehajtasra kerul

        **Pelda:**
            >>>EventHandlerContext.addMouseButtonDownEventHandler(handlerFunction=lambda event:screen.move("down"), button=5)

            *Ha az egeret lefele gorgetjuk egy fiktiv funkcio a kepernyot lefele mozgatja(pl ha kijelzendo kep nagyobb lenne mint a kepernyo ez is egy modja lehet a gorgetesnek)*
        """

        conditions = {
            'pos': pos,
            'button': button,
            'window': window
        }
        handlerProperties = HandlerProperties(cls.__getNotNoneConditionProperties(conditions), handlerFunction)
        cls.addHandlerPropertyToEventHadnlers(handlerProperties, pygame.MOUSEBUTTONDOWN)

    @classmethod
    def addJoyAxisMotionEventHandler(cls, handlerFunction: Callable[[dict], None], joy: int = None,
                                     value: float = None, axis: int = None):
        """
        **Leiras:**
            Joystick mozgas esemenyhez reakcio metodust hozzaado funkcio.

        **Paramaeterek:**
            ``joy(int=None)`` -- Annak a joysticknak az id-je(minden joystickhoz tartozik 1 joystick object) amelyik aktivalta az eventet

            ``value(float=None)`` -- -1 és 1 kozotti lebegopontos ertek ami megadja hogy az eventben feltuntetet tengelyen milyeN
                pozicioban van a joystick.(0 a kozeppont)

            ``axis(int=None)`` -- az a tengely amin a mozgas tortent egesz szamban kifejezve
                0 - x tengely
                1 - y tengely
                2 - masik analog kar eseten x tengely
                3 - masik analog kar eseten y tengely

            ``handlerFunction(Callable[[dict], None])`` -- reakciometodus, ami ha az esemeny a parameterben meghatarozott feltetelekkel
            valosul meg vegrehajtasra kerul

        **Pelda:**
            >>>EventHandlerContext.addJoyAxisMotionEventHandler(handlerFunction=lambda event:Effects.play("Jump"), axis=1)

            *Ha barmelyik joystick iranygombjain folfele iranyt nyomunk egy fiktiv funkcio lejatsza az ugras hangjat*
        """

        conditions = {
            'joy': joy,
            'value': value,
            'axis': axis
        }
        handlerProperties = HandlerProperties(cls.__getNotNoneConditionProperties(conditions), handlerFunction)
        cls.addHandlerPropertyToEventHadnlers(handlerProperties, pygame.JOYAXISMOTION)

    @classmethod
    def addJoyBallMotionEventHandler(cls, handlerFunction: Callable[[dict], None],
                                     joy: int = None, ball: int = None, rel: Tuple[int, int] = None):
        """
        **Leiras:**
            Joystick trackball mozgas esemenyhez reakcio metodust hozzaado funkcio.

        **Parameterek:**
            ``joy(int=None)`` -- Annak a joysticknak az id-je(minden joystickhoz tartozik 1 joystick object) amelyik aktivalta az eventet

            ``ball(int=None)`` -- Annak a trackballnak a szama amelyik az event-et aktiválta

            ``rel(Tuple[int,int]=None)`` -- A joystick trackball elozo event aktivalashoz kepest megtett relativ tavolsaga  (alapertelmezett: None)

            ``handlerFunction(Callable[[dict], None])`` -- reakciometodus, ami ha az esemeny a parameterben meghatarozott feltetelekkel
            valosul meg vegrehajtasra kerul

        **Pelda:**
            >>>EventHandlerContext.addJoyBallMotionEventHandler(handlerFunction=lambda event:print(event.ball), joy=1, rel=(10, 10))

            *Ha az 1-es id-ju joystick barmelyik trackball-ja 10 pixelt mozdul lefele es jobbra akkor kiiratjuk hogy melyik trackball aktivalta az esemenyt*
        """

        conditions = {
            'joy': joy,
            'ball': ball,
            'rel': rel
        }
        handlerProperties = HandlerProperties(cls.__getNotNoneConditionProperties(conditions), handlerFunction)
        cls.addHandlerPropertyToEventHadnlers(handlerProperties, pygame.JOYBALLMOTION)

    @classmethod
    def addJoyHatMotionEventHandler(cls, handlerFunction: Callable[[dict], None],
                                    joy: int = None, hat: int = None, value: Tuple[int, int] = None):
        """
        **Leiras:**
            Joystick analog kar mozgas esemenyhez reakcio metodust hozzaado funkcio.


        **Parameterek:**
            ``joy(int=None)`` -- Annak a joysticknak az id-je(minden joystickhoz tartozik 1 joystick object) amelyik aktivalta az eventet

            ``hat(int=None)`` -- Annak az analog karnak a szama amelyik az event-et aktiválta

            ``value(Tuple[int,int]=None)`` -- A joystick analog kar pozicioja az event aktivalas pillanataban  (alapertelmezett: None)

            ``handlerFunction(Callable[[dict], None])`` -- reakciometodus, ami ha az esemeny a parameterben meghatarozott feltetelekkel
            valosul meg vegrehajtasra kerul

        **Pelda:**
            >>>EventHandlerContext.addJoyHatMotionEventHandler(handlerFunction=lambda event:print(event.value), joy=1, hat=2)

            *Az 1-es id-ju joystick-on ha az 2-es id-ju analog kar megmozdul kiiratjuk a pygame szerinti uj koordinatait*

        """

        conditions = {
            'joy': joy,
            'hat': hat,
            'value': value
        }
        handlerProperties = HandlerProperties(cls.__getNotNoneConditionProperties(conditions), handlerFunction)
        cls.addHandlerPropertyToEventHadnlers(handlerProperties, pygame.JOYHATMOTION)

    @classmethod
    def addJoyButtonUpEventHandler(cls, handlerFunction: Callable[[dict], None],
                                   joy: int = None, button: int = None):
        """
        **Leiras:**
            Joystickgomb felengedes esemenyhez reakcio metodust hozzaado funkcio.

        **Parameterek:**
            ``joy(int=None)`` -- Annak a joysticknak az id-je(minden joystickhoz tartozik 1 joystick object) amelyik aktivalta az eventet

            ``button(int=None)`` -- Annak a gombnak a szama amelyik az event-et aktiválta(ez joystick-onkent valtozhat)

            ``handlerFunction(Callable[[dict], None])`` -- reakciometodus, ami ha az esemeny a parameterben meghatarozott feltetelekkel
            valosul meg vegrehajtasra kerul

        **Pelda**
            >>>EventHandlerContext.addJoyButtonUpEventHandler(handlerFunction=lambda event:print(event.button), joy=1)

            *Az 1-es id-ju joystick-on ha barmilyen gombot lenyomas utan felengedunk kiiratjuk hogy melyik gomb volt az*
        """

        conditions = {
            'joy': joy,
            'button': button
        }
        handlerProperties = HandlerProperties(cls.__getNotNoneConditionProperties(conditions), handlerFunction)
        cls.addHandlerPropertyToEventHadnlers(handlerProperties, pygame.JOYBUTTONUP)

    @classmethod
    def addVideoResizeEventHandler(cls, handlerFunction: Callable[[dict], None],
                                   size: Tuple[int, int] = None, w: int = None, h: int = None):
        """
        **Leiras:**
            Az ablak atmeretezese esemenyhez reakcio metodust hozzaado funkcio.


        **Parameterek:**
            ``size(Tuple[int, int]=None)`` -- A pygame ablak merte az event aktivalasanak pillanataban

            ``w(int=None)`` -- A pygame ablak szelessege az event aktivalasanak pillanataban

            ``h(int=None)`` -- A pygame ablak magassaga az event aktivalasanak pillanataban

            ``handlerFunction(Callable[[dict], None])`` -- reakciometodus, ami ha az esemeny a parameterben meghatarozott feltetelekkel
            valosul meg vegrehajtasra kerul

        **Pelda:**
            >>>EventHandlerContext.addVideoResizeEventHandler(w=640, handlerFunction=lambda event: print(event.size))

            *Ha a kepernyo szelessege 640-re valtozik, kiirja a kepernyo meretet*
        """

        conditions = {
            'size': size,
            'w': w,
            "h": h
        }
        handlerProperties = HandlerProperties(cls.__getNotNoneConditionProperties(conditions), handlerFunction)
        cls.addHandlerPropertyToEventHadnlers(handlerProperties, pygame.VIDEORESIZE)

    @classmethod
    def addVideoExposeEventHandler(cls, handlerFunction: Callable[[dict], None]):
        """
        **Leiras:**
            Az ablakba rajzolas(???) esemenyhez reakcio metodust hozzaado funkcio.


        **Parameterek:**
            ``handlerFunction(Callable[[dict], None])`` -- reakciometodus, ami ha az esemeny a parameterben meghatarozott feltetelekkel
            valosul meg vegrehajtasra kerul (alapertelmezett: nincs)


        **Pelda:**
            >>>EventHandlerContext.addVideoExposeEventHandler(lambda event: print(event))

            *A pygame abalkba rajzolaskor kiirja az esemeny minden korulmenyet*
        """

        conditions = {}
        eventProperties = HandlerProperties(cls.__getNotNoneConditionProperties(conditions), handlerFunction)
        cls.addHandlerPropertyToEventHadnlers(eventProperties, pygame.VIDEOEXPOSE)

    @classmethod
    def addUserEventEventHandler(cls, handlerFunction: Callable[[dict], None], conditions: dict = None):
        """
        **Leiras:**
            A felhasznalo altal aktivalt event esemenyhez reakcio metodust hozzaado funkcio.
            Peldak alapjan teszteleskor innen aktivalnak eventeket


        **Parameterek:**
            ``handlerFunction(Callable[[dict], None])`` -- reakciometodus, ami ha az esemeny a parameterben meghatarozott feltetelekkel
            valosul meg vegrehajtasra kerul

            ``conditions(dict=None)`` -- parameter lista a sajat eventhez


        **Pelda:**
            >>>EventHandlerContext.addUserEventEventHandler(lambda event: print(event))

            *Barmilyen userevent esemeny eseten kiiratjuk az esemeny kondicioit*


        """
        conditions = conditions
        handlerProperties = HandlerProperties(cls.__getNotNoneConditionProperties(conditions), handlerFunction)
        cls.addHandlerPropertyToEventHadnlers(handlerProperties, pygame.USEREVENT)
