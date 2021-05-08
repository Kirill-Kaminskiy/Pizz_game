from superwires import games, color
import random

games.init(screen_width=640, screen_height=480, fps=50)


class Pan(games.Sprite):
    """Перемещение мышью сковородки"""
    image = games.load_image("pan.bmp") # Загрзука картинки сковородки в переменную image
    score = games.Text(value=0, size=25, color=color.red, top=5, right=games.screen.width - 10)

    def __init__(self):
        """Инициализация объектов Pan и создания объекта Text для отображения счёта"""
        super(Pan, self).__init__(image=Pan.image, x = games.mouse.x, y = games.screen.height - 30)  # вызов конструктора класса Sprite
        self.upds_message = games.Message(value="Скорость повышена!",
                                                     size=50,
                                                     color=color.red,
                                                     x=games.screen.width / 2,
                                                     y=games.screen.height / 2,
                                                     lifetime=2*games.screen.fps,
                                                     after_death = self.destroy
                                                     )
        games.screen.add(self.score)

    def update(self):
        self.x = games.mouse.x
        if self.left < 0:  # если сковорода выходит за левое поле картинки
            self.left = 0  # сковорода возвращается в левый край экрана
        if self.right > games.screen.width:  # если сковорода выходит за правое поле картинки
            self.right = games.screen.width  # сковорода возвращается в правый край экрана
        self.check_catch()
        self.update_speed()
        self.distance()

    def check_catch(self):
        """Проверка пересечения спрайтов - сковороды и пиццы"""
        for pizza in self.overlapping_sprites:  # перебор всех спрайтов, пересекающихся со сковородкой
            self.score.value += 10
            self.score.right = games.screen.width - 10  # размещение счёта в правом углу, независимо от кол-ва цифр
            pizza.handle_caught()

    def update_speed(self):
        if self.score.value > 30:
            Pizza.speed = 2
            Chef.time_til_drop = int(Pizza(x=self.x).height * 1.8 / Pizza.speed)

    def distance(self):
        if self.score.value > 50:
            self.y = games.screen.height - 100


    def tick(self):
        if 30 < self.score.value < 80:
            games.screen.add(self.upds_message)

    def destroy(self):
        self.upds_message.destroy()


# дочерний класс от Sprite
class Pizza(games.Sprite):
    """Движение пиццы"""
    image = games.load_image("pizza.bmp")
    speed = 1

    def __init__(self, x, y = 90):
        super(Pizza, self).__init__(image=Pizza.image, x = x, y = y, dy=Pizza.speed)

    # метод обновлеия спрайта при каждом жизненном цикле
    def update(self):
        """Обращение компонент скорости, если достигнуты границы экрана"""
        if self.bottom > games.screen.height:
            self.end_game()
            self.destroy()

    def handle_caught(self):
        """Разрушение пиццы при пересечениии с сковородкой"""
        self.destroy()

    def end_game(self):
        """Завершение игры"""
        end_message = games.Message(value="Game Over",
                                    size=90,
                                    color=color.red,
                                    x=games.screen.width / 2,
                                    y=games.screen.height / 2,
                                    lifetime=2 * games.screen.fps,
                                    after_death=games.screen.quit)
        games.screen.add(end_message)


class Chef(games.Sprite):
    image = games.load_image("chef.bmp")
    time_til_drop = 0

    def __init__(self, y = 55, speed = 2, odds_change = 200):
        super(Chef, self).__init__(image=Chef.image, x=games.screen.width / 2,  y = y, dx=speed)
        self.odds_change = odds_change


    def update(self):
        """Определения смена направления"""
        if self.left < 0 or self.right > games.screen.width:
            self.dx = -self.dx
        elif random.randrange(self.odds_change) == 0:
            self.dx = -self.dx
        self.check_drop()

    def check_drop(self):
        """уменьшение интервала времени ожидания или же сбрасывание пиццы и восстановление интревала"""
        if self.time_til_drop > 0:
            self.time_til_drop -= 1
        else:
            new_pizza = Pizza(x = self.x)
            games.screen.add(new_pizza)
            self.time_til_drop = int(new_pizza.height * 1.3 / Pizza.speed)+1


def main():
    wall_image = games.load_image("wall.jpg", transparent = False)
    games.screen.background = wall_image

    the_Chef = Chef()
    the_Pan = Pan()

    games.screen.add(the_Chef)
    games.screen.add(the_Pan)

    games.mouse.is_visible = False  # далает стрелку мыши невидимой в поле программы
    games.mouse.event_grab = True  # "замыкает" стрелку в окне программы
    games.screen.mainloop()


if __name__ == '__main__':
    main()