/* ===== ДАННЫЕ ===== */
// Данные встроены напрямую для избежания проблем с CORS
const MENU = [
  {
    "id": "item1",
    "cat": "Бургеры",
    "title": "Биф бургер",
    "desc": "Булочка бриошь , лист салата,фирменный соус , свежие помидоры , маринованные огурцы , говяжья котлета ,сыр",
    "price": 520,
    "img": "images/Бургеры/Биф бургер.png"
  },
  {
    "id": "item2",
    "cat": "Бургеры",
    "title": "Бургер с креветкой",
    "desc": "",
    "price": 490,
    "img": "images/Бургеры/Бургер с креветкой.jpg"
  },
  {
    "id": "item3",
    "cat": "Бургеры",
    "title": "Глейз бургер",
    "desc": "",
    "price": 420,
    "img": "images/Бургеры/Глейз бургер.jpg"
  },
  {
    "id": "item4",
    "cat": "Бургеры",
    "title": "Мега биф бургер",
    "desc": "",
    "price": 690,
    "img": "images/Бургеры/Мега биф бургер.jpg"
  },
  {
    "id": "item5",
    "cat": "Бургеры",
    "title": "Монблан бургер",
    "desc": "",
    "price": 560,
    "img": "images/Бургеры/Монблан бургер.jpg"
  },
  {
    "id": "item6",
    "cat": "Бургеры",
    "title": "Чизбургер",
    "desc": "",
    "price": 290,
    "img": "images/Бургеры/Чизбургер.jpg"
  },
  {
    "id": "item7",
    "cat": "Бургеры",
    "title": "Чикен чизбургер",
    "desc": "",
    "price": 250,
    "img": "images/Бургеры/Чикен чизбургер.jpg"
  },
  {
    "id": "item8",
    "cat": "Бургеры",
    "title": "Чикенбургер двойная котлета",
    "desc": "",
    "price": 680,
    "img": "images/Бургеры/Чикенбургер двойная котлета.jpg"
  },
  {
    "id": "item9",
    "cat": "Бургеры",
    "title": "Чикенбургер",
    "desc": "",
    "price": 450,
    "img": "images/Бургеры/Чикенбургер.jpg"
  },
  {
    "id": "item10",
    "cat": "Десерты",
    "title": "Донат с клубничной начинкой",
    "desc": "",
    "price": 150,
    "img": "images/Десерты/Донат с клубничной начинкой.jpg"
  },
  {
    "id": "item11",
    "cat": "Десерты",
    "title": "Донат с начинкой из малины и сливочного сыра",
    "desc": "",
    "price": 150,
    "img": "images/Десерты/Донат с начинкой из малины и сливочного сыра.jpg"
  },
  {
    "id": "item12",
    "cat": "Добавки в шаурму",
    "title": "Картофель фри",
    "desc": "",
    "price": 50,
    "img": "images/Добавки в шаурму/Картофель фри.jpg"
  },
  {
    "id": "item13",
    "cat": "Добавки в шаурму",
    "title": "Огурцы маринованные",
    "desc": "",
    "price": 30,
    "img": "images/Добавки в шаурму/Огурцы маринованные.jpg"
  },
  {
    "id": "item14",
    "cat": "Добавки в шаурму",
    "title": "Перец халапеньо",
    "desc": "",
    "price": 30,
    "img": "images/Добавки в шаурму/Перец халапеньо.jpg"
  },
  {
    "id": "item15",
    "cat": "Добавки в шаурму",
    "title": "Сыр",
    "desc": "",
    "price": 50,
    "img": "images/Добавки в шаурму/Сыр.jpg"
  },
  {
    "id": "item16",
    "cat": "Картофель фри",
    "title": "Картофель фри (2)",
    "desc": "",
    "price": 300,
    "img": "images/Картофель фри  соусы /Картофель фри (2).jpg"
  },
  {
    "id": "item17",
    "cat": "Картофель фри",
    "title": "Картофель фри",
    "desc": "",
    "price": 150,
    "img": "images/Картофель фри  соусы /Картофель фри.jpg"
  },
  {
    "id": "item18",
    "cat": "Картофель фри",
    "title": "Картофельные дольки (2)",
    "desc": "",
    "price": 320,
    "img": "images/Картофель фри  соусы /Картофельные дольки (2).jpg"
  },
  {
    "id": "item19",
    "cat": "Картофель фри",
    "title": "Картофельные дольки",
    "desc": "",
    "price": 160,
    "img": "images/Картофель фри  соусы /Картофельные дольки.jpg"
  },
  {
    "id": "item20",
    "cat": "Соусы",
    "title": "Соус сырный",
    "desc": "",
    "price": 35,
    "img": "images/Картофель фри  соусы /Соус сырный.jpg"
  },
  {
    "id": "item21",
    "cat": "Соусы",
    "title": "Соус томатный кетчуп",
    "desc": "",
    "price": 35,
    "img": "images/Картофель фри  соусы /Соус томатный кетчуп.jpg"
  },
  {
    "id": "item22",
    "cat": "Соусы",
    "title": "Соус чесночный",
    "desc": "",
    "price": 35,
    "img": "images/Картофель фри  соусы /Соус чесночный.jpg"
  },
  {
    "id": "item23",
    "cat": "Комбо",
    "title": "Комбо 1",
    "desc": "",
    "price": 1785,
    "img": "images/Комбо/Комбо 1.jpg"
  },
  {
    "id": "item24",
    "cat": "Комбо",
    "title": "Комбо 2",
    "desc": "",
    "price": 1715,
    "img": "images/Комбо/Комбо 2.jpg"
  },
  {
    "id": "item25",
    "cat": "Комбо",
    "title": "Комбо 3",
    "desc": "",
    "price": 1675,
    "img": "images/Комбо/Комбо 3.jpg"
  },
  {
    "id": "item26",
    "cat": "Комбо",
    "title": "Комбо 4",
    "desc": "",
    "price": 1435,
    "img": "images/Комбо/Комбо 4.jpg"
  },
  {
    "id": "item27",
    "cat": "Креветки в панировке",
    "title": "Кальмар палочки в панировке",
    "desc": "",
    "price": 280,
    "img": "images/Креветки в панировке/Кальмар палочки в панировке.jpg"
  },
  {
    "id": "item28",
    "cat": "Креветки в панировке",
    "title": "Кольца кальмара",
    "desc": "",
    "price": 280,
    "img": "images/Креветки в панировке/Кольца кальмара.jpg"
  },
  {
    "id": "item29",
    "cat": "Креветки в панировке",
    "title": "Креветки в панировке",
    "desc": "",
    "price": 390,
    "img": "images/Креветки в панировке/Креветки в панировке.jpg"
  },
  {
    "id": "item30",
    "cat": "Креветки в панировке",
    "title": "Креветочный шарики",
    "desc": "",
    "price": 390,
    "img": "images/Креветки в панировке/Креветочный шарики.jpg"
  },
  {
    "id": "item31",
    "cat": "Креветки в панировке",
    "title": "Луковые кольца",
    "desc": "",
    "price": 260,
    "img": "images/Креветки в панировке/Луковые кольца.jpg"
  },
  {
    "id": "item32",
    "cat": "Крылья",
    "title": "Крылья Баффало",
    "desc": "",
    "price": 290,
    "img": "images/Крылья/Крылья Баффало.jpg"
  },
  {
    "id": "item33",
    "cat": "Крылья",
    "title": "Крылья барбекью",
    "desc": "",
    "price": 280,
    "img": "images/Крылья/Крылья барбекью.jpg"
  },
  {
    "id": "item34",
    "cat": "Крылья",
    "title": "Крылья острые в панировке",
    "desc": "",
    "price": 290,
    "img": "images/Крылья/Крылья острые в панировке.jpg"
  },
  {
    "id": "item35",
    "cat": "Крылья",
    "title": "Куриный попкорн",
    "desc": "",
    "price": 260,
    "img": "images/Крылья/Куриный попкорн.jpg"
  },
  {
    "id": "item36",
    "cat": "Крылья",
    "title": "Наггетсы",
    "desc": "",
    "price": 280,
    "img": "images/Крылья/Наггетсы.jpg"
  },
  {
    "id": "item37",
    "cat": "Крылья",
    "title": "Стрипсы",
    "desc": "",
    "price": 300,
    "img": "images/Крылья/Стрипсы.jpg"
  },
  {
    "id": "item38",
    "cat": "Напитки",
    "title": "Американо с молоком",
    "desc": "",
    "price": 150,
    "img": "images/Напитки/Американо с молоком.jpg"
  },
  {
    "id": "item39",
    "cat": "Напитки",
    "title": "Американо",
    "desc": "",
    "price": 150,
    "img": "images/Напитки/Американо.jpg"
  },
  {
    "id": "item40",
    "cat": "Напитки",
    "title": "Капучино",
    "desc": "",
    "price": 150,
    "img": "images/Напитки/Капучино.jpg"
  },
  {
    "id": "item41",
    "cat": "Напитки",
    "title": "Латте макиато",
    "desc": "",
    "price": 150,
    "img": "images/Напитки/Латте макиато.jpg"
  },
  {
    "id": "item42",
    "cat": "Напитки",
    "title": "Латте",
    "desc": "",
    "price": 150,
    "img": "images/Напитки/Латте.jpg"
  },
  {
    "id": "item43",
    "cat": "Напитки",
    "title": "Макиатто",
    "desc": "",
    "price": 150,
    "img": "images/Напитки/Макиатто.jpg"
  },
  {
    "id": "item44",
    "cat": "Напитки",
    "title": "Флейт уайт",
    "desc": "",
    "price": 150,
    "img": "images/Напитки/Флейт уайт.jpg"
  },
  {
    "id": "item45",
    "cat": "Напитки",
    "title": "Эспрессо с молоком",
    "desc": "",
    "price": 150,
    "img": "images/Напитки/Эспрессо с молоком.jpg"
  },
  {
    "id": "item46",
    "cat": "Напитки",
    "title": "Эспрессо",
    "desc": "",
    "price": 150,
    "img": "images/Напитки/Эспрессо.jpg"
  },
  {
    "id": "item47",
    "cat": "Панини",
    "title": "Панини из куриного филе (2)",
    "desc": "",
    "price": 310,
    "img": "images/Панини/Панини из куриного филе (2).jpg"
  },
  {
    "id": "item48",
    "cat": "Панини",
    "title": "Панини из куриного филе",
    "desc": "",
    "price": 310,
    "img": "images/Панини/Панини из куриного филе.jpg"
  },
  {
    "id": "item49",
    "cat": "Панини",
    "title": "Панини из свинины",
    "desc": "",
    "price": 350,
    "img": "images/Панини/Панини из свинины.jpg"
  },
  {
    "id": "item50",
    "cat": "Панини",
    "title": "Панини с говядиной",
    "desc": "",
    "price": 340,
    "img": "images/Панини/Панини с говядиной.jpg"
  },
  {
    "id": "item51",
    "cat": "Панини",
    "title": "Панини с креветкой",
    "desc": "",
    "price": 340,
    "img": "images/Панини/Панини с креветкой.jpg"
  },
  {
    "id": "item52",
    "cat": "Пицца",
    "title": "Ветчина и грибы",
    "desc": "",
    "price": 640,
    "img": "images/Пицца/Ветчина и грибы.jpg"
  },
  {
    "id": "item53",
    "cat": "Пицца",
    "title": "Комба 1 с пиццей и закусками",
    "desc": "",
    "price": 1465,
    "img": "images/Пицца/Комба 1 с пиццей и закусками.jpg"
  },
  {
    "id": "item54",
    "cat": "Пицца",
    "title": "Комба 2 с пиццей и закусками",
    "desc": "",
    "price": 1605,
    "img": "images/Пицца/Комба 2 с пиццей и закусками.jpg"
  },
  {
    "id": "item55",
    "cat": "Пицца",
    "title": "Комба 3 с пиццей и закусками",
    "desc": "",
    "price": 2175,
    "img": "images/Пицца/Комба 3 с пиццей и закусками.jpg"
  },
  {
    "id": "item56",
    "cat": "Пицца",
    "title": "Комба 4 спицы и закусками",
    "desc": "",
    "price": 1735,
    "img": "images/Пицца/Комба 4 спицы и закусками.jpg"
  },
  {
    "id": "item57",
    "cat": "Пицца",
    "title": "Маргарита",
    "desc": "",
    "price": 630,
    "img": "images/Пицца/Маргарита.jpg"
  },
  {
    "id": "item58",
    "cat": "Пицца",
    "title": "Мясная",
    "desc": "",
    "price": 680,
    "img": "images/Пицца/Мясная.jpg"
  },
  {
    "id": "item59",
    "cat": "Пицца",
    "title": "Пепперони",
    "desc": "",
    "price": 610,
    "img": "images/Пицца/Пепперони.jpg"
  },
  {
    "id": "item60",
    "cat": "Пицца",
    "title": "Флорида",
    "desc": "",
    "price": 690,
    "img": "images/Пицца/Флорида.jpg"
  },
  {
    "id": "item61",
    "cat": "Пицца",
    "title": "Четыре сыра",
    "desc": "",
    "price": 660,
    "img": "images/Пицца/Четыре сыра.jpg"
  },
  {
    "id": "item62",
    "cat": "Роллы в тортилье",
    "title": "Баф чикен",
    "desc": "",
    "price": 330,
    "img": "images/Роллы в тортилье/Баф чикен.jpg"
  },
  {
    "id": "item63",
    "cat": "Роллы в тортилье",
    "title": "Биф биг ролл",
    "desc": "",
    "price": 380,
    "img": "images/Роллы в тортилье/Биф биг ролл.jpg"
  },
  {
    "id": "item64",
    "cat": "Роллы в тортилье",
    "title": "Мега баф чикен",
    "desc": "",
    "price": 430,
    "img": "images/Роллы в тортилье/Мега баф чикен.jpg"
  },
  {
    "id": "item65",
    "cat": "Роллы в тортилье",
    "title": "Мега биф биг ролл",
    "desc": "",
    "price": 560,
    "img": "images/Роллы в тортилье/Мега биф биг ролл.jpg"
  },
  {
    "id": "item66",
    "cat": "Роллы в тортилье",
    "title": "Цезарь ролл с креветкой",
    "desc": "",
    "price": 380,
    "img": "images/Роллы в тортилье/Цезарь ролл с креветкой.jpg"
  },
  {
    "id": "item67",
    "cat": "Роллы в тортилье",
    "title": "Цезарь ролл",
    "desc": "",
    "price": 350,
    "img": "images/Роллы в тортилье/Цезарь ролл.jpg"
  },
  {
    "id": "item68",
    "cat": "Роллы в тортилье",
    "title": "Чикен ролл",
    "desc": "",
    "price": 330,
    "img": "images/Роллы в тортилье/Чикен ролл.jpg"
  },
  {
    "id": "item69",
    "cat": "Салаты",
    "title": "Овощной",
    "desc": "",
    "price": 260,
    "img": "images/Салаты/Овощной.jpg"
  },
  {
    "id": "item70",
    "cat": "Салаты",
    "title": "Цезарь с креветкой",
    "desc": "",
    "price": 380,
    "img": "images/Салаты/Цезарь с креветкой.jpg"
  },
  {
    "id": "item71",
    "cat": "Салаты",
    "title": "Цезарь с курицей",
    "desc": "",
    "price": 340,
    "img": "images/Салаты/Цезарь с курицей.jpg"
  },
  {
    "id": "item72",
    "cat": "Сырные палочки",
    "title": "Медальоны из сулугуни",
    "desc": "",
    "price": 300,
    "img": "images/Сырные палочки/Медальоны из сулугуни.jpg"
  },
  {
    "id": "item73",
    "cat": "Сырные палочки",
    "title": "Сырные палочки",
    "desc": "",
    "price": 290,
    "img": "images/Сырные палочки/Сырные палочки.jpg"
  },
  {
    "id": "item74",
    "cat": "Сырные палочки",
    "title": "Сырные шарики",
    "desc": "",
    "price": 300,
    "img": "images/Сырные палочки/Сырные шарики.jpg"
  },
  {
    "id": "item75",
    "cat": "Хот дог",
    "title": "Ход дог гриль",
    "desc": "",
    "price": 290,
    "img": "images/Хот дог/Ход дог гриль.jpg"
  },
  {
    "id": "item76",
    "cat": "Хот дог",
    "title": "Ход дог",
    "desc": "",
    "price": 280,
    "img": "images/Хот дог/Ход дог.jpg"
  },
  {
    "id": "item77",
    "cat": "Хот дог",
    "title": "Хот дог Австрийский",
    "desc": "",
    "price": 290,
    "img": "images/Хот дог/Хот дог Австрийский.jpg"
  },
  {
    "id": "item78",
    "cat": "Хот дог",
    "title": "Чикен дог",
    "desc": "",
    "price": 300,
    "img": "images/Хот дог/Чикен дог.jpg"
  },
  {
    "id": "item79",
    "cat": "Чиабатта",
    "title": "Чиабатта с куриным попкорном",
    "desc": "",
    "price": 170,
    "img": "images/Чиабатта/ Чиабатта с куриным попкорном.jpg"
  },
  {
    "id": "item80",
    "cat": "Чиабатта",
    "title": "Чиабатта с беконом и сервелад",
    "desc": "",
    "price": 200,
    "img": "images/Чиабатта/Чиабатта с беконом и сервелад.jpg"
  },
  {
    "id": "item81",
    "cat": "Чиабатта",
    "title": "Чиабатта с беконом",
    "desc": "",
    "price": 180,
    "img": "images/Чиабатта/Чиабатта с беконом.jpg"
  },
  {
    "id": "item82",
    "cat": "Чиабатта",
    "title": "Чиабатта с ветчиной",
    "desc": "",
    "price": 160,
    "img": "images/Чиабатта/Чиабатта с ветчиной.jpg"
  },
  {
    "id": "item83",
    "cat": "Чиабатта",
    "title": "Чиабатта с колбасой сервелад",
    "desc": "",
    "price": 190,
    "img": "images/Чиабатта/Чиабатта с колбасой сервелад.jpg"
  },
  {
    "id": "item84",
    "cat": "Шаурма",
    "title": "Армянский гирос большой",
    "desc": "",
    "price": 500,
    "img": "images/ШаурмаГиросы/Армянский гирос большой.jpg"
  },
  {
    "id": "item85",
    "cat": "Шаурма",
    "title": "Армянский гирос маленький",
    "desc": "",
    "price": 350,
    "img": "images/ШаурмаГиросы/Армянский гирос маленький.jpg"
  },
  {
    "id": "item86",
    "cat": "Шаурма",
    "title": "Бртуч",
    "desc": "",
    "price": 320,
    "img": "images/ШаурмаГиросы/Бртуч.jpg"
  },
  {
    "id": "item87",
    "cat": "Шаурма",
    "title": "Вегетарианская большая",
    "desc": "",
    "price": 320,
    "img": "images/ШаурмаГиросы/Вегетарианская большая.jpg"
  },
  {
    "id": "item88",
    "cat": "Шаурма",
    "title": "Вегетарианская маленькая",
    "desc": "",
    "price": 220,
    "img": "images/ШаурмаГиросы/Вегетарианская маленькая.jpg"
  },
  {
    "id": "item89",
    "cat": "Шаурма",
    "title": "Куриная большая",
    "desc": "",
    "price": 350,
    "img": "images/ШаурмаГиросы/Куриная большая.jpg"
  },
  {
    "id": "item90",
    "cat": "Шаурма",
    "title": "Куриная маленькая",
    "desc": "",
    "price": 250,
    "img": "images/ШаурмаГиросы/Куриная маленькая.jpg"
  },
  {
    "id": "item91",
    "cat": "Шаурма",
    "title": "Свиная большая",
    "desc": "",
    "price": 350,
    "img": "images/ШаурмаГиросы/Свиная большая.jpg"
  },
  {
    "id": "item92",
    "cat": "Шаурма",
    "title": "Свиная маленькая",
    "desc": "",
    "price": 250,
    "img": "images/ШаурмаГиросы/Свиная маленькая.jpg"
  },
  {
    "id": "item93",
    "cat": "Шаурма",
    "title": "Шаурма много сыра",
    "desc": "",
    "price": 350,
    "img": "images/ШаурмаГиросы/Шаурма много сыра.jpg"
  },
  {
    "id": "item94",
    "cat": "Шаурма",
    "title": "Шаурма фирменная",
    "desc": "",
    "price": 350,
    "img": "images/ШаурмаГиросы/Шаурма фирменная.jpg"
  },
  {
    "id": "item95",
    "cat": "Шашлык",
    "title": "Люля-кебаб куриный",
    "desc": "",
    "price": 350,
    "img": "images/Шашлык/Люля-кебаб куриный.jpg"
  },
  {
    "id": "item96",
    "cat": "Шашлык",
    "title": "Свиной шашлык Карбонад",
    "desc": "",
    "price": 400,
    "img": "images/Шашлык/Свиной шашлык Карбонад.jpg"
  },
  {
    "id": "item97",
    "cat": "Шашлык",
    "title": "Свиной шашлык Шейка",
    "desc": "",
    "price": 440,
    "img": "images/Шашлык/Свиной шашлык Шейка.jpg"
  },
  {
    "id": "item98",
    "cat": "Шашлык",
    "title": "Шашлык из курицы",
    "desc": "",
    "price": 360,
    "img": "images/Шашлык/Шашлык из курицы.jpg"
  }
];

