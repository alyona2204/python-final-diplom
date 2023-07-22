import requests
from django.conf import settings
from celery import shared_task
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.core.validators import URLValidator
from django.db import IntegrityError
from yaml import load as load_yaml, Loader

from .models import Shop, Category, ProductInfo, Product, Parameter, ProductParameter


@shared_task()
def send_email(title, message, email, *args, **kwargs):
    """
    Отправляет email сообщение

    :param title: Заголовок письма
    :param message: Тело письма
    :param email: Email-адрес получателя
    :param args: Аргументы
    :param kwargs: Ключевые аргументы
    :return: Строка с информацией о письме
    """
    email_list = [email]
    try:
        msg = EmailMultiAlternatives(subject=title, body=message, from_email=settings.EMAIL_HOST_USER, to=email_list)
        msg.send()
        return f'{title}: {msg.subject}, Message:{msg.body}'
    except Exception as e:
        raise e


@shared_task()
def get_import(partner, url):
    """
    Получает данные из YAML-файла и импортирует в базу данных.

    :param partner: Идентификатор пользователя
    :param url: URL YAML-файла
    :return: Словарь со статусом выполнения операции и информацией об ошибках
    """
    if url:
        validate_url = URLValidator()
        try:
            if not url.startswith('http://shop'):
                validate_url(url)
        except ValidationError as e:
            return {'Status': False, 'Error': str(e)}
        else:
            stream = requests.get(url).content

        data = load_yaml(stream, Loader=Loader)
        try:
            shop, _ = Shop.objects.get_or_create(name=data['shop'],
                                                 user_id=partner)
        except IntegrityError as e:
            return {'Status': False, 'Error': str(e)}

        for category in data['categories']:
            category_object, _ = Category.objects.get_or_create(
                id=category['id'], name=category['name'])
            category_object.shops.add(shop.id)
            category_object.save()

        ProductInfo.objects.filter(shop_id=shop.id).delete()
        for item in data['goods']:
            product, _ = Product.objects.get_or_create(
                name=item['name'], category_id=item['category']
            )
            product_info = ProductInfo.objects.create(
                product_id=product.id, external_id=item['id'],
                model=item['model'], price=item['price'],
                price_rrc=item['price_rrc'], quantity=item['quantity'],
                shop_id=shop.id
            )
            for name, value in item['parameters'].items():
                parameter_object, _ = Parameter.objects.get_or_create(
                    name=name
                )
                ProductParameter.objects.create(
                    product_info_id=product_info.id,
                    parameter_id=parameter_object.id, value=value
                )
        return {'Status': True}
    return {'Status': False, 'Errors': 'Url is false'}