from sqlalchemy_utils import ChoiceType


class BotChoiceType(ChoiceType):
    """Пользовательский класс ChoiceType."""
    cache_ok = True


STATUS = [
    (u'created', u'☑ Создана ☑️'),
    (u'denied', u'❌ Отклонена ❌'),
    (u'discussion', u'💬 Обсуждение 💬'),
    (u'accepted', u'✅ Принята ✅'),
]

ROLE = [
    (u'product_manager', u'Продукт-менеджер'),
    (u'project_manager', u'Проект-менеджер'),
    (u'other', u'Другое'),
]