/* Промокоды */
const PROMOS = { 'SHAURMA10':0.10, 'WELCOME5':0.05 };

/* ==== Телеграм-отправка (подставь свои значения) ==== */
const TG_BOT_TOKEN = '8571037966:AAG2BMP4qqijdel9Mt3ktn4xkl2ncao31wU';
const TG_CHAT_ID   = '-1003250878681';

/* ===== СОСТОЯНИЕ ===== */
let state = {
  category: 'Шаурма',
  query: '',
  cart: {},
  discount: 0,
  profile: JSON.parse(localStorage.getItem('profile')||'{}'),
  orders: JSON.parse(localStorage.getItem('orders')||'[]')
};

const $ = (s,r=document)=>r.querySelector(s);
const $$ = (s,r=document)=>Array.from(r.querySelectorAll(s));
const price = v => `${v.toLocaleString('ru-RU')} ₽`;
function toast(msg){ const t=$('#toast'); t.textContent=msg; t.classList.add('show'); setTimeout(()=>t.classList.remove('show'),1600); }

/* ===== Telegram Mini App init + фолбэк ===== */
(function initTelegram(){
  try{
    if (window.Telegram && Telegram.WebApp){
      const tg = Telegram.WebApp;
      tg.ready();
      tg.expand && tg.expand();
      document.documentElement.style.setProperty('--tg-bg', tg.backgroundColor || '#0b0c0f');

      const u = tg.initDataUnsafe?.user;
      if (u){
        const was = JSON.parse(localStorage.getItem('profile')||'{}');
        const merged = {
          name: was.name || [u.first_name, u.last_name].filter(Boolean).join(' '),
          phone: was.phone || '',
          dob: was.dob || '',
          addr: was.addr || '',
          username: was.username || was.username
        };
        state.profile = merged;
        localStorage.setItem('profile', JSON.stringify(state.profile));
      }
      hideLoader();
    } else {
      // нет SDK → просто скрываем лоадер
      hideLoader();
    }
  }catch(e){
    console.warn('Telegram init error', e);
    hideLoader();
  }
})();
function hideLoader(){
  const loader = $('#loader');
  if (loader){
    loader.classList.add('hide');
    setTimeout(()=>loader.style.display='none', 400);
  }
}

