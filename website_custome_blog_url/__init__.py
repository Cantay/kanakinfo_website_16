# -*- coding: utf-8 -*-

from crypto_module.models import CryptoModel  # import the CryptoModel class from the models.py file
from crypto_module.controllers import CryptoController  # import the CryptoController class from the controllers.py file

def main():
    # create an instance of the CryptoModel class
    crypto_model = CryptoModel()

    # create an instance of the CryptoController class and pass the crypto_model instance as an argument
    crypto_controller = CryptoController(crypto_model)

    # call the main method of the CryptoController class
    crypto_controller.main()

if __name__ == "__main__":
    main()



# -*- coding: utf-8 -*-

class CryptoModel:
    def __init__(self):
        # initialization code here
        pass

    def some_method(self):
        # some method code here
        pass



# -*- coding: utf-8 -*-

class CryptoController:
    def __init__(self, crypto_model):
        # initialization code here
        self.crypto_model = crypto_model

    def main(self):
        # main method code here
        self.crypto_model.some_method()

