from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
import mysql.connector
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
import subprocess
import tkinter as tk
from tkinter import filedialog
import io
from PIL import Image
import fitz  # PyMuPDF
from kivy.uix.popup import Popup
from kivymd.uix.filemanager import MDFileManager
from kivy.lang import Builder
from kivy.uix.scrollview import ScrollView
import PyPDF2
from PyPDF2 import PdfReader
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.core.window import Window

# З'єднання з базою даних
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="visspan01",
    database="app"
)
cursor = conn.cursor()
  
cursor.execute("CREATE TABLE IF NOT EXISTS registr (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), email VARCHAR(255), password VARCHAR(255))")
conn.commit()

KV = """
<StartScreen>:
    orientation: 'vertical'
    Label:
        text: 'Ласкаво просимо'
    Button:
        text: 'Увійти'
        on_press: root.manager.current = 'login'
    Button:
        text: 'Зареєструватися'
        on_press: root.manager.current = 'register'
    Button:
        text: 'Вийти'
        on_press: app.stop()

<LoginScreen>:
    orientation: 'vertical'
    Label:
        text: 'Увійти'
    TextInput:
        id: email_input
        multiline: False
        hint_text: 'Електронна пошта'
    TextInput:
        id: password_input
        multiline: False
        password: True
        hint_text: 'Пароль'
    Button:
        text: 'Увійти'
        on_press: root.login()
    Button:
        text: 'Назад'
        on_press: root.manager.current = 'start'

<RegisterScreen>:
    orientation: 'vertical'
    Label:
        text: 'Реєстрація'
    TextInput:
        id: username_input
        multiline: False
        hint_text: 'Імя користувача'
    TextInput:
        id: email_input
        multiline: False
        hint_text: 'Електронна пошта'
    TextInput:
        id: password_input
        multiline: False
        password: True
        hint_text: 'Пароль (мінімум 8 символів)'
    Button:
        text: 'Зареєструватися'
        on_press: root.register()
    Button:
        text: 'Назад'
        on_press: root.manager.current = 'start'
<FirstPage>
    orientation: 'vertical'
    Label:
        text: "Введіть назву книги"
    TextInput:
        id: search
        hint_text:"назва книги"
    Button:
        text: "назад"
    Button:
        text: "search"
        color:
<SearchPage>:
    orientation: 'vertical'
    Label:
        text: "soooo goood"

    TextInput:
        id: additional_input
        multiline: False
        hint_text: 'Додаткове поле для введення'

    Button:
        text: 'Додати'
        on_press: root.add_additional_info()

        

<SuccessScreen>:
    orientation: 'vertical'
    Label:
        text: 'Успіх'
    #Button:
    #    text: 'Назад'
    #    on_press: root.manager.current = 'start'
    TextInput:
        id: book_title_input
        multiline: False
        hint_text: 'Назва книги'
    TextInput:
        id: author_input
        multiline: False
        hint_text: 'Автор книги'
    TextInput:
        id: description_input
        multiline: False
        hint_text: 'Короткий опис'
    TextInput:
        id: fiel
        line: false
        hint_text: 'Завантажте книгу'
        
<BookDetailsPage>:
    orientation: 'vertical'

    Label:
        id: book_title_label
        text: root.book_title
        font_size: '20sp'
        size_hint_y: None
        height: self.texture_size[1]

    Label:
        id: book_text_label
        text: root.text
        font_size: '16sp'
        size_hint_y: None
        height: self.texture_size[1]

    Button:
        text: 'Назад'
        on_press: root.go_back()

"""