/* ===== РЕНДЕР ===== */
function renderCats(){ $$('.cat').forEach(c=>c.classList.toggle('active', c.dataset.cat===state.category)); }
function filtered(){ return MENU.filter(i=>i.cat===state.category); }

function safeImgPath(p){
  if (!p) return '';
  // КЛЮЧЕВОЙ ФИКС: убираем случайные пробелы в сегментах пути
  return p.split('/').map(part => encodeURIComponent(part.trim())).join('/');
}

function renderGrid(){
  const grid = $('#grid'); grid.innerHTML='';
  filtered().forEach(d=>{
    const card = document.createElement('article');
    card.className = 'glass card tap';
    const imgPath = safeImgPath(d.img);
    card.innerHTML = `
      <div class="img"><img src="${imgPath}" alt="${d.title}"
           onerror="this.style.display='none';this.parentElement.innerHTML='🍽️';"></div>
      <div class="title">${d.title}</div>
      <div class="sub">${d.desc || ''}</div>
      <div class="rating">⭐ 4.${Math.floor(Math.random()*5)} • 30 мин</div>
      <div class="price-badge">${d.price > 0 ? price(d.price) : 'Цена уточняется'}</div>
      <button class="add tap" data-id="${d.id}">+</button>
    `;
    card.addEventListener('click', e=>{ if(!e.target.matches('.add')) openSheet(d); });
    card.querySelector('.add').addEventListener('click', e=>{
      e.stopPropagation();
      const id = e.currentTarget.dataset.id;
      state.cart[id]=(state.cart[id]||0)+1;
      updateBadge(); renderCart(); toast('Добавлено в корзину');
    });
    grid.appendChild(card);
  });
}
function updateBadge(){ $('#badge').textContent = Object.values(state.cart).reduce((a,b)=>a+b,0); }

