from kivy.uix.textinput import TextInput
from kivy.animation import Animation
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.slider import Slider
import requests

# Définir la couleur de fond de la fenêtre principale
Window.clearcolor = (1, 1, 1, 1)  # Blanc


class LampApp(App):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(MainScreen(name='main', app=self))
        self.sm.add_widget(ProfilScreen(name='profil'))
        self.sm.add_widget(AccueilScreen(name='accueil'))
        self.sm.add_widget(ConnecterScreen(name='connecter'))
        self.sm.add_widget(page_supplementaire(name='page_supplementaire'))  # Ajout de la nouvelle page
        return self.sm


class MainScreen(Screen):
    def __init__(self, app, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.app = app

        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.add_widget(self.layout)

        # Layout principal horizontal pour le menu
        top_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        self.layout.add_widget(top_layout)

        # Layout vertical pour le menu et ses options
        self.menu_layout = BoxLayout(orientation='vertical', size_hint=(None, None), size=(50, 50))
        top_layout.add_widget(self.menu_layout)

        # Bouton Menu
        self.menu_button = Button(text="Menu", size_hint=(None, None), size=(50, 50))
        self.menu_button.bind(on_press=self.toggle_menu)
        self.menu_layout.add_widget(self.menu_button)

        # Container pour les options de menu (initialisé caché)
        self.menu_items = BoxLayout(orientation='vertical', spacing=5, size_hint=(None, None), size=(100, 0),
                                    pos_hint={'top': 1})
        top_layout.add_widget(self.menu_items)

        # Options du menu
        self.profil_button = Button(text="Profil", size_hint_y=None, height=30)
        self.profil_button.bind(on_release=self.menu_option_selected)
        self.menu_items.add_widget(self.profil_button)

        self.accueil_button = Button(text="Accueil", size_hint_y=None, height=30)
        self.accueil_button.bind(on_release=self.menu_option_selected)
        self.menu_items.add_widget(self.accueil_button)

        self.connecter_button = Button(text="Se connecter", size_hint_y=None, height=30)
        self.connecter_button.bind(on_release=self.menu_option_selected)
        self.menu_items.add_widget(self.connecter_button)

        self.menu_items.size_hint_y = None
        self.menu_items.height = 0  # Caché initialement
        self.menu_items.opacity = 0  # Caché initialement

        self.menu_hidden = True  # État initial du menu caché

        # Ajout de l'image et du label d'accueil
        self.bg = Image(source='Lampe.jpg', size_hint_y=None, height=300)
        self.layout.add_widget(self.bg)

        # Label Bienvenue
        self.welcome_label = Label(text="Bienvenue à l'Application de Commande des Lampes LED Ati Electronics",
                                   font_size=20, color=(0.9, 0.2, 0.9, 1))  # Rose
        self.layout.add_widget(self.welcome_label)

    def toggle_menu(self, instance):
        if self.menu_hidden:
            # Afficher le menu
            self.menu_hidden = False
            anim = Animation(height=90, opacity=1, duration=0.2)
            anim.start(self.menu_items)
        else:
            # Cacher le menu
            self.menu_hidden = True
            anim = Animation(height=0, opacity=0, duration=0.2)
            anim.start(self.menu_items)

    def menu_option_selected(self, instance):
        if instance.text == "Se connecter":
            self.app.sm.current = "connecter"
        elif instance.text == "Profil":
            self.app.sm.current = "profil"
        elif instance.text == "Accueil":
            self.app.sm.current = "accueil"


class ProfilScreen(Screen):
    def __init__(self, **kwargs):
        super(ProfilScreen, self).__init__(**kwargs)

        # Utilisation de FloatLayout pour superposer l'image de fond et le contenu
        self.layout = FloatLayout()
        self.add_widget(self.layout)

        # Ajout de l'image de fond
        self.bg = Image(source='ledy.jpg', allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(self.bg)

        # Création du layout principal vertical avec padding et espacement
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Container pour appliquer le background semi-transparent
        container = BoxLayout(orientation='vertical')
        with container.canvas.before:
            Color(1, 1, 1, 0.7)  # Blanc avec une opacité de 0.7
            self.rect = Rectangle(size=self.size, pos=self.pos)
        container.bind(size=self._update_rect, pos=self._update_rect)

        # Création du layout pour les boutons
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50, spacing=10)

        # Dictionnaire pour garder une trace de l'état d'affichage du texte
        self.text_shown = {
            "Description": False,
            "Notre Mission": False,
            "Nos Produits": False,
            "Pourquoi Choisir ATI Electronics": False,
            "Service Client": False
        }

        # Création des boutons en haut de la page
        btn_descriptions = Button(text="Description", size_hint=(0.2, None), height=50, background_color=(0, 0, 0, 0.6),
                                  color=(1, 1, 1, 1))
        btn_our_mission = Button(text="Notre Mission", size_hint=(0.2, None), height=50,
                                 background_color=(0, 0, 0, 0.6), color=(1, 1, 1, 1))
        btn_our_products = Button(text="Nos Produits", size_hint=(0.2, None), height=50,
                                  background_color=(0, 0, 0, 0.6), color=(1, 1, 1, 1))
        btn_why_choose = Button(text="Pourquoi Choisir ATI Electronics", size_hint=(0.2, None), height=50,
                                background_color=(0, 0, 0, 0.6), color=(1, 1, 1, 1))
        btn_customer_service = Button(text="Service Client", size_hint=(0.2, None), height=50,
                                      background_color=(0, 0, 0, 0.6), color=(1, 1, 1, 1))

        # Ajout des fonctions à chaque bouton
        btn_descriptions.bind(on_press=lambda x: self.toggle_text("Description"))
        btn_our_mission.bind(on_press=lambda x: self.toggle_text("Notre Mission"))
        btn_our_products.bind(on_press=lambda x: self.toggle_text("Nos Produits"))
        btn_why_choose.bind(on_press=lambda x: self.toggle_text("Pourquoi Choisir ATI Electronics"))
        btn_customer_service.bind(on_press=lambda x: self.toggle_text("Service Client"))

        # Ajout des boutons au layout des boutons
        button_layout.add_widget(btn_descriptions)
        button_layout.add_widget(btn_our_mission)
        button_layout.add_widget(btn_our_products)
        button_layout.add_widget(btn_why_choose)
        button_layout.add_widget(btn_customer_service)

        # Ajout du layout des boutons au layout principal
        container.add_widget(button_layout)

        # Widget pour afficher le texte
        self.text_display = Label(text="", color=(0, 0, 0, 1), size_hint=(1, None), valign='top')

        # ScrollView pour le texte
        self.scroll_view = ScrollView(size_hint=(1, 1))
        self.scroll_view.add_widget(self.text_display)

        # Ajout du ScrollView au layout principal
        container.add_widget(self.scroll_view)

        # Bouton Retour
        retour_button = Button(text="Retour", size_hint=(None, None), size=(100, 50), background_color=(0, 0, 0, 0.6),
                               color=(1, 1, 1, 1))
        retour_button.bind(on_press=self.go_back)
        container.add_widget(retour_button)

        # Ajout du container avec le background semi-transparent au layout principal
        main_layout.add_widget(container)
        self.layout.add_widget(main_layout)

    def toggle_text(self, section):
        # Fermer le texte affiché précédemment
        if self.text_shown[section]:
            self.text_display.text = ""
            self.text_display.size_hint_y = None
            self.text_display.height = 0
            self.text_shown[section] = False
        else:
            self.text_display.text = self.get_section_text(section)
            self.text_display.size_hint_y = None
            self.text_display.height = self.text_display.texture_size[1]
            self.text_shown[section] = True

    def get_section_text(self, section):
        sections = {
            "Description": """
         Description\n
-         Nom de la Société : Ati Electronics\n



             



                   Description :\n



    Ati Electronics est une entreprise innovante spécialisée dans la conception et la fabrication de lampes LED de
    haute  qualité.\n
    Fondée sur les principes de durabilité, d'efficacité énergétique et de technologie avancée,
            """,

            "Notre Mission": """
            
            
            
            
             
                       Notre Mission :\n
                    
                    
                       Chez Ati Electronics, nous nous engageons à fournir des produits d'éclairage LED de pointe qui 
                       répondent aux besoins variés de nos clients tout en contribuant à la protection de l'environnement.\n
                       
                      Nous croyons en un avenir où chaque foyer et chaque entreprise utilisent un éclairage efficace et respectueux
                       de la planète.
            """,

            "Nos Produits": """
            
            
            
            
            
            
                  Nos Produits\n
                  
                  
            -         Lampes LED Résidentielles :
            
                      Idéales pour l'éclairage domestique, nos lampes LED offrent une luminosité optimale avec une consommation d'énergie minimale.\n
                      
            -         Lampes LED Commerciales :
            
                        Conçues pour les bureaux, les magasins et les espaces commerciaux, elles garantissent une performance fiable 
                        et une longue durée de vie.\n
                               
            -         Lampes LED Industrielles :
            
                        Adaptées aux environnements industriels exigeants, nos lampes LED industrielles offrent une excellente résistance
                        et une efficacité énergétique supérieure.\n
                        
            -         Lampes LED Extérieures :
            
                            Pour l'éclairage extérieur, nos lampes LED extérieures sont résistantes aux intempéries 
                            et offrent une grande luminosité avec une faible consommation d'énergie.\n
                            
            -         Lampes LED Spéciales :
            
                           Nous offrons également des lampes LED spéciales pour des applications spécifiques telles que:
                            l'éclairage artistique, l'éclairage médical\n
                        """,

            "Pourquoi Choisir ATI Electronics": """
            
            
            
            
                Pourquoi Choisir ATI Electronics \n
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
            -    Qualité :
            
                Nous nous engageons à fournir des produits de haute qualité qui répondent aux normes les plus strictes de l'industrie.\n
            -   Efficacité Énergétique :
            
                Nos lampes LED sont conçues pour maximiser l'efficacité énergétique, réduisant ainsi la consommation d'énergie et les coûts associés.\n
            -   Durabilité :
            
                Nos produits sont construits pour durer, offrant une durée de vie plus longue par rapport aux lampes traditionnelles.\n
            -   Service Clientèle :
            
                Nous mettons un point d'honneur à offrir un service clientèle exceptionnel, garantissant une satisfaction client à long terme.\n
            -   Innovation :
                Nous sommes constamment à la recherche de nouvelles technologies et de nouvelles façons d'améliorer nos produits pour répondre aux besoins changeants du marché.\n
                        """,

            "Service Client": """
            
            
            
                    Service Client\n
                         Pour toute question ou préoccupation concernant nos produits ou services, n'hésitez pas à nous contacter.
                          Notre équipe de service clientèle est disponible pour vous aider du lundi au vendredi, de 9h à 18h.\n
            -       Téléphone : +123-456-7890\n
            -       Email : support@atielectronics.com\n
            -       Adresse : 123 Rue de l'Innovation, 75001 Paris, France\n
                        """
        }
        return sections.get(section, "")

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def go_back(self, instance):
        self.manager.current = "accueil"


class AccueilScreen(Screen):
    def __init__(self, **kwargs):
        super(AccueilScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.add_widget(self.layout)

        # Utilisation d'un ScrollView pour permettre le défilement
        scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        content_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        content_layout.bind(minimum_height=content_layout.setter('height'))
        scroll_view.add_widget(content_layout)
        self.layout.add_widget(scroll_view)

        # Ajout de l'image
        content_layout.add_widget(Image(source='background.jpg.jpg', size_hint=(1, None), height=400))

        # Ajout du texte
        welcome_label = Label(text="Bienvenue à l'Application de Commande des Lampes LED Ati Electronics",
                              font_size=24, bold=True, size_hint_y=None, height=50, color=(0.9, 0.2, 0.9, 1))
        content_layout.add_widget(welcome_label)

        additional_info = Label(
            text="Contrôlez facilement et efficacement vos lampes LED Ati Electronics à partir de votre smartphone ou tablette.\n"
                 "Notre application vous permet de :\n\n"
                 "- Commander vos lampes LED: Allumez, éteignez et ajustez la luminosité à votre convenance.\n"
                 "- Personnaliser votre éclairage: Choisissez parmi une large gamme de couleurs et d'effets pour créer l'ambiance parfaite.\n"
                 "- Automatiser vos réglages: Programmez des horaires pour que vos lampes LED s'allument et s'éteignent automatiquement.\n\n"
                 "Profitez d'une expérience utilisateur intuitive et d'un contrôle total sur vos lampes LED Ati Electronics. Téléchargez l'application dès aujourd'hui et découvrez la facilité de gestion de votre éclairage.",
            font_size=18,
            halign='left',
            valign='top',
            size_hint_y=None,
            height=600,  # Ajustez cette valeur pour s'assurer que le texte est entièrement visible
            text_size=(self.width, None),
            color=(0.9, 0.2, 0.9, 1)  # Rose
        )
        additional_info.text_size = (Window.width - 20, None)
        additional_info.bind(texture_size=additional_info.setter('size'))
        content_layout.add_widget(additional_info)

        self.layout.add_widget(Button(text="Retour", size_hint=(None, None), size=(100, 50), on_press=self.go_back))

    def go_back(self, instance):
        self.parent.current = 'main'



class ConnecterScreen(Screen):
    def __init__(self, **kwargs):
        super(ConnecterScreen, self).__init__(**kwargs)

        self.layout = GridLayout(cols=2, padding=10, spacing=10)
        self.add_widget(self.layout)

        # Champs de texte pour la connexion
        self.nom_input = TextInput(hint_text="Nom", multiline=False, size_hint=(1, None), height=30)
        self.password_input = TextInput(hint_text="Mot de passe", password=True, multiline=False, size_hint=(1, None), height=30)

        # Bouton Connexion
        self.connexion_button = Button(text="Se connecter", size_hint=(None, None), size=(100, 50))
        self.connexion_button.bind(on_press=self.login)

        # Ajout des widgets au layout
        self.layout.add_widget(self.nom_input)
        self.layout.add_widget(self.password_input)
        self.layout.add_widget(self.connexion_button)

        # Bouton Retour
        retour_button = Button(text="Retour", size_hint=(None, None), size=(100, 50))
        retour_button.bind(on_press=self.go_back)
        self.layout.add_widget(retour_button)

    def login(self, instance):
        nom = self.nom_input.text
        password = self.password_input.text

        if password == "ATIworld":
            self.manager.current = "page_supplementaire"
        else:
            # Afficher un message d'erreur avec un Popup
            invalid_password_popup = Popup(title="Mot de passe invalide",
                                           content=Label(text="Le mot de passe est invalide. Veuillez réessayer."),
                                           size_hint=(None, None), size=(400, 200))
            invalid_password_popup.open()

    def go_back(self, instance):
        self.manager.current = 'main'

ESP_IP = '192.168.1.100'  # Remplacez par l'adresse IP de votre ESP


class page_supplementaire(Screen):
    def __init__(self, **kwargs):
        super(page_supplementaire, self).__init__(**kwargs)

        # Layout principal
        float_layout = FloatLayout()
        self.add_widget(float_layout)

        # Ajouter l'image de fond
        background = Image(source='marwa.jpg', allow_stretch=True, keep_ratio=False)
        float_layout.add_widget(background)

        # Layout vertical pour les boutons et le slider
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        float_layout.add_widget(main_layout)

        # Propriétés pour les boutons stylisés
        button_background_color = [1, 1, 1, 1]  # Blanc
        text_color = [0, 0, 0, 1]  # Noir

        # Boutons de couleur
        red_button = Button(
            text="Rouge", size_hint=(0.3, 0.1), pos_hint={'center_x': 0.5},
            background_normal='', background_color=button_background_color,
            color=text_color, on_press=self.set_red
        )
        green_button = Button(
            text="Vert", size_hint=(0.3, 0.1), pos_hint={'center_x': 0.5},
            background_normal='', background_color=button_background_color,
            color=text_color, on_press=self.set_green
        )
        blue_button = Button(
            text="Bleu", size_hint=(0.3, 0.1), pos_hint={'center_x': 0.5},
            background_normal='', background_color=button_background_color,
            color=text_color, on_press=self.set_blue
        )

        # Ajout des boutons de couleur au layout principal
        main_layout.add_widget(red_button)
        main_layout.add_widget(green_button)
        main_layout.add_widget(blue_button)

        # Label et layout horizontal pour le slider et les boutons d'intensité
        intensity_label = Label(text="Intensité", size_hint=(0.3, 0.1), pos_hint={'center_x': 0.5})
        intensity_layout = BoxLayout(orientation='horizontal', size_hint=(0.6, 0.1), pos_hint={'center_x': 0.5})

        # Bouton pour diminuer l'intensité
        minus_button = Button(
            text="-", size_hint=(0.2, 1),
            background_normal='', background_color=button_background_color,
            color=text_color, on_press=self.decrease_intensity
        )

        # Slider pour contrôler l'intensité
        self.brightness_slider = Slider(min=0, max=255, value=128, size_hint=(0.6, 1))
        self.brightness_slider.bind(value=self.on_slider_value_change)

        # Bouton pour augmenter l'intensité
        plus_button = Button(
            text="+", size_hint=(0.2, 1),
            background_normal='', background_color=button_background_color,
            color=text_color, on_press=self.increase_intensity
        )

        # Ajout des widgets au layout d'intensité
        intensity_layout.add_widget(minus_button)
        intensity_layout.add_widget(self.brightness_slider)
        intensity_layout.add_widget(plus_button)

        # Ajout du label et du layout d'intensité au layout principal
        main_layout.add_widget(intensity_label)
        main_layout.add_widget(intensity_layout)

    def set_red(self, instance):
        url = f"http://{ESP_IP}/red?value=255"
        self.send_request(url)

    def set_green(self, instance):
        url = f"http://{ESP_IP}/green?value=255"
        self.send_request(url)

    def set_blue(self, instance):
        url = f"http://{ESP_IP}/blue?value=255"
        self.send_request(url)

    def on_slider_value_change(self, instance, value):
        # La méthode est appelée à chaque fois que la valeur du slider change
        self.set_brightness(int(value))

    def set_brightness(self, value):
        # Envoie une requête HTTP pour mettre à jour la luminosité
        url = f"http://{ESP_IP}/brightness?value={value}"
        self.send_request(url)

    def increase_intensity(self, instance):
        # Augmente l'intensité par pas de 10
        new_value = min(self.brightness_slider.value + 10, 255)
        self.brightness_slider.value = new_value
        self.set_brightness(new_value)

    def decrease_intensity(self, instance):
        # Diminue l'intensité par pas de 10
        new_value = max(self.brightness_slider.value - 10, 0)
        self.brightness_slider.value = new_value
        self.set_brightness(new_value)

    def send_request(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"Request successful: {url}")
            else:
                print(f"Request failed with status code {response.status_code}: {url}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")


if __name__ == '__main__':
    LampApp().run()
