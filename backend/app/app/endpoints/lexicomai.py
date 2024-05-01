import hashlib

from fastapi import APIRouter, Depends, Query

from app import schemas, deps
from app.utils.cache import Cache

router = APIRouter()


@router.post(
    '/write_data',
    tags=["Приложение / Объекты"],
    name='Создать объект',
    response_model=None
)
async def create_lexicomai(
        data: schemas.lexicomai.CreatingLexicomAI,  # Схема создания объекта
        cache: Cache = Depends(deps.get_cache)  # Кэш
):
    """
    Роут для создания или изменения объекта. Отправляем данные согласно схеме. Данные записываются в кэш по ключу
    data.phone. Если объекта с ключом data.phone нет, то объект будет записан в redis, если есть, то объект будет
    изменен.
    :param data: CreatingLexicomAI
    :param cache: Depends(deps.get_cache)
    :return: None
    """
    forbidden_signs = ('(', ')', '+', '-', ' ')
    for sign in data.phone:
        if sign in forbidden_signs:
            data.phone = data.phone.replace(sign, '')

    if data.phone.startswith('8'):
        data.phone = data.phone.replace('8', '7')
    elif data.phone.startswith('9'):
        data.phone = '7' + data.phone
    else:
        pass
    """
    При работе с номером телефона, по-хорошему, необходимо его приведение к единому формату. Кто-то записывает номер 
    телефона через +7, кто-то через 8, а бывает и начинают сразу с 9. Также в записи номера телефона используют знаки 
    '()- '. В данном случае, все номера приводятся к формату 70000000000... В случае нестандартного формата номера, 
    записываем его, как есть.
    """

    key = hashlib.md5(data.phone.encode()).hexdigest()
    """
    Ключ захэширован, так как хэширование ключей является хорошей практикой из-за того, что ключи могут быть составные
    (к примеру, при большом количестве фильтров) и занимать много памяти в redis, что, при, разрастании кэша, может 
    привести к нестабильной работе самого redis. А так мы гарантируем размер ключа в 32 байта.
    """
    await cache.set(key, data)  # Записываем данные в кэш
    # Ничего не возвращаем согласно заданию


@router.get(
    '/check_data',
    tags=["Приложение / Объекты"],
    name='Получить адрес',
    response_model=str
)
async def get_address(
        phone: str = Query(),  # Указываем номер телефона для поиска в query параметре, как указано в задании
        cache: Cache = Depends(deps.get_cache)  # Кэш
):
    """
    Роут для получения данных по ключу phone. Если ключ есть в базе, то получаем address, если нет, возвращаем
    соответствующий ответ.
    :param phone: str
    :param cache: Depends(deps.get_cache)
    :return: str
    """

    # forbidden_signs = ('(', ')', '+', '-', ' ', '’')
    """
    В задании сказано: "Клиент отправляет запрос на ручку вида 
    https://111.111.111.111/check_data?phone=’89090000000’..." то есть phone обернут в апострофы. Не ясно, это
    опечатка или имелось в виду, что Query параметр будет передаваться именно так. Так как я никогда не видел,
    чтобы Query параметр передавался в таком виде, я предположил, что это, все-таки, опечатка. Если нет, то 
    закомментированная переменная forbidden_signs является правильной.
    """

    forbidden_signs = ('(', ')', '+', '-', ' ')
    for sign in phone:
        if sign in forbidden_signs:
            phone = phone.replace(sign, '')

    if phone.startswith('8'):
        phone = phone.replace('8', '7')
    elif phone.startswith('9'):
        phone = '7' + phone
    else:
        pass
    """Форматирование номера телефона для получения адреса"""

    key = hashlib.md5(phone.encode()).hexdigest()

    data = await cache.get(key)  # Получаем ответ из кэша
    if not data:  # Проверяем, есть ли данные по этому ключу, если нет, то возвращаем соответствующий ответ.
        return f'Номер телефона {phone} на зарегистрирован в базе'

    return data  # Возвращаем данные