/* ===== SHEET ===== */
let currentDish=null, sheetQty=1;
function openSheet(dish){
  currentDish=dish; sheetQty=1;
  $('#sheetImg').src = safeImgPath(dish.img);
  $('#sheetImg').onerror = function(){ this.style.display='none'; };
  $('#sheetTitle').textContent=dish.title;
  $('#sheetDesc').textContent=dish.desc || '';
  $('#sheetPrice').textContent=dish.price > 0 ? price(dish.price) : 'Цена уточняется';
  $('#qVal').textContent=sheetQty;
  $('#sheet').classList.add('show');
}
$('#sheetBack').addEventListener('click',()=>$('#sheet').classList.remove('show'));
$('#qPlus').addEventListener('click',()=>{
  sheetQty++; $('#qVal').textContent=sheetQty;
  $('#sheetPrice').textContent=currentDish.price > 0 ? price(currentDish.price*sheetQty) : 'Цена уточняется';
});
$('#qMinus').addEventListener('click',()=>{
  sheetQty=Math.max(1, sheetQty-1); $('#qVal').textContent=sheetQty;
  $('#sheetPrice').textContent=currentDish.price > 0 ? price(currentDish.price*sheetQty) : 'Цена уточняется';
});
$('#addToCart').addEventListener('click',()=>{
  state.cart[currentDish.id]=(state.cart[currentDish.id]||0)+sheetQty;
  updateBadge(); renderCart(); toast('Добавлено в корзину'); $('#sheet').classList.remove('show');
});

