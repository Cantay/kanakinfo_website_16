from .models import User, Product  # specify the specific models to be imported

def get_users():
    return models.User.objects.all()

def get_products():
    return models.Product.objects.all()

def create_user(name, email):
    return models.User.objects.create(name=name, email=email)

def create_product(name, price):
    return models.Product.objects.create(name=name, price=price)
