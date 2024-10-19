def sp():
    return 'Бaскетбол\nВолейбол\nФутбол'
def it():
    aut='Команда, занимающаяся сетями и безопасностью:\n@au_team_news'
    bhs='Студия разработок игр:\n@bear_head_studio'
    stileru = 'Одно из ведущих IT-комьюнити ВШЭ:\n@styleruorg'
    return (f'<b>au_team</b>-\n{aut}'
            f'\n<b>BHS</b>-\n{bhs}'
            f'\n<b>Стилеру</b>-\n{stileru}')
def act():
    movem='Хочешь организовывать мероприятия ВШЭ? Тебе сюда!:\n@hse_movement'
    return f'<b>Movement</b>-\n{movem}'
def hse():
    hsek='Официальный канал лучшего ВУЗа страны:\n@hse_official'
    mem='Официальный канал лучшего факультета ВШЭ:\n@miem_hse'
    af='Знай про все события ВШЭ:\n@HSEafisha'
    return (f"<b>Высшая школа экономики</b>-\n{hsek}"
            f"\n<b>МИЭМ НИУ ВШЭ</b>-\n{mem}"
            f"\n<b>Афиша Вышки</b>-\n{af}")