/* ===== КОРЗИНА ===== */
function renderCart(){
  const wrap = $('#cartList'); wrap.innerHTML='';
  const entries = Object.entries(state.cart);
  if (!entries.length){ wrap.innerHTML='<div class="muted" style="text-align:center;padding:20px">Корзина пуста</div>'; }
  let qty=0, sum=0;

  entries.forEach(([id,n])=>{
    const d = MENU.find(x=>x.id===id);
    qty += n;
    if (d.price > 0) sum += d.price*n;
    const row = document.createElement('div');
    row.className='cart-row';
    const priceText = d.price > 0 ? `${price(d.price)} × ${n} = <strong>${price(d.price*n)}</strong>` : `Цена уточняется × ${n}`;
    row.innerHTML=`
      <div>
        <div class="title" style="font-weight:800">${d.title}</div>
        <div class="tiny muted">${d.desc || ''}</div>
        <div class="tiny muted">${priceText}</div>
      </div>
      <div class="qty-sm">
        <button class="tap" data-a="dec" data-id="${id}">−</button>
        <span>${n}</span>
        <button class="tap" data-a="inc" data-id="${id}">+</button>
        <button class="tap" data-a="rm"  data-id="${id}" title="Удалить">✕</button>
      </div>
    `;
    wrap.appendChild(row);
  });

  $$('#cartList [data-a]').forEach(b=>{
    b.addEventListener('click', e=>{
      const id = e.currentTarget.dataset.id, a = e.currentTarget.dataset.a;
      if (a==='inc') state.cart[id]=(state.cart[id]||0)+1;
      if (a==='dec') state.cart[id]=Math.max(0,(state.cart[id]||0)-1);
      if (a==='rm')  delete state.cart[id];
      if (state.cart[id]===0) delete state.cart[id];
      updateBadge(); renderCart();
    });
  });

  const sale = Math.round(sum*state.discount);
  $('#sumQty').textContent = qty;
  $('#sumPrice').textContent = price(sum - sale);
  $('#saleNote').textContent = state.discount ? `Скидка ${Math.round(state.discount*100)}% − ${price(sale)}` : '';
}

