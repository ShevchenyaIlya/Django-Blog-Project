## Django-Blog-Project
### My first django project based on laboratory work and learning the basics of django.

Тема проекта - __персональный блог__.

### Доступная функцианальность:

* __Логин__. На главной странице можно залогиниться, если аккаунт уже существует, или зарегистрировать нового пользователя сайта. Для авторизириванных пользователей отображается ссылка "Logout", каторая разлогинивает вас с сайта. Регистрация, авторизация реализованы средствами django.

* __Профиль__. Для авторизированных пользователей отображается гиперссылка "Profile", которая перенаправляет на страницу пользователя (страница с заданными персональными данными), где можно изменить адрес электронной почты и изображение профиля пользователя.

* __Просмотр списка постов__. На главной странице отображаются всё посты пользователей, отсортированные по дате публикации, причем на странице может располагаться не более 5 постов, поэтому организован переход на следующие/предыдущие страницы с постами (снизу страницы имеются кнопки перехода по номеру страницы или перехода на одну страницу вперед/назад, если пользователь находится не на первой странице, то доступен переход на самую первую страницу). Предоставляется переход по постам, при нажании на его название, где отображается сообщение в развернутом виде.

* __Список всех постов пользователя__. При нажатии на имя пользователя, можно увидеть все посты оставленные пользователем за всё время. 

* __Создание, удаление, редактирование постов__. Для авторизированных пользователей доступна возможность удаления и редактирования собственных постов (при переходе на страницу поста отображаются две ктопки "Update" - переправляет на страницу редактирования поста, "Delete" - удаляет пост с сайта). Данная возможность предоставлена только для собственных постов, иначе кнопки удаления и редактирования будут недоступны. Также для авторизированных пользователей отображается ссылка на страницу создания собственного поста ("New Post" перенаправит на форму создания своего поста на сайте и его сохранение). Для "user friendly" отображения панелей регистрации, авторизации используется модуль "crispy-forms".

* __Вкладка "About" и панель "Important"__. Содержится неактивная на данный помент информационная понель "Important", ссылка перехода на страницу "About".

* __Админка__. На вкладке администратора, куда можно попасть по адресу "http://localhost:8000/admin/", добавлены все используемые модели. Связанные модели отображаются совместно. При переходе в раздел одной из моделей доступна сортировка по выбранным полям и удаление, редактирование, добавление. Для изменения внешнего вида панели администратора используется модуль "grappelli".

#### Python version: 3.6
#### Dependencies: requirements.txt
#### Notes:
* Перед запуском необходимо выполнить `python manage.py collectstatic`

* __Database__. Для хранения данных используется база данных PostgreSQL, которую нет возможности отправить. В файле django_project/setings.py в словаре DATABASE содержатся настройки моей базы данных и пользователя. Для использования проекта предлагается создание собственной postgresql базы (в таком случае она будет пустой, следовательно на сайте не будет ни одного поста, ни одного пользователя) и изменение в словаре полей "NAME", "USER", "PASSWORD" для запуска проекта или использование предоставленной вместе с проектом уже заполненной некоторыми данными db.sqlite3 базой (для этого необходимо раскомментить код внутри словаря DATABASE).

* __Superuser__. Используя PostgreSQL необходимо будет создать суперюзера для получения доступа к панели админа на сайте. Если использовать sqlite, то можно воспользоваться уже созданным суперюзером (login: ShevchenyaIlya password: ilya12345678) или пересоздать его.

* __User__. На сайте доступна регистрация , поэтому можно создать обычного пользователя, который будет иметь возможность просматривать данные на сайте, создавать свои посты и т.д. Однако он не будет иметь доступ к панели администратора.


 