class StartScreen(Screen):
    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        label = Label(text='Ласкаво просимо')
        login_button = Button(text='Увійти', on_press=self.go_to_login)
        register_button = Button(text='Зареєструватися', on_press=self.go_to_register)
        exit_button = Button(text='Вийти', on_press=App.get_running_app().stop)
        
        layout.add_widget(label)
        layout.add_widget(login_button)
        layout.add_widget(register_button)
        layout.add_widget(exit_button)
        
        self.add_widget(layout)

    def go_to_login(self, instance):
        self.manager.current = 'login'

    def go_to_register(self, instance):
        self.manager.current = 'register'
        
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        label = Label(text='Увійти')
        self.email_input = TextInput(hint_text='Електронна пошта')
        self.password_input = TextInput(hint_text='Пароль', password=True)
        login_button = Button(text='Увійти', on_press=self.login)
        exit_button = Button(text = 'Назад',on_press=self.go_to_start)

        layout.add_widget(label)
        layout.add_widget(self.email_input)
        layout.add_widget(self.password_input)
        layout.add_widget(login_button)
        layout.add_widget(exit_button)

        self.add_widget(layout)

    def go_to_start(self, instance):
        self.manager.current = 'start'
        
    def login(self, instance):
        email = self.email_input.text
        password = self.password_input.text

        # Перевірка користувача в базі даних
        cursor.execute("SELECT * FROM registr WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()

        if user:
            print("Користувач успішно увійшов!")
            self.manager.current = 'first'
        else:
            print("Не вдалося увійти.")

class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super(RegisterScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        label = Label(text='')
        self.username_input = TextInput(hint_text='Ім\'я користувача')
        self.email_input = TextInput(hint_text='Електронна пошта')
        self.password_input = TextInput(hint_text='Пароль', password=True)
        register_button = Button(text='Зареєструватися', on_press=self.register)

        layout.add_widget(label)
        layout.add_widget(self.username_input)
        layout.add_widget(self.email_input)
        layout.add_widget(self.password_input)
        layout.add_widget(register_button)

        self.add_widget(layout)

    def register(self, instance):
        username = self.username_input.text
        email = self.email_input.text
        password = self.password_input.text

        if len(password) >= 8:
            # Перевірка, чи існує користувач з такою самою поштою
            cursor.execute("SELECT * FROM registr WHERE email = %s", (email,))
            existing_user = cursor.fetchone()

            if not existing_user:
                # Реєстрація користувача
                cursor.execute("INSERT INTO registr (name, email, password) VALUES (%s, %s, %s)", (username, email, password))
                conn.commit()
                print("Користувач успішно зареєстрований!")
            else:
                print("Електронна пошта вже існує.")
        else:
            print("Пароль повинен містити щонайменше 8 символів.")

class FirstPage(Screen):
    def __init__(self,**kwargs):
        super(FirstPage, self).__init__(**kwargs)
        layout = BoxLayout(orientation = 'vertical')
        label = Label(text='')
        button = Button(text = "Search", on_press=self.go_to_search)
        button1 = Button(text = "Load", on_press=self.login)
        
        layout.add_widget(button)
        layout.add_widget(button1)
        
        self.add_widget(layout)
        
    def go_to_search(self, instance):
        self.manager.current = 'search'
    
    def login(self, instance):
        self.manager.current ='success'
       
class SearchPage(Screen):
    def __init__(self, **kwargs):
        super(SearchPage, self).__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical')
        
        self.search_input = TextInput(hint_text='Введіть назву книги')
        layout.add_widget(self.search_input)
        
        search_button = Button(text='Пошук', on_press=self.search_book)
        layout.add_widget(search_button)
        
        self.add_widget(layout)
        
    def search_book(self, instance):
        book_title = self.search_input.text
        
        # Виконати запит до бази даних, щоб отримати результати пошуку
        cursor = conn.cursor()
        sql = "SELECT author, description, file_content FROM catalog WHERE book_title LIKE %s"
        val = ("%" + book_title + "%",)
        cursor.execute(sql, val)
        search_results = cursor.fetchall()
        cursor.close()
        
        # Відобразити результати пошуку
        self.display_search_results(search_results)
        
    def display_search_results(self, results):
        for result in results:
            author, description, file_content = result
            # Відображення тексту на новій сторінці
            text = self.extract_text_from_pdf(file_content)
            self.display_book_details(author, text)
    
    def extract_text_from_pdf(self, file_content):
        try:
        # Відкриття PDF-файлу
            pdf_file = io.BytesIO(file_content)
            reader = PdfReader(pdf_file)

        # Зчитування тексту з усіх сторінок PDF
            text = ""
            for page in reader.pages:
               text += page.extract_text()

            return text
        except Exception as e:
        # Виведення повідомлення про помилку у консоль
            print("Помилка при відкритті PDF-файлу:", str(e))
            return ''


    def display_book_details(self, author, text):
    # Перехід на нову сторінку з деталями книги
        self.manager.current = 'book_details'
    # Передача назви книги та тексту на нову сторінку
        book_details_page = self.manager.get_screen('book_details')
        book_details_page.book_title = author
        book_details_page.text = text


    def go_back(self, instance):
        # Повернення на сторінку пошуку
        self.manager.current = 'search'

class BookDetailsPage(Screen):
    def __init__(self, book_title='', text='', **kwargs):
        super(BookDetailsPage, self).__init__(**kwargs)
        self.book_title = book_title
        self.text = text

    def on_enter(self):
        super().on_enter()
        self.display_book_details()

    def display_book_details(self):
        layout = BoxLayout(orientation='vertical')

        title_label = Label(text=self.book_title, size_hint=(1, 0.1))
        layout.add_widget(title_label)

        scroll_view = ScrollView(size_hint=(1, 0.9))
        text_input = TextInput(text=self.text,size_hint_y=45, height=self.get_text_height())
        
        scroll_view.add_widget(text_input)
        layout.add_widget(scroll_view)

        back_button = Button(text='Назад', size_hint=(1, 0.1))
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def get_text_height(self):
        # Отримання висоти тексту, щоб правильно встановити розмір ScrollView
        return len(self.text.split('\n')) * 20  # Приблизно 20 пікселів на рядок

    def go_back(self, instance):
        self.manager.current = 'search'

    @staticmethod
    def extract_text_from_pdf(file_content):
        try:
            # Відкриття PDF-файлу
            pdf_document = fitz.open("pdf", file_content)

        # Зчитування тексту з першої сторінки PDF
            text = ""
            first_page = pdf_document.load_page(0)
            text += first_page.get_text()

        # Зчитування тексту з наступних сторінок, якщо вони є
            for page_num in range(1, len(pdf_document)):
                page = pdf_document.load_page(page_num)
                text += page.get_text()

            return text
        except Exception as e:
            print("Помилка при відкритті PDF-файлу:", str(e))
            return ''
        
class SuccessScreen(Screen):
    def __init__(self, **kwargs):
        super(SuccessScreen, self).__init__(**kwargs)
 
        layout = BoxLayout(orientation='vertical')
        label = Label(text='')
        choose_file_button = Button(text="Відкрити мій ПК")
        choose_file_button.bind(on_press=self.choose_file)

        layout.add_widget(choose_file_button)

        self.book_title_input = TextInput(hint_text="Назва книги")
        self.author_input = TextInput(hint_text="Автор")
        self.description_input = TextInput(hint_text="Опис")

        layout.add_widget(self.book_title_input)
        layout.add_widget(self.author_input)
        layout.add_widget(self.description_input)

        upload_button = Button(text="Завантажити до бази даних")
        upload_button.bind(on_press=self.upload_to_database)

        layout.add_widget(upload_button)

        self.selected_file = None

        self.add_widget(layout)
        
    def choose_file(self, instance):
        root = tk.Tk()
        root.withdraw()  

        self.selected_file = filedialog.askopenfilename()

        print("Вибраний файл:", self.selected_file)

    def upload_to_database(self, instance):
        if self.selected_file is None:
            print("Спочатку виберіть файл")
            return

        mycursor = conn.cursor()

        book_title = self.book_title_input.text
        author = self.author_input.text
        description = self.description_input.text

        # Читаємо вміст файлу
        with open(self.selected_file, "rb") as file:
            book_content = file.read()

        # SQL запит для вставки даних
        sql = "INSERT INTO catalog (book_title, author, description, file_content) VALUES (%s, %s, %s, %s)"
        val = (book_title, author, description, book_content)

        mycursor.execute(sql, val)

        conn.commit()

        print(mycursor.rowcount, "запис успішно вставлено.")
        
class MyApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        start_screen = StartScreen(name='start')
        login_screen = LoginScreen(name='login')
        firstpage_screen = FirstPage(name='first')
        search_screen = SearchPage(name = 'search') 
        register_screen = RegisterScreen(name='register')
        success_screen = SuccessScreen(name='success')
        book_detail_screen = BookDetailsPage(name= 'book_details')

        self.screen_manager.add_widget(start_screen)
        self.screen_manager.add_widget(login_screen)
        self.screen_manager.add_widget(firstpage_screen)
        self.screen_manager.add_widget(search_screen)
        self.screen_manager.add_widget(register_screen)
        self.screen_manager.add_widget(success_screen)
        self.screen_manager.add_widget(book_detail_screen)

        return self.screen_manager

if __name__ == "__main__":
     
    MyApp().run()