/* ===== ОФОРМЛЕНИЕ (отправка в Telegram) ===== */
async function checkout(){
  const items = Object.entries(state.cart).map(([id,n])=>{
    const d = MENU.find(x=>x.id===id);
    return {title:d.title, qty:n, price:d.price, total:d.price*n};
  });
  if (!items.length){ toast('Корзина пуста'); return; }

  const sum = items.reduce((a,i)=>a+i.total,0);
  const sale = Math.round(sum*state.discount);
  const total = sum - sale;

  const p = state.profile||{};
  const comment = $('#comment').value||'';
  const text = [
    '🧾 *Новый заказ*',
    ...items.map(i=>`• ${i.title} × ${i.qty} — ${price(i.total)}`),
    '',
    state.discount?`Скидка: ${Math.round(state.discount*100)}% (−${price(sale)})`:'',
    `Итого: *${price(total)}*`,
    '',
    '👤 *Клиент*',
    `Имя: ${p.name||'—'}`,
    `Телефон: ${p.phone||'—'}`,
    `Дата рождения: ${p.dob||'—'}`,
    `Адрес: ${p.addr||'—'}`,
    comment?`\n💬 ${comment}`:''
  ].filter(Boolean).join('\n');

  const record = { date: Date.now(), items, finalSum: total, discount: state.discount, comment };

  if (TG_BOT_TOKEN.startsWith('PASTE_') || TG_CHAT_ID.startsWith('PASTE_')){
    toast('(Демо) Заказ оформлен');
  } else {
    try{
      const resp = await fetch(`https://api.telegram.org/bot${TG_BOT_TOKEN}/sendMessage`,{
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify({chat_id:TG_CHAT_ID,text,parse_mode:'Markdown'})
      });
      if (!resp.ok) throw new Error('HTTP '+resp.status);
      toast('Заказ отправлен');
    }catch(e){ console.error(e); toast('Ошибка отправки в Telegram'); }
  }

  state.orders = [...state.orders, record].slice(-20);
  localStorage.setItem('orders', JSON.stringify(state.orders));

  state.cart={}; state.discount=0; $('#promo').value=''; $('#comment').value='';
  updateBadge(); renderCart();
  $('#cart').classList.remove('open');
  $('#scrim').classList.remove('show');
}

