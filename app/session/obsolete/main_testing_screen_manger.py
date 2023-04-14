

class WelcomeView(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.size_hint = (0.6, 0.7)
        self.pos_hint = {
            'center_x': 0.5,
            'center_y': 0.5
        }

        self.add_widget(Image(source='logo_weiß.png'))
        self.greeting = Label(text='Wie heißt du?',
                              font_size=18,
                              color='#33cccc')
        self.add_widget(self.greeting)
        self.user = TextInput(multiline=False,
                              padding_y=(20, 20),
                              size_hint=(1, 0.5)
                              )
        self.add_widget(self.user)


# upper button for starting the app

        self.btn1 = Button(text='Eintreten',
                                      size_hint=(1, 0.5),
                                      bold=True,
                                      background_color='#33cccc',
                                      background_normal='')
        self.btn1.bind(on_press=self.btn1_behaviour)
        self.add_widget(self.btn1)

    def btn1_behaviour(self, *args):
        self.greeting.text = f'Herzlich Willkommen {self.user.text}.'
        Clock.schedule_once(self.switch_to_next_view, 2)

    def switch_to_next_view(self, *args):
        app.screen_manager.current = 'sessionManagement'




class MyApp(App):
    def build(self):
        self.screen_manager = ScreenManager()
        self.welcome_view = WelcomeView()
        screen = Screen(name='welcomeView')
        screen.add_widget(self.welcome_view)
        self.screen_manager.add_widget(screen)

        self.stock_view = StockView()
        screen = Screen(name='sessionManagement')
        screen.add_widget(self.stock_view)
        self.screen_manager.add_widget(screen)

        return self.screen_manager


if __name__ == '__main__':
    app = MyApp()
    app.run()
