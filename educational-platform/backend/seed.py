import os
os.environ['DATABASE_URL'] = 'postgresql://admin:password@localhost:5432/eduplatform'

from database import SessionLocal, init_db
from models import Article
from rag.embeddings import embed_text

# Educational content for each section and language
SEED_DATA = {
    "math": {
        "en": [
            {
                "title": "Algebra Basics",
                "body": "Algebra is a branch of mathematics dealing with symbols and the rules of manipulating those symbols. Variables are symbols that represent unknown values, usually denoted by letters like x, y, or z. Equations are statements that two expressions are equal. For example, 2x + 3 = 7 is an algebraic equation where we need to find the value of x. The solution is x = 2. Algebraic expressions can be simplified using the order of operations: Parentheses, Exponents, Multiplication and Division (left to right), and Addition and Subtraction (left to right)."
            },
            {
                "title": "Pythagorean Theorem",
                "body": "The Pythagorean theorem states that in a right triangle, the square of the hypotenuse (the side opposite the right angle) is equal to the sum of the squares of the other two sides. The formula is: a² + b² = c², where c is the hypotenuse and a and b are the other two sides. For example, if a triangle has sides of length 3 and 4, the hypotenuse will have length √(3² + 4²) = √(9 + 16) = √25 = 5. This theorem is fundamental in geometry and has many practical applications in construction, navigation, and physics."
            },
            {
                "title": "Introduction to Calculus and Derivatives",
                "body": "Calculus is the mathematical study of continuous change. A derivative measures how a function changes as its input changes. The derivative of a function f(x) at a point x tells us the slope of the function at that point. Notation: f'(x) or df/dx. For a simple power function f(x) = x², the derivative is f'(x) = 2x. Derivatives are used to find maximum and minimum values of functions, calculate rates of change in physics, and optimize solutions in engineering and economics. The process of finding a derivative is called differentiation."
            }
        ],
        "uz": [
            {
                "title": "Algebra Asoslari",
                "body": "Algebra matematikaning belgili va ularning belgilari bilan ishlash qoidalaridan iborat bo'limi. O'zgaruvchilar noma'lum qiymatlarni ifodalovchi belgiler bo'lib, odatda x, y yoki z harflari bilan belgilanadi. Tenglamalar ikkita ifodaning teng ekanligini ko'rsatadigan gaplardir. Masalan, 2x + 3 = 7 algebraik tenglama bo'lib, x ning qiymatini topish kerak. Yechim x = 2 ga teng. Algebraik ifodalar operatsiyalar tartibidan foydalanib soddalashtiriladigan bo'ldir: Qavslar, Darajalar, Ko'paytirish va Bo'lish (chapdan o'ngga), va Qo'shish va Ayirish (chapdan o'ngga)."
            },
            {
                "title": "Pifagor Teoremasi",
                "body": "Pifagor teoremasi to'g'ri uchburchakda gipotenuza kvadrati (to'g'ri burchakka qarama-qarshi bo'lgan tomon) qolgan ikki tomonning kvadratlari yig'indisiga teng ekanligini aytadi. Formula: a² + b² = c², bu yerda c gipotenuza va a va b qolgan ikki tomon. Masalan, uchburchakning tomonlari 3 va 4 bo'lsa, gipotenuza √(3² + 4²) = √(9 + 16) = √25 = 5 bo'ladi. Bu teorema geometriyada asosiy va qurilish, navigatsiya va fizikada ko'p praktik qo'llanmalarga ega."
            },
            {
                "title": "Analiz va Hosilalar",
                "body": "Analiz doimiy o'zgarishning matematik o'rganishidir. Hosila funksiya kirishi o'zgargani sayin funksiya o'zgarishini ifodalaydi. f(x) funksiyasining x nuqtasidagi hosilasi funksiyaning o'sha nuqtasidagi qiyaligi bilan bog'liq. Belgilash: f'(x) yoki df/dx. Oddiy daraja funktsilari uchun f(x) = x², hosila f'(x) = 2x. Hosilalar funksiyalarning maksimal va minimal qiymatlarini topish, fizikada o'zgarish tezligini hisoblash va muhandislik va iqtisodda yechimlarni optimallashtirish uchun ishlatiladi."
            }
        ],
        "ru": [
            {
                "title": "Основы Алгебры",
                "body": "Алгебра — это раздел математики, изучающий символы и правила манипулирования этими символами. Переменные — это символы, представляющие неизвестные значения, обычно обозначаемые буквами x, y или z. Уравнения — это утверждения о равенстве двух выражений. Например, 2x + 3 = 7 — это алгебраическое уравнение, в котором нужно найти значение x, равное 2. Алгебраические выражения упрощаются с использованием порядка операций: скобки, степени, умножение и деление (слева направо), сложение и вычитание (слева направо)."
            },
            {
                "title": "Теорема Пифагора",
                "body": "Теорема Пифагора утверждает, что в прямоугольном треугольнике квадрат гипотенузы (стороны, противолежащей прямому углу) равен сумме квадратов двух других сторон. Формула: a² + b² = c², где c — гипотенуза, а a и b — два других стороны. Например, если треугольник имеет стороны длиной 3 и 4, гипотенуза будет √(3² + 4²) = √(9 + 16) = √25 = 5. Эта теорема является фундаментальной в геометрии и имеет множество практических приложений в строительстве, навигации и физике."
            },
            {
                "title": "Введение в Анализ и Производные",
                "body": "Анализ — это математическое изучение непрерывных изменений. Производная показывает, как функция меняется при изменении её входных значений. Производная функции f(x) в точке x показывает наклон функции в этой точке. Обозначение: f'(x) или df/dx. Для простой степенной функции f(x) = x² производная равна f'(x) = 2x. Производные используются для нахождения максимальных и минимальных значений функций, расчета скоростей изменения в физике и оптимизации решений в инженерии и экономике."
            }
        ]
    },
    "programming": {
        "en": [
            {
                "title": "Python Variables and Data Types",
                "body": "A variable is a named container that stores a value in your program. In Python, you create a variable by assigning a value to a name. Example: name = 'Alice' or age = 25. Python has several basic data types: strings (text), integers (whole numbers), floats (decimal numbers), and booleans (True/False). Example code: count = 5, text = 'Hello World', is_active = True. Variables are case-sensitive, so Name and name are different variables. Variable names should be descriptive and use lowercase with underscores, like user_name instead of un. You can check a variable's type using type(variable)."
            },
            {
                "title": "Loops in Python",
                "body": "Loops allow you to repeat code multiple times. The for loop iterates over a sequence of items. Example: for i in range(5): print(i) prints 0, 1, 2, 3, 4. The while loop repeats code while a condition is true. Example: count = 0; while count < 5: print(count); count += 1. The break statement exits the loop immediately. The continue statement skips to the next iteration. Example with break: for i in range(10): if i == 5: break; print(i) stops when i equals 5. Loops are essential for processing lists of data, generating sequences, and automating repetitive tasks."
            },
            {
                "title": "Functions in Python",
                "body": "A function is a reusable block of code that performs a specific task. Define a function using def: def greet(name): return 'Hello, ' + name. Call it with greet('Alice'). Functions accept parameters (inputs) and return values (outputs). Example: def add(a, b): return a + b; result = add(3, 4) stores 7 in result. Default parameters: def greet(name='Guest'): return 'Hello, ' + name makes name optional. Functions help organize code, reduce repetition, and make programs easier to understand. Always give functions descriptive names that explain what they do."
            }
        ],
        "uz": [
            {
                "title": "Python O'zgaruvchilari va Ma'lumot Turlari",
                "body": "O'zgaruvchi nomli xona bo'lib, u dasturda qiymatni saqlaydi. Python da, siz o'zgaruvchi yaratish uchun nomsiz qiymat tayinlaysiz. Misol: name = 'Ali' yoki age = 25. Python da bir necha asosiy ma'lumot turlari bor: satrlar (matn), butun raqamlar (butun raqamlar), o'nlik raqamlar (o'nlik raqamlar) va mantiqiy qiymatlar (To'g'ri/Noto'g'ri). Misol kodi: count = 5, text = 'Hello World', is_active = True. O'zgaruvchilar harfga sezgir, shuning uchun Name va name turli o'zgaruvchilardir. O'zgaruvchi nomlari tavsiflash kerak va pastki chiziqlar bilan kichik harflardan foydalaning, masalan user_name o'rniga un. type(variable) dan foydalanib o'zgaruvchining turini tekshirishingiz mumkin."
            },
            {
                "title": "Python da Sikllar",
                "body": "Sikllar kodni bir necha marta takrorlash imkonini beradi. For sikli ketma-ketlik elementlari bo'ylab takrorlanadi. Misol: for i in range(5): print(i) 0, 1, 2, 3, 4 chop etadi. While sikli shart to'g'ri bo'lgan vaqtda kodni takrorlaydi. Misol: count = 0; while count < 5: print(count); count += 1. break operatori siklni darhol chiqaradi. continue operatori keyingi iteratsiyaga o'tadi. break bilan misol: for i in range(10): if i == 5: break; print(i) i 5 ga teng bo'lganda to'xtaydi. Sikllar ma'lumotlar ro'yxatini qayta ishlash, ketma-ketlikni yaratish va takroriy vazifalarni avtomatlashtirish uchun zarur."
            },
            {
                "title": "Python da Funksiyalar",
                "body": "Funksiya ma'lum bir vazifani bajaradigan qayta foydalanish mumkin bo'lgan kod blokidir. def dan foydalanib funksiya belgilang: def greet(name): return 'Hello, ' + name. greet('Ali') bilan chaqiring. Funksiyalar parametrlarni (kirishlari) qabul qiladi va qiymatlarni (chiqarishlari) qaytaradi. Misol: def add(a, b): return a + b; result = add(3, 4) natijaga 7 saqlab qo'yadi. Standart parametrlar: def greet(name='Guest'): return 'Hello, ' + name name ni ixtiyoriy qiladi. Funksiyalar kodni tartibga soladi, takrorlanishni kamaytiradi va dasturlarni tushun."
            }
        ],
        "ru": [
            {
                "title": "Переменные и Типы Данных в Python",
                "body": "Переменная — это именованный контейнер, который хранит значение в вашей программе. В Python вы создаёте переменную, присваивая значение имени. Пример: name = 'Алиса' или age = 25. Python имеет несколько основных типов данных: строки (текст), целые числа, числа с плавающей точкой и булевы значения (истина/ложь). Пример кода: count = 5, text = 'Hello World', is_active = True. Переменные чувствительны к регистру, поэтому Name и name — разные переменные. Имена переменных должны быть описательными и использовать нижний регистр с подчёркиваниями, например user_name вместо un. Вы можете проверить тип переменной с помощью type(variable)."
            },
            {
                "title": "Циклы в Python",
                "body": "Циклы позволяют повторить код несколько раз. Цикл for повторяется для каждого элемента в последовательности. Пример: for i in range(5): print(i) выведет 0, 1, 2, 3, 4. Цикл while повторяет код, пока условие верно. Пример: count = 0; while count < 5: print(count); count += 1. Оператор break выходит из цикла. Оператор continue переходит к следующей итерации. Пример с break: for i in range(10): if i == 5: break; print(i) останавливается, когда i равно 5. Циклы необходимы для обработки списков данных, генерирования последовательностей и автоматизации повторяющихся задач."
            },
            {
                "title": "Функции в Python",
                "body": "Функция — это переиспользуемый блок кода, который выполняет определённую задачу. Определите функцию с помощью def: def greet(name): return 'Hello, ' + name. Вызовите её с greet('Алиса'). Функции принимают параметры (входные данные) и возвращают значения (выходные данные). Пример: def add(a, b): return a + b; result = add(3, 4) сохраняет 7 в результате. Параметры по умолчанию: def greet(name='Guest'): return 'Hello, ' + name делает name необязательным. Функции помогают организовать код, снизить повторение и сделать программы более понятными. Всегда давайте функциям описательные имена, которые объясняют, что они делают."
            }
        ]
    },
    "science": {
        "en": [
            {
                "title": "Newton's Laws of Motion",
                "body": "Isaac Newton's three laws of motion form the foundation of classical mechanics. The First Law states that an object at rest stays at rest, and an object in motion stays in motion unless acted upon by a force. The Second Law states that Force equals mass times acceleration (F = ma). A larger force produces greater acceleration, and a more massive object requires more force for the same acceleration. The Third Law states that for every action, there is an equal and opposite reaction. When you push a wall, the wall pushes back with equal force. These laws explain how objects move and interact with forces in the everyday world."
            },
            {
                "title": "The Periodic Table Basics",
                "body": "The periodic table organizes all known chemical elements by atomic number and chemical properties. Each element is represented by a one or two-letter symbol, like H for hydrogen, O for oxygen, and Fe for iron. Elements are arranged in rows (periods) and columns (groups). Elements in the same group have similar chemical properties. The table is divided into different blocks: metals (left side), non-metals (right side), and metalloids (middle). Atomic number tells how many protons an atom has, determining its chemical behavior. For example, carbon has atomic number 6, found in all living organisms. Understanding the periodic table helps predict how elements will react with each other."
            },
            {
                "title": "Cell Structure and Function",
                "body": "All living organisms are made of cells, the basic units of life. There are two main types: prokaryotic cells (no nucleus, like bacteria) and eukaryotic cells (have a nucleus, like plant and animal cells). A cell nucleus contains DNA and controls cell activities. The cytoplasm is the gel-like substance inside the cell where organelles float. The cell membrane controls what enters and exits the cell. Mitochondria produce energy for the cell through cellular respiration. In plant cells, chloroplasts capture light energy for photosynthesis. The endoplasmic reticulum and Golgi apparatus transport and process proteins. Understanding cell structure is essential for studying biology, genetics, and medicine."
            }
        ],
        "uz": [
            {
                "title": "Nyutonning Harakat Qonunlari",
                "body": "Isaak Nyutonning uchta harakat qonuni klassik mexanikaning asosini tashkil etadi. Birinchi qonun shundan iboratki, tinch holda bo'lgan jism tin qoladi va harakat qilyotgan jism kuch ta'sir etmagida harakat qilishda davom etadi. Ikkinchi qonun aytadi ki, Kuch massa vaqt tezlanishiga teng (F = ma). Kattaroq kuch ko'proq tezlanish beradi va og'ir jism bir xil tezlanish uchun ko'proq kuchni talab qiladi. Uchinchi qonun aytadi ki, har bir harakat uchun teng va qarama-qarshi reaksiya bor. Divarni itarayotgan bo'lsangiz, devor teng kuch bilan qaytaradi. Bu qonunlar kundalik olamda jismlar qanday harakat qilishi va kuchlar bilan o'zaro ta'sir qilishini tushuntiradi."
            },
            {
                "title": "Davriy Jadval Asoslari",
                "body": "Davriy jadval barcha ma'lum kimyoviy elementlarni atom raqami va kimyoviy xususiyatlari bo'ylab tartibga soladi. Har bir element bir yoki ikkita harfli belgisi bilan ifodalanadi, masalan H vodorod, O kislorod va Fe temir uchun. Elementlar qatorlar (davrlar) va ustunlar (guruhlar) bo'ylab joylashgan. Bir guruhda joylashgan elementlar o'xshash kimyoviy xususiyatlarga ega. Jadval turli bloklarga bo'linadi: metallar (chap tomon), metalmas (o'ng tomon) va metalloidlar (o'rta). Atom raqami atomda nechta proton borligini ko'rsatadi, uning kimyoviy harakatiga aniqlaydi. Masalan, uglerod atom raqami 6 va barcha tirik organizmlarida topiladi. Davriy jadvalni tushunish elementlarning bir-birlari bilan qanday reaksiya berish ekanligini bashorat qilishga yordam beradi."
            },
            {
                "title": "Hujayra Tuzilishi va Vazifasi",
                "body": "Barcha tirik organizmlar hujayra tashkil etiladi, bu hayotning asosiy birligi. Ikki asosiy tur bor: prokaryotik hujayra (jadval yo'q, bakteriya kabi) va eukaryotik hujayra (jadval bor, o'simlik va hayvon hujayralari kabi). Hujayra yadro DNKni saqlaydi va hujayra faoliyatini nazorat qiladi. Sitoplazma hujayra ichidagi jel-qatlamida organellalar yuzadi. Hujayra membranasi hujayra ichiga va tashqariga kirish-chiqishni nazorat qiladi. Mitoxondriyalar hujayra respiratsiyasi orqali hujayra uchun energiya ishlab chiqaradi. O'simlik hujayralarda xloroplastlar fotosintez uchun yorug'lik energiyasini tutadi. Endoplazmatik retikulyum va Golji apparati oqsillarni tashiyadi va qayta ishlaydi. Hujayra tuzilishini tushunish biologiya, genetika va tibb talaasini o'rganish uchun muhimdir."
            }
        ],
        "ru": [
            {
                "title": "Законы Движения Ньютона",
                "body": "Три закона движения Исаака Ньютона составляют основу классической механики. Первый закон гласит, что объект в покое остаётся в покое, а объект в движении остаётся в движении, пока на него не действует сила. Второй закон гласит, что сила равна массе, умноженной на ускорение (F = ma). Большая сила производит большее ускорение, а более массивный объект требует больше силы для одинакового ускорения. Третий закон гласит, что на каждое действие приходится равное и противоположное противодействие. Когда вы толкаете стену, стена толкает вас равной силой. Эти законы объясняют, как объекты движутся и взаимодействуют с силами в окружающем мире."
            },
            {
                "title": "Основы Периодической Таблицы",
                "body": "Периодическая таблица организует все известные химические элементы по атомному номеру и химическим свойствам. Каждый элемент обозначается одно- или двухбуквенным символом, например H для водорода, O для кислорода и Fe для железа. Элементы расположены в строках (периоды) и столбцах (группы). Элементы в одной группе имеют похожие химические свойства. Таблица разделена на различные блоки: металлы (левая сторона), неметаллы (правая сторона) и металлоиды (середина). Атомный номер показывает количество протонов в атоме, определяя его химическое поведение. Например, углерод имеет атомный номер 6 и находится во всех живых организмах. Понимание периодической таблицы помогает предсказать, как элементы будут реагировать друг с другом."
            },
            {
                "title": "Строение и Функция Клеток",
                "body": "Все живые организмы состоят из клеток, являющихся основной единицей жизни. Существует два основных типа: прокариотические клетки (без ядра, как бактерии) и эукариотические клетки (с ядром, как растительные и животные клетки). Ядро клетки содержит ДНК и контролирует деятельность клетки. Цитоплазма — это желеобразное вещество внутри клетки, где взвешены органеллы. Клеточная мембрана контролирует, что входит и выходит из клетки. Митохондрии вырабатывают энергию для клетки путём клеточного дыхания. В растительных клетках хлоропласты захватывают световую энергию для фотосинтеза. Эндоплазматический ретикулум и аппарат Гольджи транспортируют и обрабатывают белки. Понимание строения клетки необходимо для изучения биологии, генетики и медицины."
            }
        ]
    },
    "history": {
        "en": [
            {
                "title": "World War I Timeline",
                "body": "World War I lasted from 1914 to 1918, reshaping the world. In June 1914, Archduke Franz Ferdinand was assassinated in Sarajevo, triggering a chain reaction of declarations of war. Austria-Hungary declared war on Serbia, Russia supported Serbia, Germany declared war on Russia and France, and Britain joined when Germany invaded Belgium. The war introduced trench warfare and new weapons like tanks, planes, and poison gas, causing unprecedented casualties. The Eastern Front between Germany and Russia saw Russia's eventual withdrawal in 1917 after the Bolshevik Revolution. In 1917, the United States entered the war, tipping the balance towards the Allies. The war ended in 1918 with an armistice. The Treaty of Versailles in 1919 imposed harsh penalties on Germany, leading to resentment that would fuel World War II."
            },
            {
                "title": "Ancient Civilizations: Egypt and Mesopotamia",
                "body": "Ancient Egypt, flourishing along the Nile River for over 3,000 years, created one of history's greatest civilizations. The Egyptians built pyramids as tombs for pharaohs, developed hieroglyphic writing, and advanced mathematics and medicine. The civilization lasted from around 3100 BCE until 30 BCE when Rome conquered Egypt. Mesopotamia, nestled between the Tigris and Euphrates rivers, was home to Sumer, Akkad, Babylon, and Assyria. Sumer developed cuneiform, one of the earliest forms of writing around 3200 BCE. Babylon, under King Hammurabi (1792-1750 BCE), created the Code of Hammurabi, an early legal system. Both civilizations contributed foundational knowledge in astronomy, agriculture, government, and law."
            },
            {
                "title": "The Middle Ages and Feudalism",
                "body": "The Middle Ages, roughly 500-1500 CE, followed the fall of the Western Roman Empire. Society was organized through feudalism, a hierarchical system where peasants worked land owned by lords in exchange for protection. The feudal pyramid had the King at the top, nobles below, knights as warriors, and peasants at the bottom. The Catholic Church held enormous power, and cathedrals dominated medieval skylines. Education was limited to the clergy and nobility. Life expectancy was low due to disease, war, and poor living conditions. The period saw the development of chivalry, where knights followed codes of honour. The lack of centralized authority made the Middle Ages a time of constant warfare between feudal lords. The period ended with the Renaissance and the emergence of nation-states."
            }
        ],
        "uz": [
            {
                "title": "Birinchi Jahon Urushi Xronologiyasi",
                "body": "Birinchi Jahon Urushi 1914-1918 yillar oralig'ida bo'lib, dunyoni o'zgartirib yubordi. 1914 yil iyun oyida Avstriya-Vengriya arxiyerkasazodasi Frans Ferdinand Sarayevoda qotilga yo'l qo'yildi va bu urush e'lonlarining zanjir reaktsiyasini keltirib chiqardi. Avstriya-Vengriya Serbiyaga urush e'lon qildi, Rossiya Serbiyani qo'llab-quvvatladi, Germaniya Rossiya va Frantsiyaga urush e'lon qildi va Britaniya Germaniya Belgikani bosib olganida qo'shildi. Urush okopa urushlari va tanklari, samolyotlari va xorun gazini kabi yangi qurollari keltirib chiqardi, bunga oqibatda kutilmagani ko'p o'limlar bo'ldi. Germaniya va Rossiya orasidagi Sharqiy Front Rossiyaning 1917 yildagi Bolshevistik Inqilobdan so'ng chiqishi bilan ko'rildi. 1917 yilda Qo'shma Shtatlari urushlarga kirishdi va bu muyasson Ittifoq tomoniga surtildi. Urush 1918 yilda armistis bilan tugatildi. 1919 yilning Versalya shartnomalı Germanyaga qattiq jazo qo'llamasida, bu esa Ikkinchi Jahon Urushiga zamin yaratdi."
            },
            {
                "title": "Qadimiy Tsivilizatsiyalar: Misr va Mesopotamiya",
                "body": "Nil daryo'si bo'ylab 3000 yildan ortiq mavsumda ko'kmalgan Qadimiy Misr tarixning eng katta tsivilizatsiyalaridan birini yaratdi. Misrlilar fir'avnlari uchun mazolalar sifatida piramidalarni qurilishdi, ieroglifik yozuvini ishlab chiqdilar va matematika va tibbni rivaji qildilar. Tsivilizatsiya taxminan i.a. 3100 yildan i.a. 30 yilg'acha davom etdi, keyingi Rim Misr ni bosib oldi. Mesopotamiya Tigr va Efrat daryo'lari orasida joylashgan bo'lib, Shumer, Akkad, Babilon va Assiriya turmaning joylashgan edi. Shumer i.a. 3200 yill atrofida yozuvning eng birinchi shakllaridan biri bo'lgan kuniform yozuvni ishlab chiqdi. Babilon, Qirol Xammurapining (1792-1750 i.a.) davrusida Code Xammurapisi yaratildi, bu erta qonun tizimi edi. Ikkala tsivilizatsiya astronomiya, qishloq xo'jaligi, hukumat va qonunda asosiy bilim qo'shnasida ko'mak berdi."
            },
            {
                "title": "O'rta Asrlar va Feodalizm",
                "body": "O'rta Asrlar, taxminan 500-1500 i.a., G'arb Rim Imperiyasining qulavidan so'ng bo'ldi. Jamiyat feodalizm orqali tartibga solingan bo'lib, bu qaroq o'simlarning yerda ishlashgan bo'lib, ijara sohibi tomonidan himoya olish uchun omborga ishonishdan iborat edi. Feodal piramidani tepasida Qirol, pastda xoralari, jangchilar sifatida ritsarlar va pastda o'simlar turgan. Katolik Cherkovasi juda katta kuchga ega edi va katedrallari o'rta asrllarning ko'zni hosil qildi. Ta'lim ruhoniylar va xoralarga cheklangan edi. Umrning o'rtacha davomiyligi kasallik, urush va yomon yashash sharoitiga ko'ra pastro edi. Ushbu davrda ritsarlar faxri ta'rifning kodekslari bo'ylab ko'rsatilgan bo'lib, ritsarlik rivojlandi. Markazlashgan hokimiyatning yo'qligi o'rta asrlarni feodal xoralari orasidagi doimiy urush davriga aylantirdi. Davrni Yana tug'ilish va milliy shtat shaharining paydo bo'lishi bilan tugatildi."
            }
        ],
        "ru": [
            {
                "title": "Хронология Первой Мировой Войны",
                "body": "Первая мировая война длилась с 1914 по 1918 год, переформатировав мир. В июне 1914 года эрцгерцог Франц Фердинанд был убит в Сараеве, что спровоцировало цепь реакции объявления войны. Австро-Венграя объявила войну Сербии, Россия поддержала Сербию, Германия объявила войну России и Франции, а Британия присоединилась, когда Германия вторглась в Бельгию. Война привела к окопной войне и новому оружию, такому как танки, самолёты и ядовитый газ, вызвав беспрецедентные потери. На Восточном фронте между Германией и Россией произошло её выход из войны в 1917 году после большевистской революции. В 1917 году США вступили в войну, повернув ситуацию в пользу Союзников. Война закончилась перемирием в 1918 году. Версальский договор в 1919 году наложил суровые штрафы на Германию, вызвав возмущение, которое станет топливом для Второй мировой войны."
            },
            {
                "title": "Древние Цивилизации: Египет и Месопотамия",
                "body": "Древний Египет, процветавший вдоль Нила более 3000 лет, создал одну из величайших цивилизаций в истории. Египтяне строили пирамиды как гробницы фараонов, разработали иероглифическое письмо и делали успехи в математике и медицине. Цивилизация существовала с около 3100 года до н.э. до 30 года до н.э., когда Рим завоевал Египет. Месопотамия, расположенная между реками Тигр и Евфрат, была домом для Шумера, Аккада, Вавилона и Ассирии. Шумер разработал клинопись, одну из самых ранних форм письма около 3200 года до н.э. Вавилон при царе Хаммурапи (1792-1750 до н.э.) создал Законник Хаммурапи, раннюю систему права. Обе цивилизации внесли основополагающий вклад в астрономию, сельское хозяйство, управление и право."
            },
            {
                "title": "Средние Века и Феодализм",
                "body": "Средние века, примерно 500-1500 года нашей эры, последовали за падением Западной Римской империи. Общество было организовано через феодализм, иерархическую систему, где крестьяне работали на земле, принадлежащей лордам, в обмен на защиту. Феодальная пирамида имела короля на вершине, дворян ниже, рыцарей в качестве воинов и крестьян в основании. Католическая церковь обладала огромной властью, и соборы доминировали в средневековом пейзаже. Образование было ограничено духовенством и знатью. Продолжительность жизни была низкой из-за болезней, войн и плохих условий жизни. Период был отмечен развитием рыцарства, где рыцари следовали кодексам чести. Отсутствие централизованной власти сделало Средние века временем постоянных войн между феодальными лордами. Период закончился с Ренессансом и появлением национальных государств."
            }
        ]
    },
    "languages": {
        "en": [
            {
                "title": "English Grammar: Parts of Speech",
                "body": "English grammar is built on eight parts of speech: nouns, pronouns, verbs, adjectives, adverbs, prepositions, conjunctions, and interjections. A noun is a person, place, or thing (e.g., teacher, school, book). A pronoun replaces a noun (he, she, it, they). A verb is an action or state of being (run, jump, is). An adjective describes a noun (big, small, beautiful). An adverb modifies a verb or adjective (quickly, slowly, very). A preposition shows relationships (in, on, under, between). A conjunction connects words or ideas (and, but, or). An interjection expresses emotion (oh, wow, ouch). Understanding these parts helps you construct grammatically correct sentences and communicate clearly. Every sentence needs at least a noun and a verb to be complete."
            },
            {
                "title": "Literary Terms and Devices",
                "body": "Literature uses many devices to create meaning and emotion. A metaphor compares two unlike things without using 'like' or 'as' (e.g., 'time is money'). A simile uses 'like' or 'as' to compare (e.g., 'as brave as a lion'). Personification gives human qualities to non-human things (e.g., 'the wind whispered'). Imagery uses sensory details to create vivid descriptions. Foreshadowing hints at future events. A flashback interrupts the story to show past events. Irony occurs when reality is opposite to expectation. Symbolism uses objects or actions to represent deeper meanings (e.g., a dove for peace). Alliteration repeats initial consonant sounds (e.g., 'Sally sells seashells'). Understanding these devices helps you appreciate literature and analyze texts deeply."
            },
            {
                "title": "Effective Writing Tips",
                "body": "Good writing requires clarity, organization, and revision. Start with a clear purpose: what do you want your reader to understand? Organize your thoughts into an outline before writing. Use simple, direct language instead of complex words. Break long paragraphs into shorter ones for easier reading. Use active voice (the cat chased the mouse) instead of passive voice (the mouse was chased by the cat). Vary your sentence structure to maintain interest. Show, don't tell: instead of 'she was sad,' write 'tears rolled down her cheeks.' Read your work aloud to catch awkward phrasing. Proofread for spelling and grammar errors. Get feedback from others before finalizing your work. Remember, good writing is revising until your message is crystal clear."
            }
        ],
        "uz": [
            {
                "title": "Ingliz Tili Grammatikasi: So'z Turlari",
                "body": "Ingliz tili grammatikasi sakkiz so'z turiga asoslangan: ot, almashtiruvchi, fe'l, sifat, ravish, predlog, bog'lovchi va unday so'zlar. Ot odam, joy yoki nars'a bo'lib, masalan, o'qituvchi, maktab, kitob. Almashtiruvchi otning o'rnida o'tadi: u, u, u, ular. Fe'l harakat yoki bo'lish holati bo'lib, masalan, yugur, sakra, bu. Sifat otni tavsiflaydi, masalan, katta, kichkina, go'zal. Ravish fe'l yoki sifatni o'zgartiraydi, masalan, tezlik bilan, asta, juda. Predlog munosabatlarni ko'rsatadi: ichida, tepada, pastda, orasida. Bog'lovchi so'zlar yoki fikrlarni bog'laydi: va, lekin, yoki. Unday so'zlar hissni ifodalaydi: oh, vao, och. Bu so'z turlarini tushunish grammatik to'g'ri gaplarni tuzish va aniq ravishda muloqot qilishga yordam beradi. Har bir gapda kamida ot va fe'l bo'lishi kerak."
            },
            {
                "title": "Adabiy Atamalar va Vositalar",
                "body": "Adabiyot ma'no va hissni yaratish uchun ko'p vositalardan foydalanadi. Metafora ikki turli narsani 'kabi' yoki 'shunga o'xshash' ishlatmasdan solishtiradi, masalan, 'vaqt pul'. Shunoshalik 'kabi' yoki 'shunga o'xshash' dan foydalanib solishtiradi, masalan, 'shir kabi jasur'. Tashxisiylashtirish be-jonlarni insoniy sifatlar bilan do'stlarashur, masalan, 'shamol shiliq-siliq ayt'. Tasvirlar hissiyat tafsilotlaridan foydalanib vivid tavsilotlarni yaratadi. Oldindan ko'rsatish kelajakdagi voqealarni asqartamaydi. Orqaga qaytish hikoyani to'xtatib o'tgan voqealarni ko'rsatadi. Ironiya voqelik kutilgandan teskarisi bo'lganda yuzaga keladi. Tarnama narsalar yoki harakatlar chuqurroq ma'nolarni ko'rsatadi, masalan, bo'ri shohmuqo'ylar uchun. Alliteratsiya boshlang'ich undosh tovushlarini takrorlaydi, masalan, 'Salom sotib olamiz qushqoq'. Ushbu vositalarni tushunish adabiyotni qadr qilish va matnlarni chuqur tahlil qilishga yordam beradi."
            },
            {
                "title": "Samarali Yozish Maslahatlar",
                "body": "Yaxshi yozish aniqlik, tashkilot va qayta ishlashni talab qiladi. Aniq maqsad bilan boshlang': sizning o'quvchingani nimani tushunishini xohlaysiz? Yozishdan oldin o'z fikringizni rejaga soling. Murakkab so'zlar o'rniga sodda, bevosita tiling ishlating. Uzoq paragraflarni qisqa bo'lim uchun qisqa bo'limlarga bo'ling. Passiv ovozni (sichqon mushukka bosib olgan) o'rniga aktiv ovozni (mushuk sichqonni quvladi) ishlating. Qiziqishni saqlash uchun gap tuzilmasini o'zgartirib bering. Ko'rsating, aytmang: u mutsassir edi deyish o'rniga, 'ko'z yoshlari uning yangida oqdi'ni yozing. O'z ishingizni ovozda o'qib, noqonuniy ifodalarni ushlay. Imlo va grammatika xatolarini tekshiring. Ishingizni yakunlashdan oldin boshqalardan fikr-maslahat so'rang. Eslang, yaxshi yozish sizning xabaringiz aniq bo'lguniga qadar qayta ishlashtirish hisoblanadi."
            }
        ],
        "ru": [
            {
                "title": "Английская Грамматика: Части Речи",
                "body": "Английская грамматика основана на восьми частях речи: существительные, местоимения, глаголы, прилагательные, наречия, предлоги, союзы и междометия. Существительное — это лицо, место или предмет (например, учитель, школа, книга). Местоимение заменяет существительное (он, она, оно, они). Глагол — это действие или состояние (бежать, прыгать, быть). Прилагательное описывает существительное (большой, маленький, красивый). Наречие модифицирует глагол или прилагательное (быстро, медленно, очень). Предлог показывает отношения (в, на, под, между). Союз соединяет слова или идеи (и, но, или). Междометие выражает эмоцию (о, вау, ай). Понимание этих частей помогает вам构造 грамматически правильные предложения и общаться ясно. Каждое предложение должно иметь по крайней мере существительное и глагол, чтобы быть полным."
            },
            {
                "title": "Литературные Термины и Приёмы",
                "body": "Литература использует множество приёмов для создания смысла и эмоций. Метафора сравнивает два непохожих предмета без использования 'как' (например, 'время — это деньги'). Сравнение использует 'как' для сравнения (например, 'смелый как лев'). Персонификация придаёт человеческие качества неживым предметам (например, 'ветер шептал'). Образность использует сенсорные детали для создания яvivid описаний. Предзнаменование намекает на будущие события. Флешбэк прерывает историю, чтобы показать прошлые события. Ирония возникает, когда реальность противоположна ожиданиям. Символизм использует объекты или действия для представления более глубоких значений (например, голубь для мира). Аллитерация повторяет начальные согласные звуки (например, 'сладко спит сладкий сон'). Понимание этих приёмов поможет вам оценить литературу и глубоко проанализировать тексты."
            },
            {
                "title": "Советы для Эффективного Письма",
                "body": "Хорошее письмо требует ясности, организации и переработки. Начните с чёткой цели: что вы хотите, чтобы ваш читатель понял? Организуйте ваши мысли в план перед написанием. Используйте простой, прямой язык вместо сложных слов. Разделите длинные абзацы на более короткие для удобства чтения. Используйте активный залог (кошка гналась за мышкой) вместо пассивного (мышка была настигнута кошкой). Варьируйте структуру предложений для поддержания интереса. Показывайте, не рассказывайте: вместо 'ей было грустно' напишите 'по её щекам текли слёзы'. Прочитайте свою работу вслух, чтобы уловить неловкие формулировки. Проверьте грамматику и орфографию. Получите отзывы других перед финализацией. Помните, хорошее письмо — это переработка до тех пор, пока ваше сообщение не станет кристально чистым."
            }
        ]
    },
    "general": {
        "en": [
            {
                "title": "Logic Puzzles and Critical Thinking",
                "body": "Logic puzzles strengthen your problem-solving skills and critical thinking. A classic puzzle: 'A man pushes his car to a hotel and tells the owner he's bankrupt. Why?' Answer: He's playing Monopoly. These puzzles teach you to question assumptions. Another puzzle: 'What has cities but no houses, forests but no trees, and water but no fish?' Answer: A map. Maps represent real places in simplified form. Logic puzzles require you to think laterally, finding creative connections between clues. They improve your ability to analyze information, spot patterns, and make logical deductions. Solving puzzles regularly enhances your brain's flexibility and helps you approach real-world problems strategically. Start with simple puzzles and work your way to complex ones."
            },
            {
                "title": "Study Tips for Success",
                "body": "Effective studying goes beyond reading your notes repeatedly. First, create an active learning environment: ask questions, explain concepts to others, and test yourself. Use the Feynman Technique: explain a topic in simple words as if teaching a child. If you struggle to explain it simply, you don't fully understand it. Second, space out your studying over time rather than cramming. Study the same material on multiple days to strengthen memory through spaced repetition. Third, link new concepts to what you already know. Making connections helps your brain organize and retain information. Fourth, use multiple resources: textbooks, videos, podcasts, and study groups. Different perspectives deepen understanding. Fifth, teach someone else. Explaining material forces you to organize your thoughts clearly. Finally, get enough sleep. Sleep consolidates memories and is crucial for learning. A well-rested brain learns better and retains more."
            },
            {
                "title": "Fun Trivia: Surprising Facts",
                "body": "Did you know that honey never spoils? Archaeologists found 3,000-year-old honey in Egyptian tombs that was still edible. Honey's low moisture and high acidity prevent bacterial growth. Another fascinating fact: octopuses have three hearts. Two hearts pump blood to the gills, and the third pumps blood to the rest of the body. When an octopus swims, the heart pumping blood to the body actually stops, making them tire quickly. A giraffe's neck contains the same number of vertebrae as a human neck, just much larger ones. Giraffes have only seven cervical vertebrae, same as humans. Bananas are berries, but strawberries aren't. Botanically, a berry is a fruit from a single ovary with seeds embedded in the flesh. These surprising facts show how much we still have to learn about the natural world."
            }
        ],
        "uz": [
            {
                "title": "Mantiq Boshqotirmalar va Tanqidiy Fikrlash",
                "body": "Mantiq boshqotirmalari sizning muammoni hal qilish ko'nikmalarini va tanqidiy fikrlashni mustahkamlaydi. Klassik boshqotirma: 'Odam o'z mashinasini saxradorni bosib qo'yadi va egasiga: men bankrotman, dedi. Nega?' Javob: U Monopolpol o'ynaydi. Ushbu boshqotirmalar sizga farazlarni shakllantirish o'rgatadi. Yana boshqotirma: 'Nima shaxarlardan iborat lekin uylarsiz, o'rmonlardan iborat lekin daraxtlarsiz, va suvdan iborat lekin baligasiz?' Javob: Xarita. Xaritalar haqiqiy joylarni soddalashtirilgan shakl bilan ifodalaydi. Mantiq boshqotirmalari lateral fikrlashni talab qiladi, masalalari o'rtasida ijodiy bog'lanishlarni topish. Ular sizning axborotni tahlil qilish, naqsh topish va mantiqiy xulosa chiqarish qobiliyatingizni yaxshilaydi. Doimiy ravishda boshqotirmalarni hal qilish sizning miyangizning egiluvchanligini oshiradi va haqiqiy muammolarni strategik yondashadingizni yaxshilaydi. Oddiy boshqotirmalar bilan boshlang va murakkab boshqotirmalargacho o'tib vering."
            },
            {
                "title": "O'rganish uchun Maslahatlar",
                "body": "Samarali o'rganish sizning eslatmalarini qayta-qayta o'qishdangina yuqoriroq. Birinchidan, faol o'rganish muhitini yarating: savollar bering, tushunchalarni boshqalarga tushuntiring va o'zingizni sinab ko'ring. Baymanning Usuli dan foydalaning: mundarija oddiy so'zlar bilan tushuntiring, xuddi bola o'rgatayotgandek. Agar sodda ravishda tushuntirishda qiynalib turgan bo'lsangiz, siz uni to'liq tushunmagansiz. Ikkinchidan, vaqt mobaynida o'rganishni tarqating, chiqqunovga o'xshash bo'lmasdan. Bir xil materialn bir necha kunlarda ko'p o'rganish xotiraning mustahkamlanishiga olib keladi. Uchinchidan, yangi tushunchalarni allaqachon bilgan bilan bog'lang. Bog'lanishlar sizning miyangizning malumotlarni tartibga solib saqlashiga yordam beradi. Tort'inchidan, ko'p manbalari ishlating: darsliklar, videolar, podkastlar va o'rganish guruhlari. Turli nuqtayi nazar chuqur tushunchaga olib keladi. Beshinchidan, boshqalarni o'rgatib bering. Materiallarni tushuntirish sizni o'z fikringizni aniq tuzishga majbur qiladi. Va oxirida, etarlicha uxlay. Uyqu xotiralarni mustahkamlaydi va o'rganishda muhimdir. Yaxshi uxlagan miya yaxshiroq o'rganadi va ko'proq saqlaydi."
            },
            {
                "title": "Qiziqarli Bilgiler: Ajoyib Faktlar",
                "body": "Bilasizmi, asal hech qachon buziladini? Arxeologlar Misr qabronda 3000 yil qadimgi asal topdilar va u hali ham ea bolyapti. Asalning past na'malumlik va yuqori kislotalilik bakterial o'sishni oldini oladi. Boshqa ajoyib fakt: Oktopus uchta yurakka ega. Ikki yurak qon jukhalanganiga pompadinga yuboradi va uchinchi qon shunga otir. Oktopus suzganda, tanaga qon yuborovchi yurak to'htatib qo'yiladi, bunga o'xshash, ular tez charchunarkan. Jirafa boyniga odam bo'yni bilan bir xil soni vertebra bor, faqat ancha kattaroqdir. Jirafalar faqat etti shaxl vertebraga ega, odamlarga o'xshash. Bananlari mevli, lekin qulupnaylar emas. Botanikaga ko'ra, mevli, bitta tuxumi bilan meva bo'lib, urug'lari go'sht ichida joylashgan. Ushbu ajoyib faktlar bizning tabiiy olamni hali ham o'rganishimiz kerak ekanligini ko'rsatadi."
            }
        ],
        "ru": [
            {
                "title": "Логические Головоломки и Критическое Мышление",
                "body": "Логические головоломки укрепляют ваши навыки решения проблем и критического мышления. Классическая головоломка: 'Мужчина толкает свой автомобиль к отелю и говорит хозяину, что он банкрот. Почему?' Ответ: Он играет в Монополию. Эти головоломки учат вас сомневаться в предположениях. Ещё головоломка: 'Что имеет города, но не дома, леса, но не деревья, и воду, но не рыб?' Ответ: Карта. Карты представляют реальные места в упрощённом виде. Логические головоломки требуют латерального мышления, находя творческие связи между подсказками. Они улучшают вашу способность анализировать информацию, замечать закономерности и делать логические умозаключения. Регулярное решение головоломок повышает гибкость вашего мозга и помогает вам стратегически подходить к реальным проблемам. Начните с простых головоломок и перейдите к сложным."
            },
            {
                "title": "Советы для Успешного Обучения",
                "body": "Эффективное обучение выходит за рамки повторного чтения ваших заметок. Во-первых, создайте активную среду обучения: задавайте вопросы, объясняйте концепции другим, тестируйте себя. Используйте технику Фейнмана: объясните тему простыми словами, как если бы учили ребёнка. Если вы не можете просто объяснить это, вы не полностью его понимаете. Во-вторых, распределяйте учёбу во времени, а не зубрите. Изучайте один и тот же материал в разные дни, укрепляя память через интервальное повторение. В-третьих, свяжите новые концепции с тем, что вы уже знаете. Открытие связей помогает вашему мозгу организовать и сохранить информацию. В-четвёртых, используйте несколько источников: учебники, видео, подкасты, учебные группы. Различные перспективы углубляют понимание. В-пятых, учите кого-то ещё. Объяснение материала заставит вас чётко организовать свои мысли. Наконец, высыпайтесь. Сон консолидирует память и имеет решающее знатение для обучения. Хорошо отдохнувший мозг лучше учится и больше запоминает."
            },
            {
                "title": "Интересные Мелочи: Удивительные Факты",
                "body": "Знаете ли вы, что мёд никогда не портится? Археологи нашли 3000-летний мёд в египетских гробницах, который был всё ещё съедобен. Низкая влажность и высокая кислотность мёда предотвращают рост бактерий. Другой поразительный факт: у осьминога три сердца. Два сердца перекачивают кровь к жабрам, а третье перекачивает кровь в остальную часть тела. Когда осьминог плывёт, сердце, перекачивающее кровь в организм, фактически останавливается, из-за чего они быстро устают. Шея жирафа содержит то же количество позвонков, что и шея человека, просто намного больше. У жирафов есть только семь шейных позвонков, как и у людей. Бананы — это ягоды, но клубника — нет. С ботанической точки зрения ягода — это плод из одного пестика с семенами, встроенными в мякоть. Эти удивительные факты показывают, сколько нам ещё предстоит узнать о природном мире."
            }
        ]
    }
}


def seed_database():
    # Populate database with educational content for all sections.
    from rag.embeddings import embed_text
    
    db = SessionLocal()
    
    # Check if articles already exist
    existing = db.query(Article).first()
    if existing:
        print("Database already seeded. Skipping...")
        db.close()
        return
    
    articles_created = 0
    
    for section, languages in SEED_DATA.items():
        for language, articles in languages.items():
            for article_data in articles:
                # Embed the article text
                embedding = embed_text(article_data["body"])
                
                article = Article(
                    section=section,
                    title=article_data["title"],
                    body=article_data["body"],
                    language=language,
                    embedding=embedding
                )
                db.add(article)
                articles_created += 1
    
    db.commit()
    db.close()
    
    print(f"✅ Database seeded successfully with {articles_created} articles!")


if __name__ == "__main__":
    print("Seeding database...")
    seed_database()