/* ===== Профиль ===== */
function loadProfile(){
  const p = state.profile;
  $('#p_name').value = p.name||'';
  $('#p_phone').value = p.phone||'';
  $('#p_dob').value = p.dob||'';
  $('#p_addr').value = p.addr||'';
}

/* ===== ИНИТ + КЛИКИ ===== */
function init(){
  // категории
  $$('.cat').forEach(c=>c.addEventListener('click', ()=>{
    state.category=c.dataset.cat; renderCats(); renderGrid(); window.scrollTo({top:0,behavior:'smooth'});
  }));
  renderCats(); renderGrid(); updateBadge();

  // шторки + затемнение
  const openScrim = ()=>$('#scrim').classList.add('show');
  const closeScrim = ()=>$('#scrim').classList.remove('show');

  $('#btnMenu').addEventListener('click', ()=>{ $('#drawer').classList.add('open'); openScrim(); loadProfile(); });
  $('#drawerClose').addEventListener('click', ()=>{ $('#drawer').classList.remove('open'); closeScrim(); });

  $('#btnCart').addEventListener('click', ()=>{ $('#cart').classList.add('open'); openScrim(); renderCart(); });
  $('#cartClose').addEventListener('click', ()=>{ $('#cart').classList.remove('open'); closeScrim(); });

  $('#scrim').addEventListener('click', ()=>{
    $('#drawer').classList.remove('open');
    $('#cart').classList.remove('open');
    closeScrim();
  });

  // промокод
  $('#applyPromo').addEventListener('click', ()=>{
    const code = ($('#promo').value||'').trim().toUpperCase();
    state.discount = PROMOS[code] || 0;
    renderCart();
    toast(state.discount ? 'Промокод применён' : 'Промокод не найден');
  });

  // профиль
  $('#saveProfile').addEventListener('click', ()=>{
    state.profile={
      name:$('#p_name').value.trim(),
      phone:$('#p_phone').value.trim(),
      dob:$('#p_dob').value,
      addr:$('#p_addr').value.trim()
    };
    localStorage.setItem('profile', JSON.stringify(state.profile));
    toast('Профиль сохранён');
  });

  // оформление
  $('#btnCheckout').addEventListener('click', checkout);
}

// старт
document.addEventListener('DOMContentLoaded', init);

